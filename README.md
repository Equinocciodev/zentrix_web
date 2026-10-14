# zentrix_web

Sitio de **Zentrix®** en <https://zentrix.company>: la portada corporativa y las páginas de los dos productos, **Zentrix Work** (antes GUUAO® Work) y **Zentrix Sales** (antes Vendoo), con su privacidad y su soporte. Las URL de privacidad y soporte son las que declaran las apps y las fichas de Google Play y App Store.

Es un sitio estático: HTML, una hoja CSS (`assets/css/sitio.css`) y un script pequeño (`assets/js/sitio.js`) que solo añade movimiento: la aparición de las secciones al hacer scroll (IntersectionObserver) y el conteo de las cifras. No hay paso de compilación ni dependencias. Sin JavaScript todo el contenido se ve igual, y con `prefers-reduced-motion` no se mueve nada. Las páginas de privacidad, términos, soporte y los manuales no cargan el script: se leen enteras sin JavaScript, que es como las revisan Google y Apple.

## Rutas

| Ruta | Página |
|---|---|
| `/` | Portada de Zentrix, la marca madre: qué hacemos, los dos productos destacados, cómo trabajamos, las divisiones y el contacto. |
| `/work/` | Zentrix Work. Google Play: `com.leiros.guuaowork`. |
| `/work/docs/` + 11 páginas `.html` | Manual del operador, migrado de work.guuao.com/docs. |
| `/work/privacidad/` · `/work/soporte/` · `/work/terminos/` | Política (anclas `#c1`…`#c11`, Play declara `#c7`), soporte (`#eliminar-datos`) y términos. |
| `/sales/` | Zentrix Sales. Google Play `com.leiros.vendoo`, App Store `id6811065669`. |
| `/sales/docs/` + 12 páginas `.html` | Manual del vendedor, migrado de vendooapp.com/docs. |
| `/sales/privacidad/` · `/sales/soporte/` · `/sales/terminos/` · `/sales/contacto/` | Política, soporte, términos y contacto con el formulario de demostración (`assets/js/contacto.js` arma el correo). |
| `/sales/en/` + `privacy.html`, `terms.html`, `support.html`, `contact.html` | Versión en inglés, migrada de vendooapp.com/en. |
| `/ai/` · `/logistics/` · `/cloud/` · `/labs/` · `/software/` | Los otros productos de la Presentación Corporativa: problema, para quién, beneficios, cómo funciona y contacto. Usan solo lo que dice la presentación. Ninguno tiene app publicada, así que no enlazan a tiendas: «Solicita una demostración», o «Próximamente» en Zentrix Logistics. |
| `/privacidad/` | Privacidad del sitio web: «Cookies y analítica» en español (`#cookies`) y en inglés (`#cookies-en`), en una sola página. Las de las apps siguen en cada producto. |
| `/traza/` | Presentación breve de Traza®, que tiene sitio propio: el botón principal lleva a <https://traza.technology>. En el menú, la portada y el pie, Traza enlaza directamente a ese sitio (pestaña nueva, con indicador de enlace externo). |
| `/404.html` | Página de error. |

Las páginas de los manuales llevan, además de `sitio.css`, `manual-sales.css` o `manual-work.css`: son las hojas del manual de cada sitio anterior con los tokens de zentrix. Las capturas de los manuales están en `assets/img/sales/` y `assets/img/work/`, y algunas todavía muestran el diseño anterior de las apps.

## Monogramas de los productos

Dirección A, aprobada por Victor el 14-10-2026: dos letras en minúscula y la barra lima con el corte diagonal de la z. Sales usa «sl» (no «sa», 14-10-2026), generado con el mismo constructor que el resto de la suite. Zentrix Logistics usa «lg» (fondo lima, figura negra; el apellido en inglés como los demás, 14-10-2026, y la firma dice «zentrix® logistics»), rehecho el 14-10-2026 con el mismo constructor que «sl»: Inter ExtraBold a curvas, el conjunto (ascendente, descendente y barra de 230) centrado en el área viva 225–775. Los SVG están en `assets/img/logos/monogramas/<producto>_{icono,monocromo,firma_positivo,firma_negativo}.svg` para work, sales, ai, logistica, cloud, labs y software; los maestros y el constructor (`fuente/suite.py`, `fuente/lg.py`) en `~/Downloads/zentrix/isotipos/propuestas/`. `work-icono-512.png` y `sales-icono-512.png` salen de esos SVG con `rsvg-convert`.

- En las páginas de producto la cabecera lleva la firma del producto (monograma + zentrix® + apellido) en lugar del logotipo madre, y enlaza a la portada. Work y Sales tienen debajo una barra fina, sin logo, con sus enlaces (producto, manual, privacidad, soporte).
- El héroe de cada producto dibuja su monograma en línea (`<!--MONO:slug-->`) para animar la teja, las letras y la barra por separado.
- Traza conserva su símbolo y su wordmark propios (manual, pág. 15) con el endoso «un producto de Zentrix®»; no lleva monograma. Su icono es el de traza.technology (el wordmark blanco sobre el anillo de luz azul), recortado en la teja del sistema (radio 22 %): `assets/img/logos/traza/traza_icono-{40,64,192,208,512}.webp` y PNG de 192 y 512. Siempre enlaza a <https://traza.technology> en pestaña nueva, y en la suite, el menú y el pie va al final, como marca asociada.
- El logotipo madre, el favicon y la z de la portada no cambian: son la marca madre.

## Generador: cabecera, pie y páginas de sección

`herramientas/generar.py` (sin dependencias) es la única fuente de la cabecera con mega-menú (Productos, Soluciones, Clientes, Recursos, Nosotros y Contacto), del pie y de las páginas de sección: `/soluciones/` y una página por solución, `/clientes/`, `/recursos/`, `/nosotros/` y `/contacto/`. Su contenido está en `herramientas/contenido.py` y los datos comunes (productos, soluciones, pares de rutas por idioma) en `herramientas/sitio.py`. También escribe las páginas de redirección (`REDIRECCIONES.md`), `sitemap.xml`, `llms.txt` y `manifest.json`.

- `python3 herramientas/generar.py` escribe; `--check` comprueba que todo está al día; `--pares` lista los pares español/inglés y los huérfanos.
- `python3 herramientas/enlaces.py` comprueba que ningún enlace interno da 404.
- El menú móvil y el comportamiento del mega-menú están en `assets/js/nav.js`, que cargan todas las páginas. Sin JavaScript, los `<details>` siguen funcionando.
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

## Movimiento e ilustraciones

- La z madre del héroe de la portada se dibuja (trazo) y luego entra la pieza del corte diagonal; la geometría es la del maestro (`zentrix_z_azul.svg`).
- Cada división tiene su motivo, como pide la Presentación Corporativa: capas (software), onda (ai), nube (cloud), prisma (labs), cubos (logística) y anillo (Traza); Work lleva el pulso de un aviso y Sales la ruta del día. Son SVG en línea (`<!--MOTIVO:nombre-->`), animados solo con CSS.
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

- Paleta: azul `#244DFF` para la acción, negro `#090D12` para el texto y los fondos inmersivos, y lima `#C7FA46` solo como acento. Nunca se usa lima como texto sobre blanco. Fondo `#F5F7FA`. Sobre negro, la acción va en `#A6B6FF`.
- Tipografía: Inter 400/500/600/700, recortada a latín, y Inter ExtraBold 800 (4.1 oficial, latín + latín extendido) para los titulares del héroe, servidas desde `assets/fonts/` (licencia OFL en `LICENSE-Inter.txt`). No se cargan fuentes externas. Las páginas con héroe precargan los cinco pesos, porque todos se ven por encima del pliegue (con 4G lento llegan antes del primer pintado); mientras llegan, la reserva «Inter reserva» (Arial con las métricas de Inter) evita saltos.
- Logos: los SVG maestros de `guuao_work_app` (rama `feat/zentrix-work`, `assets/brand/`) y de `vendoo_app` (rama `feat/zentrix-sales`, `assets/marca/zentrix_sales/`), copiados en `assets/img/logos/`. `zentrix-negro.svg` y `zentrix-blanco.svg` salen del logotipo en `currentColor`.
- En texto (titulares, párrafos, menús, botones, `alt`, `aria-label`, `title`, metadatos, pies, inglés y español) la marca va siempre con mayúscula inicial: «Zentrix», «Zentrix Work», «Zentrix Sales», «Zentrix AI», «Zentrix Cloud», «Zentrix Labs», «Zentrix Software», y «Traza». Solo el logotipo (los SVG y las firmas construidas en HTML que lo imitan, como `zentrix <b>work</b>` en la familia de la portada) va en minúsculas, como pide el manual. URLs, dominios, correos y nombres de archivo no cambian.
- El contraste cumple AA: azul sobre blanco 5,9:1, texto secundario `#4A5363` sobre `#F5F7FA` 7,2:1, y `#A6B6FF` sobre negro 10:1.
- Las capturas son de `~/Downloads/zentrix/work_app` y `sales_app` (las «después»), en WebP.
- Las imágenes Open Graph (`assets/img/og*.png`, 1200×630) se generaron con la paleta y el logo; cada producto tiene la suya (`og-<producto>.png`) con su firma y su monograma, y todas las páginas llevan `og:image` y `twitter:image`.
- Favicon: `favicon.svg` (la z del maestro sobre teja azul), `favicon.ico` (16, 32 y 48), PNG de 16, 32, 192 y 512 y uno de 512 «maskable» en `assets/img/favicon/`, `apple-touch-icon.png` de 180 sin transparencia en la raíz, `safari-pinned-tab.svg` para Safari y `site.webmanifest`.

## Analítica

`assets/js/analitica.js` mide con **GA4** en la propiedad del proyecto de Firebase de GUUAO (`G-H0HG8XPTES`); todos los eventos llevan `site: "zentrix"` para filtrarlos dentro de esa propiedad. `generar.py` lo pone con `defer` en el `<head>` de cada página (no en las redirecciones; en `404.html` con `data-grupo="error"`).

- No se pide nada a Google hasta que la persona pulsa «Aceptar» en el aviso. «Rechazar», o «Do Not Track» / «Global Privacy Control» sin elección guardada, no envían nada.
- Consent Mode v2: `analytics_storage` denegado hasta aceptar; `ad_storage`, `ad_user_data` y `ad_personalization` siempre denegados; Google Signals apagado.
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
