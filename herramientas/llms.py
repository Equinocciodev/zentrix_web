#!/usr/bin/env python3
"""Genera `llms-full.txt` a partir del HTML del sitio (https://llmstxt.org).

`llms.txt` (quién es Zentrix, productos, soluciones, equipo y contacto) lo escribe
`herramientas/generar.py`; este script añade `llms-full.txt`: el mismo resumen y, por
grupos, el title, la description y el texto visible del `<main>` de cada página indexable,
para que un asistente pueda responder sobre Zentrix sin rastrear el sitio. El workflow de
Pages lo regenera en cada despliegue.

    python3 herramientas/llms.py           # escribe llms-full.txt en la raíz
    python3 herramientas/llms.py --check   # sale con 1 si difiere de lo commiteado
"""
import html
import pathlib
import re
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sitemap import RAIZ, indexable, paginas  # noqa: E402

SITIO = 'https://zentrix.company'

CABECERA = """# Zentrix

> Zentrix (zentrix.company) convierte los procesos de las empresas en apps sencillas conectadas a su sistema de gestión. Eslogan: «Tecnología para trabajar mejor» (EN: «Technology to work better»). Es el nuevo nombre de Equinoccio (eqnio.com, que redirige a Zentrix).

Datos clave:
- Productos en producción: Zentrix Work (app Android del equipo de tienda) y Zentrix Sales (app de fuerza de ventas para Android y iPhone, integración nativa con Odoo® 17, 18 y 19).
- Divisiones: Zentrix AI, Zentrix Logistics (próximamente), Zentrix Cloud, Zentrix Labs y Zentrix Software (implementación de Odoo®). Traza es un producto de Zentrix con sitio propio: [traza.technology](https://traza.technology)
- Contacto: [hola@zentrix.company](mailto:hola@zentrix.company) (general y Zentrix Sales), [soporte@zentrix.company](mailto:soporte@zentrix.company) (soporte y Zentrix Work), teléfono y [WhatsApp +58 412-346 9712](https://wa.me/584123469712). Responde una persona, en español, en menos de un día hábil.
- La marca se escribe «Zentrix», «Zentrix Work», «Zentrix Sales», «Zentrix AI», «Zentrix Logistics», «Zentrix Cloud», «Zentrix Labs», «Zentrix Software» y «Traza».
"""

PRODUCTOS = ('/work/', '/sales/', '/check/', '/ai/', '/logistics/', '/cloud/', '/labs/', '/software/', '/traza/')
GRUPOS = [
    ('Zentrix', lambda r: r in ('/', '/nosotros/', '/clientes/', '/contacto/', '/recursos/')),
    ('Productos', lambda r: r in PRODUCTOS),
    ('Soluciones', lambda r: r.startswith('/soluciones/')),
    ('English', lambda r: r.startswith('/sales/en/') or r.startswith('/en/')),
    ('Manual de Zentrix Work', lambda r: r.startswith('/work/docs/')),
    ('Manual de Zentrix Sales', lambda r: r.startswith('/sales/docs/')),
    ('Manual de Zentrix Check', lambda r: r.startswith('/check/docs/')),
    ('Legal, soporte y contacto', lambda r: True),
]


def enlace(m, base):
    """<a href> → enlace Markdown [texto](url absoluta); sin texto legible, solo el texto."""
    attrs, interior = m.group(1), m.group(2)
    t = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', interior)).split())
    h = re.search(r'href="([^"]*)"', attrs)
    if not t or not h or h.group(1).startswith(('#', 'javascript:')):
        return ' %s ' % interior
    url = urllib.parse.urljoin(base, html.unescape(h.group(1)))
    t = t.replace('[', '(').replace(']', ')')
    return ' [%s](%s) ' % (t, url.replace(' ', '%20').replace(')', '%29'))


def texto(fragmento, base=SITIO + '/'):
    s = re.sub(r'<(script|style|svg|nav|header|footer)[\s\S]*?</\1>', '', fragmento)
    s = re.sub(r'<a\b([^>]*)>([\s\S]*?)</a>', lambda m: enlace(m, base), s)
    s = re.sub(r'</?(?:a|b|strong|em|i|span|code|kbd|small|mark|abbr)\b[^>]*>', '', s)
    s = re.sub(r'<(?:h[1-6])[^>]*>', '\n\n### ', s)
    s = re.sub(r'</(?:p|h[1-6]|li|div|section|tr|dd|dt|figcaption)>', '\n', s)
    s = re.sub(r'<li[^>]*>', '- ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    lineas = [' '.join(l.split()) for l in s.splitlines()]
    out, vacia = [], False
    for l in lineas:
        if not l or l in ('-', '###'):
            if not vacia and out:
                out.append('')
            vacia = True
            continue
        out.append(re.sub(r' ([.,;:!?»)])', r'\1', l))
        vacia = False
    return '\n'.join(out).strip()


def leer():
    filas = []
    for p in paginas():
        s = p.read_text(encoding='utf-8')
        if not indexable(s):
            continue
        cab = s[:s.find('</head>')]
        url = re.search(r'<link rel="canonical" href="([^"]+)"', cab)
        if not url:
            continue
        url = url.group(1)
        titulo = html.unescape(re.search(r'<title>([\s\S]*?)</title>', cab).group(1).strip())
        d = re.search(r'<meta name="description" content="([^"]*)"', cab)
        main = re.search(r'<main[\s\S]*?</main>', s)
        filas.append((url[len(SITIO):] or '/', url, titulo, html.unescape(d.group(1)) if d else '',
                      texto(main.group(0), url) if main else ''))
    return filas


def generar():
    filas = leer()
    completo = [CABECERA, 'Índice breve: [llms.txt](%s/llms.txt)' % SITIO]
    usadas = set()
    for nombre, cond in GRUPOS:
        grupo = [f for f in filas if f[0] not in usadas and cond(f[0])]
        if not grupo:
            continue
        usadas.update(f[0] for f in grupo)
        completo.append('\n# %s\n' % nombre)
        for _, u, t, d, cuerpo in grupo:
            completo.append('\n---\n\n## [%s](%s)\n\n%s\n\n%s\n' % (t, u, d, cuerpo))
    return '\n'.join(completo).rstrip() + '\n'


def main():
    destinos = {RAIZ / 'llms-full.txt': generar()}
    if '--check' in sys.argv:
        malos = [p.name for p, t in destinos.items() if not p.exists() or p.read_text(encoding='utf-8') != t]
        if malos:
            print('difieren: ' + ', '.join(malos))
            sys.exit(1)
        print('llms al día')
        return
    for p, t in destinos.items():
        p.write_text(t, encoding='utf-8')
        print('%s: %d KB' % (p.name, len(t.encode()) // 1024))


if __name__ == '__main__':
    main()
