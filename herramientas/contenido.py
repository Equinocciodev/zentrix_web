"""Contenido de las páginas que genera `generar.py`: soluciones, clientes, recursos,
nosotros, contacto y la portada inglesa de los manuales.

Origen: los servicios, la filosofía, las alianzas y el equipo vienen de eqnio.com
(Equinoccio, hoy Zentrix), reescritos con el tono de Zentrix. Los clientes son solo lo que
eqnio.com ya publicaba y lo que este sitio ya cuenta. No hay cifras ni testimonios.
"""
from sitio import SOLUCIONES, SOL_TXT

# ── Soluciones ──────────────────────────────────────────────────────────────
SOL = {
    'odoo': {
        'producto': 'software',
        'tags': ['Odoo®', 'ERP', 'Localización Venezuela', 'Trazabilidad'],
        'es': {
            'titulo': 'Implementación de Odoo® con la localización de Venezuela',
            'corto': 'Odoo en Venezuela',
            'lead': 'Digitalizamos tu empresa desde adentro: Odoo® adaptado a la realidad fiscal y operativa del país, con los procesos unificados y cada recurso bajo control.',
            'incluye': [
                ('Primero, tus procesos', 'Vemos cómo trabaja de verdad tu empresa antes de configurar nada.'),
                ('Localización venezolana', 'Libros, retenciones, numeración de documentos y la doble moneda, como exige la ley.'),
                ('Todo en un sistema', 'Inventario, compras, ventas y tesorería con trazabilidad de punta a punta.'),
                ('Tu gente, al día', 'Capacitamos a quienes lo van a usar todos los días, y nos quedamos para acompañarlos.'),
            ],
        },
        'en': {
            'titulo': 'Odoo® implementation with Venezuelan localization',
            'corto': 'Odoo in Venezuela',
            'lead': 'We digitize your company from the inside: Odoo® adapted to Venezuela’s tax and operating reality, with unified processes and every resource under control.',
            'incluye': [
                ('Your processes first', 'We look at how your company really works before we configure anything.'),
                ('Venezuelan localization', 'Tax books, withholdings, document numbering and dual currency, as the law requires.'),
                ('One system for everything', 'Inventory, purchasing, sales and treasury, traceable end to end.'),
                ('Your people, up to speed', 'We train the people who will use it every day, and we stay to support them.'),
            ],
        },
    },
    'software': {
        'producto': 'labs',
        'tags': ['Flutter', 'Next.js', 'FastAPI', 'UI/UX'],
        'es': {
            'titulo': 'Desarrollo de software a la medida',
            'corto': 'Desarrollo de software',
            'lead': 'De la idea a la pantalla: diseño, arquitectura y desarrollo en un mismo equipo, sin perder contexto entre fases. Producto que escala desde el primer día.',
            'incluye': [
                ('Apps web y móviles', 'Construidas alrededor del proceso de tu negocio, no al revés.'),
                ('Diseño en el mismo equipo', 'Quien diseña la experiencia trabaja al lado de quien la programa.'),
                ('Arquitectura para crecer', 'Para sumar usuarios y funciones sin rehacer el sistema desde cero.'),
                ('Lo ves funcionando', 'Entregas continuas: el producto se prueba en tus manos, no en presentaciones.'),
            ],
        },
        'en': {
            'titulo': 'Custom software development',
            'corto': 'Software development',
            'lead': 'From idea to screen: design, architecture and development in one team, with no context lost between phases. A product that scales from day one.',
            'incluye': [
                ('Web and mobile apps', 'Built around your business process, not the other way around.'),
                ('Design in the same team', 'The people who design the experience sit next to the people who build it.'),
                ('Architecture that grows', 'Add users and features without rebuilding the system from scratch.'),
                ('See it working', 'Continuous delivery: you try the product in your own hands, not in slide decks.'),
            ],
        },
    },
    'auditoria': {
        'producto': None,
        'tags': ['Auditoría', 'Arquitectura', 'Hoja de ruta', 'Stack'],
        'tags_en': ['Audit', 'Architecture', 'Roadmap', 'Stack'],
        'es': {
            'titulo': 'Auditoría técnica y arquitectura de sistemas',
            'corto': 'Auditoría técnica',
            'lead': 'No vendemos horas: te damos dirección. Auditoría, hoja de ruta y decisiones de tecnología para que sepas qué construir, en qué orden y por qué.',
            'incluye': [
                ('Diagnóstico honesto', 'Cómo está tu sistema hoy y cuánto te cuesta mantenerlo.'),
                ('Hoja de ruta con motivos', 'Qué hacer primero y por qué; no una lista de deseos.'),
                ('Decisiones argumentadas', 'Qué tecnología usar, explicado para que puedas decidir.'),
                ('Segunda opinión', 'Revisamos presupuestos y propuestas de terceros antes de que firmes.'),
            ],
        },
        'en': {
            'titulo': 'Technical audit and systems architecture',
            'corto': 'Technical audit',
            'lead': 'We don’t sell hours; we give you direction. An audit, a roadmap and technology decisions so you know what to build, in what order and why.',
            'incluye': [
                ('An honest diagnosis', 'Where your system stands today and what it costs you to keep it running.'),
                ('A roadmap with reasons', 'What to do first and why, not a wish list.'),
                ('Reasoned decisions', 'Which technology to use, explained so you can decide.'),
                ('A second opinion', 'We review third-party quotes and proposals before you sign.'),
            ],
        },
    },
    'infra': {
        'producto': 'cloud',
        'tags': ['Docker', 'Kubernetes', 'Zero Trust', 'Self-hosted'],
        'es': {
            'titulo': 'Infraestructura de alta disponibilidad',
            'corto': 'Alta disponibilidad',
            'lead': 'Sistemas pensados para cuando se va la luz: servidores propios o en la nube, acceso Zero Trust y datos que no se pierden. Tu operación no se detiene.',
            'incluye': [
                ('Servidores y respaldos', 'Propios o en la nube, con respaldos que se comprueban.'),
                ('Zero Trust', 'Cada acceso se autentica; nada se da por supuesto.'),
                ('Fallos que no se contagian', 'Contenedores y orquestación para que un error no arrastre al resto.'),
                ('Hecho para Venezuela', 'Diseñado para cortes de energía y de conexión.'),
            ],
        },
        'en': {
            'titulo': 'High-availability infrastructure',
            'corto': 'High availability',
            'lead': 'Systems designed for when the power goes out: your own servers or the cloud, Zero Trust access and data that is never lost. Your operation keeps going.',
            'incluye': [
                ('Servers and backups', 'On-premises or in the cloud, with backups that are actually tested.'),
                ('Zero Trust', 'Every access is authenticated; nothing is taken for granted.'),
                ('Failures that stay contained', 'Containers and orchestration so one fault doesn’t drag down the rest.'),
                ('Built for Venezuela', 'Designed for power and connectivity outages.'),
            ],
        },
    },
    'pagos': {
        'producto': 'work',
        'tags': ['Punto de venta', 'Cajas', 'Pasarelas de pago', 'Blockchain'],
        'tags_en': ['Point of sale', 'Tills', 'Payment gateways', 'Blockchain'],
        'es': {
            'titulo': 'Pagos y comercio digital',
            'corto': 'Pagos y comercio digital',
            'lead': 'Del punto de venta físico a la transacción en línea: cajas, pasarelas de pago, comprobantes electrónicos y, cuando el proyecto lo pide, contratos inteligentes en blockchain.',
            'incluye': [
                ('Punto de venta integrado', 'La caja de la tienda conectada con el resto de tu sistema.'),
                ('Cajas bajo control', 'Turnos, aperturas, cierres y arqueos que cuadran.'),
                ('Pasarelas de pago', 'Cobros con conciliación automática.'),
                ('Comprobantes digitales', 'Tickets y comprobantes electrónicos para tu cliente.'),
            ],
        },
        'en': {
            'titulo': 'Payments and digital commerce',
            'corto': 'Payments and digital commerce',
            'lead': 'From the physical point of sale to the online transaction: tills, payment gateways, electronic receipts and, when the project calls for it, smart contracts on blockchain.',
            'incluye': [
                ('An integrated point of sale', 'Your store’s till connected to the rest of your system.'),
                ('Tills under control', 'Shifts, openings, closings and cash counts that add up.'),
                ('Payment gateways', 'Payments with automatic reconciliation.'),
                ('Digital receipts', 'Electronic tickets and receipts for your customers.'),
            ],
        },
    },
    'vision': {
        'producto': 'ai',
        'tags': ['Visión computacional', 'Analítica de video', 'Biometría', 'Tiempo real'],
        'tags_en': ['Computer vision', 'Video analytics', 'Biometrics', 'Real time'],
        'es': {
            'titulo': 'Visión computacional y analítica de video',
            'corto': 'Visión computacional',
            'lead': 'Inteligencia artificial que cuida, no que vigila: analítica sobre tus cámaras para proteger personas y espacios en tiempo real, con criterio humano.',
            'incluye': [
                ('Tus cámaras de siempre', 'Analítica de video sobre las cámaras que ya tienes.'),
                ('En el momento', 'Detección de eventos en tiempo real, no revisión de grabaciones después.'),
                ('Acceso biométrico', 'Control de acceso por reconocimiento.'),
                ('Avisos a quien actúa', 'Las alertas llegan a la persona que tiene que hacer algo.'),
            ],
        },
        'en': {
            'titulo': 'Computer vision and video analytics',
            'corto': 'Computer vision',
            'lead': 'AI that looks after people rather than watching them: analytics on your cameras to protect people and spaces in real time, with human judgment.',
            'incluye': [
                ('The cameras you already have', 'Video analytics on your existing cameras.'),
                ('In the moment', 'Real-time event detection, not reviewing footage after the fact.'),
                ('Biometric access', 'Access control by recognition.'),
                ('Alerts to whoever acts', 'Alerts reach the person who needs to do something about it.'),
            ],
        },
    },
}

# ── Sectores (lo que de verdad hacemos hoy) ─────────────────────────────────
SECTOR_TXT = {
    'retail': {
        'es': ('Comercio y tiendas',
               'El pedido entra, el equipo de tienda lo prepara y lo entrega, y la caja cuadra al cierre.',
               [('/work/', 'Zentrix Work', 'avisa al equipo de tienda, guía la preparación con el escáner y registra la entrega.'),
                ('/soluciones/pagos-y-comercio-digital/', 'Pagos y comercio digital', 'punto de venta, cajas y pasarelas de pago.'),
                ('/soluciones/odoo-venezuela/', 'Odoo® en Venezuela', 'inventario, ventas y tesorería con la localización del país.')]),
        'en': ('Retail and stores',
               'The order comes in, your store team picks and delivers it, and the till balances at closing.',
               [('/work/', 'Zentrix Work', 'alerts your store team, guides picking with the scanner and records the delivery.'),
                ('/soluciones/pagos-y-comercio-digital/', 'Payments and digital commerce', 'point of sale, tills and payment gateways.'),
                ('/soluciones/odoo-venezuela/', 'Odoo® in Venezuela', 'inventory, sales and treasury with Venezuelan localization.')]),
    },
    'distribucion': {
        'es': ('Distribución y venta en ruta',
               'Tus vendedores están en la calle, a veces sin señal, y la oficina necesita saber qué se vendió y qué se cobró.',
               [('/sales/', 'Zentrix Sales', 'pedidos, visitas y cobranza aunque no haya señal, directo a tu sistema.'),
                ('/logistics/', 'Zentrix Logistics', 'despachos, rutas y entregas en un mismo lugar (próximamente).'),
                ('/soluciones/odoo-venezuela/', 'Odoo® en Venezuela', 'el sistema de gestión que recibe los pedidos y los cobros.')]),
        'en': ('Distribution and route sales',
               'Your reps are out in the field, sometimes without signal, and the office needs to know what was sold and collected.',
               [('/sales/', 'Zentrix Sales', 'orders, visits and collections even without signal, straight into your system.'),
                ('/logistics/', 'Zentrix Logistics', 'dispatch, routes and deliveries in one place (coming soon).'),
                ('/soluciones/odoo-venezuela/', 'Odoo® in Venezuela', 'the management system that receives orders and payments.')]),
    },
}

# ── Clientes y aliados (solo lo que eqnio.com publicaba) ────────────────────
CASOS = {
    'es': [
        ('Grupo Leiros', 'Distribución de licores · Venezuela',
         'Grupo Leiros es aliado de Zentrix desde su origen, cuando todavía nos llamábamos Equinoccio: aporta respaldo institucional, estructura legal y alcance comercial. Su operación de distribución es donde nacieron nuestras apps.',
         [('/sales/', 'Zentrix Sales'), ('/soluciones/odoo-venezuela/', 'Odoo® en Venezuela')]),
        ('GUUAO', 'Venezuela',
         'GUUAO LLC publica Zentrix Work y Zentrix Sales en las tiendas de aplicaciones. Zentrix Work nació para su equipo de tienda: el pedido suena en el bolsillo, se prepara con el escáner y se entrega con todo registrado.',
         [('/work/', 'Zentrix Work'), ('/sales/', 'Zentrix Sales')]),
    ],
    'en': [
        ('Grupo Leiros', 'Beverage distribution · Venezuela',
         'Grupo Leiros has been a Zentrix ally since the beginning, back when we were still called Equinoccio: it brings institutional backing, legal structure and commercial reach. Its distribution operation is where our apps were born.',
         [('/sales/', 'Zentrix Sales'), ('/soluciones/odoo-venezuela/', 'Odoo® in Venezuela')]),
        ('GUUAO', 'Venezuela',
         'GUUAO LLC publishes Zentrix Work and Zentrix Sales on the app stores. Zentrix Work was born for its store team: the order buzzes in their pocket, gets picked with the scanner and is delivered with everything on record.',
         [('/work/', 'Zentrix Work'), ('/sales/', 'Zentrix Sales')]),
    ],
}

ALIADOS = [
    # nombre, rubro ES, rubro EN (tal como los presentaba eqnio.com)
    ('Grupo Leiros', 'Distribución de licores', 'Beverage distribution'),
    ('GUUAO', '', ''),
    ('BrandIA AI', 'Investigación aplicada y agentes de IA', 'Applied research and AI agents'),
    ('Hetzner', 'Infraestructura en la nube', 'Cloud infrastructure'),
    ('Odoo', 'ERP y operaciones', 'ERP and operations'),
    ('Diageo', '', ''),
    ('Embajada de España en Nueva Esparta', 'Nueva Esparta, Venezuela', 'Nueva Esparta, Venezuela'),
    ('Sambil Margarita', '', ''),
    ('Hoteles Sun Sol', 'Hotelería · Margarita', 'Hospitality · Margarita'),
    ('Movilmax', '', ''),
    ('Starlink', 'Conectividad satelital', 'Satellite connectivity'),
]

# ── Equipo (fotos y cargos tal cual en eqnio.com) ───────────────────────────
EQUIPO = [
    ('lenin', 'Lenin Acosta', 'Supervisor de Desarrollo',
     'Coordina el ciclo de desarrollo y traduce los requerimientos en entregas concretas y a tiempo.',
     'Runs the development cycle and turns requirements into concrete, on-time deliveries.'),
    ('juan', 'Juan Leiros', 'CTO · Jefe de Innovación',
     'Visión técnica y estratégica del grupo: marca la dirección tecnológica de Zentrix y de Grupo Leiros.',
     'The group’s technical and strategic vision: he sets the technology direction for Zentrix and Grupo Leiros.'),
    ('enmanuel', 'Enmanuel Gamero', 'Tech & Infrastructure Manager',
     'Diseña y opera la columna vertebral técnica: infraestructura que no falla y sistemas que escalan.',
     'Designs and runs the technical backbone: infrastructure that doesn’t fail and systems that scale.'),
    ('hugo', 'Hugo Mendoza', 'FinOps · Data Engineer',
     'Construye las tuberías por donde corre el dato y vigila lo que cuesta moverlo, del origen al modelo que consulta el negocio.',
     'Builds the pipelines data runs through and keeps an eye on what it costs to move, from the raw source to the model the business queries.'),
    ('miguel', 'Miguel Coronel', 'Coordinador de Soporte',
     'Primer punto de contacto técnico: resuelve con criterio y escala solo lo que merece escalar.',
     'The first technical point of contact: he solves with judgment and escalates only what deserves it.'),
    ('adrian', 'Adrian Alves', 'Backend Developer · Financial Systems',
     'Construye la lógica financiera que corre por debajo: APIs robustas y transacciones sin fisuras.',
     'Builds the financial logic running underneath: robust APIs and seamless transactions.'),
    ('celmira', 'Celmira Genes', 'Odoo Expert · Consultora',
     'Analiza, implementa y optimiza Odoo a la medida del negocio: convierte procesos complejos en flujos que funcionan.',
     'Analyzes, implements and tunes Odoo to fit the business, turning complex processes into flows that work.'),
    ('moises', 'Moisés Cárdenas', 'Ingeniero de Sistemas · UX',
     'Analiza los procesos del cliente, desarrolla la solución que los soporta y diseña la interfaz con la que su gente trabaja cada día.',
     'Analyzes the customer’s processes, builds the solution behind them and designs the interface their people use every day.'),
    ('alejandro', 'Alejandro Larez', 'Planificación · Logística · Estrategia',
     'Traza el plan antes de empezar: alcance, tiempos y recursos, y mantiene la ejecución alineada con lo que el negocio necesita.',
     'Draws up the plan before work starts (scope, timing and resources) and keeps execution aligned with what the business needs.'),
]
