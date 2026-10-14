#!/usr/bin/env python3
"""Genera `sitemap.xml` a partir del HTML del sitio, para que nunca se desfase.

- Entran todas las páginas `.html` indexables: sin `noindex` y sin `meta refresh`
  (las redirecciones y la 404 quedan fuera).
- `loc` es el `canonical` de la página.
- `lastmod` es la fecha del último commit que tocó el archivo (`git log`); sin historial
  (por ejemplo, un clon superficial) usa la fecha de hoy. El workflow de Pages hace
  checkout con `fetch-depth: 0` para que la fecha sea la real.
- Las alternativas por idioma (`xhtml:link`) salen de los `<link rel="alternate" hreflang>`
  de cada página, que escribe `herramientas/seo.py`.

    python3 herramientas/sitemap.py            # escribe sitemap.xml en la raíz
    python3 herramientas/sitemap.py --check    # sale con 1 si el sitemap.xml commiteado difiere
"""
import datetime
import html
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
EXCLUIR = {'.git', '.github', 'node_modules', '_site', 'pagefind', 'herramientas'}


def paginas():
    for p in sorted(RAIZ.rglob('*.html')):
        if EXCLUIR.intersection(p.relative_to(RAIZ).parts):
            continue
        yield p


def indexable(s):
    return 'http-equiv="refresh"' not in s and not re.search(r'name="robots" content="[^"]*noindex', s)


def lastmod(p):
    try:
        f = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', str(p.relative_to(RAIZ))],
                           cwd=RAIZ, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        f = ''
    return f or datetime.date.today().isoformat()


def entradas():
    for p in paginas():
        s = p.read_text(encoding='utf-8')
        if not indexable(s):
            continue
        cab = s[:s.find('</head>')]
        m = re.search(r'<link rel="canonical" href="([^"]+)"', cab)
        if not m:
            continue
        alternas = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', cab)
        yield html.unescape(m.group(1)), lastmod(p), alternas


def generar():
    filas = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for loc, fecha, alternas in sorted(entradas(), key=lambda e: (e[0].count('/'), e[0])):
        filas.append('  <url>')
        filas.append('    <loc>%s</loc>' % html.escape(loc))
        filas.append('    <lastmod>%s</lastmod>' % fecha)
        for lang, href in alternas:
            filas.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (lang, html.escape(href)))
        filas.append('  </url>')
    filas.append('</urlset>')
    return '\n'.join(filas) + '\n'


def sin_fechas(texto):
    return re.sub(r'<lastmod>[^<]*</lastmod>', '', texto)


def main():
    destino = RAIZ / 'sitemap.xml'
    nuevo = generar()
    if '--check' in sys.argv:
        viejo = destino.read_text(encoding='utf-8') if destino.exists() else ''
        if sin_fechas(viejo) != sin_fechas(nuevo):
            print('sitemap.xml difiere: ejecuta python3 herramientas/sitemap.py')
            sys.exit(1)
        print('sitemap.xml al día')
        return
    destino.write_text(nuevo, encoding='utf-8')
    print('sitemap.xml: %d URL' % nuevo.count('<url>'))


if __name__ == '__main__':
    main()
