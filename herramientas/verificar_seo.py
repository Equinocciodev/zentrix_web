#!/usr/bin/env python3
"""Verificación SEO del sitio PUBLICADO, página por página y en los dos idiomas.

    python3 herramientas/verificar_seo.py                         # https://zentrix.company
    python3 herramientas/verificar_seo.py http://localhost:8000   # una copia local
    python3 herramientas/verificar_seo.py --informe ruta/informe.md

Lee `robots.txt` y `sitemap.xml`, rastrea los enlaces internos y comprueba en cada página:
HTTP 200; title (≤ 60, único); description (140–160, única); canonical = URL; `lang`;
hreflang es/en/x-default recíprocos; Open Graph (title, description, url, locale, imagen
1200×630 que existe) y `og:locale:alternate` si hay traducción; `twitter:card`;
`theme-color`, favicon y manifest; un solo `<h1>` y sin saltos de nivel; JSON-LD válido
con los campos obligatorios de su plantilla; `alt` (vacío si es decorativa), `width` y `height` en cada
imagen, y cada `<svg>` en línea oculto (`aria-hidden`) o nombrado (`role="img"` + `aria-label`);
enlaces internos y anclas sin romper. Además: la 404 responde 404 con `noindex`, las
redirecciones llevan `noindex` y ninguna página indexable falta en el sitemap.

Sale con 1 si algo falla. Sin dependencias: solo la biblioteca estándar.
"""
import html
import json
import re
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import OrderedDict
from html.parser import HTMLParser

PRODUCCION = 'https://zentrix.company'
AGENTE = 'zentrix-verificar-seo/1.0'
REDIRECCIONES = ['/logistica/']
SOLUCIONES = ['/ai/', '/cloud/', '/labs/', '/logistics/', '/software/', '/traza/']
DIRECCIONES = set()  # PostalAddress de Organization vistas en el JSON-LD
APPS = ['/work/', '/sales/', '/sales/en/', '/en/work/', '/en/sales/', '/check/', '/en/check/']


class Pagina(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.titulo = ''
        self._en_titulo = False
        self._svg = 0
        self.metas = {}
        self.metas_multi = {}
        self.links = []
        self.encabezados = []
        self._h = None
        self.imgs = []
        self.svgs = []  # <svg> en línea de primer nivel
        self.hrefs = []
        self.ids = set()
        self.jsonld = []
        self._ld = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        elif tag == 'svg':
            if not self._svg:
                self.svgs.append(a)
            self._svg += 1
        elif tag == 'title' and not self._svg and not self.titulo:
            self._en_titulo = True
        elif tag == 'meta':
            clave = a.get('name') or a.get('property') or a.get('http-equiv')
            if clave:
                self.metas.setdefault(clave, a.get('content', ''))
                self.metas_multi.setdefault(clave, []).append(a.get('content', ''))
        elif tag == 'link':
            self.links.append(a)
        elif re.fullmatch(r'h[1-6]', tag):
            self._h = [int(tag[1]), '']
        elif tag == 'img':
            self.imgs.append(a)
        elif tag == 'a' and a.get('href'):
            self.hrefs.append(a['href'])
        elif tag == 'script' and a.get('type') == 'application/ld+json':
            self._ld = ''

    def handle_endtag(self, tag):
        if tag == 'title':
            self._en_titulo = False
        elif tag == 'svg':
            self._svg = max(0, self._svg - 1)
        elif self._h and tag == 'h%d' % self._h[0]:
            self.encabezados.append((self._h[0], ' '.join(self._h[1].split())))
            self._h = None
        elif tag == 'script' and self._ld is not None:
            self.jsonld.append(self._ld)
            self._ld = None

    def handle_data(self, data):
        if self._en_titulo:
            self.titulo += data
        if self._h:
            self._h[1] += data
        if self._ld is not None:
            self._ld += data

    def link(self, rel, **filtros):
        return [l for l in self.links if rel in (l.get('rel') or '').split()
                and all(l.get(k) == v for k, v in filtros.items())]


class Cliente:
    def __init__(self):
        self.cache = {}

    def get(self, url):
        if url in self.cache:
            return self.cache[url]
        req = urllib.request.Request(url, headers={'User-Agent': AGENTE})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                res = (r.status, r.geturl(), r.read(), dict(r.headers))
        except urllib.error.HTTPError as e:
            res = (e.code, url, e.read(), dict(e.headers))
        except Exception as e:  # noqa: BLE001 — se informa como fallo de red
            res = (0, url, str(e).encode(), {})
        self.cache[url] = res
        return res


def tamano_png(datos):
    if datos[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', datos[16:24])
    return None


def nodos(ld):
    if isinstance(ld, list):
        for x in ld:
            yield from nodos(x)
    elif isinstance(ld, dict):
        if '@graph' in ld:
            yield from nodos(ld['@graph'])
        else:
            yield ld


def tipos(n):
    t = n.get('@type')
    return set(t) if isinstance(t, list) else {t}


def validar_jsonld(pag, ruta, url):
    errores, encontrados = [], set()
    if not pag.jsonld:
        return ['sin JSON-LD'], encontrados
    for bloque in pag.jsonld:
        try:
            ld = json.loads(bloque)
        except ValueError as e:
            errores.append('JSON-LD no es JSON válido: %s' % e)
            continue
        if 'schema.org' not in str(ld.get('@context', '') if isinstance(ld, dict) else ''):
            errores.append('JSON-LD sin @context schema.org')
        for n in nodos(ld):
            t = tipos(n)
            encontrados |= t
            falta = lambda *campos: [c for c in campos if not n.get(c)]
            if 'Organization' in t and n.get('logo'):
                f = falta('name', 'url', 'logo', 'sameAs', 'contactPoint')
                if f:
                    errores.append('Organization sin ' + ', '.join(f))
                for cp in n.get('contactPoint', []):
                    if not cp.get('contactType') or not (cp.get('email') or cp.get('telephone')):
                        errores.append('ContactPoint incompleto')
            if 'Organization' in t:
                ad = n.get('address')
                if not isinstance(ad, dict) or ad.get('@type') != 'PostalAddress' or \
                        [c for c in ('streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'addressCountry') if not ad.get(c)]:
                    errores.append('Organization sin PostalAddress completa')
                else:
                    encontrados.add('PostalAddress')
                    DIRECCIONES.add(tuple(ad.get(c) for c in ('streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'addressCountry')))
            if 'WebSite' in t:
                pa = n.get('potentialAction') or {}
                tgt = pa.get('target')
                tgt = tgt.get('urlTemplate') if isinstance(tgt, dict) else tgt
                if pa.get('@type') != 'SearchAction' or '{search_term_string}' not in str(tgt) \
                        or 'search_term_string' not in str(pa.get('query-input')):
                    errores.append('WebSite sin SearchAction válida')
            if 'SoftwareApplication' in t:
                f = falta('name', 'applicationCategory', 'operatingSystem', 'url')
                if f:
                    errores.append('SoftwareApplication sin ' + ', '.join(f))
                if 'aggregateRating' in n or 'review' in n:
                    errores.append('SoftwareApplication con valoraciones (no se publican)')
            if 'Service' in t:
                f = falta('name', 'serviceType', 'provider', 'url')
                if f:
                    errores.append('Service sin ' + ', '.join(f))
            if 'BreadcrumbList' in t:
                items = n.get('itemListElement') or []
                if len(items) < 2:
                    errores.append('BreadcrumbList con menos de 2 elementos')
                for i, it in enumerate(items, 1):
                    if it.get('position') != i or not it.get('name') or not it.get('item'):
                        errores.append('BreadcrumbList: elemento %d incompleto' % i)
                if items and items[-1].get('item') != url:
                    errores.append('BreadcrumbList: el último no es la página')
            if 'TechArticle' in t:
                f = falta('headline', 'url', 'inLanguage')
                if f:
                    errores.append('TechArticle sin ' + ', '.join(f))
            idioma = n.get('inLanguage')
            if isinstance(idioma, str) and pag.lang and idioma != pag.lang:
                errores.append('inLanguage «%s» ≠ lang «%s»' % (idioma, pag.lang))
            if 'FAQPage' in t:
                qs = n.get('mainEntity') or []
                if not qs or any(not q.get('name') or not (q.get('acceptedAnswer') or {}).get('text') for q in qs):
                    errores.append('FAQPage vacía o con preguntas sin respuesta')
    plantilla = ruta.replace('/en/', '/', 1) if ruta.startswith('/en/') else ruta
    if ruta in ('/', '/en/'):
        for t in ('Organization', 'WebSite'):
            if t not in encontrados:
                errores.append('portada sin ' + t)
    else:
        if 'BreadcrumbList' not in encontrados:
            errores.append('página interior sin BreadcrumbList')
    if ruta in APPS and 'SoftwareApplication' not in encontrados:
        errores.append('app sin SoftwareApplication')
    if re.match(r'^/(work|sales|check)/docs/', plantilla) and 'TechArticle' not in encontrados:
        errores.append('documentación sin TechArticle')
    if plantilla in SOLUCIONES and 'Service' not in encontrados:
        errores.append('solución sin Service')
    return errores, encontrados


def verificar(base):
    base = base.rstrip('/')
    cli = Cliente()
    globales = []
    filas = OrderedDict()

    estado, _, robots, _ = cli.get(base + '/robots.txt')
    robots = robots.decode('utf-8', 'replace')
    if estado != 200:
        globales.append(('robots.txt', 'HTTP %s' % estado))
    elif not re.search(r'(?im)^sitemap:\s*%s/sitemap\.xml\s*$' % re.escape(PRODUCCION), robots):
        globales.append(('robots.txt', 'sin línea Sitemap: %s/sitemap.xml' % PRODUCCION))
    if re.search(r'(?im)^disallow:\s*/\s*$', robots):
        globales.append(('robots.txt', 'Disallow: / bloquea el sitio'))

    # llms.txt: la auditoría «llms-txt» de Lighthouse (H1, al menos un enlace Markdown, ≥ 50
    # caracteres) y lo que pide https://llmstxt.org (resumen en blockquote, secciones ##
    # con listas de enlaces). /en/llms.txt solo si existe.
    for ruta_llms, obligatorio in (('/llms.txt', True), ('/en/llms.txt', False), ('/llms-full.txt', True)):
        est, _, cuerpo_llms, _ = cli.get(base + ruta_llms)
        if est != 200:
            if obligatorio or est != 404:
                globales.append((ruta_llms, 'HTTP %s' % est))
            continue
        t = cuerpo_llms.decode('utf-8', 'replace')
        if not re.search(r'^\s*#\s+.+', t, re.M):
            globales.append((ruta_llms, 'sin H1 (# Título)'))
        if not re.search(r'\[.+\]\(.+\)', t):
            globales.append((ruta_llms, 'sin enlaces Markdown (Lighthouse: «File does not appear to contain any links»)'))
        if len(t) < 50:
            globales.append((ruta_llms, 'demasiado corto'))
        if ruta_llms != '/llms-full.txt':
            if not re.search(r'^> .+', t, re.M):
                globales.append((ruta_llms, 'sin resumen en blockquote (> …)'))
            if not re.search(r'^- \[[^\]]+\]\([^)]+\)', t, re.M):
                globales.append((ruta_llms, 'sin listas de enlaces «- [nombre](url)»'))
            sueltas = [l for l in t.splitlines() if re.match(r'^- ', l) and re.search(r'https?://', l)
                       and not re.match(r'^- \[[^\]]+\]\(', l)]
            if sueltas:
                globales.append((ruta_llms, '%d elementos con URL en texto plano, p. ej. «%s»' % (len(sueltas), sueltas[0][:60])))

    estado, _, xml, _ = cli.get(base + '/sitemap.xml')
    en_sitemap = OrderedDict()
    alternas_sitemap = {}
    if estado != 200:
        globales.append(('sitemap.xml', 'HTTP %s' % estado))
    else:
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
        try:
            raiz = ET.fromstring(xml)
            for u in raiz.findall('s:url', ns):
                loc = u.findtext('s:loc', '', ns).strip()
                lm = u.findtext('s:lastmod', '', ns).strip()
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lm):
                    globales.append(('sitemap.xml', 'lastmod inválido en %s' % loc))
                en_sitemap[loc] = lm
                alternas_sitemap[loc] = {l.get('hreflang'): l.get('href') for l in u.findall('x:link', ns)}
        except ET.ParseError as e:
            globales.append(('sitemap.xml', 'XML inválido: %s' % e))

    pendientes = [u[len(PRODUCCION):] or '/' for u in en_sitemap] or ['/']
    vistas = set()
    titulos, descripciones = {}, {}
    enlaces = {}  # destino → páginas que lo enlazan
    paginas = {}

    while pendientes:
        ruta = pendientes.pop(0)
        if ruta in vistas:
            continue
        vistas.add(ruta)
        url = PRODUCCION + ruta
        estado, final, cuerpo, cab = cli.get(base + ruta)
        errores = {}
        fila = {'lang': '', 'errores': errores, 'sitemap': url in en_sitemap}
        filas[ruta] = fila
        if estado != 200:
            errores['HTTP'] = ['HTTP %s' % estado]
            continue
        if 'text/html' not in cab.get('Content-Type', cab.get('content-type', 'text/html')):
            continue
        pag = Pagina()
        pag.feed(cuerpo.decode('utf-8', 'replace'))
        paginas[ruta] = pag
        fila['lang'] = pag.lang or '?'
        robots_meta = pag.metas.get('robots', '')
        noindex = 'noindex' in robots_meta
        redireccion = 'refresh' in pag.metas
        fila['noindex'] = noindex
        for h in pag.hrefs:
            destino = urllib.parse.urljoin(url, h)
            p = urllib.parse.urlparse(destino)
            if p.scheme in ('http', 'https') and p.netloc == urllib.parse.urlparse(PRODUCCION).netloc:
                enlaces.setdefault(destino, set()).add(ruta)
                limpio = p.path + ('?' + p.query if p.query else '')
                if p.path.startswith('/cdn-cgi/'):
                    continue
                if not re.search(r'\.(png|jpe?g|webp|svg|pdf|xml|txt|ico|json|webmanifest|css|js)$', p.path):
                    if not p.query:
                        pendientes.append(limpio)
        if redireccion or noindex:
            m = []
            if url in en_sitemap:
                m.append('página noindex/redirección dentro del sitemap')
            if redireccion and not noindex:
                m.append('redirección sin noindex')
            if m:
                errores['Meta'] = m
            fila['tipo'] = 'redirección' if redireccion else 'noindex'
            continue
        fila['tipo'] = 'indexable'
        e = []
        t = ' '.join(pag.titulo.split())
        if not t:
            e.append('sin title')
        elif len(t) > 60:
            e.append('title de %d caracteres (> 60)' % len(t))
        titulos.setdefault(t, []).append(ruta)
        d = pag.metas.get('description', '')
        if not 140 <= len(d) <= 160:
            e.append('description de %d caracteres (140–160)' % len(d))
        descripciones.setdefault(d, []).append(ruta)
        canon = pag.link('canonical')
        if len(canon) != 1 or canon[0].get('href') != url:
            e.append('canonical ≠ URL (%s)' % (canon[0].get('href') if canon else 'falta'))
        esperado = 'en' if ruta.startswith('/en/') or ruta.startswith('/sales/en/') else 'es'
        if (pag.lang or '')[:2] != esperado:
            e.append('lang="%s", se esperaba %s' % (pag.lang, esperado))
        if url not in en_sitemap:
            e.append('indexable pero fuera del sitemap')
        if e:
            errores['Meta'] = e

        e = []
        alt = {l.get('hreflang'): l.get('href') for l in pag.link('alternate') if l.get('hreflang')}
        if alt:
            for k in ('es', 'en', 'x-default'):
                if k not in alt:
                    e.append('hreflang sin %s' % k)
            if url not in alt.values():
                e.append('hreflang no se incluye a sí misma')
            if url in alternas_sitemap and alternas_sitemap[url] != alt:
                e.append('xhtml:link del sitemap ≠ hreflang de la página')
            if not pag.metas.get('og:locale:alternate'):
                e.append('sin og:locale:alternate')
        else:
            # Todo el sitio es bilingüe: una página indexable sin hreflang es una página sin par.
            e.append('sin hreflang: falta su versión en el otro idioma')
        fila['alternas'] = alt
        if e:
            errores['hreflang'] = e

        e = []
        for k in ('og:title', 'og:description', 'og:url', 'og:image', 'og:locale', 'og:type'):
            if not pag.metas.get(k):
                e.append('sin ' + k)
        if pag.metas.get('og:url') and pag.metas['og:url'] != url:
            e.append('og:url ≠ canonical')
        img = pag.metas.get('og:image')
        if img:
            est, _, datos, _ = cli.get(img.replace(PRODUCCION, base, 1))
            tam = tamano_png(datos) if est == 200 else None
            if est != 200:
                e.append('og:image HTTP %s' % est)
            elif tam != (1200, 630):
                e.append('og:image de %s, no 1200×630' % (tam,))
        if pag.metas.get('twitter:card') != 'summary_large_image':
            e.append('twitter:card ≠ summary_large_image')
        if not pag.metas.get('theme-color'):
            e.append('sin theme-color')
        if not pag.link('icon'):
            e.append('sin favicon')
        if not pag.link('manifest'):
            e.append('sin manifest')
        if e:
            errores['OG'] = e

        e = []
        h1 = [h for h in pag.encabezados if h[0] == 1]
        if len(h1) != 1:
            e.append('%d <h1>' % len(h1))
        previo = 0
        for nivel, txt in pag.encabezados:
            if previo and nivel > previo + 1:
                e.append('salto h%d → h%d («%s»)' % (previo, nivel, txt[:40]))
                break
            previo = nivel
        if pag.encabezados and pag.encabezados[0][0] != 1:
            e.append('el primer encabezado no es h1')
        if e:
            errores['H1'] = e

        e, encontrados = validar_jsonld(pag, ruta, url)
        fila['schema'] = sorted(x for x in encontrados if x)
        if e:
            errores['JSON-LD'] = e

        e = []
        for im in pag.imgs:
            src = im.get('src', '?')
            if 'alt' not in im:
                e.append('sin alt: %s' % src)
            if not im.get('width') or not im.get('height'):
                e.append('sin width/height: %s' % src)
        for sv in pag.svgs:  # un SVG en línea es una imagen: o se oculta o se nombra
            if sv.get('aria-hidden') != 'true' and not (sv.get('role') == 'img' and (sv.get('aria-label') or sv.get('aria-labelledby'))):
                e.append('svg sin aria-hidden="true" ni role="img" con aria-label: class="%s"' % sv.get('class', ''))
        if e:
            errores['Imágenes'] = e[:5] + (['… y %d más' % (len(e) - 5)] if len(e) > 5 else [])

    # Enlaces internos y anclas. Los de /cdn-cgi/l/email-protection los inserta Cloudflare
    # («Email Address Obfuscation») al servir la página: no están en el HTML del repo y
    # se informan una sola vez como fallo global de configuración.
    protegidas = sorted({o for d, os_ in enlaces.items() if urllib.parse.urlparse(d).path.startswith('/cdn-cgi/')
                         for o in os_})
    if protegidas:
        globales.append(('Cloudflare', 'Email Address Obfuscation activa: %d páginas cambian sus mailto: por '
                         '/cdn-cgi/l/email-protection, que responde 404 sin JavaScript y oculta el correo a '
                         'buscadores y modelos. Desactivarla (Scrape Shield) en la zona zentrix.company.' % len(protegidas)))
    for destino, origenes in enlaces.items():
        p = urllib.parse.urlparse(destino)
        if p.path.startswith('/cdn-cgi/'):
            continue
        ruta = p.path or '/'
        est, _, cuerpo, _ = cli.get(base + ruta + ('?' + p.query if p.query else ''))
        problema = None
        if est != 200:
            problema = 'enlace roto (HTTP %s): %s' % (est, ruta)
        elif p.fragment and ruta in paginas and p.fragment not in paginas[ruta].ids:
            problema = 'ancla inexistente: %s#%s' % (ruta, p.fragment)
        if problema:
            for o in origenes:
                if o in filas:
                    filas[o]['errores'].setdefault('Enlaces', []).append(problema)

    # La dirección del JSON-LD debe ser la misma que /contacto/ publica en microdatos
    for r in ('/contacto/', '/en/contact/'):
        if r in paginas:
            _, _, c, _ = cli.get(base + r)
            c = c.decode('utf-8', 'replace')
            m = re.search(r'itemtype="https://schema.org/PostalAddress">([\s\S]*?)</address>', c)
            if m:
                md = {k: html.unescape(v).strip() for k, v in re.findall(r'itemprop="(\w+)"(?: content="([^"]*)")?', m.group(1)) and
                      [(k, cont or val) for k, cont, val in re.findall(r'itemprop="(\w+)"(?: content="([^"]*)")?>([^<]*)<', m.group(1))]}
                vista = tuple(md.get(k) for k in ('streetAddress', 'addressLocality', 'addressRegion', 'postalCode', 'addressCountry'))
                if DIRECCIONES and DIRECCIONES != {vista}:
                    filas[r]['errores'].setdefault('JSON-LD', []).append('PostalAddress del JSON-LD ≠ la de la página: %s' % (vista,))

    # Reciprocidad de hreflang
    for ruta, fila in filas.items():
        for lang, href in (fila.get('alternas') or {}).items():
            otra = href[len(PRODUCCION):] or '/'
            if lang == 'x-default' or otra == ruta:
                continue
            vuelta = (filas.get(otra) or {}).get('alternas') or {}
            if PRODUCCION + ruta not in vuelta.values():
                fila['errores'].setdefault('hreflang', []).append('%s no devuelve el hreflang' % otra)

    # Únicos
    for t, rutas in titulos.items():
        if len(rutas) > 1:
            for r in rutas:
                filas[r]['errores'].setdefault('Meta', []).append('title repetido con %s' % ', '.join(x for x in rutas if x != r))
    for d, rutas in descripciones.items():
        if len(rutas) > 1 and d:
            for r in rutas:
                filas[r]['errores'].setdefault('Meta', []).append('description repetida')

    # 404 y redirecciones conocidas
    est, _, cuerpo, _ = cli.get(base + '/no-existe-verificacion-seo/')
    p404 = Pagina()
    p404.feed(cuerpo.decode('utf-8', 'replace'))
    e = []
    if est != 404:
        e.append('responde %s, no 404' % est)
    if 'noindex' not in p404.metas.get('robots', ''):
        e.append('404 sin noindex')
    filas['(404) /no-existe-verificacion-seo/'] = {'lang': p404.lang or '?', 'tipo': '404', 'errores': {'Meta': e} if e else {}}
    for r in REDIRECCIONES:
        if r not in filas:
            est, _, cuerpo, _ = cli.get(base + r)
            pr = Pagina()
            pr.feed(cuerpo.decode('utf-8', 'replace'))
            e = [] if 'noindex' in pr.metas.get('robots', '') else ['redirección sin noindex']
            filas[r] = {'lang': pr.lang or '?', 'tipo': 'redirección', 'errores': {'Meta': e} if e else {}}
    for loc in en_sitemap:
        r = loc[len(PRODUCCION):] or '/'
        if r not in filas:
            globales.append(('sitemap.xml', 'URL no verificada: %s' % loc))
    return filas, globales


COLUMNAS = ['HTTP', 'Meta', 'hreflang', 'OG', 'H1', 'JSON-LD', 'Imágenes', 'Enlaces']


def informe(base, filas, globales):
    import datetime
    total = len(filas)
    malas = [r for r, f in filas.items() if f['errores']]
    idx = [r for r, f in filas.items() if f.get('tipo') == 'indexable']
    out = ['# Verificación SEO — zentrix.company', '',
           'Fecha: %s · Sitio verificado: `%s` · Script: `herramientas/verificar_seo.py`' % (
               datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), base), '',
           '**Resultado: %s** — %d páginas revisadas (%d indexables, %d en inglés), %d con fallos; %d fallos globales.' % (
               'OK' if not malas and not globales else 'FALLA', total, len(idx),
               sum(1 for r in idx if filas[r]['lang'].startswith('en')), len(malas), len(globales)), '']
    out += ['## Global', '', '| Comprobación | Resultado |', '|---|---|']
    out.append('| robots.txt con `Sitemap:` | %s |' % ('falla' if any(g[0] == 'robots.txt' for g in globales) else 'OK'))
    out.append('| sitemap.xml (XML, lastmod, todas las URL responden) | %s |' % ('falla' if any(g[0] == 'sitemap.xml' for g in globales) else 'OK'))
    out.append('| llms.txt y llms-full.txt (auditoría llms-txt de Lighthouse + llmstxt.org) | %s |' % ('falla' if any(g[0].endswith('llms.txt') or g[0] == '/llms-full.txt' for g in globales) else 'OK'))
    for g in globales:
        out.append('| %s | falla: %s |' % g)
    out += ['', '## Página por página', '',
            '| Página | Idioma | Tipo | Schema | ' + ' | '.join(COLUMNAS) + ' |',
            '|---|---|---|---|' + '---|' * len(COLUMNAS)]
    for r, f in filas.items():
        celdas = []
        for c in COLUMNAS:
            if f.get('tipo') != 'indexable' and c not in ('HTTP', 'Meta', 'Enlaces'):
                celdas.append('—')
            else:
                celdas.append('falla' if c in f['errores'] else 'OK')
        out.append('| `%s` | %s | %s | %s | %s |' % (r, f['lang'], f.get('tipo', '?'),
                                                    ', '.join(f.get('schema', [])) or '—', ' | '.join(celdas)))
    if malas:
        out += ['', '## Detalle de los fallos', '']
        for r in malas:
            for c, es in filas[r]['errores'].items():
                for x in es:
                    out.append('- `%s` · %s: %s' % (r, c, x))
    return '\n'.join(out) + '\n', not malas and not globales


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    base = args[0] if args else PRODUCCION
    destino = None
    if '--informe' in sys.argv:
        destino = sys.argv[sys.argv.index('--informe') + 1]
        if destino in args:
            args.remove(destino)
            base = args[0] if args else PRODUCCION
    filas, globales = verificar(base)
    texto, ok = informe(base, filas, globales)
    if destino:
        with open(destino, 'w', encoding='utf-8') as f:
            f.write(texto)
    resumen = [l for l in texto.splitlines() if l.startswith('**Resultado')]
    print(resumen[0] if resumen else '')
    for r, f in filas.items():
        for c, es in f['errores'].items():
            for x in es:
                print('  %s · %s: %s' % (r, c, x))
    for g in globales:
        print('  %s: %s' % g)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
