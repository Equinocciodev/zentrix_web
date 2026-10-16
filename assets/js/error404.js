/* 404 de zentrix.company: sugerencias según la URL pedida y buscador integrado.
   - Las rutas y títulos vienen en #e404-datos (los escribe herramientas/generar.py).
   - Primero reglas por palabras (rutas viejas de eqnio.com y vendooapp.com, «sales»,
     «work», «privacidad», «soporte»…); luego, rutas parecidas por distancia de edición.
   - El campo de búsqueda abre el buscador del sitio (buscador.js, window.zxBuscar) con
     autocompletado; sin JavaScript, el formulario lleva a /?q=… y se abre allí. */
(function () {
  'use strict';
  var D = document, W = window;
  var nodo = D.getElementById('e404-datos');
  if (!nodo) return;
  var datos;
  try { datos = JSON.parse(nodo.textContent); } catch (e) { return; }
  var EN = /^en/i.test(D.documentElement.lang || '');
  var LISTA = (datos.rutas && datos.rutas[EN ? 'en' : 'es']) || [];
  var TITULO = {};
  LISTA.forEach(function (x) { TITULO[x[0]] = x[1]; });

  var pedido = location.pathname || '/';
  try { pedido = decodeURIComponent(pedido); } catch (e) { /* se queda como viene */ }
  var directa = /^\/(en\/)?404(\.html)?$/.test(pedido);

  function plano(s) {
    return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }
  function limpia(r) {
    return plano(r).replace(/^\/en(\/|$)/, '/').replace(/\/(index)?\.(html?|php|aspx?)$/, '/')
      .replace(/\.(html?|php|aspx?)$/, '').replace(/\/+$/, '') || '/';
  }
  var p = limpia(pedido);
  var tokens = p.split(/[^a-z0-9]+/).filter(Boolean);
  var texto = ' ' + tokens.join(' ') + ' ';

  /* ---------- reglas (rutas en español; se pasan al inglés con datos.par) ---------- */
  function hay(re) { return re.test(texto); }
  var PROD = [
    ['work', / (work|guuao\w*|trabajo|operador\w*|tienda) /],
    ['sales', / (sales|vendoo\w*|ventas?|vendedor\w*|seller\w*) /],
    ['ai', / (ai|ia|inteligencia) /],
    ['logistics', / (logistics?|logistica|reparto|despachos?|delivery) /],
    ['cloud', / (cloud|nube|hosting) /],
    ['labs', / (labs?|laboratorio) /],
    ['traza', / (traza|trazabilidad|traceability) /],
    ['software', / software /]
  ];
  var SOL = [
    ['/soluciones/odoo-venezuela/', / odoo /],
    ['/soluciones/auditoria-tecnica/', / (auditoria|audit) /],
    ['/soluciones/infraestructura-alta-disponibilidad/', / (infraestructura|infrastructure|disponibilidad|availability) /],
    ['/soluciones/pagos-y-comercio-digital/', / (pagos?|payments?|comercio|commerce|pos) /],
    ['/soluciones/vision-computacional/', / (vision|computacional|computer) /],
    ['/soluciones/desarrollo-de-software/', / (desarrollo|development) /]
  ];
  var TEMA = [
    ['privacidad', / (privacidad|privacy|privacy\w*|cookies?|datos) /],
    ['soporte', / (soporte|support|ayuda|help|eliminar|delete|borrar) /],
    ['terminos', / (terminos?|terms|condiciones|conditions|legal) /],
    ['docs', / (docs?|manual|manuales|guia|guide|documentacion|documentation) /],
    ['contacto', / (contacto?|contact|demo|demostracion) /]
  ];
  var EMPRESA = [
    ['/nosotros/', / (nosotros|about|equipo|team|empresa|company|quienes) /],
    ['/clientes/', / (clientes?|customers?|casos|cases|portfolio|portafolio) /],
    ['/recursos/', / (recursos|resources|blog) /],
    ['/soluciones/', / (soluciones|solutions|servicios|services) /]
  ];
  function primero(lista) {
    for (var i = 0; i < lista.length; i++) if (hay(lista[i][1])) return lista[i][0];
    return null;
  }

  function lev(a, b) {
    if (a === b) return 0;
    var m = a.length, n = b.length, prev = [], cur, i, j;
    if (!m) return n;
    if (!n) return m;
    for (j = 0; j <= n; j++) prev[j] = j;
    for (i = 1; i <= m; i++) {
      cur = [i];
      for (j = 1; j <= n; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      prev = cur;
    }
    return prev[n];
  }
  function parecido(a, b) { return a && b ? 1 - lev(a, b) / Math.max(a.length, b.length) : 0; }
  function ultimo(r) { var s = r.split('/').filter(Boolean); return s.length ? s[s.length - 1] : ''; }

  // Ruta española → ruta del idioma de la página (o null si no existe en ese idioma).
  function enIdioma(r) {
    if (!EN) return TITULO[r] ? r : null;
    if (TITULO[r]) return r;
    var x = datos.par && datos.par[r];
    if (x && TITULO[x]) return x;
    var m = /^\/(work|sales)\/docs\//.exec(r);
    return m && TITULO['/en/' + m[1] + '/docs/'] ? '/en/' + m[1] + '/docs/' : null;
  }

  function porReglas() {
    var out = [];
    var prod = primero(PROD), tema = primero(TEMA);
    if (prod === 'work' || prod === 'sales') {
      // Un capítulo de la documentación con nombre parecido va primero (/sales/cobrar-viejo → cobrar.html).
      out = out.concat(mejores(function (r) { return r.indexOf('/' + prod + '/docs/') === 0 && /\.html$/.test(r); }, 1, .7));
      if (tema === 'docs') {
        out.push('/' + prod + '/docs/');
      } else if (tema === 'contacto') out.push(prod === 'sales' ? '/sales/contacto/' : '/contacto/');
      else if (tema) out.push('/' + prod + '/' + tema + '/');
      out.push('/' + prod + '/');
    } else if (prod) {
      out.push('/' + prod + '/');
    }
    var sol = primero(SOL);
    if (sol) out.push(sol);
    if (!prod && tema) {
      out.push({ privacidad: '/privacidad/', contacto: '/contacto/' }[tema] || '/recursos/');
      if (tema === 'privacidad' || tema === 'soporte') out.push('/sales/' + tema + '/', '/work/' + tema + '/');
    }
    var emp = primero(EMPRESA);
    if (emp) out.push(emp);
    return out;
  }

  // Rutas del sitio que más se parecen a lo pedido (toda la ruta o su último tramo).
  function mejores(filtro, n, umbral) {
    var u = ultimo(p);
    var orden = LISTA.map(function (x) {
      var r = x[0];
      if (filtro && !filtro(r)) return null;
      var lr = limpia(r);
      var ul = ultimo(lr).replace(/\.html$/, '');
      var s = Math.max(parecido(p, lr), u ? parecido(u, ul) - .05 : 0);
      tokens.forEach(function (t) { if (t.length > 3) s = Math.max(s, parecido(t, ul) - .05); });
      return [r, s];
    }).filter(function (x) { return x && x[1] >= umbral; });
    orden.sort(function (a, b) { return b[1] - a[1]; });
    return orden.slice(0, n).map(function (x) { return x[0]; });
  }

  function sugerencias() {
    if (directa || p === '/') return [];
    var vistos = {}, out = [];
    porReglas().map(enIdioma).concat(mejores(null, 3, .6)).forEach(function (r) {
      if (r && !vistos[r] && TITULO[r] && limpia(r) !== p) { vistos[r] = 1; out.push(r); }
    });
    return out.slice(0, 3);
  }

  /* ---------- pintar ---------- */
  var M = '/assets/img/logos/monogramas/';
  var ICONO = { work: 'work', sales: 'sales', ai: 'ai', logistics: 'logistica', cloud: 'cloud', labs: 'labs', software: 'software' };
  function icono(r) {
    var s = r.replace(/^\/en\//, '/').split('/')[1] || '';
    if (s === 'traza') return '/assets/img/logos/traza/traza_icono-64.webp';
    return ICONO[s] ? M + ICONO[s] + '_icono.svg' : '/favicon.svg';
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  var pedidoNodo = D.querySelector('.e404__pedido');
  if (pedidoNodo && !directa) {
    pedidoNodo.querySelector('code').textContent = pedido.length > 80 ? pedido.slice(0, 77) + '…' : pedido;
    pedidoNodo.hidden = false;
  }

  var sug = sugerencias();
  var pista = D.querySelector('.e404__pista');
  if (pista && sug.length) {
    var flecha = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false"><path d="M4 10h11m-4-4 4 4-4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    pista.querySelector('ul').innerHTML = sug.map(function (r, i) {
      return '<li><a class="e404-sug' + (i === 0 ? ' e404-sug--primera' : '') + '" href="' + esc(r) + '" data-sugerencia="' + i + '">' +
        '<img src="' + icono(r) + '" alt="" width="36" height="36">' +
        '<span class="e404-sug__txt"><span class="e404-sug__tit">' + esc(TITULO[r]) + '</span>' +
        '<span class="e404-sug__ruta">zentrix.company' + esc(r) + '</span></span>' + flecha + '</a></li>';
    }).join('');
    pista.hidden = false;
  }

  /* ---------- buscador ---------- */
  var VACIAS = { en: 1, es: 1, html: 1, htm: 1, php: 1, index: 1, www: 1, de: 1, del: 1, la: 1, el: 1, los: 1, las: 1, y: 1, the: 1, and: 1, of: 1, page: 1, pagina: 1 };
  var form = D.querySelector('.e404__buscar');
  var campo = form && form.querySelector('input');
  if (campo && !directa) {
    var palabras = tokens.filter(function (t) { return t.length > 2 && !VACIAS[t] && !/^\d+$/.test(t); }).slice(-4);
    if (palabras.length) campo.value = palabras.join(' ');
  }
  function abrir(q) {
    if (W.zxBuscar && typeof W.zxBuscar.abrir === 'function') { W.zxBuscar.abrir(q); return true; }
    return false;
  }
  if (form && campo) {
    form.addEventListener('submit', function (e) {
      if (abrir(campo.value.trim())) e.preventDefault();
    });
    // Al escribir, el buscador del sitio toma el relevo con su autocompletado.
    campo.addEventListener('input', function () {
      if (abrir(campo.value)) campo.value = '';
    });
  }

  /* ---------- analítica ---------- */
  D.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-sugerencia]') : null;
    if (a && W.zxAnalytics && W.zxAnalytics.track) {
      W.zxAnalytics.track('select_content', { content_type: '404_suggestion', item_id: a.getAttribute('href') });
    }
  });
  // analitica.js se ejecuta después que este script: se espera al DOMContentLoaded.
  D.addEventListener('DOMContentLoaded', function () {
    if (!directa && W.zxAnalytics && W.zxAnalytics.track) {
      W.zxAnalytics.track('page_not_found', { page_path: pedido.slice(0, 100), suggestion: sug[0] || '' });
    }
  });
})();
