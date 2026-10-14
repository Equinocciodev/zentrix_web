# SEO de zentrix.company

Cómo está montado el SEO del sitio, qué palabra clave trabaja cada página y qué falta hacer fuera del repositorio. El estado real se comprueba siempre sobre el sitio **publicado** con `herramientas/verificar_seo.py`.

## Herramientas

| Script | Qué hace | Cuándo |
|---|---|---|
| `herramientas/seo.py` | Title, description, `og:title`/`og:description`/`og:image:alt`, `twitter:title`/`twitter:description` y el JSON-LD de cada página (bloque `<!-- seo -->` antes de `</head>`). La tabla `PAGINAS` es la fuente de los títulos y descripciones. | Lo aplica `generar.py` como último paso; `--check` comprueba, `--tabla` imprime la tabla de abajo. |
| `herramientas/generar.py` | Cabecera, pie, páginas de sección, `hreflang` y `og:locale:alternate`, `llms.txt`, redirecciones (dueño: estructura y multiidioma). | Tras cualquier cambio de contenido: `python3 herramientas/generar.py`. |
| `herramientas/sitemap.py` | `sitemap.xml` desde el HTML: páginas indexables (sin `noindex` ni redirección), `loc` = canonical, `lastmod` del último commit de cada archivo y `xhtml:link` de sus `hreflang`. | En cada despliegue (workflow de Pages, con `fetch-depth: 0`) y desde `generar.py` si cambian las URL. |
| `herramientas/llms.py` | `llms-full.txt`: el texto visible de cada página indexable, agrupado. `llms.txt` (el índice) lo escribe `generar.py` y enlaza a este. | En cada despliegue y a mano. |
| `herramientas/verificar_seo.py` | Verificación del sitio publicado, página por página y en los dos idiomas. Sale con 1 si algo falla. | Antes de fusionar (contra una copia local) y después de cada despliegue (contra producción). |

```sh
python3 herramientas/generar.py                      # aplica estructura + SEO
python3 herramientas/verificar_seo.py --informe ~/Downloads/zentrix/web/seo/verificacion_seo.md
```

## Palabras clave por página

Una palabra clave principal por página, sin canibalizar: `/soluciones/odoo-venezuela/` trabaja «implementación de Odoo en Venezuela» y `/software/` «consultoría e integración de Odoo»; `/work/` lleva «app para el equipo de tienda y reparto» y `/logistics/` «gestión de despachos y entregas»; los manuales trabajan colas largas de su tema. Las legales no tienen palabra clave (—). Formato del title: «Producto — beneficio | Zentrix», sin repetir «| Zentrix» cuando el producto ya se llama Zentrix; ≤ 60 caracteres. Description: 140–160 caracteres, con contenido real de la página.

Otras búsquedas que cubren las páginas como secundarias: «partner/consultoría Odoo» y «localización venezolana Odoo» (solución Odoo y Zentrix Software); «app para vendedores de campo», «preventa y cobranza», «app de ventas para Odoo» (Zentrix Sales, que tiene integración nativa con Odoo® 17, 18 y 19); «app para repartidores» (manual `reparto.html`); «trazabilidad» (Traza); «field sales app» (inglés).

**No usadas, a propósito:** «partner Odoo» como afirmación, «facturación digital SENIAT Odoo» e «IGTF Odoo». El sitio no dice que Zentrix sea partner oficial de Odoo ni menciona SENIAT o IGTF (la solución de Odoo habla de libros, retenciones, numeración y doble moneda). Si Victor confirma esos datos, se añaden a `/soluciones/odoo-venezuela/` y se actualiza su title y description.

| Página | Palabra clave principal | Title | Description | Schema |
|---|---|---|---|---|
| `/ai/` | inteligencia artificial para empresas | Zentrix AI — Inteligencia artificial para empresas | Zentrix AI conecta el conocimiento y los sistemas de tu empresa con agentes de IA y asistentes para consultar, analizar y actuar, con permisos por rol. | Service, BreadcrumbList |
| `/clientes/` | clientes y casos de Zentrix | Clientes — Casos en distribución y comercio \| Zentrix | Grupo Leiros y GUUAO usan las apps de Zentrix cada día en distribución y comercio en Venezuela. Conoce sus casos y las empresas que nos acompañan. | BreadcrumbList |
| `/cloud/` | hospedaje, monitoreo y respaldos para empresas | Zentrix Cloud — Hospedaje, monitoreo y respaldos | Zentrix Cloud se ocupa del hospedaje, el monitoreo y los respaldos de tus aplicaciones y tus datos, para que tu operación siga en marcha sin cuidar servidores. | Service, BreadcrumbList |
| `/contacto/` | contacto Zentrix | Contacto — Proyectos, demostraciones y soporte \| Zentrix | Escribe a hola@zentrix.company por proyectos y demostraciones, a soporte@zentrix.company por soporte, o por WhatsApp. Te responde una persona. | BreadcrumbList |
| `/` | software y apps para empresas en Venezuela | Zentrix — Software y apps para empresas en Venezuela | Tecnología para trabajar mejor: apps para tu equipo de tienda y tu fuerza de ventas, Odoo® con localización venezolana y software a la medida. | Organization, WebSite |
| `/labs/` | prototipos y validación de productos | Zentrix Labs — Prototipos y validación de productos | En Zentrix Labs investigamos tu reto, construimos prototipos y los validamos antes de convertirlos en herramientas para tu equipo. Cuéntanos tu idea. | Service, BreadcrumbList |
| `/logistics/` | gestión de despachos y entregas | Zentrix Logistics — Gestión de despachos y entregas | Zentrix Logistics, próximamente: despachos, rutas, entregas y gestión de incidencias en un mismo lugar, para cumplir lo que prometiste a tus clientes. | Service, BreadcrumbList |
| `/nosotros/` | empresa de software en Isla Margarita, Venezuela | Nosotros — Ingeniería en Isla Margarita \| Zentrix | Zentrix es la nueva marca de Equinoccio (EQNIO), un equipo de ingeniería, IA y producto con base en Isla Margarita, Venezuela. Conoce al equipo. | BreadcrumbList |
| `/privacidad/` | — | Privacidad del sitio — Zentrix | Qué mide zentrix.company y con qué herramienta, sin publicidad, y cómo retirar el consentimiento de cookies. Las apps tienen su propia política. | BreadcrumbList |
| `/recursos/` | manuales y documentación de Zentrix | Recursos — Manuales, soporte y documentación \| Zentrix | Manuales de Zentrix Work y Zentrix Sales, soporte, privacidad y términos de cada app, y documentación para desarrolladores y modelos de IA, en un solo lugar. | BreadcrumbList |
| `/sales/contacto/` | demostración de app de ventas | Contacto — Zentrix Sales | Pide una demostración de Zentrix Sales con tus datos: cuéntanos cómo vende hoy tu equipo. O escríbenos por correo, teléfono o WhatsApp, sin compromiso. | BreadcrumbList |
| `/sales/docs/actividad.html` | — | Tus pedidos y tu actividad — Manual de Zentrix Sales | La pestaña Actividad de Zentrix Sales: los borradores en «Abiertos», qué significa cada estado de un pedido, tus visitas y tus devoluciones. | BreadcrumbList |
| `/sales/docs/catalogo.html` | catálogo de productos en la app de ventas | El catálogo — Manual de Zentrix Sales | Buscar un producto en Zentrix Sales por nombre, código o código de barras, usar el escáner, filtrar, elegir la tarifa y compartir por WhatsApp. | BreadcrumbList |
| `/sales/docs/clientes.html` | alta de clientes desde la app de ventas | Clientes nuevos y correcciones — Manual de Zentrix Sales | Cómo proponer un cliente nuevo desde Zentrix Sales y sugerir la corrección de uno que ya tienes: los pasos, los recaudos y cómo queda la solicitud. | BreadcrumbList |
| `/sales/docs/cobrar.html` | registrar cobranza en la calle | Cobrarle a un cliente — Manual de Zentrix Sales | Cómo registrar un cobro en Zentrix Sales: banco, monto, referencia y comprobante, aplicarlo a las facturas y seguir el estado de la solicitud. | BreadcrumbList |
| `/sales/docs/conversacion.html` | — | Hablar con la oficina — Manual de Zentrix Sales | Cómo hablar con la oficina desde Zentrix Sales: la conversación de un pedido, una factura, una cobranza o un cliente, con notas internas, menciones y adjuntos. | BreadcrumbList |
| `/sales/docs/dudas.html` | — | Dudas rápidas — Manual de Zentrix Sales | Lo que más se pregunta de Zentrix Sales, en una o dos frases: el PIN, el permiso de ubicación, los precios que cambian, los avisos y el punto de sincronización. | FAQPage, BreadcrumbList |
| `/sales/docs/entrar.html` | entrar a la app de ventas | Entrar y sincronizar — Manual de Zentrix Sales | Cómo entrar a Zentrix Sales la primera vez: el subdominio de tu empresa, tu correo y el PIN. Y por qué conviene sincronizar antes de salir a la calle. | BreadcrumbList |
| `/sales/docs/facturas.html` | cartera de cuentas por cobrar | Facturas y lo que te deben — Manual de Zentrix Sales | Cómo leer la cartera en Zentrix Sales: «TE DEBEN», «VENCIDO» y «EN REVISIÓN», las tarjetas, las etiquetas, el compromiso de pago y la moneda. | BreadcrumbList |
| `/sales/docs/` | manual de app para vendedores | Manual del vendedor — Zentrix Sales | Cómo se usa Zentrix Sales en la calle, pantalla por pantalla: la ruta, la visita, el pedido, la cobranza y qué pasa cuando no hay señal. Versión 5.2.24. | BreadcrumbList |
| `/sales/docs/inicio.html` | — | Tu Inicio — Manual de Zentrix Sales | La pantalla que más vas a ver en Zentrix Sales: el saludo, los avisos, tu empresa, las tasas del día, el bloque «Hoy» y los ocho accesos rápidos. | BreadcrumbList |
| `/sales/docs/ruta.html` | — | La ruta del día — Manual de Zentrix Sales | Cómo planificar y recorrer tu ruta en Zentrix Sales: asignar clientes a un día, ordenar las paradas por cercanía, navegar y quitar a alguien del día. | BreadcrumbList |
| `/sales/docs/sin-internet.html` | app de ventas sin internet | Trabajar sin internet — Manual de Zentrix Sales | En Zentrix Sales nada se pierde sin señal: qué significa cada color del punto de sincronización y qué hacer si algo dice «No se pudo enviar». | BreadcrumbList |
| `/sales/docs/visita.html` | visita al cliente paso a paso | La visita paso a paso — Manual de Zentrix Sales | Los ocho pasos de una visita en Zentrix Sales: check-in, inventario, pedido, fotos, devoluciones, notas, firma y check-out, con lo que conviene saber. | BreadcrumbList |
| `/sales/en/contact.html` | field sales app demo | Contact — Zentrix Sales | Request a Zentrix Sales demo on your own data: tell us how your team sells today. Or write to us by email, phone or WhatsApp, no strings attached. | BreadcrumbList |
| `/sales/en/` | field sales app | Zentrix Sales — Field sales app for Android and iPhone | Zentrix Sales is the field sales app for Android and iPhone: route, orders, collections and proof of visit for your reps, with or without a signal. | SoftwareApplication, BreadcrumbList |
| `/sales/en/privacy.html` | — | Privacy policy — Zentrix Sales | What data Zentrix Sales, the field sales app, collects, why, where it is stored, how long it is kept and how to exercise your rights over it. | BreadcrumbList |
| `/sales/en/support.html` | — | Support — Zentrix Sales | Zentrix Sales support: a person replies in under one business day by email, phone or WhatsApp. And how to request access to or deletion of your data. | BreadcrumbList |
| `/sales/en/terms.html` | — | Terms of service — Zentrix Sales | Terms of service of Zentrix Sales, the field sales app for Android and iPhone: who contracts it, who uses it every day and which rules apply. | BreadcrumbList |
| `/sales/` | app de fuerza de ventas | Zentrix Sales — App de fuerza de ventas y cobranza | Zentrix Sales, app de fuerza de ventas para Android y iPhone: ruta, visitas, pedidos y cobranza de tus vendedores de campo, con o sin señal, conectada a Odoo®. | SoftwareApplication, BreadcrumbList |
| `/sales/privacidad/` | — | Política de privacidad — Zentrix Sales | Qué datos recoge Zentrix Sales, la app de fuerza de ventas, para qué, dónde se almacenan, cuánto tiempo se conservan y cómo ejercer tus derechos. | BreadcrumbList |
| `/sales/soporte/` | — | Soporte — Zentrix Sales | Soporte de Zentrix Sales: te contesta una persona en español en menos de un día hábil, por correo, teléfono o WhatsApp. Y cómo pedir tus datos o borrarlos. | BreadcrumbList |
| `/sales/terminos/` | — | Términos de servicio — Zentrix Sales | Términos de servicio de Zentrix Sales, la app de fuerza de ventas de campo para Android y iPhone: quién la contrata, quién la usa y qué reglas aplican. | BreadcrumbList |
| `/software/` | consultoría e integración de Odoo | Zentrix Software — Consultoría e integración de Odoo | Zentrix Software implementa, configura e integra Odoo® con tus otros sistemas y con Zentrix Work y Zentrix Sales: del diagnóstico a la adopción de tu equipo. | Service, BreadcrumbList |
| `/soluciones/auditoria-tecnica/` | auditoría técnica de software | Auditoría técnica y arquitectura de sistemas \| Zentrix | No vendemos horas: te damos dirección. Auditoría, hoja de ruta y decisiones de tecnología para que sepas qué construir, en qué orden y por qué. | Service, BreadcrumbList |
| `/soluciones/desarrollo-de-software/` | desarrollo de software a la medida | Desarrollo de software a la medida \| Zentrix | Desarrollo de software a la medida: apps web y móviles construidas alrededor de tu proceso, con diseño, arquitectura y desarrollo en un mismo equipo. | Service, BreadcrumbList |
| `/soluciones/` | soluciones de software para empresas | Soluciones — Odoo, software e infraestructura \| Zentrix | Odoo® en Venezuela, software a la medida, auditoría técnica, infraestructura de alta disponibilidad, pagos y visión computacional, con el equipo de Zentrix. | BreadcrumbList |
| `/soluciones/infraestructura-alta-disponibilidad/` | infraestructura de alta disponibilidad | Infraestructura de alta disponibilidad \| Zentrix | Sistemas pensados para cuando se va la luz: servidores propios o en la nube, acceso Zero Trust y datos que no se pierden. Tu operación no se detiene. | Service, BreadcrumbList |
| `/soluciones/odoo-venezuela/` | implementación de Odoo en Venezuela | Implementación de Odoo en Venezuela \| Zentrix | Implementación de Odoo® con la localización de Venezuela: libros, retenciones, numeración de documentos y doble moneda, con tu equipo capacitado. | Service, BreadcrumbList |
| `/soluciones/pagos-y-comercio-digital/` | pasarelas de pago y punto de venta | Pagos y comercio digital — Punto de venta \| Zentrix | Pagos y comercio digital: punto de venta integrado, cajas que cuadran, pasarelas de pago con conciliación automática y comprobantes electrónicos. | Service, BreadcrumbList |
| `/soluciones/vision-computacional/` | visión computacional y analítica de video | Visión computacional y analítica de video \| Zentrix | Inteligencia artificial que cuida, no que vigila: analítica sobre tus cámaras para proteger personas y espacios en tiempo real, con criterio humano. | Service, BreadcrumbList |
| `/traza/` | trazabilidad de documentos, productos y activos | Traza — Trazabilidad de documentos, productos y activos | Traza, un producto de Zentrix: trazabilidad de documentos, productos y activos con identidad única, responsables, evidencias e historial completo. | Service, BreadcrumbList |
| `/work/docs/ajustes.html` | — | Ajustes — Manual de Zentrix Work | Los ajustes de Zentrix Work: probar una llamada, vibrar y sonar al trabajar, el flash en la llamada, el tema oscuro o claro y los permisos de la app. | BreadcrumbList |
| `/work/docs/devoluciones.html` | — | Recibir una devolución — Manual de Zentrix Work | Cómo se recibe una devolución en Zentrix Work: contar lo que llegó sin pasarse de lo autorizado, la foto obligatoria y la nota si la cuenta no cuadra. | BreadcrumbList |
| `/work/docs/dudas.html` | — | Dudas rápidas — Manual de Zentrix Work | Las preguntas más comunes de los operadores de Zentrix Work, resueltas en dos líneas: no suenan los pedidos, olvidé mi PIN, el servidor y el turno. | FAQPage, BreadcrumbList |
| `/work/docs/entrar.html` | — | Entrar: la primera vez y cada día — Manual de Zentrix Work | Cómo se entra a Zentrix Work: el servidor, el correo y la contraseña una sola vez; después, con tu PIN o tu huella. Y qué hacer si olvidas el PIN. | BreadcrumbList |
| `/work/docs/entregar.html` | — | Entregar en la tienda — Manual de Zentrix Work | Cómo se entrega un pedido en Zentrix Work: validar el código de retiro, leer los bultos, la foto de la prueba y verificar la edad en pedidos con licor. | BreadcrumbList |
| `/work/docs/` | manual del operador de tienda | Manual del operador — Zentrix Work | Cómo se usa Zentrix Work en la tienda, pantalla a pantalla: entrar, encender el turno, atender la llamada, preparar, entregar, repartir o recibir devoluciones. | BreadcrumbList |
| `/work/docs/llamada.html` | — | La llamada — Manual de Zentrix Work | Cuando hay trabajo, Zentrix Work suena como una llamada aunque la pantalla esté apagada. Tienes 60 segundos para tomarla deslizando o decir «No puedo». | BreadcrumbList |
| `/work/docs/permisos.html` | — | Permisos y sonido — Manual de Zentrix Work | Qué permisos pide Zentrix Work y para qué: avisos, ubicación solo en turno y cámara opcional. Y cómo comprobar que tu teléfono de verdad va a sonar. | BreadcrumbList |
| `/work/docs/preparar.html` | — | Preparar un pedido — Manual de Zentrix Work | Cómo se prepara un pedido en Zentrix Work: comenzar, escanear, marcar lo que no hay, preguntar al cliente, contar los bultos, ubicarlos en el rack y validar. | BreadcrumbList |
| `/work/docs/reparto.html` | app para repartidores | Reparto a domicilio — Manual de Zentrix Work | Cómo se carga el viaje en la tienda, cómo se ordenan las paradas, cómo se navega, se cobra en la puerta y qué hacer si no se puede entregar. | BreadcrumbList |
| `/work/docs/tu-dia.html` | — | Tu día y tu desempeño — Manual de Zentrix Work | Qué muestra «Mi trabajo» en Zentrix Work: lo que cerraste hoy o esta semana, cuánto fue a tiempo, tu ritmo de trabajo y tu nivel como operador. | BreadcrumbList |
| `/work/docs/turno.html` | — | El turno — Manual de Zentrix Work | Cómo se enciende el turno en Zentrix Work: elegir tienda y tareas, deslizar para encender, pedir una pausa, apagar, y cuándo el turno se apaga solo. | BreadcrumbList |
| `/work/` | app para el equipo de tienda y reparto | Zentrix Work — App para el equipo de tienda y reparto | Zentrix Work, la app Android del equipo de tienda: el trabajo llega al teléfono para preparar pedidos, entregar, repartir y recibir devoluciones en su turno. | SoftwareApplication, BreadcrumbList |
| `/work/privacidad/` | — | Política de privacidad — Zentrix Work | Qué datos trata Zentrix Work, la app del equipo de tienda, para qué, dónde se guardan, cuánto tiempo se conservan y cómo pedir su eliminación. | BreadcrumbList |
| `/work/soporte/` | — | Soporte — Zentrix Work | Soporte de Zentrix Work, la app del equipo de tienda: preguntas frecuentes, cómo contactarnos y cómo eliminar tu cuenta o tus datos de la app. | BreadcrumbList |
| `/work/terminos/` | — | Términos de uso — Zentrix Work | Términos de uso de Zentrix Work, la app Android del equipo de tienda: quién puede usarla, cómo se da la cuenta de operador y qué reglas aplican. | BreadcrumbList |

## Schema por plantilla

| Plantilla | JSON-LD |
|---|---|
| Portada (`/`, `/en/`) | `Organization` (nombre, logo 512×512, url, eslogan, `sameAs`: traza.technology, Google Play de Zentrix Work y Zentrix Sales, App Store de Zentrix Sales; `contactPoint`: ventas hola@zentrix.company + teléfono/WhatsApp +58 412-346 9712, soporte soporte@zentrix.company) y `WebSite` con `SearchAction` → `https://zentrix.company/?q={search_term_string}`. |
| Apps (`/work/`, `/sales/`, `/sales/en/`) | `SoftwareApplication` (BusinessApplication, Android / Android e iOS, enlaces a las tiendas, editor Zentrix) + `BreadcrumbList`. Sin `aggregateRating` ni `offers`: no hay datos publicados, y no se inventan (por eso Google no mostrará estrellas ni precio). |
| Productos de servicio (`/ai/`, `/cloud/`, `/labs/`, `/logistics/`, `/software/`, `/traza/`) y cada solución (`/soluciones/*/`) | `Service` (nombre, tipo, descripción, proveedor Zentrix; `areaServed` Venezuela y Latinoamérica solo en Odoo) + `BreadcrumbList`. |
| Manuales, legales, secciones | `BreadcrumbList` (Inicio › producto › manual › página). |
| Dudas rápidas de los dos manuales | `FAQPage` con las preguntas y respuestas reales de la página + `BreadcrumbList`. |
| 404 y redirecciones | Nada: llevan `noindex` y no entran en el sitemap. |

## Checklist

- [x] `<title>` único ≤ 60 y `meta description` única de 140–160 en cada página indexable.
- [x] `canonical`, `<html lang>`; `hreflang` es/en/x-default recíprocos donde hay traducción (hoy, Zentrix Sales en `/sales/en/`; con `/en/`, todo el sitio).
- [x] `og:title`, `og:description`, `og:image` 1200×630 existente, `og:url`, `og:locale` (+ `og:locale:alternate` con traducción), `twitter:card`, `theme-color`, favicon y manifest.
- [x] Un solo `<h1>` y sin saltos de nivel.
- [x] 404 y redirecciones con `noindex`.
- [x] `sitemap.xml` generado en el despliegue, con `lastmod` de git y alternativas por idioma; `robots.txt` con `Sitemap:`.
- [x] JSON-LD validado por script (estructura y campos obligatorios por plantilla).
- [x] Imágenes con `alt`, `width` y `height`; enlaces internos y anclas sin romper.
- [x] `llms.txt` y `llms-full.txt`.
- [x] Lighthouse SEO 100.
- [ ] Search Console y Bing Webmaster (Victor, abajo).
- [ ] Cambio de dirección de eqnio.com (Victor, abajo).

## Pasos para Victor

### 1. Google Search Console (verificación por DNS en Cloudflare)

1. Entra en <https://search.google.com/search-console> → **Añadir propiedad** → **Dominio** → `zentrix.company`.
2. Copia el registro `TXT` que te da Google (`google-site-verification=…`).
3. En Cloudflare, zona `zentrix.company` → **DNS → Records → Add record**: tipo `TXT`, nombre `@`, contenido el valor copiado, TTL Auto. Guarda.
4. Vuelve a Search Console y pulsa **Verificar** (si falla, espera unos minutos: la propagación en Cloudflare suele tardar menos de cinco).
5. **Sitemaps** → escribe `sitemap.xml` → **Enviar**. Debe quedar «Correcto» con todas las URL.
6. Repite los pasos 1–4 con la propiedad de dominio `eqnio.com` (hace falta para el paso 3).

### 2. Bing Webmaster Tools

1. Entra en <https://www.bing.com/webmasters>. Lo más rápido: **Importar desde Google Search Console** (trae la propiedad verificada y el sitemap).
2. Si prefieres DNS: **Añadir sitio** → `https://zentrix.company` → verificación por **registro DNS**: en Cloudflare, un `CNAME` con el nombre y el destino que indique Bing (`verify.bing.com`), sin proxy (nube gris).
3. **Sitemaps** → `https://zentrix.company/sitemap.xml` → Enviar.

### 3. Cambio de dirección eqnio.com → zentrix.company

Cuando la regla 301 de Cloudflare de `eqnio.com` esté activa (`REDIRECCIONES.md`):

1. Comprueba que `https://eqnio.com/`, `https://eqnio.com/odoo-venezuela.html` y `https://www.eqnio.com/contact.html` responden **301** hacia `zentrix.company` (no 302).
2. En Search Console, abre la propiedad **eqnio.com** → **Configuración → Cambio de dirección** → elige `zentrix.company` → **Validar y actualizar**. Search Console comprueba las 301 de la portada y de algunas URL.
3. Deja las 301 activas al menos 180 días (mejor, para siempre) y no borres la propiedad de eqnio.com.
4. En Bing: **Configuración → Herramienta de mover sitio** con los mismos dominios.
