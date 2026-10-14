# Bloques de contenido

Sistema de bloques de las páginas de zentrix.company. Sustituye las tarjetas blancas con borde fino, los números en tejas lila y las pastillas de texto por seis variantes con recursos del manual: la barra lima con el corte diagonal de la z, la z madre grande y recortada como fondo, los motivos de cada división y el trazo grueso de los monogramas.

- **CSS:** `assets/css/bloques.css`, cargada después de `sitio.css` en todas las páginas. Todas las clases empiezan por `bq-`.
- **JS:** `assets/js/bloques.js` (unas 20 líneas). Solo mueve el brillo que sigue al cursor, y solo con ratón y sin `prefers-reduced-motion`. La aparición escalonada y los contadores usan lo que ya tenía `sitio.js` (`.revela` → `.visible`, `data-cuenta`).
- **Marcado:** `herramientas/bloques.py`. `generar.py` lo usa en las páginas que genera (soluciones, clientes, recursos, nosotros, contacto) y llama a `bloques.aplicar()` en todas las demás. `aplicar()` enlaza la hoja y el script, rellena los marcadores `<!--BQ:NOMBRE-->…<!--/BQ:NOMBRE-->` y convierte el marcado antiguo de las páginas escritas a mano: `funciones` → pilares, `casos` → pilares sobre negro, `proceso` → ruta, `cifras` → cifras y la llamada final `descarga` → cierre. Es idempotente, así que una página nueva escrita con el marcado antiguo (por ejemplo, una traducción) queda convertida la próxima vez que se ejecuta `python3 herramientas/generar.py`.
- **Logotipos de tecnología:** `herramientas/bloques_logos.py`, con los trazados oficiales de Simple Icons (CC0) en una sola tinta. No se deforman (viewBox 24×24) y cada marca pertenece a su titular.
- **Zentrix Logistics:** `assets/css/logistics.css` (prefijo `lg-`, solo en `/logistics/` y `/en/logistics/`) añade la etiqueta de estado (`lg-estado--prod` «En producción» en lima, `lg-estado--dev` «En desarrollo» en contorno), la ruta de siete pasos (`lg-ruta`, una fila desde 1200 px y dos filas en tableta), el trazo del héroe que va de los cubos al pin, el puesto de control dibujado de la tesela protagonista (`lg-monitor`, con un repartidor que recorre la ruta) y las tres capas de la integración (Zentrix Work, Zentrix Logistics, Odoo®). Las ilustraciones de sus módulos (`estante`, `caja`, `guia`, `seguimiento`, `devolucion`; cobro usa `pagos`) están en `ILU` de `bloques.py`. Lo que está en producción y lo que está en desarrollo sale del concepto (`~/Downloads/zentrix/logistics/CONCEPTO.md`): no se presenta como hecho lo que no existe.
- **Ilustraciones de las soluciones:** `assets/img/soluciones/<clave>.svg` (odoo, software, auditoria, infra, pagos, vision), las mismas que se dibujan en línea en las páginas, para reutilizarlas en el mega-menú. Los iconos de contacto (correo, whatsapp, reloj, lugar, idioma) están en `assets/img/iconos/`.

## Reglas comunes

- **Colores:** negro `#090D12`, blanco, azul `#244DFF` y lima `#C7FA46`, y sus transparencias. La lima es acento (barras, CTA con texto negro, números al pasar el ratón sobre fondo oscuro): nunca texto lima sobre blanco. No hay lila: sobre fondo oscuro, el botón principal es lima con texto negro, el secundario va con borde y texto blancos, y los enlaces y el texto de acción van en lima (el azul no llega a AA en texto normal sobre negro). Sobre claro, la acción es azul.
- **Tipografía:** Geist (`var(--display)`) en 800 para los números gigantes, las cifras y los titulares de las protagonistas; Inter para el texto y la interfaz.
- **Esquina cortada:** tarjetas, teselas y paneles cortan la esquina superior derecha en diagonal (`--bq-esquina`, 28 px), como el remate de la z.
- **Barra lima:** `.bq-barra`, 56 × 10 px, con el bisel de los monogramas (73,2 de avance por 64,4 de alto).
- **Ritmo:** se alternan blanco, gris muy claro (`seccion--gris`), negro (`oscuro`) y azul (`bq-seccion--azul`), sin dos fondos iguales seguidos cuando se puede evitar.
- **Movimiento:** elevación de 6 px al pasar el ratón, flecha que avanza, brillo que sigue al cursor, aparición escalonada y trazos que se dibujan. Con `prefers-reduced-motion` no se mueve nada y el contenido se ve entero sin JavaScript.
- **Accesibilidad:** contraste AA en todos los textos (blanco sobre las teselas azules ≥ 4,9:1), foco visible (azul sobre claro, lima sobre negro y azul), listas `ol`/`ul` y títulos `h3` dentro de cada `h2`. Los números, ilustraciones y motivos son decorativos (`aria-hidden`). No hay texto dentro de imágenes.
- **Retícula:** `.bq-reja` reparte los anchos para que no queden huecos: 1 columna en móvil, 2 en tableta y 3 o 4 en escritorio. `reja(n, prota)` en `bloques.py` calcula las clases `bq-c2`, `bq-c3`, `bq-r2` y `bq-t2`.

## Las seis variantes

### 1. Pilares — `bloques.pilares(items, variante, arte)`

Tarjetas con un número gigante en Inter 800, en contorno y recortado por el borde, la barra lima y el título. Al pasar el ratón el número se rellena (azul sobre claro, lima sobre negro).

- `''`: cuatro tarjetas iguales. **Qué incluye** de cada solución, la historia de Nosotros.
- `'oscuro'`: sobre negro. **Casos de uso** de los productos.
- `'prota'`: la primera tarjeta es protagonista, en negro, el doble de grande y con el motivo de la división (onda en AI, nube en Cloud…). **Qué ganas** de cada producto.

### 2. Bento — `bloques.bento(items, variante)`

Mosaico de teselas enlazadas, de tamaños distintos, con una ilustración propia por ítem en el lenguaje de los monogramas (trazo 104/1000 y la barra lima con el corte) y una flecha que avanza. Toda la tesela es el enlace.

- Protagonista (`prota: True`): negra, grande, con el motivo y una ilustración. En la portada, «Odoo en Venezuela» lleva el motivo de capas y una pantalla de sistema de gestión dibujada en vectorial (sin datos reales).
- `'azul'`: sobre la sección azul. **Soluciones** de la portada.
- `''`: sobre claro. **Por necesidad** en `/soluciones/` y los grupos de `/recursos/`.
- `'compacto'`: lista vertical con la ilustración a la izquierda. **Otras soluciones** en cada solución.

### 3. Stack de tecnología — `bloques.stack(tags, titulo)`

Banda negra con los logotipos oficiales en blanco y su nombre (Flutter, Next.js, FastAPI, Odoo®, Docker, Kubernetes). Lo que no es una marca (UI/UX, ERP, Zero Trust…) lleva la barra lima en pequeño. Sustituye a las pastillas de texto.

### 4. Banda y cierre — `bloques.banda(...)`, `bloques.cierre(...)`

- **Banda** de producto relacionado, a todo el ancho, en negro: el monograma grande, el beneficio en una línea (el titular de la página del producto), el motivo de la división de fondo y un CTA lima con el corte diagonal. Sustituye al bloque gris «Producto relacionado».
- **Cierre**: la llamada final de cada página, a todo el ancho en azul, con la z madre recortada en negro de fondo, titular en Inter 800 con la barra lima y botones grandes (blanco y contorno).

### 5. Ruta y cifras — `bloques.pasos(items)`, `bloques.cifras(items)`

- **Ruta:** pasos numerados en Inter 800, con un trazo que se dibuja de izquierda a derecha (de arriba abajo en móvil) y conectores con el corte diagonal; el último en lima. **Cómo trabajamos** y **Cómo funciona**.
- **Cifras:** números enormes que cuentan al aparecer, la barra lima que se estira y separadores inclinados. **Zentrix en cifras** de la portada.

### 6. Contacto — `bloques.hablemos(lang)` y `bloques.contacto(lang)`

- **Hablemos** (`hablemos`): la banda que se repite (portada, marcador `<!--BQ:CONTACTO-->`, que genera la sección entera con `id="contacto"`/`"contact"`). Un panel negro con la esquina cortada: a la izquierda el titular grande («Cuéntanos cómo trabaja tu equipo.»), la barra lima y una sola línea de apoyo («Te responde una persona, en español, en menos de un día hábil.»); a la derecha dos grupos de botones reales: **Escríbenos** (correo hola@ en lima y WhatsApp en contorno) y **¿Ya usas nuestras apps?** (soporte@, el centro de soporte y los manuales de Work y Sales en pastillas). **No lleva dirección.**
- **Contacto** (`contacto`, solo en `/contacto/` y `/en/contact/`): la misma banda con el titular de la página y, debajo, el lugar (mapa estático ilustrado en SVG, sin iframes, y la dirección en tres líneas con microdatos `PostalAddress` y los enlaces a Google Maps y Apple Maps) y los datos (horario, idiomas y dónde está el equipo).
- **La dirección** se ve solo en `/contacto/`, `/en/contact/` y en la ficha de Zentrix Sales de `/soporte/`, que la declara como dirección legal. En el resto vive únicamente en el JSON-LD de Organization (`PostalAddress`). No volver a ponerla en la banda (Victor, 14-10-2026).

## Manifiesto de la portada — `.bq-manifiesto` (a mano en `index.html` y `en/index.html`)

Lista 01–04 con el número en contorno en su columna. Cada `<li>` es un grid de dos columnas, así que debe tener **un solo hijo**: `<div class="bq-manifiesto__texto">` con `<strong class="bq-manifiesto__t">` (título) y `<span class="bq-manifiesto__d">` (la frase, con mayúscula inicial). Texto suelto junto al `<strong>` se vuelve otra celda del grid y cae en la columna estrecha del número, palabra por palabra (corregido el 14-10-2026). Entre título y frase va `<span class="sr">. </span>` para que lectores de pantalla y `llms-full.txt` lean dos frases. La columna izquierda del `.duo--arriba` va alineada arriba y fija (`.duo__fijo`, sticky) desde 900 px.

## Cómo añadir un bloque

1. En una página generada, llama a la función de `bloques.py` desde su `pag_*` en `generar.py`.
2. En una página escrita a mano, escribe el marcado antiguo (se convierte solo) o un marcador `<!--BQ:NOMBRE--><!--/BQ:NOMBRE-->` y añade su caso en `_marcador()`.
3. Ejecuta `python3 herramientas/generar.py` y comprueba con `--check`.
