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
| `/ai/` · `/logistica/` · `/cloud/` · `/labs/` · `/software/` | Los otros productos de la Presentación Corporativa: problema, para quién, beneficios, cómo funciona y contacto. Usan solo lo que dice la presentación. Ninguno tiene app publicada, así que no enlazan a tiendas: «Solicita una demostración», o «Próximamente» en logística, cuyo nombre comercial está por definir. |
| `/traza/` | Presentación breve de Traza®, que tiene sitio propio: el botón principal lleva a <https://traza.technology>. En el menú, la portada y el pie, Traza enlaza directamente a ese sitio (pestaña nueva, con indicador de enlace externo). |
| `/404.html` | Página de error. |

Las páginas de los manuales llevan, además de `sitio.css`, `manual-sales.css` o `manual-work.css`: son las hojas del manual de cada sitio anterior con los tokens de zentrix. Las capturas de los manuales están en `assets/img/sales/` y `assets/img/work/`, y algunas todavía muestran el diseño anterior de las apps.

## Monogramas de los productos

Dirección A, aprobada por Victor el 14-10-2026: dos letras en minúscula y la barra lima con el corte diagonal de la z. Sales usa «sl» (no «sa», 14-10-2026), generado con el mismo constructor que el resto de la suite. Los SVG están en `assets/img/logos/monogramas/<producto>_{icono,monocromo,firma_positivo,firma_negativo}.svg` para work, sales, ai, cloud, labs y software. `work-icono-512.png` y `sales-icono-512.png` salen de esos SVG con `rsvg-convert`.

- En las páginas de producto la cabecera lleva la firma del producto (monograma + zentrix® + apellido) en lugar del logotipo madre, y enlaza a la portada. Work y Sales tienen debajo una barra fina, sin logo, con sus enlaces (producto, manual, privacidad, soporte).
- El héroe de cada producto dibuja su monograma en línea (`<!--MONO:slug-->`) para animar la teja, las letras y la barra por separado.
- Traza conserva su símbolo y su wordmark propios (manual, pág. 15) con el endoso «un producto de Zentrix®»; no lleva monograma. Logística sigue con el wordmark provisional «zentrix logística» hasta que tenga nombre comercial.
- El logotipo madre, el favicon y la z de la portada no cambian: son la marca madre.

## Movimiento e ilustraciones

- La z madre del héroe de la portada se dibuja (trazo) y luego entra la pieza del corte diagonal; la geometría es la del maestro (`zentrix_z_azul.svg`).
- Cada división tiene su motivo, como pide la Presentación Corporativa: capas (software), onda (ai), nube (cloud), prisma (labs), cubos (logística) y anillo (Traza); Work lleva el pulso de un aviso y Sales la ruta del día. Son SVG en línea (`<!--MOTIVO:nombre-->`), animados solo con CSS.
- Solo se usan los cuatro colores del manual y sus transparencias. El lima es acento, salvo el fondo del héroe de logística.

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

## Cómo editar

La cabecera, la barra de producto y el pie se repiten en cada `index.html`. Si cambias uno, cambia los ocho (`grep -l 'class="pie"' -r .`). Para probar en local:

```sh
python3 -m http.server 8765
# http://127.0.0.1:8765/
```

Las dos políticas reutilizan el texto vigente. Solo cambian el nombre de la app, una nota de cambio fechada el 13-10-2026 y el párrafo sobre el sitio web, porque este sitio no usa analítica ni formularios. La revisión legal de la entidad responsable (GUUAO LLC) sigue pendiente, como señala el assessment de rebranding.
