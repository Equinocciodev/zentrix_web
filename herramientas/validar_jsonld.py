#!/usr/bin/env python3
"""Validador del JSON-LD del sitio contra schema.org y los requisitos de Google.

    python3 herramientas/validar_jsonld.py                       # todo el HTML del repositorio
    python3 herramientas/validar_jsonld.py --url https://zentrix.company / /check/
    python3 herramientas/validar_jsonld.py --estricto            # los avisos de Google también fallan

Comprueba en cada bloque `application/ld+json`:

- que el JSON se lee y lleva `"@context": "https://schema.org"`;
- schema.org: cada `@type` existe y cada propiedad existe y admite ese tipo (por herencia),
  con el vocabulario oficial (`schemaorg-current-https.jsonld`, se descarga una vez y se
  guarda en `~/.cache/zentrix/`; sin red usa la copia guardada);
- `@id`: URL absoluta con fragmento, un mismo `@id` no cambia de tipo ni de nombre en
  todo el sitio, y toda referencia `{"@id": …}` apunta a un nodo definido en la página
  o en otra página del sitio;
- URLs absolutas (`https://`) en `url`, `item`, `image`, `logo`, `sameAs`, `installUrl`,
  `urlTemplate`…;
- requisitos de Google (resultados enriquecidos): BreadcrumbList (posiciones 1..n, `name`,
  `item` salvo el último), FAQPage (`Question.name` + `acceptedAnswer.text`), Organization
  (`name`, `url`, `logo`), Article/TechArticle (`headline` ≤ 110; recomendados `author`,
  `image`), SoftwareApplication (`name`, `offers.price` y `aggregateRating` o `review`).

Los errores (JSON, schema.org, `@id`, URLs, obligatorios de Google salvo SoftwareApplication)
hacen salir con 1. Lo que solo impide un resultado enriquecido sin ser un error del marcado
—SoftwareApplication sin valoraciones, que no se inventan— sale como AVISO; con
`--estricto` también falla. Sin dependencias: solo la biblioteca estándar.
"""
import html
import json
import pathlib
import re
import sys
import urllib.request
from collections import defaultdict

RAIZ = pathlib.Path(__file__).resolve().parent.parent
VOCAB_URL = 'https://schema.org/version/latest/schemaorg-current-https.jsonld'
CACHE = pathlib.Path.home() / '.cache' / 'zentrix' / 'schemaorg-current-https.jsonld'
SITIO = 'https://zentrix.company'
EXCLUIR = {'.git', '.github', 'node_modules', '_site', 'pagefind', 'herramientas'}
# Propiedades cuyo valor es una URL (o un objeto con url) y que tienen que ser absolutas.
PROPS_URL = {'url', 'item', 'image', 'logo', 'sameAs', 'installUrl', 'urlTemplate', 'downloadUrl',
             'contentUrl', 'thumbnailUrl', 'mainEntityOfPage'}
# Extensiones que schema.org no define como propiedad pero que sus propias especificaciones usan.
PROPS_ESPECIALES = {'query-input', 'url-template'}
TIPOS_DATO = {'Text', 'URL', 'Number', 'Integer', 'Float', 'Boolean', 'Date', 'DateTime', 'Time'}


# ------------------------------------------------------------------ vocabulario de schema.org
def vocabulario():
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(VOCAB_URL, headers={'User-Agent': 'zentrix-validar-jsonld/1.0'})
        CACHE.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    datos = json.loads(CACHE.read_text(encoding='utf-8'))
    padres, dominios, tipos, props = defaultdict(set), defaultdict(set), set(), set()

    def nombres(v):
        v = v if isinstance(v, list) else [v]
        return [x['@id'].split(':', 1)[1] for x in v if isinstance(x, dict) and '@id' in x]

    for n in datos['@graph']:
        nid = n['@id'].split(':', 1)[1]
        t = n.get('@type')
        t = t if isinstance(t, list) else [t]
        if 'rdfs:Class' in t:
            tipos.add(nid)
            padres[nid].update(nombres(n.get('rdfs:subClassOf', [])))
        if 'rdf:Property' in t:
            props.add(nid)
            dominios[nid].update(nombres(n.get('schema:domainIncludes', [])))
    return tipos, props, padres, dominios


def ancestros(tipo, padres, memo={}):
    if tipo not in memo:
        vistos, pila = {tipo}, [tipo]
        while pila:
            for p in padres.get(pila.pop(), ()):
                if p not in vistos:
                    vistos.add(p)
                    pila.append(p)
        memo[tipo] = vistos
    return memo[tipo]


# ------------------------------------------------------------------ lectura de las páginas
def bloques(texto):
    return re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', texto)


def ruta_de(p):
    rel = p.relative_to(RAIZ).as_posix()
    if rel == 'index.html':
        return '/'
    return '/' + (rel[:-len('index.html')] if rel.endswith('/index.html') else rel)


def paginas_locales():
    for p in sorted(RAIZ.rglob('*.html')):
        if EXCLUIR.intersection(p.relative_to(RAIZ).parts):
            continue
        s = p.read_text(encoding='utf-8')
        if 'http-equiv="refresh"' in s or re.search(r'name="robots" content="[^"]*noindex', s):
            continue
        yield ruta_de(p), s


def paginas_remotas(base, rutas):
    for r in rutas:
        req = urllib.request.Request(base.rstrip('/') + r, headers={'User-Agent': 'zentrix-validar-jsonld/1.0'})
        yield r, urllib.request.urlopen(req, timeout=30).read().decode('utf-8')


# ------------------------------------------------------------------ comprobaciones
class Informe:
    def __init__(self):
        self.errores, self.avisos = defaultdict(list), defaultdict(list)

    def error(self, ruta, msg):
        self.errores[ruta].append(msg)

    def aviso(self, ruta, msg):
        self.avisos[ruta].append(msg)


def tipos_de(n):
    t = n.get('@type', [])
    return t if isinstance(t, list) else [t]


def recorrer(nodo, camino='$'):
    """Todos los objetos con sus caminos (incluidos los anidados)."""
    if isinstance(nodo, dict):
        yield camino, nodo
        for k, v in nodo.items():
            if not k.startswith('@'):
                yield from recorrer(v, f'{camino}.{k}')
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from recorrer(v, f'{camino}[{i}]')


def es_absoluta(u):
    return isinstance(u, str) and re.match(r'^https://[^\s/]+\.[^\s/]+', u) is not None


def revisar_urls(ruta, camino, prop, valor, inf):
    for v in (valor if isinstance(valor, list) else [valor]):
        if isinstance(v, str):
            if not es_absoluta(v):
                inf.error(ruta, f'{camino}.{prop}: URL no absoluta «{v}»')
        elif isinstance(v, dict) and 'url' in v:
            revisar_urls(ruta, camino + '.' + prop, 'url', v['url'], inf)


def revisar_google(ruta, camino, n, inf):
    t = set(tipos_de(n))
    if 'BreadcrumbList' in t:
        items = n.get('itemListElement') or []
        if not items:
            inf.error(ruta, f'{camino}: BreadcrumbList sin itemListElement')
        for i, it in enumerate(items):
            if it.get('@type') != 'ListItem':
                inf.error(ruta, f'{camino}.itemListElement[{i}]: no es ListItem')
            if it.get('position') != i + 1:
                inf.error(ruta, f'{camino}.itemListElement[{i}]: position {it.get("position")!r}, se esperaba {i + 1}')
            if not it.get('name'):
                inf.error(ruta, f'{camino}.itemListElement[{i}]: falta name')
            if not it.get('item') and i < len(items) - 1:
                inf.error(ruta, f'{camino}.itemListElement[{i}]: falta item (solo el último puede omitirlo)')
    if 'FAQPage' in t:
        qs = n.get('mainEntity') or []
        if not qs:
            inf.error(ruta, f'{camino}: FAQPage sin mainEntity')
        for i, q in enumerate(qs if isinstance(qs, list) else [qs]):
            if q.get('@type') != 'Question' or not q.get('name'):
                inf.error(ruta, f'{camino}.mainEntity[{i}]: Question sin name')
            a = q.get('acceptedAnswer') or {}
            if a.get('@type') != 'Answer' or not a.get('text'):
                inf.error(ruta, f'{camino}.mainEntity[{i}]: falta acceptedAnswer.text')
    if 'Organization' in t and set(n) - {'@type', '@id'}:  # no una simple referencia
        for p in ('name', 'url'):
            if not n.get(p):
                inf.error(ruta, f'{camino}: Organization sin {p}')
    if t & {'Article', 'TechArticle', 'NewsArticle', 'BlogPosting'}:
        h = n.get('headline', '')
        if not h:
            inf.error(ruta, f'{camino}: {"/".join(t)} sin headline')
        elif len(h) > 110:
            inf.error(ruta, f'{camino}: headline de {len(h)} caracteres (Google: ≤ 110)')
        for p in ('author', 'image'):
            if not n.get(p):
                inf.aviso(ruta, f'{camino}: {"/".join(t)} sin {p} (recomendado por Google)')
    if t & {'SoftwareApplication', 'MobileApplication', 'WebApplication'} and set(n) - {'@type', '@id', 'name'}:
        if not n.get('name'):
            inf.error(ruta, f'{camino}: SoftwareApplication sin name')
        falta = []
        if not isinstance(n.get('offers'), dict) or 'price' not in n['offers']:
            falta.append('offers.price')
        if not (n.get('aggregateRating') or n.get('review')):
            falta.append('aggregateRating o review')
        if falta:
            inf.aviso(ruta, f'{camino}: {n.get("name")} no es apto para el resultado enriquecido de apps '
                            f'de Google (falta {", ".join(falta)}); no se inventan')


def validar(paginas, vocab, inf):
    tipos, props, padres, dominios = vocab
    definidos = {}  # @id -> (tipos, nombre, ruta)
    referencias = []  # (ruta, camino, @id)
    n_bloques = 0
    for ruta, texto in paginas:
        bs = bloques(texto)
        if not bs:
            inf.aviso(ruta, 'sin JSON-LD')
        for b in bs:
            n_bloques += 1
            try:
                datos = json.loads(b.replace('<\\/', '</'))
            except ValueError as e:
                inf.error(ruta, f'JSON inválido: {e}')
                continue
            if datos.get('@context') not in ('https://schema.org', 'https://schema.org/'):
                inf.error(ruta, f'@context {datos.get("@context")!r} (se espera "https://schema.org")')
            raiz = datos.get('@graph', [datos])
            for camino, n in recorrer(raiz):
                ts = tipos_de(n)
                solo_ref = set(n) <= {'@id'}
                if solo_ref:
                    referencias.append((ruta, camino, n['@id']))
                    continue
                if not ts:
                    inf.error(ruta, f'{camino}: objeto sin @type')
                for tp in ts:
                    if tp not in tipos:
                        inf.error(ruta, f'{camino}: @type «{tp}» no existe en schema.org')
                conocidos = [tp for tp in ts if tp in tipos]
                linaje = set().union(*(ancestros(tp, padres) for tp in conocidos)) if conocidos else set()
                for p, v in n.items():
                    if p.startswith('@'):
                        continue
                    if p in PROPS_ESPECIALES:
                        continue
                    if p not in props:
                        inf.error(ruta, f'{camino}: propiedad «{p}» no existe en schema.org')
                    elif linaje and not (dominios[p] & linaje):
                        inf.error(ruta, f'{camino}: «{p}» no es propiedad de {"/".join(ts)} en schema.org')
                    if p in PROPS_URL:
                        revisar_urls(ruta, camino, p, v, inf)
                if '@id' in n:
                    i = n['@id']
                    if not es_absoluta(i) or '#' not in i:
                        inf.error(ruta, f'{camino}: @id «{i}» no es una URL absoluta con fragmento')
                    previo = definidos.get(i)
                    actual = (tuple(sorted(ts)), n.get('name'))
                    if previo and previo[:2] != actual and n.get('name') and previo[1]:
                        inf.error(ruta, f'{camino}: @id «{i}» es {actual} aquí y {previo[:2]} en {previo[2]}')
                    if not previo or (not previo[1] and n.get('name')):
                        definidos[i] = actual + (ruta,)
                revisar_google(ruta, camino, n, inf)
    for ruta, camino, i in referencias:
        if i not in definidos:
            inf.error(ruta, f'{camino}: la referencia @id «{i}» no está definida en ninguna página')
    return n_bloques


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    estricto = '--estricto' in sys.argv
    if '--url' in sys.argv:
        base, rutas = args[0], args[1:] or ['/']
        paginas = list(paginas_remotas(base, rutas))
    else:
        paginas = list(paginas_locales())
    inf = Informe()
    n = validar(paginas, vocabulario(), inf)
    for ruta in sorted(set(inf.errores) | set(inf.avisos)):
        print(ruta)
        for m in inf.errores.get(ruta, []):
            print('  ERROR', m)
        for m in inf.avisos.get(ruta, []):
            print('  aviso', m)
    ne = sum(map(len, inf.errores.values()))
    na = sum(map(len, inf.avisos.values()))
    print(f'\n{len(paginas)} páginas, {n} bloques JSON-LD · errores: {ne} · avisos: {na}')
    sys.exit(1 if ne or (estricto and na) else 0)


if __name__ == '__main__':
    main()
