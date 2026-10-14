#!/usr/bin/env python3
"""Comprobador de enlaces internos: cada href/src que empieza por «/» debe existir en el
repo (fichero, carpeta con index.html o ancla de una página). Sale con 1 si hay rotos.

    python3 herramientas/enlaces.py
"""
import pathlib
import re
import sys
from urllib.parse import unquote

RAIZ = pathlib.Path(__file__).resolve().parent.parent
GENERADOS_EN_DESPLIEGUE = ('/pagefind/',)


def destino(ruta):
    ruta = unquote(ruta.split('?')[0])
    p = RAIZ / ruta.lstrip('/')
    if ruta.endswith('/'):
        p = p / 'index.html'
    return p


def main():
    rotos, anclas_rotas, total = [], [], 0
    ids = {}
    paginas = [f for f in RAIZ.rglob('*.html') if not any(x.startswith('.') or x == 'herramientas' for x in f.relative_to(RAIZ).parts)]
    for f in paginas:
        ids[f.resolve()] = set(re.findall(r'\sid="([^"]+)"', f.read_text(encoding='utf-8')))
    for f in paginas:
        s = f.read_text(encoding='utf-8')
        urls = [u for _, u in re.findall(r'\s(href|src)="(/[^"]*)"', s)]
        for ss in re.findall(r'\ssrcset="([^"]*)"', s):
            urls += [c.strip().split(' ')[0] for c in ss.split(',') if c.strip().startswith('/')]
        for url in urls:
            if url.startswith('//') or url.startswith(GENERADOS_EN_DESPLIEGUE):
                continue
            total += 1
            base, _, ancla = url.partition('#')
            d = destino(base or '/')
            if not d.exists():
                rotos.append(f'{f.relative_to(RAIZ)} → {url}')
            elif ancla and d.suffix == '.html' and 'http-equiv="refresh"' not in d.read_text(encoding='utf-8'):
                if ancla not in ids.get(d.resolve(), set()):
                    anclas_rotas.append(f'{f.relative_to(RAIZ)} → {url}')
    print(f'enlaces comprobados: {total} · rotos: {len(rotos)} · anclas rotas: {len(anclas_rotas)}')
    for x in sorted(set(rotos)) + sorted(set(anclas_rotas)):
        print('  ' + x)
    sys.exit(1 if rotos or anclas_rotas else 0)


if __name__ == '__main__':
    main()
