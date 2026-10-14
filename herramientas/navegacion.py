#!/usr/bin/env python3
"""Fuente única del menú «Productos» y del pie de página de todo el sitio.

El sitio es estático y no tiene paso de compilación: este script reescribe, en cada
página .html, el bloque `<details class="menu-productos">…</details>` de la cabecera y
el `<footer class="pie">…</footer>`, a partir de los datos de abajo. Se ejecuta a mano
después de cambiar un producto, un enlace o un texto del pie, y el resultado se commitea:

    python3 herramientas/navegacion.py          # reescribe
    python3 herramientas/navegacion.py --check  # solo comprueba (sale con 1 si algo difiere)

Las páginas de `sales/en/` reciben la versión en inglés. En texto, la marca va siempre con
mayúscula inicial («Zentrix AI», «Traza», «© 2026 Zentrix®»); solo el logotipo gráfico va
en minúscula.
"""
import html
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MONO = '/assets/img/logos/monogramas'
TRAZA_ICONO = '/assets/img/logos/traza/traza_icono-64.webp'
TRAZA_URL = 'https://traza.technology'

# Orden de la suite: los productos Zentrix y, al final, Traza como marca asociada.
# clave, ruta, nombre, descripción ES, descripción EN
PRODUCTOS = [
    ('work', '/work/', 'Zentrix Work', 'El equipo de tienda', 'Store teams'),
    ('sales', '/sales/', 'Zentrix Sales', 'La fuerza de ventas', 'Field sales'),
    ('ai', '/ai/', 'Zentrix AI', 'Inteligencia aplicada', 'Applied intelligence'),
    ('logistica', '/logistica/', 'Zentrix Logística', 'Despachos y entregas · Próximamente', 'Dispatch and delivery · Coming soon'),
    ('cloud', '/cloud/', 'Zentrix Cloud', 'Infraestructura', 'Infrastructure'),
    ('labs', '/labs/', 'Zentrix Labs', 'Investigación', 'Research'),
    ('software', '/software/', 'Zentrix Software', 'Implementación de Odoo®', 'Odoo® implementation'),
    ('traza', TRAZA_URL, 'Traza', 'Un producto de Zentrix®', 'A Zentrix® product'),
]

T = {
    'es': {
        'productos': 'Productos', 'recursos': 'Recursos', 'legal': 'Legal y soporte', 'contacto': 'Contacto',
        'externo': ' (se abre en otra pestaña)', 'lema': 'La inteligencia se convierte en operación.',
        'manual_work': 'Manual de Zentrix Work', 'manual_sales': 'Manual de Zentrix Sales',
        'privacidad': 'Privacidad', 'soporte': 'Soporte', 'terminos': 'Términos', 'contacto_l': 'Contacto',
        'copy': '© 2026 Zentrix®. Todos los derechos reservados.', 'odoo': 'Odoo® conserva su marca y propiedad.',
        'idioma': 'Idioma', 'suite': 'La suite de Zentrix', 'nota_en': '',
    },
    'en': {
        'productos': 'Products', 'recursos': 'Resources', 'legal': 'Legal and support', 'contacto': 'Contact',
        'externo': ' (opens in a new tab)', 'lema': 'Intelligence becomes operation.',
        'manual_work': 'Zentrix Work manual', 'manual_sales': 'Zentrix Sales manual',
        'privacidad': 'Privacy', 'soporte': 'Support', 'terminos': 'Terms', 'contacto_l': 'Contact',
        'copy': '© 2026 Zentrix®. All rights reserved.', 'odoo': 'Odoo® remains the property of its owner.',
        'idioma': 'Language', 'suite': 'The Zentrix suite', 'nota_en': ' (en español)',
    },
}

# Legal y soporte, agrupado por producto. (texto, ruta ES, ruta EN o None si solo hay español)
LEGAL = [
    ('Zentrix Work', [
        ('privacidad', '/work/privacidad/', None),
        ('soporte', '/work/soporte/', None),
        ('terminos', '/work/terminos/', None),
    ]),
    ('Zentrix Sales', [
        ('privacidad', '/sales/privacidad/', '/sales/en/privacy.html'),
        ('soporte', '/sales/soporte/', '/sales/en/support.html'),
        ('terminos', '/sales/terminos/', '/sales/en/terms.html'),
        ('contacto_l', '/sales/contacto/', '/sales/en/contact.html'),
    ]),
]

# Equivalencias ES ↔ EN para el selector de idioma (solo Zentrix Sales tiene inglés).
EQUIV = {
    '/sales/': '/sales/en/',
    '/sales/privacidad/': '/sales/en/privacy.html',
    '/sales/terminos/': '/sales/en/terms.html',
    '/sales/soporte/': '/sales/en/support.html',
    '/sales/contacto/': '/sales/en/contact.html',
}
EQUIV_INV = {v: k for k, v in EQUIV.items()}

SVG_EXTERNO = ('<svg class="externo" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
               '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')
SVG_CORREO = ('<svg class="pie__icono" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
              '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5 12 13l8.5-6.5"/></svg>')
SVG_WHATSAPP = ('<svg class="pie__icono" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
                '<path d="M4 20l1.3-3.9A8.5 8.5 0 1 1 8 18.8z"/>'
                '<path d="M9 8.6c0 3.3 3 6.4 6.4 6.4l1.1-1.6-2-1-1 .8a5 5 0 0 1-2.7-2.7l.8-1-1-2z"/></svg>')


def ruta_de(archivo: pathlib.Path) -> str:
    rel = archivo.relative_to(RAIZ).as_posix()
    if rel.endswith('index.html'):
        rel = rel[: -len('index.html')]
    return '/' + rel


def icono(clave, tam, lazy=False):
    src = TRAZA_ICONO if clave == 'traza' else f'{MONO}/{clave}_icono.svg'
    carga = ' loading="lazy" decoding="async"' if lazy else ''
    return f'<img src="{src}" alt="" width="{tam}" height="{tam}"{carga}>'


def menu(ruta, lang):
    t = T[lang]
    seccion = next((p for p in PRODUCTOS if p[1] != TRAZA_URL and ruta.startswith(p[1])), None)
    activo = ' class="activo"' if seccion else ''
    items = []
    for clave, href, nombre, d_es, d_en in PRODUCTOS:
        desc = d_en if lang == 'en' else d_es
        if clave == 'traza':
            items.append(f'<li><a href="{href}" target="_blank" rel="noopener">{icono(clave, 32)}'
                         f'<b>{nombre}{SVG_EXTERNO}<span class="sr">{t["externo"]}</span></b>'
                         f'<span>{html.escape(desc, quote=False)}</span></a></li>')
        else:
            cur = ' aria-current="page"' if seccion and seccion[0] == clave else ''
            items.append(f'<li><a href="{href}"{cur}>{icono(clave, 32)}<b>{nombre}</b>'
                         f'<span>{html.escape(desc, quote=False)}</span></a></li>')
    return (f'<details class="menu-productos"><summary{activo}>{t["productos"]}</summary>'
            f'<ul class="menu-productos__lista">{"".join(items)}</ul></details>')


def pie(ruta, lang):
    t = T[lang]
    # Columna de marca: wordmark, lema y la suite en miniatura.
    suite = ''.join(f'<li>{icono(c, 24, lazy=True)}</li>' for c, *_ in PRODUCTOS)
    marca = (
        '      <div class="pie__marca">\n'
        f'        <img class="pie__logo" src="/assets/img/logos/zentrix-blanco.svg" alt="Zentrix" width="110" height="22" loading="lazy">\n'
        f'        <p class="pie__lema">{t["lema"]}</p>\n'
        f'        <ul class="pie__suite" aria-label="{t["suite"]}">{suite}</ul>\n'
        '      </div>\n'
    )
    # Productos
    prods = []
    for clave, href, nombre, *_ in PRODUCTOS:
        if clave == 'traza':
            prods.append(f'<li><a href="{href}" target="_blank" rel="noopener">{icono(clave, 20, lazy=True)}'
                         f'<span>{nombre}{SVG_EXTERNO}<span class="sr">{t["externo"]}</span></span></a></li>')
        else:
            prods.append(f'<li><a href="{href}">{icono(clave, 20, lazy=True)}<span>{nombre}</span></a></li>')
    col_prod = (
        '      <div class="pie__col pie__col--productos">\n'
        f'        <h2>{t["productos"]}</h2>\n'
        f'        <ul class="pie__productos">{"".join(prods)}</ul>\n'
        '      </div>\n'
    )
    es_lang = '' if lang == 'es' else ' hreflang="es"'
    nota = t['nota_en']
    col_rec = (
        '      <div class="pie__col">\n'
        f'        <h2>{t["recursos"]}</h2>\n'
        '        <ul>'
        f'<li><a href="/work/docs/"{es_lang}>{t["manual_work"]}{nota}</a></li>'
        f'<li><a href="/sales/docs/"{es_lang}>{t["manual_sales"]}{nota}</a></li>'
        '</ul>\n'
        '      </div>\n'
    )
    grupos = []
    for prod, enlaces in LEGAL:
        links = []
        for k, r_es, r_en in enlaces:
            if lang == 'en' and r_en:
                href, extra = r_en, ''
            else:
                href, extra = r_es, es_lang
            links.append(f'<li><a href="{href}"{extra}>{t[k]}</a></li>')
        grupos.append(f'<div class="pie__grupo"><h3>{prod}</h3><ul class="pie__enlinea">{"".join(links)}</ul></div>')
    col_legal = (
        '      <div class="pie__col pie__col--legal">\n'
        f'        <h2>{t["legal"]}</h2>\n'
        f'        {"".join(grupos)}\n'
        '      </div>\n'
    )
    col_cont = (
        '      <div class="pie__col pie__col--contacto">\n'
        f'        <h2>{t["contacto"]}</h2>\n'
        '        <ul class="pie__contacto">'
        f'<li><a href="mailto:hola@zentrix.company">{SVG_CORREO}<span>hola@zentrix.company</span></a></li>'
        f'<li><a href="mailto:soporte@zentrix.company">{SVG_CORREO}<span>soporte@zentrix.company</span></a></li>'
        f'<li><a href="https://wa.me/584123469712">{SVG_WHATSAPP}<span>WhatsApp +58 412-346 9712</span></a></li>'
        '</ul>\n'
        '      </div>\n'
    )
    # Selector de idioma: la página equivalente si existe; si no, la portada (ES) o Zentrix Sales (EN).
    if lang == 'es':
        href_es, href_en = ruta, EQUIV.get(ruta, '/sales/en/')
    else:
        href_es, href_en = EQUIV_INV.get(ruta, '/'), ruta
    cur_es = ' aria-current="true"' if lang == 'es' else ''
    cur_en = ' aria-current="true"' if lang == 'en' else ''
    idioma = (
        f'<ul class="pie__idioma" aria-label="{t["idioma"]}">'
        f'<li><a href="{href_es}" lang="es" hreflang="es"{cur_es} title="Español">ES</a></li>'
        f'<li><a href="{href_en}" lang="en" hreflang="en"{cur_en} title="English (Zentrix Sales)">EN</a></li>'
        '</ul>'
    )
    return (
        '<footer class="pie">\n'
        '  <div class="envoltura">\n'
        '    <div class="pie__reja">\n'
        f'{marca}{col_prod}{col_rec}{col_legal}{col_cont}'
        '    </div>\n'
        '    <div class="pie__base">\n'
        f'      <p>{t["copy"]}</p>\n'
        f'      <div class="pie__base-der">{idioma}<p>{t["odoo"]}</p></div>\n'
        '    </div>\n'
        '  </div>\n'
        '</footer>'
    )


RE_MENU = re.compile(r'<details class="menu-productos">.*?</details>', re.S)
RE_PIE = re.compile(r'<footer class="pie">.*?</footer>', re.S)


def main():
    check = '--check' in sys.argv
    distintos = []
    for f in sorted(RAIZ.rglob('*.html')):
        if any(p.startswith('.') or p == 'herramientas' for p in f.relative_to(RAIZ).parts):
            continue
        s = f.read_text(encoding='utf-8')
        ruta = ruta_de(f)
        lang = 'en' if ruta.startswith('/sales/en/') else 'es'
        n = RE_MENU.sub(lambda m: menu(ruta, lang), s, count=1)
        n = RE_PIE.sub(lambda m: pie(ruta, lang), n, count=1)
        if n != s:
            distintos.append(f.relative_to(RAIZ).as_posix())
            if not check:
                f.write_text(n, encoding='utf-8')
    print(('difieren: ' if check else 'reescritas: ') + str(len(distintos)))
    if check and distintos:
        print('\n'.join(distintos))
        sys.exit(1)


if __name__ == '__main__':
    main()
