# Redirecciones

GitHub Pages no admite redirecciones 301 propias. Por eso cada ruta vieja es una página que redirige con `<meta http-equiv="refresh">` y `location.replace` (conserva el `?` y el `#`), lleva `rel="canonical"` hacia la ruta nueva, `noindex` y un enlace visible. Las genera `herramientas/generar.py` a partir de la lista `REDIRECCIONES`.

| Ruta vieja | Ruta nueva | Desde | Motivo |
|---|---|---|---|
| `/logistica/` | `/logistics/` | 14-10-2026 | El producto se llama «Zentrix Logistics»: el apellido va en inglés, como los demás. |
| `/about.html` | `/nosotros/` | 14-10-2026 | eqnio.com → zentrix.company: «Sobre Equinoccio». |
| `/contact.html` | `/contacto/` | 14-10-2026 | eqnio.com → zentrix.company: contacto. |
| `/privacy.html` | `/legal/#privacidad` | 14-10-2026 | eqnio.com → zentrix.company: índice de las políticas de privacidad. |
| `/terms.html` | `/legal/#terminos` | 14-10-2026 | eqnio.com → zentrix.company: índice de los términos. |
| `/odoo-venezuela.html` | `/soluciones/odoo-venezuela/` | 14-10-2026 | eqnio.com → zentrix.company: servicio. |
| `/desarrollo-de-software.html` | `/soluciones/desarrollo-de-software/` | 14-10-2026 | eqnio.com → zentrix.company: servicio. |
| `/auditoria-tecnica.html` | `/soluciones/auditoria-tecnica/` | 14-10-2026 | eqnio.com → zentrix.company: servicio. |
| `/infraestructura-alta-disponibilidad.html` | `/soluciones/infraestructura-alta-disponibilidad/` | 14-10-2026 | eqnio.com → zentrix.company: servicio. |
| `/pagos-y-comercio-digital.html` | `/soluciones/pagos-y-comercio-digital/` | 14-10-2026 | eqnio.com → zentrix.company: servicio. |
| `/vision-computacional.html` | `/soluciones/vision-computacional/` | 14-10-2026 | eqnio.com → zentrix.company: servicio. |
| `/sales/en/` | `/en/sales/` | 15-10-2026 | El inglés pasa a /en/, con las mismas rutas que el español. |
| `/sales/en/index.html` | `/en/sales/` | 15-10-2026 | Ídem. |
| `/sales/en/privacy.html` | `/en/sales/privacy/` | 15-10-2026 | Ídem. |
| `/sales/en/terms.html` | `/en/sales/terms/` | 15-10-2026 | Ídem. |
| `/sales/en/support.html` | `/en/support/#sales` | 15-10-2026 | Ídem; desde el 16-10-2026, al soporte unificado. |
| `/sales/en/contact.html` | `/en/contact/?producto=sales#motivo` | 15-10-2026 | Ídem; desde el 16-10-2026, al contacto unificado. |
| `/work/soporte/` | `/soporte/#work` | 16-10-2026 | Soporte unificado de la suite. |
| `/sales/soporte/` | `/soporte/#sales` | 16-10-2026 | Soporte unificado de la suite. |
| `/sales/contacto/` | `/contacto/?producto=sales#motivo` | 16-10-2026 | Contacto unificado, con el motivo «Ventas o demostración» y Zentrix Sales. |
| `/en/work/support/` | `/en/support/#work` | 16-10-2026 | Soporte unificado de la suite. |
| `/en/sales/support/` | `/en/support/#sales` | 16-10-2026 | Soporte unificado de la suite. |
| `/en/sales/contact/` | `/en/contact/?producto=sales#motivo` | 16-10-2026 | Contacto unificado. |

## eqnio.com → zentrix.company (Cloudflare)

Regla recomendada en Cloudflare, en la zona `eqnio.com`: **Rules → Redirect Rules → Single Redirect**.

- Cuándo: *Hostname* es igual a `eqnio.com` **o** `www.eqnio.com` (expresión: `(http.host in {"eqnio.com" "www.eqnio.com"})`).
- Qué: *Dynamic*, expresión `concat("https://zentrix.company", http.request.uri.path)`, código **301**, con **Preserve query string** activado.
- El registro DNS de `eqnio.com` y `www` debe estar **proxied** (nube naranja) para que la regla se aplique; si no hay origen, basta un registro `A` a `192.0.2.1` proxied.

Así `eqnio.com/<ruta>` llega a `zentrix.company/<ruta>`, y las páginas de arriba llevan cada ruta vieja a la nueva. Las rutas de eqnio.com que no son páginas (`/llms.txt`, `/sitemap.xml`, `/robots.txt`) existen también aquí; `/manifest.json` es una copia del `site.webmanifest`.
