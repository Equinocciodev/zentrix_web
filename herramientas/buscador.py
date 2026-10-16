#!/usr/bin/env python3
"""Prepara el sitio para el buscador (Pagefind) en el paso de publicación.

Lo ejecuta el workflow de Pages sobre la copia que se publica, justo antes de
`npx pagefind --site .`; no hace falta commitear su resultado. Sin dependencias.

1. Marca el contenido de cada página indexable (el `<main>`) con
   `data-pagefind-body`, los filtros `producto` y `tipo`, el peso de los títulos
   y, en las portadas de producto, el nombre del producto con peso alto.
   Cabecera, mega-menú, pie y banner de cookies quedan fuera (están fuera de
   `<main>` y además en `exclude_selectors` de `pagefind.yml`).
2. Deja fuera las páginas de redirección (meta refresh), la 404, las de eqnio,
   `/logistica/` y las rutas viejas de idioma.
3. Escribe `buscador/terminos-<lang>.json`: títulos y palabras del sitio por
   frecuencia, para el autocompletado en gris del campo.

Uso:  python3 herramientas/buscador.py [--sitio DIR] [--check]
      --check  solo lista qué se indexaría, sin escribir nada.
"""
import argparse
import collections
import html
import json
import pathlib
import re
import sys
import unicodedata

PRODUCTOS = {
    'work': 'Zentrix Work',
    'sales': 'Zentrix Sales',
    'check': 'Zentrix Check',
    'ai': 'Zentrix AI',
    'logistics': 'Zentrix Logistics',
    'cloud': 'Zentrix Cloud',
    'labs': 'Zentrix Labs',
    'software': 'Zentrix Software',
    'traza': 'Traza',
}
LEGAL = {'privacidad', 'terminos', 'soporte', 'privacy', 'terms', 'support', 'legal'}
SOLUCIONES = {'soluciones', 'solutions'}
# Prefijos que nunca se indexan (rutas relativas a la raíz del sitio).
FUERA = ('eqnio/', 'logistica/', 'pagefind/', 'buscador/', 'herramientas/',
         'node_modules/', '.github/', '.git/')
FUERA_ARCHIVOS = {'404.html', 'en/404.html'}

RE_MAIN = re.compile(r'<main\b([^>]*)>', re.I)
RE_LANG = re.compile(r'<html\b[^>]*\blang="([a-zA-Z-]+)"', re.I)
RE_REFRESH = re.compile(r'<meta[^>]+http-equiv=["\']refresh', re.I)
RE_NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', re.I)
RE_TITULO = re.compile(r'<(h[12])\b([^>]*)>', re.I)


def lengua(texto):
    m = RE_LANG.search(texto)
    return (m.group(1).split('-')[0].lower() if m else 'es')


def ruta_relativa(raiz, archivo):
    return archivo.relative_to(raiz).as_posix()


def indexable(raiz, rel, texto):
    if rel in FUERA_ARCHIVOS or rel.startswith(FUERA):
        return False
    if RE_REFRESH.search(texto) or RE_NOINDEX.search(texto):
        return False
    # Rutas viejas de idioma: /sales/en/ cuando ya existe /en/ (multiidioma).
    if rel.startswith('sales/en/') and (raiz / 'en' / 'index.html').exists():
        return False
    return bool(RE_MAIN.search(texto))


def clasificar(rel):
    """(producto, tipo, portada) a partir de la ruta."""
    partes = rel.split('/')
    if partes[0] == 'en':
        partes = partes[1:]
    if partes[-1] == 'index.html':
        partes = partes[:-1]
    if partes[-1:] and partes[-1] == 'en':      # /sales/en/ (ruta vieja de idioma)
        partes = partes[:-1]
    if not partes:
        return 'Zentrix', 'producto', True
    seg = partes[0]
    producto = PRODUCTOS.get(seg, 'Zentrix')
    resto = [p.removesuffix('.html') for p in partes[1:]]
    if 'docs' in resto:
        return producto, 'manual', False
    if any(p in LEGAL for p in resto) or seg.removesuffix('.html') in LEGAL:
        return producto, 'legal', False
    if seg.removesuffix('.html') in SOLUCIONES:
        return producto, 'solucion', False
    if seg in PRODUCTOS:
        return producto, 'producto', not resto
    return producto, 'pagina', False


def anotar(texto, producto, tipo, portada):
    """Añade los atributos de Pagefind al <main> y a sus títulos (idempotente)."""
    m = RE_MAIN.search(texto)
    attrs = m.group(1)
    if 'data-pagefind-body' in attrs:
        return texto
    nuevos = f' data-pagefind-body data-pagefind-filter="producto:{producto}"'
    if portada and producto != 'Zentrix':
        nuevos += f' data-pagefind-meta="title:{producto}"'
    # Un filtro por elemento: Pagefind no separa «a:x, b:y» en dos filtros.
    extra = f'\n<span hidden data-pagefind-filter="tipo:{tipo}"></span>'
    if portada:
        # El nombre del producto, con peso alto, para que «Logistics» o «Traza»
        # traigan primero su portada. No se ve: solo lo lee el indexador.
        extra += f'\n<p hidden data-pagefind-weight="10">{html.escape(producto)}</p>'
    ini, fin = m.span()
    cierre = texto.find('</main>', fin)
    cuerpo = texto[fin:cierre if cierre != -1 else len(texto)]

    def peso(mt):
        etiqueta, a = mt.group(1), mt.group(2)
        if 'data-pagefind-weight' in a:
            return mt.group(0)
        w = '9' if etiqueta.lower() == 'h1' else '6'
        return f'<{etiqueta}{a} data-pagefind-weight="{w}">'

    cuerpo = RE_TITULO.sub(peso, cuerpo)
    return (texto[:ini] + f'<main{attrs}{nuevos}>' + extra + cuerpo
            + (texto[cierre:] if cierre != -1 else ''))


# --- Términos para el autocompletado ---------------------------------------

RE_QUITAR = re.compile(r'<(script|style|svg|nav|noscript|template)\b.*?</\1>', re.S | re.I)
RE_ETIQUETA = re.compile(r'<[^>]+>')
RE_PALABRA = re.compile(r"[A-Za-zÀ-ÿñÑ][A-Za-zÀ-ÿñÑ'’-]*[A-Za-zÀ-ÿñÑ]")
RE_H = re.compile(r'<h[1-3]\b[^>]*>(.*?)</h[1-3]>', re.S | re.I)
VACIAS = set('''
a al algo ante antes aqui así asi aun cada como con contra cual cuando de del desde donde dos el ella
ellos en entre era es esa ese eso esta este esto estos estas fue ha hay la las le les lo los mas más me
mi muy no nos o para pero por que qué se ser si sí sin sobre son su sus tambien también te tiene todo
todos tu un una uno unos y ya the and for with from that this your you are our not can will its into
when what which how all any has have was were they them their been also out more only
'''.split())


def sin_tildes(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()


def texto_de(fragmento):
    return html.unescape(RE_ETIQUETA.sub(' ', RE_QUITAR.sub(' ', fragmento)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sitio', default=str(pathlib.Path(__file__).resolve().parent.parent))
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    raiz = pathlib.Path(args.sitio).resolve()

    palabras = collections.defaultdict(collections.Counter)  # lang -> forma -> n
    titulos = collections.defaultdict(dict)                    # lang -> clave -> título
    rutas = collections.defaultdict(list)                      # lang -> rutas indexadas
    n_idx = n_fuera = 0
    for archivo in sorted(raiz.rglob('*.html')):
        rel = ruta_relativa(raiz, archivo)
        texto = archivo.read_text(encoding='utf-8')
        if not indexable(raiz, rel, texto):
            n_fuera += 1
            if args.check:
                print(f'  fuera   {rel}')
            continue
        n_idx += 1
        producto, tipo, portada = clasificar(rel)
        if args.check:
            print(f'  índice  {rel:42} {producto:18} {tipo}{" (portada)" if portada else ""}')
            continue
        archivo.write_text(anotar(texto, producto, tipo, portada), encoding='utf-8')

        lang = lengua(texto)
        rutas[lang].append('/' + rel.removesuffix('index.html'))
        m = RE_MAIN.search(texto)
        cuerpo = texto[m.end():texto.find('</main>', m.end())]
        for h in RE_H.findall(cuerpo):
            t = ' '.join(texto_de(h).split())
            if 3 <= len(t) <= 60:
                titulos[lang].setdefault(sin_tildes(t), t)
        for p in RE_PALABRA.findall(texto_de(cuerpo)):
            if len(p) >= 4 and sin_tildes(p) not in VACIAS and not p.isupper():
                palabras[lang][p] += 1

    if args.check:
        print(f'{n_idx} páginas al índice, {n_fuera} fuera')
        return 0

    salida = raiz / 'buscador'
    salida.mkdir(exist_ok=True)
    nombres = list(PRODUCTOS.values()) + ['Zentrix', 'Odoo']
    for lang in set(palabras) | set(titulos):
        # Una sola forma por palabra sin tildes: la más frecuente, en minúscula
        # si también aparece así («cobrar», no «Cobrar»; «Odoo» se queda).
        formas = {}
        for forma, n in palabras[lang].most_common():
            clave = sin_tildes(forma)
            if clave in formas:
                formas[clave][1] += n
            else:
                baja = forma.lower()
                formas[clave] = [baja if palabras[lang].get(baja) else forma, n]
        lista = sorted(formas.values(), key=lambda x: -x[1])[:2500]
        datos = {
            'p': [f for f, _ in lista],
            't': sorted(set(titulos[lang].values()) | set(nombres), key=len)[:400],
            # Rutas que existen: los accesos directos eligen la primera que esté.
            'r': sorted(set(r for l in rutas for r in rutas[l])),
        }
        (salida / f'terminos-{lang}.json').write_text(
            json.dumps(datos, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        print(f'buscador/terminos-{lang}.json: {len(datos["p"])} palabras, {len(datos["t"])} títulos')
    print(f'{n_idx} páginas al índice, {n_fuera} fuera')
    return 0


if __name__ == '__main__':
    sys.exit(main())
