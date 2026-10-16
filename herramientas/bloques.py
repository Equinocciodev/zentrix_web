"""Sistema de bloques de contenido de zentrix.company (documentado en BLOQUES.md).

Seis variantes con prefijo `bq-`, todas con su CSS en assets/css/bloques.css y un JS mínimo
(assets/js/bloques.js, solo el brillo que sigue al cursor):

    1. pilares()  · tarjetas con número gigante recortado y la barra lima con el corte de la z
    2. bento()    · mosaico de enlaces con una tarjeta protagonista e ilustración propia
    3. stack()    · fila de tecnologías con los logotipos oficiales en una sola tinta
    4. banda()    · banda a todo el ancho (producto relacionado) y cierre() (llamada final)
    5. pasos()    · pasos con un trazo que se dibuja, y cifras() con contadores
    6. hablemos() · banda de contacto que se repite: titular, escríbenos y soporte (sin dirección)
       contacto() · la de /contacto/: la misma banda más el lugar (dirección y mapa) y los datos

`aplicar(s, ruta)` lo llama generar.py en cada página: enlaza la hoja y el script, rellena
los marcadores `<!--BQ:…-->` y convierte el marcado antiguo de las páginas escritas a mano
(funciones, casos, proceso, cifras y la llamada final). Es idempotente.
"""
import pathlib
import re
from urllib.parse import quote

from bloques_logos import LOGOS

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MONO = '/assets/img/logos/monogramas'
CSS_BLOQUEANTE = '<link rel="stylesheet" href="/assets/css/bloques.css?v=4">'
# Los bloques van siempre debajo del héroe: su hoja se carga sin bloquear el primer pintado
# (media=print + onload, prioridad baja, con <noscript> de respaldo). Ahorra ~0,3 s de LCP en móvil.
CSS_PRELOAD = ('<link rel="preload" href="/assets/css/bloques.css?v=4" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">'
               '<noscript><link rel="stylesheet" href="/assets/css/bloques.css?v=4"></noscript>')
CSS = ('<link rel="stylesheet" href="/assets/css/bloques.css?v=4" media="print" onload="this.media=\'all\'">'
       '<noscript><link rel="stylesheet" href="/assets/css/bloques.css?v=4"></noscript>')
JS = '<script src="/assets/js/bloques.js?v=1" defer></script>'

# ── Piezas de marca ─────────────────────────────────────────────────────────
# Corte diagonal de la z: la barra lima de los monogramas termina en un bisel de 48,7°
# (73,2 de avance por 64,4 de alto en la retícula de 1000).
BISEL = 73.2 / 64.4
Z_PATH = ('M0 0H110V20.9L8.8 110H0V89.1L64.9 25.3H0Z'
          'M19.8 110H110V84.7H47.3Z')


def barra(clase=''):
    return f'<span class="bq-barra{" " + clase if clase else ""}" aria-hidden="true"></span>'


def zfondo(clase=''):
    """La z madre, grande y recortada, como recurso de fondo (manual, págs. 8 y 10)."""
    return (f'<svg class="bq-zfondo{" " + clase if clase else ""}" viewBox="0 0 110 110" aria-hidden="true" '
            f'focusable="false"><path d="{Z_PATH}"/></svg>')


FLECHA = ('<svg class="bq-flecha" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" '
          'stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M4 12h14M13 6l6 6-6 6"/></svg>')
EXTERNO = ('<svg class="bq-flecha bq-flecha--externo" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2.25" stroke-linecap="square" aria-hidden="true" focusable="false">'
           '<path d="M8 6h10v10M18 6 6 18"/></svg>')


def _b(x, y, w=230, h=64):
    """Barra lima con el bisel de la z, en la retícula de 1000."""
    return f'<path class="bq-ilu__l" d="M{x} {y}h{w}l-{h * BISEL:.0f} {h}H{x}z"/>'


# ── Microilustraciones: retícula 1000, trazo 104 (el grueso de los monogramas),
#    remate recto y la barra lima con el corte diagonal como acento ──────────
_T = '<g class="bq-ilu__t">{}</g>'
ILU = {
    # soluciones
    'odoo': _T.format('<path d="M500 170 820 330 500 490 180 330Z"/><path d="M180 520 500 680 820 520"/>') + _b(385, 790),
    'software': _T.format('<path d="M380 290 190 500l190 210"/><path d="M620 290l190 210-190 210"/>')
                + '<path class="bq-ilu__l" d="M560 220h112L440 780H328z"/>',
    'auditoria': _T.format('<circle cx="430" cy="430" r="250"/><path d="M610 610 840 840"/>') + _b(315, 398),
    'infra': _T.format('<circle cx="500" cy="500" r="310" stroke-dasharray="1540 408" transform="rotate(-62 500 500)"/>')
             + '<circle class="bq-ilu__f" cx="500" cy="500" r="118"/>' + _b(640, 150, 230, 64),
    'pagos': _T.format('<path d="M150 250h540l160 160v340H150Z"/><path d="M150 440h700"/>') + _b(250, 600),
    'vision': _T.format('<path d="M110 500Q500 90 890 500 500 910 110 500Z"/>')
              + '<circle class="bq-ilu__f" cx="500" cy="500" r="130"/>' + _b(385, 840),
    # sectores y recursos
    'tienda': _T.format('<path d="M140 210h720l40 210H100Z"/><path d="M180 420v400h640V420"/><path d="M430 820V610h140v210"/>') + _b(230, 520, 150, 52),
    'camion': _T.format('<path d="M110 280h500v410H110Z"/><path d="M610 420h170l110 130v140H610"/>')
              + '<circle class="bq-ilu__f" cx="290" cy="770" r="86"/><circle class="bq-ilu__f" cx="730" cy="770" r="86"/>' + _b(200, 420),
    'ayuda': _T.format('<path d="M170 190h660v480H480L300 830V670H170Z"/>') + _b(330, 398, 300, 64),
    'escudo': _T.format('<path d="M500 140 830 260v240q0 260-330 380Q170 760 170 500V260Z"/>') + _b(385, 460),
    'documento': _T.format('<path d="M210 130h400l180 180v560H210Z"/><path d="M330 560h340M330 730h220"/>') + _b(330, 330, 200, 64),
    'codigo': None,  # se rellena abajo (alias de software)
    'correo': _T.format('<path d="M130 230h740v540H130Z"/><path d="M130 270 500 560l370-290"/>') + _b(200, 650),
    'whatsapp': _T.format('<path d="M520 150a330 330 0 1 1-170 612L150 860l90-190A330 330 0 0 1 520 150Z"/>') + _b(395, 448),
    'reloj': _T.format('<circle cx="500" cy="500" r="340"/><path d="M500 290v242"/>') + _b(500, 470, 210, 64),
    'lugar': _T.format('<path d="M500 890 255 575a300 300 0 1 1 490 0Z"/>') + _b(385, 330),
    'idioma': _T.format('<circle cx="500" cy="500" r="340"/><path d="M500 160c-200 200-200 480 0 680M500 160c200 200 200 480 0 680M170 500h660"/>'),
    # módulos de Zentrix Logistics
    'estante': _T.format('<path d="M170 900V120h660v780M170 410h660M170 680h660"/><path d="M290 250h170v160H290Z"/>'
                         '<path d="M540 530h170v150H540Z"/>') + _b(290, 776, 200, 64),
    'caja': _T.format('<path d="M500 140 840 300v400L500 860 160 700V300Z"/><path d="M160 300l340 160 340-160M500 460v400"/>')
            + _b(250, 560, 150, 52),
    'guia': _T.format('<path d="M210 120h580v760H210Z"/>')
            + '<path class="bq-ilu__f" d="M320 520h40v240h-40zM410 520h24v240h-24zM484 520h56v240h-56zM590 520h24v240h-24zM650 520h30v240h-30z"/>'
            + _b(320, 250, 300, 64),
    'seguimiento': _T.format('<path d="M150 860C260 640 470 770 560 560"/><path d="M700 560 570 395a185 185 0 1 1 260 0Z"/>')
                   + '<circle class="bq-ilu__f" cx="700" cy="270" r="66"/>' + _b(130, 160, 230, 64),
    'devolucion': _T.format('<path d="M820 300H380a200 200 0 0 0 0 400h330"/><path d="M520 150 370 300l150 150"/>')
                  + _b(560, 800, 230, 64),
}
ILU['codigo'] = ILU['software']


def ilustracion(nombre, clase='bq-ilu'):
    return (f'<svg class="{clase}" viewBox="0 0 1000 1000" aria-hidden="true" focusable="false">'
            f'{ILU[nombre]}</svg>')


# ── Motivos de las divisiones (los mismos SVG que dibuja el héroe de cada producto) ──
MOTIVO_PAGINA = {'capas': 'software', 'onda': 'ai', 'nube': 'cloud', 'prisma': 'labs', 'cubos': 'logistics',
                 'anillo': 'traza', 'pulso': 'work', 'ruta': 'sales', 'garita': 'check'}
MOTIVO_DE_RUTA = {'/work/': 'pulso', '/sales/': 'ruta', '/check/': 'garita', '/ai/': 'onda', '/cloud/': 'nube', '/labs/': 'prisma',
                  '/logistics/': 'cubos', '/software/': 'capas', '/traza/': 'anillo'}
_motivos = {}


def motivo(nombre, clase='bq-motivo'):
    if nombre not in _motivos:
        s = (RAIZ / MOTIVO_PAGINA[nombre] / 'index.html').read_text(encoding='utf-8')
        m = re.search(rf'<!--MOTIVO:{nombre}(?::[\w-]+)?-->(.*?)<!--/MOTIVO-->', s, re.S)
        _motivos[nombre] = m.group(1).strip() if m else ''
    svg = _motivos[nombre]
    # ids propios para no repetir los del héroe en la misma página
    svg = re.sub(r'id="([\w-]+)"', r'id="bq-\1"', svg)
    svg = re.sub(r'url\(#([\w-]+)\)', r'url(#bq-\1)', svg)
    return svg.replace('class="motivo"', f'class="motivo {clase}"', 1)


# ── Retícula: reparte anchos para que no queden huecos (3 o 4 columnas en escritorio,
#    2 en tableta, 1 en móvil) ─────────────────────────────────────────────
def reja(n, prota=False):
    """Clases por ítem y número de columnas de escritorio."""
    clases = [[] for _ in range(n)]
    if prota and n >= 2:
        cols = 3
        clases[0] += ['bq-c2', 'bq-t2'] + (['bq-r2'] if n >= 3 else [])
        resto = n - 3 if n >= 3 else 0
        r = resto % 3
        if r == 1:
            clases[-1].append('bq-c3')
        elif r == 2:
            clases[-1].append('bq-c2')
        if (n - 1) % 2:
            clases[-1].append('bq-t2')
    else:
        cols = n if n <= 4 else (3 if n in (5, 6, 9) else 4)
        r = n % cols
        if r:
            clases[-1].append(f'bq-c{cols - r + 1}')
        if n % 2:
            clases[-1].append('bq-t2')
    return [' '.join(c) for c in clases], cols


# ── 1. Pilares ──────────────────────────────────────────────────────────────
def pilares(items, variante='', arte='', etiqueta=''):
    """items: [(titulo, texto)]. variante: '' | 'oscuro' | 'prota' (la primera, en negro con el motivo)."""
    prota = 'prota' in variante
    clases, cols = reja(len(items), prota)
    if 'texto' in variante:  # textos largos: dos columnas
        cols = 2
        clases = ['' for _ in items[:-1]] + (['bq-c2 bq-t2'] if len(items) % 2 else [''])
    lis = []
    for i, it in enumerate(items):
        ante, t, p = it if len(it) == 3 else ('', *it)
        ante = f'<span class="antetitulo">{ante}</span>' if ante else ''
        es_prota = prota and i == 0
        extra = ' bq-pilar--prota' if es_prota else ''
        arte_html = f'<span class="bq-pilar__arte" aria-hidden="true">{arte}</span>' if es_prota and arte else ''
        lis.append(f'<li class="bq-pilar{extra} bq-brillo revela {clases[i]}" style="--retardo:{(i % 4) * .07:.2f}s">'
                   f'<span class="bq-pilar__num" aria-hidden="true">{i + 1:02d}</span>{arte_html}'
                   f'{barra()}{ante}<h3>{t}</h3><p>{p}</p></li>')
    mod = ''.join(f' bq-pilares--{v}' for v in variante.split() if v)
    al = f' aria-label="{etiqueta}"' if etiqueta else ''
    return f'<ol class="bq-pilares bq-reja{mod}" style="--cols:{cols}"{al}>{"".join(lis)}</ol>'


# ── 2. Bento ────────────────────────────────────────────────────────────────
def bento(items, variante='', ir='Conocer más'):
    """items: dicts con href, titulo, texto, arte (SVG o <img>), y opcionales prota, externo, extra (HTML).
    variante: '' (sobre claro) | 'azul' | 'oscuro'; 'compacto' para listas cortas."""
    prota = any(x.get('prota') for x in items)
    clases, cols = reja(len(items), prota)
    if 'compacto' in variante:
        clases, cols = ['' for _ in items], 1
    lis = []
    for i, x in enumerate(items):
        p = ' bq-tesela--prota' if x.get('prota') else (f' bq-tesela--{x["tono"]}' if x.get('tono') else '')
        ext = ' target="_blank" rel="noopener"' if x.get('externo') else ''
        flecha = EXTERNO if x.get('externo') else FLECHA
        texto = f'<p class="bq-tesela__p">{x["texto"]}</p>' if x.get('texto') else ''
        lis.append(f'<li class="{clases[i]}"><a class="bq-tesela{p} bq-brillo revela" style="--retardo:{(i % 3) * .07:.2f}s" '
                   f'href="{x["href"]}"{ext}><span class="bq-tesela__arte" aria-hidden="true">{x["arte"]}</span>'
                   f'<h3 class="bq-tesela__t">{x["titulo"]}</h3>{texto}{x.get("extra", "")}'
                   f'<span class="bq-tesela__ir">{x.get("ir", ir)}{flecha}</span></a></li>')
    mod = ''.join(f' bq-bento--{v}' for v in variante.split() if v)
    return f'<ul class="bq-bento bq-reja{mod}" style="--cols:{cols}">{"".join(lis)}</ul>'


def mock_odoo():
    """Pantalla de un sistema de gestión en vectorial, sin datos reales: menú, tabla y gráfico."""
    filas = ''.join(f'<rect x="96" y="{112 + i * 34}" width="{[168, 132, 186, 150][i]}" height="10" rx="2" fill="#fff" opacity=".55"/>'
                    f'<rect x="300" y="{112 + i * 34}" width="44" height="10" rx="2" fill="#fff" opacity=".3"/>'
                    for i in range(4))
    barras = ''.join(f'<rect x="{384 + i * 22}" y="{232 - h}" width="14" height="{h}" fill="{"#C7FA46" if i == 4 else "#fff"}" '
                     f'opacity="{1 if i == 4 else .5}"/>' for i, h in enumerate([40, 64, 52, 88, 112]))
    return ('<svg class="bq-mock" viewBox="0 0 520 300" aria-hidden="true" focusable="false">'
            '<rect x="1" y="1" width="518" height="298" rx="14" fill="#090D12" stroke="#fff" stroke-opacity=".22"/>'
            '<rect x="1" y="1" width="64" height="298" rx="14" fill="#fff" fill-opacity=".06"/>'
            '<rect x="20" y="24" width="26" height="26" rx="6" fill="#244DFF"/>'
            + ''.join(f'<rect x="24" y="{78 + i * 30}" width="18" height="6" rx="2" fill="#fff" opacity=".4"/>' for i in range(5)) +
            '<rect x="96" y="32" width="150" height="16" rx="3" fill="#fff"/>'
            '<path d="M96 68h48l-8 8H96z" fill="#C7FA46"/>'
            '<rect x="398" y="28" width="96" height="28" rx="8" fill="#244DFF"/>'
            + filas + barras +
            '<path d="M96 268h398" stroke="#fff" stroke-opacity=".18"/></svg>')


def caso(nombre, rubro, texto, enlaces, i=0):
    """Caso de cliente: inicial gigante en contorno, como los números de los pilares."""
    inicial = ''.join(w[0] for w in nombre.split()[:2]).upper()
    links = ''.join(f'<li><a href="{h}">{n}{FLECHA}</a></li>' for h, n in enlaces)
    return (f'<article class="bq-caso bq-brillo revela" style="--retardo:{i * .08:.2f}s">'
            f'<span class="bq-caso__inicial" aria-hidden="true">{inicial}</span>'
            f'<h3>{nombre}</h3><p class="bq-caso__rubro">{rubro}</p>{barra()}<p>{texto}</p>'
            f'<ul class="bq-caso__enlaces">{links}</ul></article>')


def sector(id_, ilu, nombre, texto, lista_html, i=0):
    return (f'<article class="bq-sector revela" id="{id_}" style="--retardo:{i * .08:.2f}s">{ilustracion(ilu)}'
            f'<h3>{nombre}</h3><p>{texto}</p>{lista_html}</article>')


# ── 3. Stack de tecnología ─────────────────────────────────────────────────
def stack(tags, titulo):
    lis = []
    for t in tags:
        clave = t.replace('®', '') if t.replace('®', '') in LOGOS else t
        d = LOGOS.get(t) or LOGOS.get(clave)
        if d:
            lis.append(f'<li class="bq-stack__item"><svg class="bq-stack__logo" viewBox="0 0 24 24" aria-hidden="true" '
                       f'focusable="false"><path d="{d}"/></svg><span>{t}</span></li>')
        else:
            lis.append(f'<li class="bq-stack__item bq-stack__item--idea">{barra("bq-barra--mini")}<span>{t}</span></li>')
    return (f'<div class="bq-stack revela"><h3 class="bq-stack__t">{titulo}</h3>'
            f'<ul class="bq-stack__lista">{"".join(lis)}</ul></div>')


# ── 4. Banda y cierre ───────────────────────────────────────────────────────
def banda(id_, ante, titulo, texto, href, cta, mono, mot=None, variante='negro'):
    arte = f'<div class="bq-banda__arte" aria-hidden="true">{motivo(mot)}</div>' if mot else ''
    return f'''<section class="bq-banda bq-banda--{variante} oscuro" aria-labelledby="{id_}">
  {zfondo()}
  {arte}
  <div class="envoltura bq-banda__fila revela">
    <img class="bq-banda__mono" src="{MONO}/{mono}_icono.svg" alt="" width="112" height="112" loading="lazy">
    <div class="bq-banda__texto">
      <span class="antetitulo">{ante}</span>
      <h2 id="{id_}">{titulo}</h2>
      <p>{texto}</p>
    </div>
    <a class="bq-cta" href="{href}">{cta}{FLECHA}</a>
  </div>
</section>'''


def cierre(id_, titulo, texto, botones, icono='', pie=''):
    """Llamada final: banda azul con la z madre recortada. `botones` es HTML con .boton."""
    ico = f'<img class="bq-cierre__icono" src="{icono}" alt="" width="64" height="64" loading="lazy">' if icono else ''
    return f'''<section class="seccion bq-cierre llamada" aria-labelledby="{id_}">
  {zfondo()}
  <div class="envoltura">
    <div class="bq-cierre__fila revela">
      <div>
        {ico}
        <h2 id="{id_}">{titulo}</h2>
        <p>{texto}</p>
      </div>
      <div class="botones">{botones}</div>
    </div>{('\n    ' + pie.replace('class="apagado"', 'class="bq-cierre__pie"')) if pie else ''}
  </div>
</section>'''


# ── 5. Ruta y cifras ────────────────────────────────────────────────────────
def pasos(items, etiqueta=''):
    lis = ''.join(f'<li class="bq-ruta__paso" style="--i:{i}"><span class="bq-ruta__n" aria-hidden="true">{i + 1:02d}</span>'
                  f'<h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(items))
    al = f' aria-label="{etiqueta}"' if etiqueta else ''
    return f'<ol class="bq-ruta revela" style="--pasos:{len(items)}"{al}>{lis}</ol>'


def cifras(items):
    lis = ''.join(f'<li class="bq-cifra" style="--i:{i}"><b data-cuenta="{n}">{n}</b>{barra()}<span>{t}</span></li>'
                  for i, (n, t) in enumerate(items))
    return f'<ul class="bq-cifras revela">{lis}</ul>'


# ── 6. Contacto ─────────────────────────────────────────────────────────────
DIRECCION = {'calle': '10302 NW South River Drive', 'ciudad': 'Medley', 'region': 'FL', 'cp': '33178',
             'pais': {'es': 'Estados Unidos', 'en': 'United States'}, 'iso': 'US'}
_Q = quote('10302 NW South River Drive, Medley, FL 33178')
MAPAS = {'google': f'https://www.google.com/maps/search/?api=1&query={_Q}', 'apple': f'https://maps.apple.com/?q={_Q}'}

CONTACTO_TXT = {
    'es': {'ante': 'Contacto', 'titulo': 'Cuéntanos cómo trabaja tu equipo.',
           'apoyo': 'Te responde una persona, en español, en menos de un día hábil.',
           'g1': 'Escríbenos', 'correo': 'Correo', 'wa': 'WhatsApp', 'asunto': 'Zentrix: hablemos',
           'g2': '¿Ya usas nuestras apps?', 'soporte': 'Soporte', 'manual': 'Documentación de', 'centro': 'Centro de soporte',
           'dir_t': 'Dirección', 'llegar': 'Cómo llegar', 'en_google': 'Google Maps', 'en_apple': 'Apple Maps',
           'horario_t': 'Horario', 'horario': 'Lunes a viernes, 9:00 a 19:00 (UTC−4)',
           'base_t': 'Equipo', 'base': 'Isla Margarita, Venezuela, en remoto para todo el mundo',
           'idiomas_t': 'Idiomas', 'idiomas': 'Español e inglés', 'mapa': 'Mapa ilustrado de la zona de la dirección'},
    'en': {'ante': 'Contact', 'titulo': 'Tell us how your team works.',
           'apoyo': 'A real person replies, in Spanish or English, within one business day.',
           'g1': 'Write to us', 'correo': 'Email', 'wa': 'WhatsApp', 'asunto': 'Zentrix: let’s talk',
           'g2': 'Already using our apps?', 'soporte': 'Support', 'manual': 'Documentation for', 'centro': 'Support center',
           'dir_t': 'Address', 'llegar': 'Get directions', 'en_google': 'Google Maps', 'en_apple': 'Apple Maps',
           'horario_t': 'Hours', 'horario': 'Monday to Friday, 9:00 to 19:00 (UTC−4)',
           'base_t': 'Team', 'base': 'Isla Margarita, Venezuela, working remotely worldwide',
           'idiomas_t': 'Languages', 'idiomas': 'Spanish and English', 'mapa': 'Illustrated map of the area around the address'},
}


CONTACTO_DETALLE = {
    'es': {'horario': 'Lunes a viernes, 9:00 a 19:00 (UTC−4). Lo que llega fuera de horario se atiende el siguiente día hábil.',
           'base': 'Isla Margarita, Nueva Esparta, Venezuela. Los proyectos se trabajan en remoto, así que la zona horaria no es un problema.'},
    'en': {'horario': 'Monday to Friday, 9:00 to 19:00 (UTC−4). Messages sent outside these hours are answered the next business day.',
           'base': 'Isla Margarita, Nueva Esparta, Venezuela. Projects run remotely, so time zones are not a problem.'},
}


def icono(nombre, clase='bq-ico'):
    return ilustracion(nombre, clase)


def mapa():
    """Mapa estático estilizado (no es cartografía): calles, el río y el punto de la dirección."""
    calles = ''.join(f'<path d="M{x} 0V360"/>' for x in (70, 190, 330, 470)) + ''.join(f'<path d="M0 {y}H600"/>' for y in (60, 150, 250))
    manzanas = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>' for x, y, w, h in
                       ((84, 74, 92, 62), (204, 74, 112, 62), (344, 74, 112, 62), (84, 164, 92, 72),
                        (344, 164, 112, 72), (484, 164, 100, 72), (204, 264, 112, 80), (484, 74, 100, 62)))
    return ('<svg class="bq-mapa" viewBox="0 0 600 360" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            '<rect width="600" height="360" class="bq-mapa__fondo"/>'
            f'<g class="bq-mapa__manzanas">{manzanas}</g>'
            f'<g class="bq-mapa__calles">{calles}</g>'
            '<path class="bq-mapa__rio" d="M-20 330C110 300 160 222 262 214S430 262 620 196"/>'
            '<path class="bq-mapa__ruta" d="M70 360V250H260V196"/>'
            '<g class="bq-mapa__pin" transform="translate(260 196)"><path d="M0 0-30-38a38 38 0 1 1 60 0Z"/>'
            f'<path class="bq-ilu__l" d="M-17-73h34l-{12 * BISEL:.0f} 12h-22z"/></g></svg>')


def _docs(lang):
    sop = '/en/' if lang == 'en' and (RAIZ / 'en' / 'index.html').exists() else '/'
    return f'{sop}work/docs/', f'{sop}sales/docs/'


def hablemos(lang, id_='contacto', h='h2', ante=None, titulo=None, seccion=True):
    """Banda de contacto: titular a la izquierda y dos acciones a la derecha. Sin dirección:
    esa vive solo en /contacto/, en las páginas legales y en el JSON-LD de Organization."""
    t = CONTACTO_TXT[lang]
    w_docs, s_docs = _docs(lang)
    idt = f'{id_}-t'
    panel = f'''<div class="bq-hablemos oscuro">
    {zfondo()}
    <div class="bq-hablemos__texto revela">
      <span class="antetitulo">{ante or t['ante']}</span>
      <{h} class="bq-hablemos__t" id="{idt}">{titulo or t['titulo']}</{h}>
      <p class="bq-hablemos__apoyo">{barra()}<span>{t['apoyo']}</span></p>
    </div>
    <div class="bq-hablemos__acciones revela" style="--retardo:.1s">
      <div class="bq-hablemos__grupo" role="group" aria-labelledby="{id_}-g1">
        <p class="bq-hablemos__g" id="{id_}-g1">{t['g1']}</p>
        <div class="bq-hablemos__botones">
          <a class="bq-btn bq-btn--lima" href="mailto:hola@zentrix.company?subject={quote(t['asunto'])}">{icono('correo')}<span><small>{t['correo']}</small><b>hola@zentrix.company</b></span></a>
          <a class="bq-btn bq-btn--contorno" href="https://wa.me/584123469712">{icono('whatsapp')}<span><small>{t['wa']}</small><b>+58 412-346 9712</b></span></a>
        </div>
      </div>
      <div class="bq-hablemos__grupo bq-hablemos__grupo--sec" role="group" aria-labelledby="{id_}-g2">
        <p class="bq-hablemos__g" id="{id_}-g2">{t['g2']}</p>
        <div class="bq-hablemos__botones bq-hablemos__botones--sec">
          <a class="bq-btn bq-btn--suave" href="mailto:soporte@zentrix.company"><span><small>{t['soporte']}</small><b>soporte@zentrix.company</b></span></a>
          <a class="bq-btn bq-btn--chip" href="{w_docs.replace('work/docs/', 'support/' if lang == 'en' else 'soporte/')}">{t['centro']}{FLECHA}</a>
          <a class="bq-btn bq-btn--chip" href="{w_docs}">{t['manual']} Zentrix Work{FLECHA}</a>
          <a class="bq-btn bq-btn--chip" href="{s_docs}">{t['manual']} Zentrix Sales{FLECHA}</a>
        </div>
      </div>
    </div>
  </div>'''
    if not seccion:
        return panel
    return f'''<section class="seccion bq-seccion--hablemos" id="{id_}" aria-labelledby="{idt}">
  <div class="envoltura">
  {panel}
  </div>
</section>'''


def contacto(lang, detalle=True, ante=None, titulo=None):
    """Bloque de /contacto/: la banda, y debajo el lugar (dirección y mapa) y los datos."""
    t = dict(CONTACTO_TXT[lang])
    if detalle:
        t.update(CONTACTO_DETALLE[lang])
    d = DIRECCION
    return f'''{hablemos(lang, id_='canales', ante=ante, titulo=titulo, seccion=False)}
<div class="bq-contacto">
  <div class="bq-contacto__lugar revela">
    <div class="bq-contacto__mapa" role="img" aria-label="{t['mapa']}">{mapa()}</div>
    <div class="bq-contacto__dir">
      <h3 class="bq-contacto__dt">{icono('lugar')}{t['dir_t']}</h3>
      <address itemscope itemtype="https://schema.org/PostalAddress">
        <span itemprop="streetAddress">{d['calle']}</span><br>
        <span itemprop="addressLocality">{d['ciudad']}</span>, <span itemprop="addressRegion">{d['region']}</span> <span itemprop="postalCode">{d['cp']}</span><br>
        <span itemprop="addressCountry" content="{d['iso']}">{d['pais'][lang]}</span>
      </address>
      <p class="bq-contacto__llegar"><b>{t['llegar']}:</b> <a href="{MAPAS['google']}">{t['en_google']}{FLECHA}</a> <a href="{MAPAS['apple']}">{t['en_apple']}{FLECHA}</a></p>
    </div>
  </div>
  <dl class="bq-datos revela" style="--retardo:.1s">
    <div>{icono('reloj')}<dt>{t['horario_t']}</dt><dd>{t['horario']}</dd></div>
    <div>{icono('idioma')}<dt>{t['idiomas_t']}</dt><dd>{t['idiomas']}</dd></div>
    <div>{icono('lugar')}<dt>{t['base_t']}</dt><dd>{t['base']}</dd></div>
  </dl>
</div>'''


# ── Aplicación a las páginas ────────────────────────────────────────────────
def lang_de(ruta):
    return 'en' if ruta.startswith('/en/') or ruta.startswith('/sales/en/') else 'es'


RE_BQ = re.compile(r'<!--BQ:(\w+)-->.*?<!--/BQ:\1-->', re.S)


def _marcador(m, ruta):
    nombre = m.group(1)
    lang = lang_de(ruta)
    if nombre == 'CONTACTO':
        cuerpo = hablemos(lang, id_='contact' if lang == 'en' else 'contacto')
    elif nombre == 'ZFONDO':
        cuerpo = zfondo()
    elif nombre == 'FLECHA':
        cuerpo = FLECHA
    else:
        return m.group(0)
    return f'<!--BQ:{nombre}-->{cuerpo}<!--/BQ:{nombre}-->'


def _texto(li):
    """<li><b>Título</b> texto</li> → (título, texto)."""
    m = re.match(r'\s*<b>(.*?)</b>\s*(.*)', li, re.S)
    return (m.group(1).strip(), m.group(2).strip()) if m else ('', li.strip())


def _funciones(m, ruta):
    tarjetas = re.findall(r'<div class="tarjeta[^"]*"[^>]*>.*?<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>', m.group(0), re.S)
    mot = MOTIVO_DE_RUTA.get(ruta.replace('/en/', '/'))
    if ruta.startswith('/sales/en/'):
        mot = 'ruta'
    return pilares(tarjetas, 'prota' if mot else '', motivo(mot) if mot else '')


def _casos(m, ruta):
    items = [_texto(li) for li in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S)]
    return pilares(items, 'oscuro')


def _proceso(m, ruta):
    items = [_texto(li) for li in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S)]
    return pasos(items)


def _cifras(m, ruta):
    items = re.findall(r'<li><b data-cuenta="(\d+)">\d+</b><span>(.*?)</span></li>', m.group(1), re.S)
    return cifras(items)


RE_FUNCIONES = re.compile(r'<div class="rejilla rejilla--\d funciones">(.*?)</div>\s*(?=</div>\s*</section>)', re.S)
RE_CASOS = re.compile(r'<ol class="casos casos--\d">(.*?)</ol>', re.S)
RE_PROCESO = re.compile(r'<ol class="proceso[^"]*">(.*?)</ol>', re.S)
RE_CIFRAS = re.compile(r'<ul class="cifras revela"[^>]*>(.*?)</ul>', re.S)
RE_LLAMADA = re.compile(r'<section class="seccion(?: seccion--gris)?(?: llamada)?" aria-labelledby="([\w-]+)">\s*<div class="envoltura">\s*'
                        r'<div class="descarga revela">\s*(?:<svg class="descarga__z".*?</svg>|<img class="descarga__z"[^>]*>)?\s*'
                        r'<div>(.*?)</div>\s*<div class="botones">(.*?)</div>\s*</div>\s*(<p class="apagado"[^>]*>.*?</p>)?\s*</div>\s*</section>', re.S)


def _llamada(m):
    id_, texto, botones, pie = m.group(1), m.group(2), m.group(3), m.group(4) or ''
    pie = re.sub(r' style="[^"]*"', '', pie)
    ico = re.search(r'<img class="descarga__icono" src="([^"]+)"', texto)
    texto = re.sub(r'\s*<img class="descarga__icono"[^>]*>', '', texto).strip()
    h2 = re.search(r'<h2[^>]*>(.*?)</h2>', texto, re.S)
    resto = texto[h2.end():].strip()
    p = re.sub(r'^<p>|</p>$', '', resto, flags=re.S) if resto.count('<p>') == 1 else None
    if p is None:  # varios párrafos: se conservan tal cual
        s = cierre(id_, h2.group(1), '', botones.strip(), ico.group(1) if ico else '', pie)
        return s.replace('<p></p>', resto)
    return cierre(id_, h2.group(1), p, botones.strip(), ico.group(1) if ico else '', pie)


RE_NOTA = re.compile(r'(aria-labelledby="problema-t">(?:(?!</section>).)*?)<div class="tarjeta(?: revela)?"( style="[^"]*")?>\s*'
                     r'(<h3>.*?</h3>\s*<p>.*?</p>)\s*</div>', re.S)


def _nota(m):
    return f'{m.group(1)}<div class="bq-nota revela"{m.group(2) or ""}>{zfondo()}{barra()}{m.group(3)}</div>'


def aplicar(s, ruta):
    if '<main' not in s:
        return s
    s = re.sub(r'/assets/css/bloques\.css\?v=\d+', '/assets/css/bloques.css?v=4', s)  # versión al día
    s = s.replace(CSS_PRELOAD, CSS)
    s = re.sub(r'(?<!<noscript>)' + re.escape(CSS_BLOQUEANTE), lambda m: CSS, s)
    if 'bloques.css' not in s:
        s = re.sub(r'(<link rel="stylesheet" href="/assets/css/sitio\.css[^"]*">)', r'\1\n  ' + CSS, s, count=1)
    s = RE_BQ.sub(lambda m: _marcador(m, ruta), s)
    s = RE_FUNCIONES.sub(lambda m: _funciones(m, ruta), s)
    s = RE_CASOS.sub(lambda m: _casos(m, ruta), s)
    s = RE_PROCESO.sub(lambda m: _proceso(m, ruta), s)
    s = RE_CIFRAS.sub(lambda m: _cifras(m, ruta), s)
    s = RE_LLAMADA.sub(_llamada, s)
    s = RE_NOTA.sub(_nota, s)
    if 'bq-brillo' in s and 'bloques.js' not in s:
        s = s.replace('</head>', f'  {JS}\n</head>', 1)
    return s


# ── SVG sueltos para reutilizar fuera de los bloques (mega-menú, pie) ───────
SUELTOS = {'soluciones': ('odoo', 'software', 'auditoria', 'infra', 'pagos', 'vision'),
           'iconos': ('correo', 'whatsapp', 'reloj', 'lugar', 'idioma')}


def svgs_sueltos(color='#244DFF'):
    """{ruta relativa: contenido}: assets/img/soluciones/<clave>.svg y assets/img/iconos/<nombre>.svg.
    Mismo dibujo que en línea, con los colores escritos (azul y lima) para usarlos con <img>."""
    salida = {}
    for carpeta, nombres in SUELTOS.items():
        for n in nombres:
            cuerpo = (ILU[n].replace('class="bq-ilu__t"', f'fill="none" stroke="{color}" stroke-width="104"')
                      .replace('class="bq-ilu__f"', f'fill="{color}"').replace('class="bq-ilu__l"', 'fill="#C7FA46"'))
            salida[f'assets/img/{carpeta}/{n}.svg'] = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -60 1120 1120" '
                                                      f'width="48" height="48">{cuerpo}</svg>\n')
    return salida
