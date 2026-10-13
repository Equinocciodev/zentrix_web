# zentrix_web

Sitio de **zentrix®** en <https://zentrix.company>: la portada corporativa y las páginas de los dos productos, **Zentrix Work** (antes GUUAO® Work) y **Zentrix Sales** (antes Vendoo), con su privacidad y su soporte. Las URL de privacidad y soporte son las que declaran las apps y las fichas de Google Play y App Store.

Es un sitio estático: HTML, una hoja CSS y ninguna línea de JavaScript. No hay paso de compilación. Las páginas de privacidad y soporte se leen enteras sin JavaScript, que es como las revisan Google y Apple.

## Rutas

| Ruta | Página |
|---|---|
| `/` | Portada de zentrix, la marca madre: qué hacemos, los dos productos destacados, cómo trabajamos, las divisiones y el contacto. |
| `/work/` | Zentrix Work. Google Play: `com.leiros.guuaowork`. |
| `/work/docs/` + 11 páginas `.html` | Manual del operador, migrado de work.guuao.com/docs. |
| `/work/privacidad/` · `/work/soporte/` · `/work/terminos/` | Política (anclas `#c1`…`#c11`, Play declara `#c7`), soporte (`#eliminar-datos`) y términos. |
| `/sales/` | Zentrix Sales. Google Play `com.leiros.vendoo`, App Store `id6811065669`. |
| `/sales/docs/` + 12 páginas `.html` | Manual del vendedor, migrado de vendooapp.com/docs. |
| `/sales/privacidad/` · `/sales/soporte/` · `/sales/terminos/` · `/sales/contacto/` | Política, soporte, términos y contacto con el formulario de demostración (`assets/js/contacto.js` arma el correo). |
| `/sales/en/` + `privacy.html`, `terms.html`, `support.html`, `contact.html` | Versión en inglés, migrada de vendooapp.com/en. |
| `/404.html` | Página de error. |

Las páginas de los manuales llevan, además de `sitio.css`, `manual-sales.css` o `manual-work.css`: son las hojas del manual de cada sitio anterior con los tokens de zentrix. Las capturas de los manuales están en `assets/img/sales/` y `assets/img/work/`, y algunas todavía muestran el diseño anterior de las apps.

## Correos de contacto

- `hola@zentrix.company`: contacto general y Zentrix Sales. Teléfono/WhatsApp `+58 412-346 9712`.
- `soporte@zentrix.company`: soporte y Zentrix Work.

Los buzones se crearon el 13-10-2026. Las apps todavía llevan los correos anteriores (`hola@vendooapp.com` y `contacto@guuao.com`): hay que cambiarlos en la próxima versión.

## Nombres

zentrix es la marca madre. En la portada, la navegación, las tarjetas y el pie no se nombran GUUAO ni los nombres anteriores de las apps. GUUAO LLC aparece solo donde la ley lo exige: en privacidad, soporte y términos, como responsable que publica las apps. Las notas de cambio de nombre se quedan en esas mismas páginas.

## Marca

- Paleta: azul `#244DFF` para la acción, negro `#090D12` para el texto y los fondos inmersivos, y lima `#C7FA46` solo como acento. Nunca se usa lima como texto sobre blanco. Fondo `#F5F7FA`. Sobre negro, la acción va en `#A6B6FF`.
- Tipografía: Inter 400/500/600/700, recortada a latín y servida desde `assets/fonts/` (licencia OFL en `LICENSE-Inter.txt`). No se cargan fuentes externas.
- Logos: los SVG maestros de `guuao_work_app` (rama `feat/zentrix-work`, `assets/brand/`) y de `vendoo_app` (rama `feat/zentrix-sales`, `assets/marca/zentrix_sales/`), copiados en `assets/img/logos/`. `zentrix-negro.svg` y `zentrix-blanco.svg` salen del logotipo en `currentColor`.
- En los textos corridos los productos se escriben «Zentrix Work» y «Zentrix Sales», como el nombre visible de las apps y de las fichas. En los logos van en minúsculas, como pide el manual.
- El contraste cumple AA: azul sobre blanco 5,9:1, texto secundario `#4A5363` sobre `#F5F7FA` 7,2:1, y `#A6B6FF` sobre negro 10:1.
- Las capturas son de `~/Downloads/zentrix/work_app` y `sales_app` (las «después»), en WebP.
- Las imágenes Open Graph (`assets/img/og*.png`, 1200×630) se generaron con la paleta y el logo.

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
