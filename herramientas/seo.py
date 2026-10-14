#!/usr/bin/env python3
"""Fuente única del SEO de cada página: title, description, Open Graph, hreflang y JSON-LD.

`herramientas/generar.py` lo aplica a cada página como último paso (`seo.aplicar`), así que
basta con ejecutar el generador; este script también se puede ejecutar solo y da lo mismo.
No toca el diseño: solo la cabecera `<head>`.

    python3 herramientas/seo.py          # reescribe
    python3 herramientas/seo.py --check  # solo comprueba (sale con 1 si algo difiere)
    python3 herramientas/seo.py --tabla  # imprime la tabla de SEO.md

Qué hace en cada página indexable:
- `<title>`, `meta description`, `og:title`, `og:description` y `og:image:alt` salen de
  PAGINAS (si la página no está en la tabla, se respetan los que tiene);
- entre `<!-- seo -->` y `<!-- /seo -->`, antes de `</head>`: `twitter:title`,
  `twitter:description` y el JSON-LD de su plantilla (ver `jsonld()`). Los `hreflang` y
  `og:locale:alternate` los pone `generar.py`; aquí solo se añaden los de las páginas
  inglesas antiguas de `/sales/en/` (PARES_LEGADO) mientras no exista `/en/`.
Las páginas de redirección y la 404 no se tocan: ya llevan `noindex`.

La tabla página → palabra clave → title → description está en `SEO.md`.
"""
import html
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIO = 'https://zentrix.company'
ORG_ID = SITIO + '/#organizacion'
WEB_ID = SITIO + '/#sitio'
LOGO = SITIO + '/assets/img/icono-512.png'
PLAY_WORK = 'https://play.google.com/store/apps/details?id=com.leiros.guuaowork'
PLAY_SALES = 'https://play.google.com/store/apps/details?id=com.leiros.vendoo'
APPSTORE_SALES = 'https://apps.apple.com/app/id6811065669'
TRAZA_URL = 'https://traza.technology'

# ruta → (palabra clave principal, title, description). Title ≤ 60, description 140–160.
# Cuando el nombre del producto ya lleva «Zentrix», el title no repite «| Zentrix».
PAGINAS = {
    '/': ('software y apps para empresas en Venezuela',
          'Zentrix — Software y apps para empresas en Venezuela',
          None),
    '/work/': ('app para el equipo de tienda y reparto',
               'Zentrix Work — App para el equipo de tienda y reparto',
               'Zentrix Work, la app Android del equipo de tienda: el trabajo llega al teléfono '
               'para preparar pedidos, entregar, repartir y recibir devoluciones en su turno.'),
    '/sales/': ('app de fuerza de ventas',
                'Zentrix Sales — App de fuerza de ventas y cobranza',
                'Zentrix Sales, app de fuerza de ventas para Android y iPhone: ruta, visitas, '
                'pedidos y cobranza de tus vendedores de campo, con o sin señal, conectada a Odoo®.'),
    '/sales/en/': ('field sales app',
                   'Zentrix Sales — Field sales app for Android and iPhone',
                   'Zentrix Sales is the field sales app for Android and iPhone: route, orders, '
                   'collections and proof of visit for your reps, with or without a signal.'),
    '/ai/': ('inteligencia artificial para empresas',
             'Zentrix AI — Inteligencia artificial para empresas',
             'Zentrix AI conecta el conocimiento y los sistemas de tu empresa con agentes de IA y '
             'asistentes para consultar, analizar y actuar, con permisos por rol.'),
    '/cloud/': ('hospedaje, monitoreo y respaldos para empresas',
                'Zentrix Cloud — Hospedaje, monitoreo y respaldos',
                'Zentrix Cloud se ocupa del hospedaje, el monitoreo y los respaldos de tus aplicaciones '
                'y tus datos, para que tu operación siga en marcha sin cuidar servidores.'),
    '/labs/': ('prototipos y validación de productos',
               'Zentrix Labs — Prototipos y validación de productos',
               'En Zentrix Labs investigamos tu reto, construimos prototipos y los validamos antes de '
               'convertirlos en herramientas para tu equipo. Cuéntanos tu idea.'),
    '/logistics/': ('gestión de despachos y entregas',
                    'Zentrix Logistics — Gestión de despachos y entregas',
                    'Zentrix Logistics, próximamente: despachos, rutas, entregas y gestión de incidencias '
                    'en un mismo lugar, para cumplir lo que prometiste a tus clientes.'),
    '/software/': ('consultoría e integración de Odoo',
                   'Zentrix Software — Consultoría e integración de Odoo',
                   'Zentrix Software implementa, configura e integra Odoo® con tus otros sistemas y con '
                   'Zentrix Work y Zentrix Sales: del diagnóstico a la adopción de tu equipo.'),
    '/traza/': ('trazabilidad de documentos, productos y activos',
                'Traza — Trazabilidad de documentos, productos y activos',
                'Traza, un producto de Zentrix: trazabilidad de documentos, productos y activos con '
                'identidad única, responsables, evidencias e historial completo.'),
    # Estructura: soluciones, clientes, recursos, nosotros y contacto
    '/soluciones/': ('soluciones de software para empresas',
                     'Soluciones — Odoo, software e infraestructura | Zentrix', None),
    '/soluciones/odoo-venezuela/': ('implementación de Odoo en Venezuela',
                                    'Implementación de Odoo en Venezuela | Zentrix',
                                    'Implementación de Odoo® con la localización de Venezuela: libros, retenciones, '
                                    'numeración de documentos y doble moneda, con tu equipo capacitado.'),
    '/soluciones/desarrollo-de-software/': ('desarrollo de software a la medida',
                                            'Desarrollo de software a la medida | Zentrix',
                                            'Desarrollo de software a la medida: apps web y móviles construidas alrededor '
                                            'de tu proceso, con diseño, arquitectura y desarrollo en un mismo equipo.'),
    '/soluciones/auditoria-tecnica/': ('auditoría técnica de software',
                                       'Auditoría técnica y arquitectura de sistemas | Zentrix', None),
    '/soluciones/infraestructura-alta-disponibilidad/': ('infraestructura de alta disponibilidad',
                                                         'Infraestructura de alta disponibilidad | Zentrix', None),
    '/soluciones/pagos-y-comercio-digital/': ('pasarelas de pago y punto de venta',
                                              'Pagos y comercio digital — Punto de venta | Zentrix',
                                              'Pagos y comercio digital: punto de venta integrado, cajas que cuadran, '
                                              'pasarelas de pago con conciliación automática y comprobantes electrónicos.'),
    '/soluciones/vision-computacional/': ('visión computacional y analítica de video',
                                          'Visión computacional y analítica de video | Zentrix', None),
    '/clientes/': ('clientes y casos de Zentrix',
                   'Clientes — Casos en distribución y comercio | Zentrix',
                   'Grupo Leiros y GUUAO usan las apps de Zentrix cada día en distribución y comercio en '
                   'Venezuela. Conoce sus casos y las empresas que nos acompañan.'),
    '/recursos/': ('manuales y documentación de Zentrix',
                   'Recursos — Manuales, soporte y documentación | Zentrix',
                   'Manuales de Zentrix Work y Zentrix Sales, soporte, privacidad y términos de cada app, '
                   'y documentación para desarrolladores y modelos de IA, en un solo lugar.'),
    '/nosotros/': ('empresa de software en Isla Margarita, Venezuela',
                   'Nosotros — Ingeniería en Isla Margarita | Zentrix', None),
    '/contacto/': ('contacto Zentrix',
                   'Contacto — Proyectos, demostraciones y soporte | Zentrix',
                   'Escribe a hola@zentrix.company por proyectos y demostraciones, a '
                   'soporte@zentrix.company por soporte, o por WhatsApp. Te responde una persona.'),
    '/privacidad/': (None, 'Privacidad del sitio — Zentrix',
                     'Qué mide zentrix.company y con qué herramienta, sin publicidad, y cómo retirar el '
                     'consentimiento de cookies. Las apps tienen su propia política.'),
    # Zentrix Sales: contacto, legales y versión en inglés
    '/sales/contacto/': ('demostración de app de ventas',
                         'Contacto — Zentrix Sales',
                         'Pide una demostración de Zentrix Sales con tus datos: cuéntanos cómo vende hoy tu '
                         'equipo. O escríbenos por correo, teléfono o WhatsApp, sin compromiso.'),
    '/sales/en/contact.html': ('field sales app demo',
                               'Contact — Zentrix Sales',
                               'Request a Zentrix Sales demo on your own data: tell us how your team sells today. '
                               'Or write to us by email, phone or WhatsApp, no strings attached.'),
    '/sales/privacidad/': (None, 'Política de privacidad — Zentrix Sales',
                           'Qué datos recoge Zentrix Sales, la app de fuerza de ventas, para qué, dónde se '
                           'almacenan, cuánto tiempo se conservan y cómo ejercer tus derechos.'),
    '/sales/en/privacy.html': (None, 'Privacy policy — Zentrix Sales',
                               'What data Zentrix Sales, the field sales app, collects, why, where it is stored, '
                               'how long it is kept and how to exercise your rights over it.'),
    '/sales/soporte/': (None, 'Soporte — Zentrix Sales',
                        'Soporte de Zentrix Sales: te contesta una persona en español en menos de un día hábil, '
                        'por correo, teléfono o WhatsApp. Y cómo pedir tus datos o borrarlos.'),
    '/sales/en/support.html': (None, 'Support — Zentrix Sales',
                               'Zentrix Sales support: a person replies in under one business day by email, phone '
                               'or WhatsApp. And how to request access to or deletion of your data.'),
    '/sales/terminos/': (None, 'Términos de servicio — Zentrix Sales',
                         'Términos de servicio de Zentrix Sales, la app de fuerza de ventas de campo para '
                         'Android y iPhone: quién la contrata, quién la usa y qué reglas aplican.'),
    '/sales/en/terms.html': (None, 'Terms of service — Zentrix Sales',
                             'Terms of service of Zentrix Sales, the field sales app for Android and iPhone: who '
                             'contracts it, who uses it every day and which rules apply.'),
    # Zentrix Work: legales
    '/work/privacidad/': (None, 'Política de privacidad — Zentrix Work',
                          'Qué datos trata Zentrix Work, la app del equipo de tienda, para qué, dónde se '
                          'guardan, cuánto tiempo se conservan y cómo pedir su eliminación.'),
    '/work/soporte/': (None, 'Soporte — Zentrix Work',
                       'Soporte de Zentrix Work, la app del equipo de tienda: preguntas frecuentes, cómo '
                       'contactarnos y cómo eliminar tu cuenta o tus datos de la app.'),
    '/work/terminos/': (None, 'Términos de uso — Zentrix Work',
                        'Términos de uso de Zentrix Work, la app Android del equipo de tienda: quién puede '
                        'usarla, cómo se da la cuenta de operador y qué reglas aplican.'),
    # Manuales: palabras clave de cola larga, sin pisar a las páginas de producto
    '/sales/docs/': ('manual de app para vendedores',
                     'Manual del vendedor — Zentrix Sales',
                     None),
    '/sales/docs/catalogo.html': ('catálogo de productos en la app de ventas', None,
                                  'Buscar un producto en Zentrix Sales por nombre, código o código de barras, '
                                  'usar el escáner, filtrar, elegir la tarifa y compartir por WhatsApp.'),
    '/sales/docs/clientes.html': ('alta de clientes desde la app de ventas', None,
                                  'Cómo proponer un cliente nuevo desde Zentrix Sales y sugerir la corrección de '
                                  'uno que ya tienes: los pasos, los recaudos y cómo queda la solicitud.'),
    '/sales/docs/cobrar.html': ('registrar cobranza en la calle', None,
                                'Cómo registrar un cobro en Zentrix Sales: banco, monto, referencia y '
                                'comprobante, aplicarlo a las facturas y seguir el estado de la solicitud.'),
    '/sales/docs/entrar.html': ('entrar a la app de ventas', None,
                                'Cómo entrar a Zentrix Sales la primera vez: el subdominio de tu empresa, tu '
                                'correo y el PIN. Y por qué conviene sincronizar antes de salir a la calle.'),
    '/sales/docs/facturas.html': ('cartera de cuentas por cobrar', None,
                                  'Cómo leer la cartera en Zentrix Sales: «TE DEBEN», «VENCIDO» y «EN REVISIÓN», '
                                  'las tarjetas, las etiquetas, el compromiso de pago y la moneda.'),
    '/sales/docs/sin-internet.html': ('app de ventas sin internet', None,
                                      'En Zentrix Sales nada se pierde sin señal: qué significa cada color del '
                                      'punto de sincronización y qué hacer si algo dice «No se pudo enviar».'),
    '/sales/docs/visita.html': ('visita al cliente paso a paso', None,
                                'Los ocho pasos de una visita en Zentrix Sales: check-in, inventario, pedido, '
                                'fotos, devoluciones, notas, firma y check-out, con lo que conviene saber.'),
    '/work/docs/': ('manual del operador de tienda',
                    'Manual del operador — Zentrix Work',
                    'Cómo se usa Zentrix Work en la tienda, pantalla a pantalla: entrar, encender '
                    'el turno, atender la llamada, preparar, entregar, repartir o recibir devoluciones.'),
    '/work/docs/ajustes.html': (None, None,
                                'Los ajustes de Zentrix Work: probar una llamada, vibrar y sonar al trabajar, el '
                                'flash en la llamada, el tema oscuro o claro y los permisos de la app.'),
    '/work/docs/dudas.html': (None, None,
                              'Las preguntas más comunes de los operadores de Zentrix Work, resueltas en dos '
                              'líneas: no suenan los pedidos, olvidé mi PIN, el servidor y el turno.'),
    '/work/docs/entrar.html': (None, None,
                               'Cómo se entra a Zentrix Work: el servidor, el correo y la contraseña una sola vez; '
                               'después, con tu PIN o tu huella. Y qué hacer si olvidas el PIN.'),
    '/work/docs/llamada.html': (None, None,
                                'Cuando hay trabajo, Zentrix Work suena como una llamada aunque la pantalla esté '
                                'apagada. Tienes 60 segundos para tomarla deslizando o decir «No puedo».'),
    '/work/docs/permisos.html': (None, None,
                                 'Qué permisos pide Zentrix Work y para qué: avisos, ubicación solo en turno y '
                                 'cámara opcional. Y cómo comprobar que tu teléfono de verdad va a sonar.'),
    '/work/docs/reparto.html': ('app para repartidores', None, None),
    '/work/docs/tu-dia.html': (None, None,
                               'Qué muestra «Mi trabajo» en Zentrix Work: lo que cerraste hoy o esta semana, '
                               'cuánto fue a tiempo, tu ritmo de trabajo y tu nivel como operador.'),
    '/work/docs/turno.html': (None, None,
                              'Cómo se enciende el turno en Zentrix Work: elegir tienda y tareas, deslizar para '
                              'encender, pedir una pausa, apagar, y cuándo el turno se apaga solo.'),
}

# Inglés antiguo de Zentrix Sales (ES, EN), solo mientras no exista /en/: después los
# hreflang los pone generar.py. x-default apunta a la versión en español.
PARES_LEGADO = [
    ('/sales/', '/sales/en/'),
    ('/sales/contacto/', '/sales/en/contact.html'),
    ('/sales/privacidad/', '/sales/en/privacy.html'),
    ('/sales/soporte/', '/sales/en/support.html'),
    ('/sales/terminos/', '/sales/en/terms.html'),
]

SOLUCIONES = {
    '/soluciones/odoo-venezuela/': 'Implementación de Odoo con la localización de Venezuela',
    '/soluciones/desarrollo-de-software/': 'Desarrollo de software a la medida',
    '/soluciones/auditoria-tecnica/': 'Auditoría técnica y arquitectura de sistemas',
    '/soluciones/infraestructura-alta-disponibilidad/': 'Infraestructura de alta disponibilidad',
    '/soluciones/pagos-y-comercio-digital/': 'Pagos y comercio digital',
    '/soluciones/vision-computacional/': 'Visión computacional y analítica de video',
}

SERVICIOS = {
    '/ai/': ('Zentrix AI', 'Inteligencia artificial aplicada a la empresa'),
    '/cloud/': ('Zentrix Cloud', 'Hospedaje, monitoreo y respaldos de aplicaciones'),
    '/labs/': ('Zentrix Labs', 'Investigación, prototipos y validación de productos'),
    '/logistics/': ('Zentrix Logistics', 'Gestión de despachos, rutas y entregas'),
    '/software/': ('Zentrix Software', 'Implementación y personalización de Odoo'),
    '/traza/': ('Traza', 'Trazabilidad de documentos, productos y activos'),
}


def ruta_de(archivo: pathlib.Path) -> str:
    rel = archivo.relative_to(RAIZ).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]  # /work/index.html → /work/
    return '/' + rel


def lang_de(ruta):
    return 'en' if ruta.startswith('/sales/en/') or ruta.startswith('/en/') else 'es'


def texto(fragmento):
    s = re.sub(r'<(script|style|svg)[\s\S]*?</\1>', '', fragmento)
    s = re.sub(r'</?(?:a|b|strong|em|i|span|code|kbd|small|mark|abbr)\b[^>]*>', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = ' '.join(html.unescape(s).split())
    return re.sub(r' ([.,;:!?»)])', r'\1', s)


def org_ref():
    return {'@type': 'Organization', '@id': ORG_ID, 'name': 'Zentrix', 'url': SITIO + '/'}


def organizacion():
    return {
        '@type': 'Organization', '@id': ORG_ID, 'name': 'Zentrix', 'url': SITIO + '/',
        'logo': {'@type': 'ImageObject', 'url': LOGO, 'width': 512, 'height': 512},
        'image': SITIO + '/assets/img/og.png',
        'slogan': 'Tecnología para trabajar mejor',
        'description': 'Zentrix convierte los procesos de las empresas en apps sencillas conectadas a su '
                       'sistema de gestión: Zentrix Work, Zentrix Sales e implementación de Odoo®.',
        'email': 'hola@zentrix.company',
        'telephone': '+58-412-346-9712',
        'sameAs': [TRAZA_URL, PLAY_WORK, PLAY_SALES, APPSTORE_SALES],
        'contactPoint': [
            {'@type': 'ContactPoint', 'contactType': 'sales', 'email': 'hola@zentrix.company',
             'telephone': '+58-412-346-9712', 'url': 'https://wa.me/584123469712',
             'availableLanguage': ['es']},
            {'@type': 'ContactPoint', 'contactType': 'technical support', 'email': 'soporte@zentrix.company',
             'availableLanguage': ['es']},
        ],
    }


NOMBRES_SECCION = {
    'es': {'work': ('Zentrix Work', 'Manual del operador'), 'sales': ('Zentrix Sales', 'Manual del vendedor'),
           'soluciones': ('Soluciones', None)},
    'en': {'work': ('Zentrix Work', 'Operator manual'), 'sales': ('Zentrix Sales', 'Sales rep manual'),
           'solutions': ('Solutions', None)},
}


def migas(ruta, nombre_pagina, lang):
    """Inicio › sección › (manual) › página, según la ruta."""
    if ruta.startswith('/sales/en/'):  # inglés antiguo de Zentrix Sales
        items = [('Home', '/'), ('Zentrix Sales', '/sales/en/')]
    else:
        prefijo = '/en/' if ruta.startswith('/en/') else '/'
        items = [('Home' if lang == 'en' else 'Inicio', prefijo)]
        partes = ruta[len(prefijo):].strip('/').split('/')
        sec = NOMBRES_SECCION[lang].get(partes[0])
        if sec and len(partes) > 0 and partes[0]:
            base = prefijo + partes[0] + '/'
            items.append((sec[0], base))
            if len(partes) > 1 and partes[1] == 'docs' and sec[1]:
                items.append((sec[1], base + 'docs/'))
    if items[-1][1] != ruta:
        items.append((nombre_pagina, ruta))
    return {
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITIO + r}
            for i, (n, r) in enumerate(items)
        ],
    }


def faq(cuerpo):
    m = re.search(r'<main[\s\S]*?</main>', cuerpo)
    main = m.group(0) if m else ''
    trozos = re.split(r'(<h2[^>]*>[\s\S]*?</h2>)', main)
    preguntas = []
    for i in range(1, len(trozos) - 1, 2):
        q = texto(trozos[i])
        a = texto(re.split(r'<(?:section|aside|nav)\b', trozos[i + 1])[0])
        if q and a:
            preguntas.append({'@type': 'Question', 'name': q,
                              'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    return {'@type': 'FAQPage', 'mainEntity': preguntas} if preguntas else None


def jsonld(ruta, titulo, descripcion, cuerpo, lang):
    url = SITIO + ruta
    nombre = re.split(r' — | \| ', titulo)[0].strip()
    plantilla = ruta[3:] if ruta.startswith('/en/') else ruta
    grafo = []
    if plantilla == '/':
        grafo.append(organizacion())
        grafo.append({
            '@type': 'WebSite', '@id': WEB_ID, 'name': 'Zentrix', 'url': SITIO + '/',
            'inLanguage': ['es', 'en'], 'publisher': {'@id': ORG_ID},
            'potentialAction': {'@type': 'SearchAction',
                                'target': {'@type': 'EntryPoint', 'urlTemplate': SITIO + '/?q={search_term_string}'},
                                'query-input': 'required name=search_term_string'},
        })
        return grafo
    if plantilla in ('/work/', '/sales/') or ruta == '/sales/en/':
        work = plantilla == '/work/'
        tiendas = [PLAY_WORK] if work else [PLAY_SALES, APPSTORE_SALES]
        grafo.append({
            '@type': 'SoftwareApplication', '@id': url + '#app',
            'name': 'Zentrix Work' if work else 'Zentrix Sales',
            'applicationCategory': 'BusinessApplication',
            'operatingSystem': 'Android' if work else 'Android, iOS',
            'description': descripcion, 'url': url, 'inLanguage': lang,
            'image': SITIO + ('/assets/img/work-icono-512.png' if work else '/assets/img/sales-icono-512.png'),
            'installUrl': tiendas, 'sameAs': tiendas,
            'publisher': org_ref(),
        })
    elif plantilla in SERVICIOS or plantilla in SOLUCIONES or re.match(r'^/solutions/[^/]+/$', plantilla):
        n, tipo = SERVICIOS.get(plantilla) or (nombre, SOLUCIONES.get(plantilla, nombre))
        servicio = {'@type': 'Service', '@id': url + '#servicio', 'name': n, 'serviceType': tipo,
                    'description': descripcion, 'url': url, 'inLanguage': lang, 'provider': org_ref()}
        if plantilla in ('/software/', '/soluciones/odoo-venezuela/', '/solutions/odoo-venezuela/'):
            servicio['areaServed'] = ['Venezuela', 'Latinoamérica']
        if plantilla == '/traza/':
            servicio['sameAs'] = [TRAZA_URL]
        grafo.append(servicio)
    if ruta.endswith('/dudas.html'):
        f = faq(cuerpo)
        if f:
            grafo.append(f)
    grafo.append(migas(ruta, nombre, lang))
    return grafo


def poner_meta(cab, atributo, clave, valor):
    """Reemplaza el content de una meta existente; si no existe, no la crea."""
    patron = re.compile(r'(<meta %s="%s" content=")[^"]*(")' % (atributo, re.escape(clave)))
    return patron.sub(lambda m: m.group(1) + html.escape(valor, quote=True) + m.group(2), cab)


def meta(cab, atributo, clave):
    m = re.search(r'<meta %s="%s" content="([^"]*)"' % (atributo, re.escape(clave)), cab)
    return html.unescape(m.group(1)) if m else ''


def aplicar(original, ruta):
    """Devuelve la página con su SEO al día. La usa también generar.py."""
    if 'http-equiv="refresh"' in original or re.search(r'name="robots" content="[^"]*noindex', original):
        return original
    lang = lang_de(ruta)
    fin = original.index('</head>')
    cab, cuerpo = original[:fin], original[fin:]
    cab = re.sub(r'\n?\s*<!-- seo -->[\s\S]*?<!-- /seo -->', '', cab)

    _, titulo, descripcion = PAGINAS.get(ruta, (None, None, None))
    if titulo:
        cab = re.sub(r'<title>[\s\S]*?</title>', '<title>%s</title>' % html.escape(titulo, quote=False), cab)
        cab = poner_meta(cab, 'property', 'og:title', titulo)
        cab = poner_meta(cab, 'property', 'og:image:alt', titulo)
    if descripcion:
        cab = poner_meta(cab, 'name', 'description', descripcion)
        cab = poner_meta(cab, 'property', 'og:description', descripcion)
    titulo = html.unescape(re.search(r'<title>([\s\S]*?)</title>', cab).group(1))
    descripcion = meta(cab, 'name', 'description')

    lineas = ['<!-- seo -->']
    if 'hreflang=' not in cab:
        for es, en in PARES_LEGADO:
            if ruta in (es, en):
                lineas += [
                    '<link rel="alternate" hreflang="es" href="%s%s">' % (SITIO, es),
                    '<link rel="alternate" hreflang="en" href="%s%s">' % (SITIO, en),
                    '<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITIO, es),
                    '<meta property="og:locale:alternate" content="%s">' % ('en_US' if lang == 'es' else 'es_VE'),
                ]
    lineas += [
        '<meta name="twitter:title" content="%s">' % html.escape(titulo, quote=True),
        '<meta name="twitter:description" content="%s">' % html.escape(descripcion, quote=True),
    ]
    datos = {'@context': 'https://schema.org', '@graph': jsonld(ruta, titulo, descripcion, cuerpo, lang)}
    lineas.append('<script type="application/ld+json">%s</script>'
                  % json.dumps(datos, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
    lineas.append('<!-- /seo -->')
    cab = cab.rstrip() + '\n  ' + '\n  '.join(lineas) + '\n'
    return cab + cuerpo


def procesar(archivo: pathlib.Path):
    return aplicar(archivo.read_text(encoding='utf-8'), ruta_de(archivo))


def paginas():
    excluir = {'.git', '.github', 'node_modules', '_site', 'pagefind', 'herramientas'}
    return sorted(p for p in RAIZ.rglob('*.html') if not excluir.intersection(p.relative_to(RAIZ).parts))


def tabla():
    """Tabla Markdown página → palabra clave → title → description → schema (para SEO.md)."""
    filas = ['| Página | Palabra clave principal | Title | Description | Schema |', '|---|---|---|---|---|']
    for p in paginas():
        s = p.read_text(encoding='utf-8')
        if 'http-equiv="refresh"' in s or re.search(r'name="robots" content="[^"]*noindex', s):
            continue
        r = ruta_de(p)
        t = html.unescape(re.search(r'<title>([\s\S]*?)</title>', s).group(1))
        m = re.search(r'application/ld\+json">(.*?)</script>', s)
        ld = json.loads(m.group(1).replace('<\\/', '</')) if m else {'@graph': []}
        filas.append('| `%s` | %s | %s | %s | %s |' % (
            r, (PAGINAS.get(r) or (None,))[0] or '—', t.replace('|', '\\|'),
            meta(s, 'name', 'description').replace('|', '\\|'), ', '.join(n['@type'] for n in ld['@graph'])))
    return '\n'.join(filas)


def main():
    if '--tabla' in sys.argv:
        print(tabla())
        return
    check = '--check' in sys.argv
    distintos = []
    for p in paginas():
        nuevo = procesar(p)
        if nuevo != p.read_text(encoding='utf-8'):
            distintos.append(p.relative_to(RAIZ).as_posix())
            if not check:
                p.write_text(nuevo, encoding='utf-8')
    print(('difieren: ' if check else 'reescritas: ') + str(len(distintos)))
    if check and distintos:
        print('\n'.join(distintos))
        sys.exit(1)


if __name__ == '__main__':
    main()
