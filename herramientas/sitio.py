"""Datos comunes del sitio: rutas por idioma, productos, soluciones y textos de la navegación.

Lo usan `generar.py` (páginas nuevas, cabecera, pie, SEO, sitemap) y `contenido.py`.
"""
import html

DOMINIO = 'https://zentrix.company'
MONO = '/assets/img/logos/monogramas'
TRAZA_URL = 'https://traza.technology'
TRAZA_ICONO = '/assets/img/logos/traza/traza_icono-64.webp'

# ── Pares de rutas español ↔ inglés ─────────────────────────────────────────
SOLUCIONES = [
    # clave, slug ES, slug EN, icono
    ('odoo', 'odoo-venezuela', 'odoo-venezuela', 'capas'),
    ('software', 'desarrollo-de-software', 'software-development', 'codigo'),
    ('auditoria', 'auditoria-tecnica', 'technical-audit', 'lupa'),
    ('infra', 'infraestructura-alta-disponibilidad', 'high-availability-infrastructure', 'servidor'),
    ('pagos', 'pagos-y-comercio-digital', 'payments-and-digital-commerce', 'tarjeta'),
    ('vision', 'vision-computacional', 'computer-vision', 'ojo'),
]

PARES = [
    ('/', '/en/'),
    ('/work/', '/en/work/'),
    ('/work/docs/', '/en/work/docs/'),
    ('/work/privacidad/', '/en/work/privacy/'),
    ('/work/soporte/', '/en/work/support/'),
    ('/work/terminos/', '/en/work/terms/'),
    ('/sales/', '/en/sales/'),
    ('/sales/docs/', '/en/sales/docs/'),
    ('/sales/privacidad/', '/en/sales/privacy/'),
    ('/sales/soporte/', '/en/sales/support/'),
    ('/sales/terminos/', '/en/sales/terms/'),
    ('/sales/contacto/', '/en/sales/contact/'),
    ('/ai/', '/en/ai/'),
    ('/logistics/', '/en/logistics/'),
    ('/cloud/', '/en/cloud/'),
    ('/labs/', '/en/labs/'),
    ('/software/', '/en/software/'),
    ('/traza/', '/en/traza/'),
    ('/soluciones/', '/en/solutions/'),
    *[(f'/soluciones/{es}/', f'/en/solutions/{en}/') for _, es, en, _ in SOLUCIONES],
    ('/clientes/', '/en/customers/'),
    ('/recursos/', '/en/resources/'),
    ('/nosotros/', '/en/about/'),
    ('/contacto/', '/en/contact/'),
    ('/404.html', '/en/404.html'),
]
ES_A_EN = dict(PARES)
EN_A_ES = {en: es for es, en in PARES}


def idioma_de(ruta):
    return 'en' if ruta == '/en/' or ruta.startswith('/en/') else 'es'


def par(ruta):
    """Ruta equivalente en el otro idioma. Los capítulos de los manuales (solo en
    español) apuntan a la portada inglesa del manual."""
    if ruta in ES_A_EN:
        return ES_A_EN[ruta]
    if ruta in EN_A_ES:
        return EN_A_ES[ruta]
    for prod in ('work', 'sales'):
        if ruta.startswith(f'/{prod}/docs/'):
            return f'/en/{prod}/docs/'
    return None


def es_capitulo_manual(ruta):
    return any(ruta.startswith(f'/{p}/docs/') and ruta != f'/{p}/docs/' for p in ('work', 'sales'))


def L(ruta_es, lang):
    """Ruta en el idioma pedido a partir de la española (anclas incluidas)."""
    base, _, ancla = ruta_es.partition('#')
    if lang == 'en':
        base = ES_A_EN.get(base, base)
        if base == '/en/' and ancla == 'contacto':
            ancla = 'contact'
    return base + ('#' + ancla if ancla else '')


# ── Productos ───────────────────────────────────────────────────────────────
PRODUCTOS = [
    # clave, ruta ES, nombre, descripción ES, descripción EN
    ('work', '/work/', 'Zentrix Work', 'El equipo de tienda', 'Store teams'),
    ('sales', '/sales/', 'Zentrix Sales', 'La fuerza de ventas', 'Field sales'),
    ('ai', '/ai/', 'Zentrix AI', 'Inteligencia aplicada', 'Applied intelligence'),
    ('logistica', '/logistics/', 'Zentrix Logistics', 'Despachos y entregas · Próximamente', 'Dispatch and delivery · Coming soon'),
    ('cloud', '/cloud/', 'Zentrix Cloud', 'Infraestructura', 'Infrastructure'),
    ('labs', '/labs/', 'Zentrix Labs', 'Investigación', 'Research'),
    ('software', '/software/', 'Zentrix Software', 'Implementación de Odoo®', 'Odoo® implementation'),
    ('traza', TRAZA_URL, 'Traza', 'Un producto de Zentrix®', 'A Zentrix® product'),
]

# Nombres y líneas de las soluciones (menú, pie, tarjetas)
SOL_TXT = {
    'odoo': {'es': ('Odoo en Venezuela', 'Implementación con la localización del país'),
             'en': ('Odoo in Venezuela', 'Implementation with Venezuelan localization')},
    'software': {'es': ('Desarrollo de software', 'Apps web y móviles a la medida de tu proceso'),
                 'en': ('Software development', 'Web and mobile apps built around your process')},
    'auditoria': {'es': ('Auditoría técnica', 'Diagnóstico, arquitectura y hoja de ruta'),
                  'en': ('Technical audit', 'Diagnosis, architecture and roadmap')},
    'infra': {'es': ('Alta disponibilidad', 'Infraestructura que sigue cuando se va la luz'),
              'en': ('High availability', 'Infrastructure that keeps running through outages')},
    'pagos': {'es': ('Pagos y comercio digital', 'Punto de venta, cajas y pasarelas de pago'),
              'en': ('Payments and digital commerce', 'Point of sale, tills and payment gateways')},
    'vision': {'es': ('Visión computacional', 'Analítica de video en tiempo real'),
               'en': ('Computer vision', 'Real-time video analytics')},
}

SECTORES = {
    'es': [('retail', 'Comercio y tiendas', 'Pedidos, preparación, entrega y caja'),
           ('distribucion', 'Distribución y venta en ruta', 'Vendedores en la calle, cobranza y despachos')],
    'en': [('retail', 'Retail and stores', 'Orders, picking, delivery and checkout'),
           ('distribucion', 'Distribution and route sales', 'Field reps, collections and dispatch')],
}

# Iconos de línea (24×24, trazo currentColor)
ICONOS = {
    'capas': '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 13 9 5 9-5"/><path d="m3 17.5 9 4.5 9-4.5" opacity=".55"/>',
    'codigo': '<path d="m8 8-4 4 4 4"/><path d="m16 8 4 4-4 4"/><path d="m13.5 5-3 14"/>',
    'lupa': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/><path d="m7.8 10.6 2 2 3.6-4"/>',
    'servidor': '<rect x="3.5" y="4" width="17" height="6.5" rx="1.5"/><rect x="3.5" y="13.5" width="17" height="6.5" rx="1.5"/><path d="M7 7.25h.01M7 16.75h.01"/>',
    'tarjeta': '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 9.5h19M6 15h4"/>',
    'ojo': '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    'tienda': '<path d="M4 9.5V20h16V9.5"/><path d="M3 4h18l-1.5 5.5a2.6 2.6 0 0 1-5 0 2.6 2.6 0 0 1-5 0 2.6 2.6 0 0 1-5 0Z"/><path d="M10 20v-5h4v5"/>',
    'camion': '<path d="M2.5 6h11v10h-11z"/><path d="M13.5 9.5h4l3 3.5V16h-7"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'libro': '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5v-15Z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
    'ayuda': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.2a2.6 2.6 0 0 1 5 .9c0 1.7-2.5 2.2-2.5 3.9"/><path d="M12 17.2h.01"/>',
    'escudo': '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6L12 3Z"/><path d="m9 12 2 2 4-4"/>',
    'documento': '<path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8l-5-5Z"/><path d="M14 3v5h5M8.5 13h7M8.5 17h5"/>',
    'correo': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5 12 13l8.5-6.5"/>',
    'personas': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.6-3.4 3-5.5 6-5.5s5.4 2.1 6 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M16.5 14.6c2.4.3 4 2.1 4.5 5.4"/>',
    'estrella': '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3Z"/>',
}


def svg_icono(nombre, clase='icono-linea'):
    return (f'<svg class="{clase}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONOS[nombre]}</svg>')


SVG_EXTERNO = ('<svg class="externo" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
               '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')
SVG_WHATSAPP = ('<svg class="pie__icono" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
                '<path d="M4 20l1.3-3.9A8.5 8.5 0 1 1 8 18.8z"/>'
                '<path d="M9 8.6c0 3.3 3 6.4 6.4 6.4l1.1-1.6-2-1-1 .8a5 5 0 0 1-2.7-2.7l.8-1-1-2z"/></svg>')
SVG_GLOBO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/>'
             '<path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/></svg>')

T = {
    'es': {
        'productos': 'Productos', 'soluciones': 'Soluciones', 'clientes': 'Clientes', 'recursos': 'Recursos',
        'nosotros': 'Nosotros', 'contacto': 'Contacto', 'legal': 'Legal y soporte', 'externo': ' (se abre en otra pestaña)',
        'lema': 'Tecnología para trabajar mejor.', 'suite': 'La suite de Zentrix',
        'manual_work': 'Manual de Zentrix Work', 'manual_sales': 'Manual de Zentrix Sales',
        'privacidad': 'Privacidad', 'soporte': 'Soporte', 'terminos': 'Términos', 'contacto_l': 'Contacto',
        'copy': '© 2026 Zentrix®. Todos los derechos reservados.', 'odoo': 'Odoo® conserva su marca y propiedad.',
        'idioma': 'Idioma', 'nota_es': '', 'principal': 'Principal', 'menu': 'Menú', 'cerrar': 'Cerrar el menú',
        'ver_productos': 'Ver toda la suite', 'ver_soluciones': 'Ver todas las soluciones',
        'por_necesidad': 'Por necesidad', 'por_sector': 'Por sector', 'suite_zentrix': 'Suite Zentrix',
        'marca_asociada': 'Marca asociada', 'aprende': 'Aprende', 'ayuda': 'Ayuda', 'legal_t': 'Legal',
        'llms': 'Zentrix para modelos de IA (llms.txt)', 'centro': 'Centro de recursos',
        'empresa': 'Empresa', 'casos': 'Clientes y casos',
        'soporte_work': 'Soporte de Zentrix Work', 'soporte_sales': 'Soporte de Zentrix Sales',
        'privacidad_terminos': 'Privacidad y términos', 'hablemos': 'Hablemos',
        'lang_es': 'Español', 'lang_en': 'English',
    },
    'en': {
        'productos': 'Products', 'soluciones': 'Solutions', 'clientes': 'Customers', 'recursos': 'Resources',
        'nosotros': 'About', 'contacto': 'Contact', 'legal': 'Legal and support', 'externo': ' (opens in a new tab)',
        'lema': 'Technology to work better.', 'suite': 'The Zentrix suite',
        'manual_work': 'Zentrix Work manual', 'manual_sales': 'Zentrix Sales manual',
        'privacidad': 'Privacy', 'soporte': 'Support', 'terminos': 'Terms', 'contacto_l': 'Contact',
        'copy': '© 2026 Zentrix®. All rights reserved.', 'odoo': 'Odoo® remains the property of its owner.',
        'idioma': 'Language', 'nota_es': ' (in Spanish)', 'principal': 'Main', 'menu': 'Menu', 'cerrar': 'Close menu',
        'ver_productos': 'See the whole suite', 'ver_soluciones': 'See all solutions',
        'por_necesidad': 'By need', 'por_sector': 'By industry', 'suite_zentrix': 'Zentrix suite',
        'marca_asociada': 'Associated brand', 'aprende': 'Learn', 'ayuda': 'Help', 'legal_t': 'Legal',
        'llms': 'Zentrix for AI models (llms.txt)', 'centro': 'Resource center',
        'empresa': 'Company', 'casos': 'Customers and case studies',
        'soporte_work': 'Zentrix Work support', 'soporte_sales': 'Zentrix Sales support',
        'privacidad_terminos': 'Privacy and terms', 'hablemos': "Let's talk",
        'lang_es': 'Español', 'lang_en': 'English',
    },
}


def esc(s):
    return html.escape(s, quote=False)
