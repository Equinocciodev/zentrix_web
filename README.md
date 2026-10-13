# zentrix_web

Sitio de **zentrix®** en <https://zentrix.company>: la portada corporativa y las páginas de los dos productos, **Zentrix Work** (antes GUUAO® Work) y **Zentrix Sales** (antes Vendoo), con su privacidad y su soporte. Las URL de privacidad y soporte son las que declaran las apps y las fichas de Google Play y App Store.

Es un sitio estático: HTML, una hoja CSS y ninguna línea de JavaScript. No hay paso de compilación. Las páginas de privacidad y soporte se leen enteras sin JavaScript, que es como las revisan Google y Apple.

## Rutas

| Ruta | Página |
|---|---|
| `/` | Portada corporativa: qué es zentrix, los productos, las divisiones, el modelo y el contacto. Los textos vienen de la Presentación Corporativa. |
| `/work/` | Zentrix Work. Enlace a Google Play: `com.leiros.guuaowork`. |
| `/work/privacidad/` | La política de privacidad de work.guuao.com, cambiando solo el nombre. Conserva las anclas `#c1`…`#c11`; Play tiene declarada la `#c7`. |
| `/work/soporte/` | Preguntas frecuentes y `#eliminar-datos`, la URL de eliminación de datos que pide Play. |
| `/sales/` | Zentrix Sales. Enlaces a Google Play (`com.leiros.vendoo`) y App Store (`id6811065669`). |
| `/sales/privacidad/` | La política de vendooapp.com, cambiando solo el nombre. Conserva las anclas `#c1`…`#c11`. |
| `/sales/soporte/` | Contacto, soporte y `#eliminar-datos`. |
| `/404.html` | Página de error. |

Cada página es un `index.html` dentro de su carpeta. GitHub Pages sirve `/work/privacidad` con un 301 a `/work/privacidad/`, y esa URL devuelve 200.

## Correos de contacto (provisionales)

Mientras no haya buzones en zentrix.company, el sitio usa los correos actuales:

- **Zentrix Sales:** `hola@vendooapp.com` y el teléfono/WhatsApp `+58 412-346 9712`, los mismos de vendooapp.com y de la app.
- **Zentrix Work:** `contacto@guuao.com`, el mismo de work.guuao.com y de la app (`WorkConfig.privacyEmail`).

Cuando existan los buzones nuevos, hay que cambiarlos aquí, en las políticas (cláusulas 7 y 11) y en las apps, en la misma versión. Los términos de uso siguen en los sitios anteriores (`work.guuao.com/terminos.html` y `vendooapp.com/terminos.html`), y el manual del vendedor en `vendooapp.com/docs/`.

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
