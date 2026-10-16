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
# URL de tienda: fuente única en herramientas/productos.json (también la usa generar.py)
_TIENDAS = json.loads((RAIZ / 'herramientas' / 'productos.json').read_text(encoding='utf-8'))
PLAY_WORK = _TIENDAS['work']['play']
PLAY_SALES = _TIENDAS['sales']['play']
APPSTORE_SALES = _TIENDAS['sales']['appstore']
TRAZA_URL = 'https://traza.technology'
# Redes sociales oficiales (herramientas/redes.json): solo las que tienen URL. Las usan el pie
# (generar.py) y el sameAs de la Organization. No se inventan perfiles.
NOMBRES_REDES = {'linkedin': 'LinkedIn', 'instagram': 'Instagram', 'x': 'X', 'youtube': 'YouTube', 'facebook': 'Facebook'}
_REDES_JSON = json.loads((RAIZ / 'herramientas' / 'redes.json').read_text(encoding='utf-8'))
REDES = [(k, n, _REDES_JSON[k].strip()) for k, n in NOMBRES_REDES.items() if (_REDES_JSON.get(k) or '').strip()]

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
    '/check/': ('app de control de acceso y garita',
                'Zentrix Check — App de garita y control de acceso',
                'Zentrix Check, la app Android de la garita: el vigilante revisa cada camión contra Odoo®, '
                'toma fotos y firma un acta que no se puede cambiar, con o sin señal.'),
    '/en/sales/': ('field sales app',
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
    '/logistics/': ('software de logística y reparto',
                    'Zentrix Logistics — Software de logística y reparto',
                    'Software de logística y reparto sobre Odoo®: preparación, despacho y última milla, '
                    'control de flota de reparto en vivo, cobro contra entrega y devoluciones.'),
    '/software/': ('consultoría Odoo; soporte y desarrollo a medida en Odoo',
                   'Zentrix Software — Consultoría, soporte y desarrollo en Odoo',
                   'Consultoría Odoo, soporte y desarrollo a medida en Odoo: configuramos, integramos y mantenemos '
                   'tu sistema, y lo conectamos con Zentrix Work y Zentrix Sales.'),
    '/traza/': ('trazabilidad de documentos, productos y activos',
                'Traza — Trazabilidad de documentos, productos y activos',
                'Traza, un producto de Zentrix: trazabilidad de documentos, productos y activos con '
                'identidad única, responsables, evidencias e historial completo.'),
    # Estructura: soluciones, clientes, recursos, nosotros y contacto
    '/soluciones/': ('soluciones de software para empresas',
                     'Soluciones — Odoo, software e infraestructura | Zentrix', None),
    '/soluciones/odoo-venezuela/': ('implementación de Odoo en Venezuela',
                                    'Implementación de Odoo en Venezuela | Zentrix',
                                    'Implementación de Odoo 19 en Venezuela con la localización: factura digital SENIAT, '
                                    'IGTF, retenciones de IVA e ISLR, libros y bolívares y dólares a tasa BCV.'),
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
    '/recursos/': ('documentación de Zentrix',
                   'Recursos — Documentación, soporte y legal | Zentrix',
                   'Documentación de Zentrix Work, Sales y Check, soporte, privacidad y términos de cada app, '
                   'y archivos para desarrolladores y modelos de IA, en un solo lugar.'),
    '/nosotros/': ('empresa de software en Isla Margarita, Venezuela',
                   'Nosotros — Ingeniería en Isla Margarita | Zentrix', None),
    '/contacto/': ('contacto Zentrix',
                   'Contacto — Proyectos, demostraciones y soporte | Zentrix',
                   'Escribe a hola@zentrix.company por proyectos y demostraciones, a '
                   'soporte@zentrix.company por soporte, o por WhatsApp. Te responde una persona.'),
    '/soporte/': ('soporte Zentrix',
                  'Soporte — Preguntas, acceso y tus datos | Zentrix',
                  'Soporte de Zentrix Work, Sales y Check: preguntas frecuentes, acceso, documentación y cómo '
                  'eliminar tu cuenta o tus datos. Te responde una persona.'),
    '/legal/': (None, 'Legal — Privacidad y términos | Zentrix',
                'Las políticas de privacidad y los términos de Zentrix Work y Zentrix Sales, y la privacidad '
                'y las cookies del sitio web zentrix.company, en un solo índice.'),
    '/privacidad/': (None, 'Privacidad del sitio — Zentrix',
                     'Qué mide zentrix.company y con qué herramienta, sin publicidad, y cómo retirar el '
                     'consentimiento de cookies. Las apps tienen su propia política.'),
    # Zentrix Sales: contacto, legales y versión en inglés
    '/sales/privacidad/': (None, 'Política de privacidad — Zentrix Sales',
                           'Qué datos recoge Zentrix Sales, la app de fuerza de ventas, para qué, dónde se '
                           'almacenan, cuánto tiempo se conservan y cómo ejercer tus derechos.'),
    '/en/sales/privacy/': (None, 'Privacy policy — Zentrix Sales',
                               'What data Zentrix Sales, the field sales app, collects, why, where it is stored, '
                               'how long it is kept and how to exercise your rights over it.'),
    '/sales/terminos/': (None, 'Términos de servicio — Zentrix Sales',
                         'Términos de servicio de Zentrix Sales, la app de fuerza de ventas de campo para '
                         'Android y iPhone: quién la contrata, quién la usa y qué reglas aplican.'),
    '/en/sales/terms/': (None, 'Terms of service — Zentrix Sales',
                             'Terms of service of Zentrix Sales, the field sales app for Android and iPhone: who '
                             'contracts it, who uses it every day and which rules apply.'),
    '/check/docs/': ('documentación para el vigilante de garita',
                     'Documentación para el vigilante — Zentrix Check',
                     'Cómo se usa Zentrix Check en la garita, pantalla a pantalla: entrar, sacar un camión, '
                     'recibir mercancía, llaves, activos, novedades y trabajar sin señal.'),
    '/check/docs/entrar.html': (None, None,
        'Cómo se entra a Zentrix Check: tu correo y tu contraseña de la empresa la primera vez, el servidor y tu sede, el PIN de cada día y qué hacer si lo olvidas.'),
    '/check/docs/encender.html': (None, None,
        'Cómo se enciende y se apaga el vigilante en Zentrix Check: qué cambia al encenderte, cómo apagarte al terminar y qué pasa si dejas el teléfono sin usar.'),
    '/check/docs/hoy.html': (None, None,
        'La pantalla Hoy de Zentrix Check: las pestañas Salen, Llegan y Adentro, la barra de abajo, el menú Más y el escáner que abre cualquier camión, llave o activo.'),
    '/check/docs/salida.html': (None, None,
        'Cómo sale un camión con Zentrix Check: placa y chofer, guía y facturas, conteo, foto, candado, firma con tu PIN y qué hacer con las diferencias.'),
    '/check/docs/recepcion.html': (None, None,
        'Cómo se recibe mercancía con Zentrix Check: fotos al llegar, el precinto de un contenedor, la factura del proveedor, el conteo y los retornos de ruta.'),
    '/check/docs/sin-documento.html': (None, None,
        'Cómo se registra en Zentrix Check lo que entra o sale sin documento en Odoo: qué es, los artículos con su foto y qué queda en el registro de la garita.'),
    '/check/docs/llaves.html': (None, None,
        'Cómo se controlan las llaves con Zentrix Check: el llavero con código QR, quién se lleva cada llave, cuándo vuelve y qué hacer si una llave no regresa a tiempo.'),
    '/check/docs/activos.html': (None, None,
        'Cómo salen y regresan los activos con Zentrix Check: la etiqueta QR, el pase que aprueba el gerente, la salida, el regreso y lo que vuelve incompleto.'),
    '/check/docs/novedades.html': (None, None,
        'Cómo se registra una novedad en Zentrix Check, qué hacer si es grave, los teléfonos de la sede y cómo se anota a quién llamaste con «¿Quién autorizó?».'),
    '/check/docs/sin-senal.html': (None, None,
        'Cómo trabaja Zentrix Check sin señal en la garita: qué se guarda cifrado en el teléfono, cómo ver lo que falta por enviar y qué necesita conexión.'),
    '/check/docs/administrador.html': (None, None,
        'La consola del administrador de Seguridad en Zentrix Check: el código para entrar, el día de la sede, las actas, las diferencias y las fotos, solo para mirar.'),
    '/check/docs/dudas.html': (None, None,
        'Dudas rápidas de Zentrix Check resueltas en dos líneas: el PIN, la contraseña, el teléfono de la garita, la señal, las diferencias y quién te ayuda.'),
    # Zentrix Check: legales
    '/check/privacidad/': (None, 'Política de privacidad — Zentrix Check',
                           'Qué datos registra Zentrix Check, la app de la garita de seguridad, para qué, dónde '
                           'se guardan, quién los ve y cómo pedir su acceso, corrección o eliminación.'),
    '/check/terminos/': (None, 'Términos de uso — Zentrix Check',
                         'Términos de uso de Zentrix Check, la app Android de la garita: quién puede usarla, '
                         'cómo se da la cuenta del vigilante y qué reglas aplican a las actas.'),
    # Zentrix Work: legales
    '/work/privacidad/': (None, 'Política de privacidad — Zentrix Work',
                          'Qué datos trata Zentrix Work, la app del equipo de tienda, para qué, dónde se '
                          'guardan, cuánto tiempo se conservan y cómo pedir su eliminación.'),
    '/work/terminos/': (None, 'Términos de uso — Zentrix Work',
                        'Términos de uso de Zentrix Work, la app Android del equipo de tienda: quién puede '
                        'usarla, cómo se da la cuenta de operador y qué reglas aplican.'),
    # Documentación: palabras clave de cola larga, sin pisar a las páginas de producto
    '/sales/docs/': ('documentación de app para vendedores',
                     'Documentación para el vendedor — Zentrix Sales',
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
                                'Cómo entrar a Zentrix Sales la primera vez: el dominio de tu empresa, tu '
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
    '/work/docs/': ('documentación para el operador de tienda',
                    'Documentación para el operador — Zentrix Work',
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
                               'Qué muestra «Mi trabajo de hoy» en Zentrix Work: lo que cerraste hoy o esta semana, '
                               'cuánto fue a tiempo, tu ritmo de trabajo y tu nivel como operador.'),
    '/work/docs/turno.html': (None, None,
                              'Cómo se enciende el turno en Zentrix Work: elegir tienda y tareas, deslizar para '
                              'encender, pedir una pausa, apagar, y cuándo el turno se apaga solo.'),
}

# Inglés bajo /en/ (fase 3 del multiidioma)
PAGINAS.update({
    '/en/': ('business software and apps in Venezuela',
        'Zentrix — Business software and apps for Venezuela',
        'Technology to work better: apps for your store team and field sales force, Odoo® with Venezuelan localization, and custom software built in Venezuela.'),
    '/en/work/': ('store team app',
        'Zentrix Work — The app for store and delivery teams',
        'Zentrix Work, the Android app for store teams: work lands on the phone to pick orders, deliver, run delivery routes and take returns during the shift.'),
    '/en/check/': ('gate and access control app',
        'Zentrix Check — Security gate and access control app',
        'Zentrix Check, the Android app for the security gate: guards check every truck against Odoo®, take photos and sign a record that cannot be changed.'),
    '/en/check/docs/': ('Zentrix Check documentation',
        'Zentrix Check documentation — For security guards',
        'The Zentrix Check documentation for security guards, screen by screen: signing in, trucks leaving, receipts, keys, assets, incidents and working offline.'),
    '/en/check/privacy/': (None,
        'Privacy policy — Zentrix Check',
        'What the Zentrix Check gate app records, why, who sees it and how it is protected, and how to ask for access to your data, its correction or its deletion.'),
    '/en/check/terms/': (None,
        'Terms of use — Zentrix Check',
        'The terms of use of the Zentrix Check app for security guards: what it is for, what you agree to when using it, the records it keeps and who provides it.'),
    '/en/ai/': ('AI for business',
        'Zentrix AI — Applied artificial intelligence for business',
        'Zentrix AI connects your company’s knowledge and systems to AI agents and assistants that query, analyze and act, with role-based permissions for each user.'),
    '/en/logistics/': ('logistics and delivery software',
        'Zentrix Logistics — Logistics and delivery software',
        'Logistics and delivery software on Odoo®: picking, dispatch and last-mile delivery, live delivery fleet management, cash on delivery and returns.'),
    '/en/cloud/': ('managed hosting and backups',
        'Zentrix Cloud — Hosting, monitoring and backups',
        'Zentrix Cloud takes care of hosting, monitoring and backups for your apps and data, so they stay available and your team can focus on the work itself.'),
    '/en/labs/': ('product research and prototyping',
        'Zentrix Labs — Research and new product validation',
        'Zentrix Labs researches, prototypes and validates new products to expand what we can offer you, testing each idea before it joins the Zentrix suite.'),
    '/en/software/': ('Odoo consulting',
        'Zentrix Software — Odoo consulting, support and development',
        'Odoo consulting, support and custom development: we configure, integrate and maintain your Odoo® system, and connect it with Zentrix Work and Zentrix Sales.'),
    '/en/traza/': ('product traceability',
        'Traza — Traceability for documents, products and assets',
        'Traza gives your documents, products and assets a verifiable journey: where they came from, where they went, who moved them and where they are now.'),
    '/en/solutions/': ('software solutions Venezuela',
        'Solutions — Odoo®, software and infrastructure | Zentrix',
        'Odoo® with Venezuelan localization, custom software, technical audits, high-availability infrastructure, payments and computer vision, by the Zentrix team.'),
    '/en/solutions/odoo-venezuela/': ('Odoo implementation in Venezuela',
        'Odoo® implementation in Venezuela | Zentrix',
        'Odoo 19 implementation in Venezuela with the Venezuelan localization: SENIAT e-invoicing, IGTF, VAT and income-tax withholdings and Bs/USD at the BCV rate.'),
    '/en/solutions/software-development/': ('custom software development',
        'Custom software development | Zentrix',
        'Custom web and mobile apps built around your process: design and engineering in one team, an architecture that grows and continuous delivery you can try.'),
    '/en/solutions/technical-audit/': ('technical audit and architecture',
        'Technical audit and systems architecture | Zentrix',
        'An honest diagnosis of your systems, a roadmap with reasons, argued technology choices and a second opinion on third-party quotes before you sign anything.'),
    '/en/solutions/high-availability-infrastructure/': ('high availability infrastructure',
        'High-availability infrastructure | Zentrix',
        'Servers on-premises or in the cloud with tested backups, Zero Trust access and containers, designed to keep your operation running through power outages.'),
    '/en/solutions/payments-and-digital-commerce/': ('POS and payment gateways',
        'Payments and digital commerce | Zentrix',
        'Integrated point of sale, tills with shifts and cash counts, payment gateways with automatic reconciliation, and electronic receipts for your customers.'),
    '/en/solutions/computer-vision/': ('computer vision video analytics',
        'Computer vision and video analytics | Zentrix',
        'Real-time video analytics on the cameras you already have: event detection, biometric access control and alerts that reach the person who needs to act.'),
    '/en/customers/': ('Zentrix customers',
        'Customers and case studies | Zentrix',
        'Grupo Leiros and GUUAO run on Zentrix apps every day, in stores, on the street and in the office. Meet the companies and institutions we work alongside.'),
    '/en/resources/': ('Zentrix documentation and support',
        'Resources: documentation, support and legal | Zentrix',
        'Zentrix Work and Zentrix Sales documentation, support pages, privacy policies and terms for every app, plus llms.txt and the sitemap for developers and AI.'),
    '/en/about/': ('software company Isla Margarita',
        'About Zentrix — Engineering team in Venezuela',
        'Zentrix is the new brand of Equinoccio (EQNIO), an engineering, AI and product team on Isla Margarita, Venezuela, working with clients across the Americas.'),
    '/en/contact/': ('contact Zentrix',
        'Contact Zentrix — A person replies in one day',
        'Write to hola@zentrix.company for projects and demos, soporte@zentrix.company for support, or use WhatsApp. A person replies within one business day.'),
    '/en/work/docs/': ('Zentrix Work documentation',
        'Zentrix Work documentation — For store teams',
        'The Zentrix Work documentation for store teams, step by step: signing in, your shift, picking orders with the scanner, delivery runs, returns and settings.'),
    '/en/sales/docs/': ('Zentrix Sales documentation',
        'Zentrix Sales documentation — For field reps',
        'The Zentrix Sales documentation for field reps, screen by screen: your route, the visit, orders, collections, invoices and working without a signal or internet.'),
    '/en/work/privacy/': (None,
        'Privacy policy — Zentrix Work',
        'What the Zentrix Work app collects, why, who sees it and for how long, how it is protected, and how to ask for access to your data or for its deletion.'),
    '/en/work/terms/': (None,
        'Terms of use — Zentrix Work',
        'The terms of use of the Zentrix Work app for store staff: what it is for, what you agree to when using it, the data involved and who provides the app.'),
    '/en/support/': ('Zentrix support',
        'Support — Questions, access and your data | Zentrix',
        'Zentrix Work, Sales and Check support: common questions, access, documentation and how to delete your account or your data. A person replies within a day.'),
    '/en/legal/': (None,
        'Legal — Privacy and terms | Zentrix',
        'The privacy policies and terms of Zentrix Work and Zentrix Sales, plus the privacy and cookie policy of the zentrix.company website, in one index.'),
    '/en/privacy/': (None,
        'Website privacy — Zentrix',
        'What zentrix.company measures and with which tool, with no advertising, and how to withdraw cookie consent. The apps have their own privacy policies.'),
})

# Inglés antiguo de Zentrix Sales (ES, EN), solo mientras no exista /en/: después los
# hreflang los pone generar.py. x-default apunta a la versión en español.
PARES_LEGADO = [
    ('/sales/', '/sales/en/'),
    ('/sales/privacidad/', '/sales/en/privacy.html'),
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
    '/logistics/': ('Zentrix Logistics', 'Software de logística y reparto: despacho y última milla'),
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


# La dirección que publica /contacto/ (y las legales). verificar_seo.py comprueba que coincida.
DIRECCION = {'@type': 'PostalAddress', 'streetAddress': '10302 NW South River Drive', 'addressLocality': 'Medley',
             'addressRegion': 'FL', 'postalCode': '33178', 'addressCountry': 'US'}


def direccion():
    return dict(DIRECCION)


def org_ref():
    return {'@type': 'Organization', '@id': ORG_ID, 'name': 'Zentrix', 'url': SITIO + '/', 'address': direccion()}


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
        'address': direccion(),
        'sameAs': [u for _, _, u in REDES] + [TRAZA_URL, PLAY_WORK, PLAY_SALES, APPSTORE_SALES],
        'contactPoint': [
            {'@type': 'ContactPoint', 'contactType': 'sales', 'email': 'hola@zentrix.company',
             'telephone': '+58-412-346-9712', 'url': 'https://wa.me/584123469712',
             'availableLanguage': ['es']},
            {'@type': 'ContactPoint', 'contactType': 'technical support', 'email': 'soporte@zentrix.company',
             'availableLanguage': ['es']},
        ],
    }


NOMBRES_SECCION = {
    'es': {'work': ('Zentrix Work', 'Documentación para el operador'), 'sales': ('Zentrix Sales', 'Documentación para el vendedor'),
           'check': ('Zentrix Check', 'Documentación para el vigilante'),
           'soluciones': ('Soluciones', None)},
    'en': {'work': ('Zentrix Work', 'Operator documentation'), 'sales': ('Zentrix Sales', 'Sales rep documentation'),
           'check': ('Zentrix Check', 'Guard documentation'),
           'solutions': ('Solutions', None)},
}


def migas(ruta, nombre_pagina, lang):
    """Inicio › sección › (documentación) › página, según la ruta."""
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
    bloque = re.search(r'<div class="preguntas[^"]*">([\s\S]*?)</div>', main)
    if bloque:  # preguntas en <details><summary>…</summary>respuesta</details>
        qs = [{'@type': 'Question', 'name': texto(q), 'acceptedAnswer': {'@type': 'Answer', 'text': texto(r)}}
              for q, r in re.findall(r'<details[^>]*>\s*<summary>([\s\S]*?)</summary>([\s\S]*?)</details>', bloque.group(1))]
        return {'@type': 'FAQPage', 'mainEntity': qs} if qs else None
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
    if plantilla in ('/work/', '/sales/') or ruta in ('/sales/en/', '/en/sales/'):
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
    elif plantilla == '/check/':
        # Sin URL de tienda hasta que la ficha de Google Play esté publicada (productos.json).
        app = {
            '@type': 'SoftwareApplication', '@id': url + '#app', 'name': 'Zentrix Check',
            'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Android',
            'description': descripcion, 'url': url, 'inLanguage': lang,
            'image': SITIO + '/assets/img/check-icono-512.png', 'publisher': org_ref(),
        }
        if _TIENDAS['check'].get('play'):
            app['installUrl'] = app['sameAs'] = [_TIENDAS['check']['play']]
        grafo.append(app)
    elif plantilla in SERVICIOS or plantilla in SOLUCIONES or re.match(r'^/solutions/[^/]+/$', plantilla):
        n, tipo = SERVICIOS.get(plantilla) or (nombre, SOLUCIONES.get(plantilla, nombre))
        if lang == 'en':
            n, tipo = (SERVICIOS[plantilla][0] if plantilla in SERVICIOS else nombre), nombre
        servicio = {'@type': 'Service', '@id': url + '#servicio', 'name': n, 'serviceType': tipo,
                    'description': descripcion, 'url': url, 'provider': org_ref()}  # Service no tiene inLanguage
        if plantilla in ('/software/', '/soluciones/odoo-venezuela/', '/solutions/odoo-venezuela/'):
            servicio['areaServed'] = ['Venezuela', 'Latinoamérica']
        if plantilla == '/traza/':
            servicio['sameAs'] = [TRAZA_URL]
        if plantilla == '/logistics/':
            # El servicio se presta con un software: la capa logística sobre Odoo® y la app Zentrix Work.
            servicio['areaServed'] = ['Venezuela', 'Latinoamérica'] if lang == 'es' else ['Venezuela', 'Latin America']
            servicio['audience'] = {'@type': 'BusinessAudience', 'audienceType': (
                'Retail, distribución y consumo masivo' if lang == 'es' else 'Retail, distribution and consumer goods')}
            servicio['isRelatedTo'] = {'@id': url + '#app'}
            grafo.append({
                '@type': 'SoftwareApplication', '@id': url + '#app', 'name': 'Zentrix Logistics',
                'applicationCategory': 'BusinessApplication',
                'applicationSubCategory': 'Logística y reparto' if lang == 'es' else 'Logistics and delivery',
                'operatingSystem': 'Web, Android', 'description': descripcion, 'url': url, 'inLanguage': lang,
                'image': SITIO + '/assets/img/og-logistics.png',
                'featureList': ([
                    'Preparación con escáner, bultos en rack y etiqueta por bulto',
                    'FEFO y control de lotes', 'Lotes de despacho y guías',
                    'Reparto con flota propia o de terceros', 'Seguimiento en vivo y puesto de control',
                    'Cobro contra entrega', 'Devoluciones autorizadas'] if lang == 'es' else [
                    'Scanner-guided picking, parcels on the rack and a label per parcel',
                    'FEFO and lot control', 'Dispatch batches and dispatch notes',
                    'Delivery with your own fleet or a third party', 'Live tracking and control room',
                    'Cash on delivery', 'Authorized returns']),
                'softwareRequirements': 'Odoo® 19', 'publisher': org_ref(),
            })
        grafo.append(servicio)
    if plantilla in ('/contacto/', '/contact/'):
        grafo.append({'@type': 'ContactPage', '@id': url + '#pagina', 'name': nombre, 'url': url, 'inLanguage': lang,
                      'description': descripcion, 'about': {'@id': ORG_ID}})
    prod_manual = re.match(r'^/(work|sales|check)/docs/', plantilla)
    if prod_manual:
        # Documentación (portada y capítulos) en los dos idiomas: artículo técnico con su idioma.
        clave = prod_manual.group(1)
        app = NOMBRES_SECCION[lang][clave][0]
        raiz = ('/en' if lang == 'en' else '') + f'/{clave}/docs/'
        pref = '/en' if lang == 'en' else ''
        articulo = {'@type': 'TechArticle', '@id': url + '#articulo', 'headline': nombre,
                    'description': descripcion, 'url': url, 'inLanguage': lang,
                    # La app es el mismo nodo que define su página (/work/#app…), con el mismo tipo y nombre.
                    'about': {'@type': 'SoftwareApplication', '@id': f'{SITIO}{pref}/{clave}/#app', 'name': app},
                    'image': f'{SITIO}/assets/img/og-{clave}.png',
                    'author': org_ref(), 'publisher': org_ref()}
        if url != SITIO + raiz:
            articulo['isPartOf'] = {'@id': SITIO + raiz + '#articulo'}  # la portada de la documentación
        grafo.append(articulo)
    if ruta.endswith('/dudas.html') or 'class="preguntas' in cuerpo:
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
