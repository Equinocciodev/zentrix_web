# zentrix_web

Sitio de **Zentrix®** en <https://zentrix.company>: la portada corporativa y las páginas de las apps, **Zentrix Work** (antes GUUAO® Work), **Zentrix Sales** (antes Vendoo) y **Zentrix Check** (la garita de seguridad, desde el 16-10-2026), con su privacidad y su soporte. Las URL de privacidad y soporte son las que declaran las apps y las fichas de Google Play y App Store.

Es un sitio estático: HTML, una hoja CSS (`assets/css/sitio.css`) y un script pequeño (`assets/js/sitio.js`) que solo añade movimiento: la aparición de las secciones al hacer scroll (IntersectionObserver) y el conteo de las cifras. No hay paso de compilación ni dependencias. Sin JavaScript todo el contenido se ve igual, y con `prefers-reduced-motion` no se mueve nada. Las páginas de privacidad, términos y los manuales no cargan el script: se leen enteras sin JavaScript, que es como las revisan Google y Apple. `/soporte/` sí lo carga (es una página generada), pero todo su contenido, incluidas las instrucciones de borrado de cuenta, se ve igual sin JavaScript.

## Rutas

| Ruta | Página |
|---|---|
| `/` | Portada de Zentrix, la marca madre: qué hacemos, los dos productos destacados, cómo trabajamos, las divisiones y el contacto. |
| `/work/` | Zentrix Work. Google Play: `com.leiros.guuaowork`. |
| `/work/docs/` + 11 páginas `.html` | Manual del operador, migrado de work.guuao.com/docs. En inglés, `/en/work/docs/` con los mismos ficheros. |
| `/work/privacidad/` · `/work/terminos/` | Política (anclas `#c1`…`#c11`, Play declara `#c7`) y términos. `/work/soporte/` redirige a `/soporte/#work`. |
| `/sales/` | Zentrix Sales. Google Play `com.leiros.vendoo`, App Store `id6811065669`. |
| `/sales/docs/` + 12 páginas `.html` | Manual del vendedor, migrado de vendooapp.com/docs. En inglés, `/en/sales/docs/` con los mismos ficheros. |
| `/sales/privacidad/` · `/sales/terminos/` | Política y términos. `/sales/soporte/` y `/sales/contacto/` redirigen a `/soporte/#sales` y a `/contacto/?producto=sales#motivo`. |
| `/check/` | Zentrix Check, la app de la garita (solo Android, `com.leiros.check`). Sin ficha de Play publicada todavía: `productos.json` no lleva `play` y no se ponen insignias. |
| `/check/docs/` + 12 páginas `.html` | Manual del vigilante, escrito a partir de las pantallas de `zentrix_check_app`. En inglés, `/en/check/docs/` con los mismos ficheros. |
| `/check/privacidad/` · `/check/terminos/` | Política (anclas `#c1`…`#c11`; la app abre `zentrix.company/check/privacidad`) y términos, con la estructura de Work. `/check/soporte/` (la URL de soporte de la app) redirige a `/soporte/#check`. La cláusula 5 (conservación) es general, sin plazos concretos, por decisión de Victor (16-10-2026). |
| `/soporte/` | Soporte unificado de la suite (`herramientas/ayuda.py`): buscador (Pagefind, el de la cabecera), chips por producto y una sección por app con preguntas rápidas, acceso, manual, **eliminación de cuenta** y datos de la app. Anclas estables que declaran las tiendas: `#eliminar-cuenta-work`, `#eliminar-cuenta-sales` y `#eliminar-cuenta-check` (en inglés `/en/support/#delete-account-work`, `#delete-account-sales` y `#delete-account-check`). Los productos sin app (AI, Logistics, Cloud, Labs, Software) solo llevan a contacto. |
| `/contacto/` | Contacto unificado: selector de motivo (ventas o demostración, soporte de una app, alianzas, prensa) y producto, que solo cambia el asunto del correo y del WhatsApp (`assets/js/contacto.js`; `?motivo=` y `?producto=` lo preseleccionan). La dirección postal vive aquí. |
| `/legal/` | Índice de las políticas de privacidad y los términos de cada app y del sitio. El pie lleva aquí («Privacidad» → `#privacidad`, «Términos» → `#terminos`); las URL de las políticas no cambian. |
| `/en/…` | Todo el sitio en inglés, con las mismas rutas (ver «Idiomas»). Las antiguas `/sales/en/…` redirigen. |
| `/ai/` · `/logistics/` · `/cloud/` · `/labs/` · `/software/` | Los otros productos de la Presentación Corporativa: problema, para quién, beneficios, cómo funciona y contacto. Usan solo lo que dice la presentación. Ninguno tiene app publicada, así que no enlazan a tiendas: «Solicita una demostración». Zentrix Logistics (desde el 14-10-2026) es la capa logística de la suite, del almacén a la puerta, con lo que ya está en producción en GUUAO y Grupo Leiros y lo que está en desarrollo marcado como tal; su CTA es «Hablemos». |
| `/privacidad/` | Privacidad del sitio web: «Cookies y analítica» en español (`#cookies`) y en inglés (`#cookies-en`), en una sola página. Las de las apps siguen en cada producto. |
| `/traza/` | Presentación breve de Traza®, que tiene sitio propio: el botón principal lleva a <https://traza.technology>. En el menú, la portada y el pie, Traza enlaza directamente a ese sitio (pestaña nueva, con indicador de enlace externo). |
| `/404.html` | Página de error (ver «La 404»). |

Las páginas de los manuales llevan, además de `sitio.css`, `manual-sales.css` o `manual-work.css`: son las hojas del manual de cada sitio anterior con los tokens de zentrix. Las capturas de los manuales están en `assets/img/sales/` y `assets/img/work/`, y algunas todavía muestran el diseño anterior de las apps.

## Monogramas de los productos

Dirección A, aprobada por Victor el 14-10-2026: dos letras en minúscula y la barra lima con el corte diagonal de la z. Sales usa «sl» (no «sa», 14-10-2026), generado con el mismo constructor que el resto de la suite. Zentrix Logistics usa «lg» (fondo lima, figura negra; el apellido en inglés como los demás, 14-10-2026, y la firma dice «zentrix® logistics»), rehecho el 14-10-2026 con el mismo constructor que «sl»: Inter ExtraBold a curvas, el conjunto (ascendente, descendente y barra de 230) centrado en el área viva 225–775. Los SVG están en `assets/img/logos/monogramas/<producto>_{icono,monocromo,firma_positivo,firma_negativo}.svg` para work, sales, check, ai, logistica, cloud, labs y software; los maestros y el constructor (`fuente/suite.py`, `fuente/lg.py`) en `~/Downloads/zentrix/isotipos/propuestas/`. `work-icono-512.png`, `sales-icono-512.png` y `check-icono-512.png` salen de esos SVG con `rsvg-convert`. Check usa «ck» tal como lo trae `zentrix_check_app` (`assets/brand/monograma/`, 16-10-2026): teja negra con filo `#2A3140`, letras blancas y barra `#A6B6FF`.

- En las páginas de producto la cabecera lleva la firma del producto (monograma + zentrix® + apellido) en lugar del logotipo madre, y enlaza a la portada. Work, Sales y Check tienen debajo una barra fina, sin logo, con sus enlaces (producto, manual, privacidad, soporte).
- El héroe de cada producto dibuja su monograma en línea (`<!--MONO:slug-->`) para animar la teja, las letras y la barra por separado.
- Traza conserva su símbolo y su wordmark propios (manual, pág. 15) con el endoso «un producto de Zentrix®»; no lleva monograma. Su icono es el de traza.technology (el wordmark blanco sobre el anillo de luz azul), recortado en la teja del sistema (radio 22 %): `assets/img/logos/traza/traza_icono-{40,64,192,208,512}.webp` y PNG de 192 y 512. Siempre enlaza a <https://traza.technology> en pestaña nueva, y en la suite, el menú y el pie va al final, como marca asociada.
- El logotipo madre, el favicon y la z de la portada no cambian: son la marca madre.

## Generador: cabecera, pie y páginas de sección

`herramientas/generar.py` (sin dependencias) es la única fuente de la cabecera con mega-menú (Productos, Soluciones, Clientes, Recursos, Nosotros y Contacto), del pie y de las páginas de sección: `/soluciones/` y una página por solución, `/clientes/`, `/recursos/`, `/nosotros/` y `/contacto/`. Su contenido está en `herramientas/contenido.py` y los datos comunes (productos, soluciones, pares de rutas por idioma) en `herramientas/sitio.py`. También escribe las páginas de redirección (`REDIRECCIONES.md`), `sitemap.xml`, `llms.txt` y `manifest.json`.

- `python3 herramientas/generar.py` escribe; `--check` comprueba que todo está al día; `--pares` comprueba que todo el sitio es bilingüe y sale con 1 si no (ver «Idiomas»).
- `python3 herramientas/enlaces.py` comprueba que ningún enlace interno da 404.
- El menú móvil y el comportamiento del mega-menú están en `assets/js/nav.js`, que cargan todas las páginas. Sin JavaScript, los `<details>` siguen funcionando.
- El pie: logo, eslogan (sin la fila de monogramas: ya están en la columna Productos), Productos, Empresa, Recursos, «Legal y soporte» (Soporte, Contacto, Privacidad y Términos; los dos últimos al índice `/legal/`) y Contacto.
- Huecos para otros módulos: `<div id="zx-buscar">` en la cabecera (buscador) y el enlace `#zx-cookies` en el pie (preferencias de cookies).
- Lo que viene de eqnio.com (servicios, filosofía, alianzas, equipo con sus fotos y cargos, partners) está en `contenido.py`, reescrito con el tono de Zentrix.

## Buscador

`assets/js/buscador.js` (con `defer`) llena el hueco `<div id="zx-buscar">` de la cabecera con la pastilla «Buscar… ⌘K» (una lupa en móvil), y `assets/css/buscador.css` le da estilo; los dos los añade `generar.py` al `<head>` de cada página. Se abre con la pastilla, con Cmd/Ctrl+K, con «/» y con `?q=término` en la URL (lo usa el `SearchAction` del JSON-LD). El índice es de **Pagefind** (versión fija 1.5.2) y no se descarga nada de él hasta abrir el buscador.

- **Compilación:** el workflow de Pages ejecuta `python3 herramientas/buscador.py` y luego `npx -y pagefind@1.5.2 --site .`. El script, sobre la copia que se publica, marca el `<main>` de cada página con `data-pagefind-body`, los filtros `producto` y `tipo` (producto, solucion, manual, legal, pagina), el peso de `h1`/`h2` y el nombre del producto en su portada, y escribe `buscador/terminos-<lang>.json` (palabras, títulos y rutas para el autocompletado). Nada de eso se commitea: `pagefind/` y los JSON están en `.gitignore`. `python3 herramientas/buscador.py --check` lista qué entra al índice.
- **Fuera del índice:** las redirecciones (meta refresh) y las páginas `noindex`, la 404, `/eqnio/`, `/logistica/` y `/sales/en/` cuando ya existe `/en/`. La cabecera, el mega-menú, la barra de producto, el pie, el aviso de cookies y la navegación dentro de `<main>` quedan fuera por `exclude_selectors` en `pagefind.yml`.
- **Idioma:** Pagefind arma un índice por `<html lang>` y busca solo en el de la página.
- **Autocompletado:** la palabra se completa en gris dentro del campo y se acepta con Tab o →. Arriba salen accesos directos (productos, manuales, privacidad, soporte, soluciones, contacto) cuando lo escrito los nombra. No distingue tildes ni mayúsculas. Con el campo vacío salen las búsquedas recientes (localStorage) y sugerencias.
- **Analítica:** si existe `window.zxAnalytics.track`, envía `search`, `search_no_results` y `select_content`.
- **Probar en local:** sobre una copia del repo (el script modifica los HTML): `python3 herramientas/buscador.py && npx -y pagefind@1.5.2 --site . && python3 -m http.server`.

## La 404

`generar.py` escribe `/404.html` y `/en/404.html` (`pag_404`). GitHub Pages sirve el mismo `/404.html` para cualquier ruta que no existe, también bajo `/en/`: por eso la española lleva la cabecera, el `<main>` y el pie en inglés dentro de un `<template>`, y un script en línea los cambia antes de pintar cuando la ruta empieza por `/en/` (la URL no cambia y sigue respondiendo 404). Lleva `noindex` y queda fuera del sitemap y del buscador.

- **Ilustración:** el «404» armado con la cuadrícula de cubos de la marca (esquina cortada como la z), en azul; la pieza lima es la que falta y se sale de su hueco. Al pasar el ratón vuelve a su sitio. SVG en línea y CSS (`assets/css/error404.css`); con `prefers-reduced-motion` no se mueve nada.
- **Sugerencias** (`assets/js/error404.js`): reglas por palabras de la URL (rutas viejas de eqnio.com y vendooapp.com, «sales», «work», «privacidad», «soporte», «docs», soluciones…) y, si no, la ruta más parecida (distancia de edición). Las rutas y títulos los escribe `generar.py` en `#e404-datos`.
- **Buscador:** el campo abre el buscador del sitio con lo escrito (`window.zxBuscar.abrir`, en `buscador.js`), con su autocompletado; viene relleno con las palabras de la URL. Sin JavaScript lleva a `/?q=…`.
- **Suite:** los productos con sus monogramas; Work y Sales con manual, privacidad y soporte.
- Analítica: `page_not_found` (ruta y primera sugerencia) y `select_content` al elegir una sugerencia.

## Idiomas

**Todo el sitio es bilingüe** (decisión de Victor, 16-10-2026): cada página de contenido existe en español y en inglés. El español vive en la raíz y el inglés bajo `/en/`, con rutas espejo (`/en/work/`, `/en/solutions/…`, `/en/customers/`, `/en/about/`, `/en/contact/`, `/en/privacy/`…). Los pares están en `PARES` de `herramientas/sitio.py`; los capítulos de los manuales no hace falta listarlos: `par()` los empareja por ruta espejo (`/check/docs/llaves.html` ↔ `/en/check/docs/llaves.html`). Las únicas páginas sin par son las redirecciones (meta refresh, `noindex`), que ya llevan cada una a su idioma, y la 404, que es bilingüe (ver «La 404»).

`python3 herramientas/generar.py --pares` es la comprobación, y **sale con 1** si algo falla. Sobre el HTML tal como lo deja el generador, para cada página de contenido mira que:

- su par existe (si no, «HUÉRFANAS»: hay que traducirla o añadir el par a `PARES`);
- su `<head>` lleva `hreflang` es/en/x-default, se incluye a sí misma y apunta al par;
- el `hreflang` es recíproco: el par devuelve el enlace;
- el selector ES/EN de la cabecera y del pie lleva al par, no a la portada del otro idioma;
- no enlaza a una página del otro idioma que tiene versión en el suyo (salvo a su propio par, como «la versión vinculante es la española» de las legales).

Hasta el 16-10-2026 `--pares` solo miraba la tabla `PARES` y contaba los capítulos de los manuales aparte, «solo en español», así que daba 0 huérfanas con 35 capítulos sin traducir. `verificar_seo.py` también falla ya con una página indexable sin `hreflang`, con un manual sin `TechArticle` o con un `inLanguage` distinto del `lang` de la página.

- Cada página lleva `<html lang>`, su `canonical`, `hreflang` es/en/x-default (x-default = español) y `og:locale` + `og:locale:alternate`; el sitemap repite las alternativas.
- El selector ES/EN está en la cabecera (también dentro del menú móvil) y en el pie, y lleva a la misma página en el otro idioma. `assets/js/nav.js` recuerda la elección (`localStorage`, `zx-idioma`) y en cualquier página española con versión inglesa (la de su `<link rel="alternate" hreflang="en">`), si el navegador está en inglés o se eligió inglés, sugiere esa misma página en inglés («View in English →»; en los manuales conserva el ancla) con una píldora pequeña fija bajo la cabecera, con la punta bajo el «EN» del selector (en móvil, bajo la cabecera a la derecha, o bajo la barra de producto si la página la tiene). Nunca coincide con el aviso de cookies: solo aparece cuando ya hay decisión de cookies (en esa visita o en una anterior); cerrarla (× o Esc) se recuerda. Nunca redirige solo.
- Los manuales de Work, Sales y Check están traducidos enteros (16-10-2026): `/en/<app>/docs/` y cada capítulo con el mismo nombre de fichero, las mismas anclas y las mismas capturas. Se escriben a mano, como los españoles: si cambia un capítulo, se cambia también su traducción. Como las apps solo están en español, los textos de la pantalla se dejan en español, tal como salen, con la traducción al lado: `<span class="boton-app" lang="es">Registrar</span> (Register)` (en Sales, `<strong lang="es">«Sincronizar ahora»</strong> (Sync now)`) y `<em lang="es">«Llave entregada.»</em> (“Key handed over.”)`. Cada página del manual lleva un `TechArticle` con su `inLanguage` en el JSON-LD.
- Los textos legales en inglés son traducciones de cortesía; la versión vinculante es la española.
- Las rutas inglesas antiguas de Zentrix Sales (`/sales/en/…`) redirigen a `/en/sales/…` (ver `REDIRECCIONES.md`).

## Insignias de las tiendas

Las URL de Google Play y App Store de cada app están en `herramientas/productos.json` (fuente única; la usan `generar.py` y `seo.py`). Donde una página lleva `<!--TIENDAS:work-->` o `<!--TIENDAS:sales-->`, `generar.py` pone las insignias oficiales localizadas (`assets/img/tiendas/`: Google Play «Disponible en / Get it on», del generador de Google, recortada a su contorno; App Store «Descárgalo en el / Download on the», negra, de Apple Marketing Tools), a 48 px de alto las dos, sin texto encima y con `data-zx-store="play|appstore"` para la analítica. Si una app no está en una tienda, no se pone su insignia: Work solo está en Google Play.

## Movimiento e ilustraciones

- La z madre del héroe de la portada se dibuja (trazo) y luego entra la pieza del corte diagonal; la geometría es la del maestro (`zentrix_z_azul.svg`).
- Cada división tiene su motivo, como pide la Presentación Corporativa: capas (software), onda (ai), nube (cloud), prisma (labs), cubos (logística) y anillo (Traza); Work lleva el pulso de un aviso, Sales la ruta del día y Check el visor de la garita (marco de escáner con la línea de lectura en lima). Son SVG en línea (`<!--MOTIVO:nombre-->`), animados solo con CSS.
- Solo se usan los cuatro colores del manual y sus transparencias. El lima es acento, salvo el fondo del héroe de logística.

## Redirecciones

Las rutas que cambiaron siguen respondiendo con una página de redirección (meta refresh, `canonical` y enlace visible). La tabla está en `REDIRECCIONES.md`.

## Correos de contacto

- `hola@zentrix.company`: contacto general y Zentrix Sales. Teléfono/WhatsApp `+58 412-346 9712`.
- `soporte@zentrix.company`: soporte y Zentrix Work.

Los buzones se crearon el 13-10-2026. Las apps todavía llevan los correos anteriores (`hola@vendooapp.com` y `contacto@guuao.com`): hay que cambiarlos en la próxima versión.

## Nombres

Zentrix es la marca madre. En la portada, la navegación, las tarjetas y el pie no se nombran GUUAO ni los nombres anteriores de las apps. GUUAO LLC aparece solo donde la ley lo exige: en privacidad, soporte y términos, como responsable que publica las apps. Las notas de cambio de nombre se quedan en esas mismas páginas.

## Marca

- Paleta: azul `#244DFF` para la acción, negro `#090D12` para el texto y los fondos inmersivos, y lima `#C7FA46` solo como acento. Nunca se usa lima como texto sobre blanco. Fondo `#F5F7FA`. No hay lila: sobre negro, los enlaces y el texto de acción van en lima o blanco y el botón principal es lima con texto negro (el azul no llega a AA en texto normal sobre negro); sobre claro, la acción es azul.
- Tipografía: **Geist** para los titulares (h1 y h2 en 800, h3 en 700, cifras, antetítulos y el titular de contacto, con tracking negativo de −0,03 a −0,042 em) e **Inter** 400/500/600/700 para texto, botones, menú y formularios. Geist (`geist@1.7.2`, OFL en `LICENSE-Geist.txt`) es un solo woff2 variable recortado a los pesos 500–800 y latín + latín extendido (`assets/fonts/geist-var.woff2`, 21 KB); la pila está en la variable `--display` de `sitio.css`. Todo se sirve desde `assets/fonts/` y no se cargan fuentes externas. Las páginas con héroe precargan Inter 400–700 y el Geist variable. Mientras llegan, «Inter reserva» y «Geist reserva» (Arial con las métricas de cada una) evitan saltos.
- Logos: los SVG maestros de `guuao_work_app` (rama `feat/zentrix-work`, `assets/brand/`) y de `vendoo_app` (rama `feat/zentrix-sales`, `assets/marca/zentrix_sales/`), copiados en `assets/img/logos/`. `zentrix-negro.svg` y `zentrix-blanco.svg` salen del logotipo en `currentColor`.
- En texto (titulares, párrafos, menús, botones, `alt`, `aria-label`, `title`, metadatos, pies, inglés y español) la marca va siempre con mayúscula inicial: «Zentrix», «Zentrix Work», «Zentrix Sales», «Zentrix AI», «Zentrix Cloud», «Zentrix Labs», «Zentrix Software», y «Traza». Solo el logotipo (los SVG y las firmas construidas en HTML que lo imitan, como `zentrix <b>work</b>` en la familia de la portada) va en minúsculas, como pide el manual. URLs, dominios, correos y nombres de archivo no cambian.
- El contraste cumple AA: azul sobre blanco 5,9:1, texto secundario `#4A5363` sobre `#F5F7FA` 7,2:1, lima `#C7FA46` sobre negro 15,9:1 y blanco sobre negro 19,5:1.
- Las capturas son de `~/Downloads/zentrix/work_app` y `sales_app` (las «después»), en WebP.
- Las imágenes Open Graph (`assets/img/og*.png`, 1200×630) se generaron con la paleta y el logo; cada producto tiene la suya (`og-<producto>.png`) con su firma y su monograma, y todas las páginas llevan `og:image` y `twitter:image`.
- Favicon: `favicon.svg` (la z del maestro sobre teja azul), `favicon.ico` (16, 32 y 48), PNG de 16, 32, 192 y 512 y uno de 512 «maskable» en `assets/img/favicon/`, `apple-touch-icon.png` de 180 sin transparencia en la raíz, `safari-pinned-tab.svg` para Safari y `site.webmanifest`.

## Analítica

`assets/js/analitica.js` mide con **GA4** en la propiedad del proyecto de Firebase de GUUAO (`G-H0HG8XPTES`); todos los eventos llevan `site: "zentrix"` para filtrarlos dentro de esa propiedad. `generar.py` lo pone con `defer` en el `<head>` de cada página (no en las redirecciones; en `404.html` con `data-grupo="error"`).

- No se pide nada a Google hasta que la persona pulsa «Aceptar» en el aviso. «Rechazar», o «Do Not Track» / «Global Privacy Control» sin elección guardada, no envían nada.
- Consent Mode v2: `analytics_storage` denegado hasta aceptar; `ad_storage`, `ad_user_data` y `ad_personalization` siempre denegados; Google Signals apagado.
- El aviso es una tarjeta compacta (380 px abajo a la izquierda en escritorio; ancho completo con margen en móvil) que no tapa los botones del hero en 1280×800 ni en 1440×900. «Rechazar» y «Aceptar» son idénticos (tamaño, color y nivel). Va al principio del orden de tabulación, no atrapa el foco y no mueve el contenido. En la primera visita no tiene X ni se cierra con Esc: hay que elegir; al reabrirlo, la X o Esc cierran sin cambiar la elección. Al decidir emite `zx:consent` en `document` (lo escucha la sugerencia de idioma). Si se cambia `analitica.js`, se sube `ANALITICA_JS_V` en `generar.py`.
- La elección se guarda en `localStorage` (`zx-consent`). El enlace «Preferencias de cookies» del pie (`#zx-cookies`) reabre el aviso; sin JavaScript lleva a `/privacidad/#cookies`. Retirar el consentimiento borra las cookies `_ga`.
- Eventos: `page_view` con `content_group` (producto o sección, p. ej. `sales/docs`), `click` con `link_type` (`contacto`, `correo`, `whatsapp`, `tienda`, `traza`), `link_url` sin consulta y `outbound`, y `language_change`. Nada de formularios.
- Otros scripts miden con `window.zxAnalytics.track(nombre, params)`: encola hasta el consentimiento y descarta si se rechaza.
- gtag.js se carga tras la primera interacción o cuando el navegador está ocioso.

## Publicación

El sitio se publica con **GitHub Pages** desde **GitHub Actions**: `.github/workflows/pages.yml` es la plantilla oficial «Static HTML» y se dispara con cada push a `main` o a mano. No se publica con Cloudflare Pages; Cloudflare solo lleva el DNS.

Ajustes de Pages del repo, ya configurados: Source = GitHub Actions, dominio personalizado `zentrix.company` (verificado) y Enforce HTTPS. El fichero `CNAME` contiene `zentrix.company`.

DNS en Cloudflare (cuenta de GitHub Pages: la organización **Equinocciodev**, es decir, `equinocciodev.github.io`):

| Tipo | Nombre | Valor |
|---|---|---|
| A | `zentrix.company` | `185.199.108.153` |
| A | `zentrix.company` | `185.199.109.153` |
| A | `zentrix.company` | `185.199.110.153` |
| A | `zentrix.company` | `185.199.111.153` |
| AAAA | `zentrix.company` | `2606:50c0:8000::153` |
| AAAA | `zentrix.company` | `2606:50c0:8001::153` |
| AAAA | `zentrix.company` | `2606:50c0:8002::153` |
| AAAA | `zentrix.company` | `2606:50c0:8003::153` |
| CNAME | `www` | `equinocciodev.github.io` |
| TXT | `_github-pages-challenge-equinocciodev` | el valor que da GitHub al verificar el dominio |

Para emitir el certificado, los registros tienen que estar en «DNS only». Una vez emitido se pueden pasar a «Proxied», con SSL en «Full (strict)».

## Agentes de IA (agent readiness)

Lo mide https://isitagentready.com/zentrix.company. `herramientas/agentes.py` (lo llama `generar.py`) escribe:

- `robots.txt` (no se edita a mano): `User-agent: *` más un grupo con los crawlers de IA nombrados (búsqueda: OAI-SearchBot, Claude-SearchBot, PerplexityBot; a petición: ChatGPT-User, Claude-User, Perplexity-User; entrenamiento: GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Bytespider, Amazonbot), todos con `Allow: /`, y la línea `Content-Signal` (https://contentsignals.org/).
- **Decisión de Victor, 14-10-2026:** `Content-Signal: search=yes, ai-input=yes, ai-train=yes`. Es contenido público de marketing y se permite todo, también el entrenamiento; no se bloquea a ningún crawler de IA. Para cambiarlo, la constante `CONTENT_SIGNAL` de `agentes.py` (y, si se quiere bloquear a alguno, sacarlo de `CRAWLERS_IA` a un grupo con `Disallow: /`).
- `/.well-known/agent-skills/index.json` y `/.well-known/agent-skills/zentrix/SKILL.md` (Agent Skills Discovery v0.2.0): una skill que explica a un agente dónde está la información pública de Zentrix y qué citar. El `digest` se calcula al generar.
- `/.well-known/ai-catalog.json` (ARD / AI Catalog), también anunciado con `Agentmap:` en `robots.txt` y `<link rel="ai-catalog">`: solo lista esa skill.
- En el `<head>` de cada página: `<link rel="describedby">` a `/llms.txt`, `<link rel="sitemap">` y `<link rel="ai-catalog">`, equivalentes a las cabeceras `Link`.

Zentrix **no** tiene API pública, servidor MCP ni agente A2A, así que no se publican `api-catalog` (RFC 9727), OAuth, `auth.md`, MCP Server Card, WebMCP ni registros DNS-AID: anunciarlos sería falso. Las cabeceras `Link`, la negociación de Markdown y DNSSEC necesitan que Cloudflare haga de proxy delante de GitHub Pages (hoy solo lleva el DNS); los pasos están en la instrucción para la IA de Cloudflare (`INSTRUCCION_AGENT_READY_CLOUDFLARE.md`, fuera del repo).

## Cómo editar

La cabecera, la barra de producto y el pie se repiten en cada `index.html`. Si cambias uno, cambia los ocho (`grep -l 'class="pie"' -r .`). Para probar en local:

```sh
python3 -m http.server 8765
# http://127.0.0.1:8765/
```

Las dos políticas reutilizan el texto vigente. Solo cambian el nombre de la app, una nota de cambio fechada el 13-10-2026 y el párrafo sobre el sitio web, que desde el 14-10-2026 remite a `/privacidad/#cookies` (el sitio mide visitas solo con consentimiento). La revisión legal de la entidad responsable (GUUAO LLC) sigue pendiente, como señala el assessment de rebranding.
