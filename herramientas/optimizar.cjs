/* Optimización de la copia que se publica (la ejecuta el workflow de Pages, nunca sobre el repo):

     node herramientas/optimizar.cjs            # sobre el directorio actual (la copia del sitio)

   1. Minifica assets/css/*.css y assets/js/*.js con esbuild (los fuentes del repo siguen legibles).
   2. CSS crítico con beasties: en cada página va en línea, en un <style>, lo que esa página usa
      de sitio.css (y de manual-*.css en la documentación), y la hoja completa pasa a cargarse sin
      bloquear el primer pintado: <link media="print" data-asincrona>, que nav.js pasa a media="all"
      (el mismo mecanismo que bloques.css). Así no hay onload= ni scripts en línea nuevos que la
      Content-Security-Policy tenga que permitir.
      Las clases que pone JavaScript al cargar (.js, .nav-js, .visible, la pastilla del buscador,
      el aviso de cookies…) no están en el HTML: van siempre en el CSS crítico (SIEMPRE) para que
      nada se vea un instante sin estilo ni salte (el menú móvil, sobre todo).

   Dependencias (fuera del repo, para que no se publiquen):
     npm install --prefix "$RUNNER_TEMP/opt" beasties@0.5.5 esbuild@0.28.2
     NODE_PATH="$RUNNER_TEMP/opt/node_modules" node herramientas/optimizar.cjs */
'use strict';
const fs = require('fs');
const path = require('path');
const esbuild = require('esbuild');
const Beasties = require('beasties').default || require('beasties');

const RAIZ = process.cwd();
const SIEMPRE = [
  /(^|[\s,>+~(])\.js\b/, /\.nav-js\b/, /\.nav--abierta\b/, /\.visible\b/, /\.zx-/, /\.zxb-pastilla/,
  /\.zx-ck/, /\.e404-en\b/, /\[open\]/, /\[hidden\]/, /aria-expanded/, /\.sr\b/,
];

function archivos(dir, ext, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.') || e.name === 'node_modules' || e.name === 'herramientas' || e.name === 'pagefind') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) archivos(p, ext, out);
    else if (p.endsWith(ext)) out.push(p);
  }
  return out;
}

async function minificar() {
  let antes = 0, despues = 0;
  for (const [carpeta, loader] of [['assets/css', 'css'], ['assets/js', 'js']]) {
    for (const f of fs.readdirSync(path.join(RAIZ, carpeta))) {
      if (!f.endsWith('.' + loader)) continue;
      const p = path.join(RAIZ, carpeta, f);
      const src = fs.readFileSync(p, 'utf8');
      // target esnext: no se reescribe nada moderno (anidado, @starting-style, sibling-index…)
      const r = await esbuild.transform(src, { loader, minify: true, target: 'esnext', legalComments: 'none' });
      fs.writeFileSync(p, r.code);
      antes += src.length; despues += r.code.length;
    }
  }
  console.log(`minificado: ${Math.round(antes / 1024)} KB → ${Math.round(despues / 1024)} KB`);
}

async function critico() {
  const b = new Beasties({
    path: RAIZ, publicPath: '/', preload: 'media-script', noscriptFallback: true,
    allowRules: SIEMPRE, inlineFonts: true, preloadFonts: false, keyframes: 'critical', pruneSource: false,
    reduceInlineStyles: false, mergeStylesheets: true, logLevel: 'warn',
  });
  // Todas las @font-face de sitio.css van siempre en línea: beasties solo ve las familias escritas
  // en una regla, y Geist (y su reserva con size-adjust) se usa a través de var(--display). Sin
  // ellas el primer pintado saldría con otra fuente y el texto saltaría al llegar la hoja.
  const FUENTES = (fs.readFileSync(path.join(RAIZ, 'assets/css/sitio.css'), 'utf8').match(/@font-face\s*\{[^}]*\}/g) || []).join('');
  let n = 0, enLinea = 0;
  for (const f of archivos(RAIZ, '.html')) {
    let html = fs.readFileSync(f, 'utf8');
    if (html.includes('http-equiv="refresh"') || !/<link rel="stylesheet" href="\/assets\/css\//.test(html)) continue;
    // bloques.css ya se carga sin bloquear (data-asincrona, con su <noscript>): beasties no la toca.
    html = html.replace(/<link rel="stylesheet" href="\/assets\/css\/bloques\.css[^"]*"[^>]*>/g, (m) => m.replace('<link ', '<link data-beasties-skip '));
    // Se analiza la página entera (limitarlo a la «primera pantalla» con data-beasties-container
    // cambiaba el primer pintado en las páginas de producto y la documentación). Pero los paneles
    // del mega-menú no cuentan: un <details> cerrado oculta su contenido sin CSS, y sus reglas eran
    // casi un tercio del CSS crítico (el HTML crecía ~10 KB comprimido y el primer pintado tardaba más). Se apartan antes de analizar y se devuelven después.
    const paneles = [];
    html = html.replace(/(<details class="mega"[^>]*>\s*<summary[\s\S]*?<\/summary>)([\s\S]*?)(<\/details>)/g,
      (m, a, panel, z) => { paneles.push(panel); return `${a}<!--ZXMEGA${paneles.length - 1}-->${z}`; });
    let out = await b.process(html);
    out = out.replace(/<!--ZXMEGA(\d+)-->/g, (m, k) => paneles[+k]);
    if (/ZXMEGA/.test(out)) throw new Error('panel del mega-menú sin devolver en ' + f);
    out = out.replace(/<link data-beasties-skip /g, '<link ');
    // media-script deja data-beasties-media en los <link> y un <script> en línea que los activa:
    // se cambian por <link media="print" data-asincrona> (lo activa nav.js) y el script se quita,
    // porque la CSP solo deja los scripts en línea que generar.py calculó.
    out = out.replace(/<link([^>]*?)\sdata-beasties-media(?:="[^"]*")?([^>]*)>/g, (m, a, c) => {
      const attrs = (a + c).replace(/\smedia="[^"]*"/, '');
      return `<link${attrs} media="print" data-asincrona>`;
    });
    out = out.replace(/<script>[^<]*data-beasties-media[^<]*<\/script>/g, '');
    if (/data-beasties-media/.test(out)) throw new Error('quedó data-beasties-media en ' + f);
    out = out.replace(/<style>([\s\S]*?)<\/style>/, (m, css) => `<style>${FUENTES}${css.replace(/@font-face\s*\{[^}]*\}/g, '')}</style>`);
    const estilo = out.match(/<style>([\s\S]*?)<\/style>/);
    enLinea += estilo ? estilo[1].length : 0;
    fs.writeFileSync(f, out);
    n++;
  }
  console.log(`CSS crítico en línea: ${n} páginas, media ${Math.round(enLinea / Math.max(n, 1) / 1024)} KB por página`);
}

(async () => {
  await minificar();
  await critico();
})().catch((e) => { console.error(e); process.exit(1); });
