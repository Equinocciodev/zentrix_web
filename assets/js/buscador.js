/* Buscador de zentrix.company.
   Pastilla «Buscar… ⌘K» en la cabecera (#zx-buscar) y ventana de búsqueda
   con Pagefind. Nada de Pagefind se descarga hasta abrir el buscador.
   - Índice: lo compila el workflow de Pages (`npx pagefind --site .`) tras
     `herramientas/buscador.py`, que además escribe /buscador/terminos-<lang>.json
     (palabras y títulos para el autocompletado en gris).
   - Se busca solo en el idioma de la página (<html lang>).
   - ?q=término abre el buscador y busca (SearchAction del JSON-LD).
   - window.zxBuscar.abrir(q) lo abre desde otro campo (el de la 404).
   - Analítica opcional: window.zxAnalytics.track(...). */
(function () {
  'use strict';
  var D = document, W = window, H = D.documentElement;
  if (W.__zxBuscador) return;
  W.__zxBuscador = true;

  var LANG = /^en/i.test(H.lang || '') ? 'en' : 'es';
  var MAC = /Mac|iPhone|iPad|iPod/.test(navigator.platform || navigator.userAgent || '');
  var M = '/assets/img/logos/monogramas/';
  var ICONOS = {
    'Zentrix Work': M + 'work_icono.svg', 'Zentrix Sales': M + 'sales_icono.svg',
    'Zentrix Check': M + 'check_icono.svg',
    'Zentrix AI': M + 'ai_icono.svg', 'Zentrix Logistics': M + 'logistica_icono.svg',
    'Zentrix Cloud': M + 'cloud_icono.svg', 'Zentrix Labs': M + 'labs_icono.svg',
    'Zentrix Software': M + 'software_icono.svg', 'Traza': '/assets/img/logos/traza/traza_icono-64.webp',
    'Zentrix': '/favicon.svg'
  };
  var TX = {
    es: {
      buscar: 'Buscar…', etiqueta: 'Buscar en Zentrix', placeholder: 'Busca productos, manuales o ayuda',
      cerrar: 'Cerrar', cancelar: 'Cancelar', resultados: 'Resultados', recientes: 'Recientes',
      sugerencias: 'Sugerencias', atajos: 'Ir directo', borrar: 'Borrar', mover: 'moverse', abrir: 'abrir',
      completar: 'completar', salir: 'cerrar', nada: 'Sin resultados para', nadaPista: 'Prueba con otra palabra o escríbenos a',
      error: 'El buscador no está disponible ahora.', n1: 'resultado', nN: 'resultados',
      tipos: { producto: 'Productos', solucion: 'Soluciones', manual: 'Manuales', legal: 'Legal y soporte', pagina: 'Páginas' },
      ruta: { manual: 'Manual', legal: 'Legal y soporte', solucion: 'Soluciones', pagina: '' },
      populares: ['manual de Sales', 'cobrar', 'turno', 'soporte', 'privacidad', 'Odoo'],
      correo: 'hola@zentrix.company'
    },
    en: {
      buscar: 'Search…', etiqueta: 'Search Zentrix', placeholder: 'Search products, manuals or help',
      cerrar: 'Close', cancelar: 'Cancel', resultados: 'Results', recientes: 'Recent',
      sugerencias: 'Suggestions', atajos: 'Jump to', borrar: 'Clear', mover: 'move', abrir: 'open',
      completar: 'complete', salir: 'close', nada: 'No results for', nadaPista: 'Try another word or write to',
      error: 'Search is not available right now.', n1: 'result', nN: 'results',
      tipos: { producto: 'Products', solucion: 'Solutions', manual: 'Manuals', legal: 'Legal & support', pagina: 'Pages' },
      ruta: { manual: 'Manual', legal: 'Legal & support', solucion: 'Solutions', pagina: '' },
      populares: ['Zentrix Sales', 'support', 'privacy', 'Odoo', 'contact', 'Zentrix Work'],
      correo: 'hola@zentrix.company'
    }
  }[LANG];

  /* Accesos directos: [nombre, detalle, icono, rutas candidatas, palabras clave].
     Se usa la primera ruta que exista en el índice (lista `r` de terminos-*.json). */
  var ATAJOS = LANG === 'en' ? [
    ['Zentrix Work', 'The store team', 'Zentrix Work', ['/en/work/', '/work/'], 'work store team shift'],
    ['Zentrix Sales', 'The sales force', 'Zentrix Sales', ['/en/sales/', '/sales/en/', '/sales/'], 'sales seller vendor'],
    ['Zentrix Check', 'The security gate', 'Zentrix Check', ['/en/check/', '/check/'], 'check gate security guard access truck'],
    ['Zentrix AI', 'Applied intelligence', 'Zentrix AI', ['/en/ai/', '/ai/'], 'ai artificial intelligence'],
    ['Zentrix Logistics', 'Dispatch and delivery', 'Zentrix Logistics', ['/en/logistics/', '/logistics/'], 'logistics logistica delivery dispatch'],
    ['Zentrix Cloud', 'Infrastructure', 'Zentrix Cloud', ['/en/cloud/', '/cloud/'], 'cloud hosting infrastructure'],
    ['Zentrix Labs', 'Research', 'Zentrix Labs', ['/en/labs/', '/labs/'], 'labs research'],
    ['Zentrix Software', 'Custom software', 'Zentrix Software', ['/en/software/', '/software/'], 'software development odoo'],
    ['Traza', 'traza.technology', 'Traza', ['https://traza.technology'], 'traza traceability'],
    ['Zentrix Sales manual', 'Manual', 'Zentrix Sales', ['/en/sales/docs/', '/sales/docs/'], 'manual docs help guide sales'],
    ['Zentrix Work manual', 'Manual', 'Zentrix Work', ['/en/work/docs/', '/work/docs/'], 'manual docs help guide work'],
    ['Support', 'Zentrix Sales', 'Zentrix Sales', ['/en/sales/support/', '/sales/en/support.html'], 'support help delete account'],
    ['Privacy', 'Zentrix Sales', 'Zentrix Sales', ['/en/sales/privacy/', '/sales/en/privacy.html'], 'privacy data policy'],
    ['Solutions', 'What we do', 'Zentrix', ['/en/solutions/', '/en/soluciones/', '/soluciones/'], 'solutions services'],
    ['Odoo in Venezuela', 'Implementation', 'Zentrix Software', ['/en/solutions/odoo-venezuela/', '/en/soluciones/odoo-venezuela/', '/soluciones/odoo-venezuela/'], 'odoo erp implementation venezuela'],
    ['Contact', 'hola@zentrix.company', 'Zentrix', ['/en/contact/', '/en/contacto/', '/sales/en/contact.html', '/contacto/'], 'contact demo email']
  ] : [
    ['Zentrix Work', 'El equipo de tienda', 'Zentrix Work', ['/work/'], 'work trabajo tienda equipo turno'],
    ['Zentrix Sales', 'La fuerza de ventas', 'Zentrix Sales', ['/sales/'], 'sales ventas vendedor vendedores'],
    ['Zentrix Check', 'La garita de seguridad', 'Zentrix Check', ['/check/'], 'check garita seguridad vigilante acceso camión'],
    ['Zentrix AI', 'Inteligencia aplicada', 'Zentrix AI', ['/ai/'], 'ai ia inteligencia artificial'],
    ['Zentrix Logistics', 'Despacho y reparto', 'Zentrix Logistics', ['/logistics/'], 'logistics logística reparto despacho'],
    ['Zentrix Cloud', 'Infraestructura', 'Zentrix Cloud', ['/cloud/'], 'cloud nube hospedaje infraestructura servidores'],
    ['Zentrix Labs', 'Investigación', 'Zentrix Labs', ['/labs/'], 'labs laboratorio investigación'],
    ['Zentrix Software', 'Software a la medida', 'Zentrix Software', ['/software/'], 'software desarrollo odoo'],
    ['Traza', 'traza.technology', 'Traza', ['https://traza.technology'], 'traza trazabilidad'],
    ['Manual de Zentrix Sales', 'Manual', 'Zentrix Sales', ['/sales/docs/'], 'manual ayuda guía docs sales ventas'],
    ['Manual de Zentrix Work', 'Manual', 'Zentrix Work', ['/work/docs/'], 'manual ayuda guía docs work'],
    ['Cobrarle a un cliente', 'Manual de Zentrix Sales', 'Zentrix Sales', ['/sales/docs/cobrar.html'], 'cobrar cobro cobranza pago'],
    ['El turno', 'Manual de Zentrix Work', 'Zentrix Work', ['/work/docs/turno.html'], 'turno encender pausa'],
    ['Recibir una devolución', 'Manual de Zentrix Work', 'Zentrix Work', ['/work/docs/devoluciones.html'], 'devolución devoluciones devolver'],
    ['Soporte de Zentrix Work', 'Soporte', 'Zentrix Work', ['/work/soporte/'], 'soporte ayuda work eliminar cuenta'],
    ['Soporte de Zentrix Sales', 'Soporte', 'Zentrix Sales', ['/sales/soporte/'], 'soporte ayuda sales eliminar cuenta'],
    ['Privacidad de Zentrix Work', 'Legal', 'Zentrix Work', ['/work/privacidad/'], 'privacidad datos política work'],
    ['Privacidad de Zentrix Sales', 'Legal', 'Zentrix Sales', ['/sales/privacidad/'], 'privacidad datos política sales'],
    ['Soporte de Zentrix Check', 'Soporte', 'Zentrix Check', ['/soporte/#check'], 'soporte ayuda check garita eliminar cuenta'],
    ['Privacidad de Zentrix Check', 'Legal', 'Zentrix Check', ['/check/privacidad/'], 'privacidad datos política check garita'],
    ['Soluciones', 'Lo que hacemos', 'Zentrix', ['/soluciones/'], 'soluciones servicios'],
    ['Odoo en Venezuela', 'Implementación', 'Zentrix Software', ['/soluciones/odoo-venezuela/', '/software/'], 'odoo erp implementación localización venezuela'],
    ['Contacto', 'hola@zentrix.company', 'Zentrix', ['/contacto/', '/sales/contacto/', '/#contacto'], 'contacto demostración demo correo whatsapp']
  ];

  var SVG = {
    lupa: '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="8.75" cy="8.75" r="5.75" stroke="currentColor" stroke-width="1.8"/><path d="m13.2 13.2 4.05 4.05" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    reloj: '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.6"/><path d="M10 6.5V10l2.5 1.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    flecha: '<svg viewBox="0 0 20 20" width="16" height="16" fill="none" aria-hidden="true"><path d="M8 6h6v6M14 6l-8 8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    enter: '<svg viewBox="0 0 20 20" width="16" height="16" fill="none" aria-hidden="true"><path d="M15 5v4a3 3 0 0 1-3 3H5m0 0 3-3m-3 3 3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    vacio: '<svg viewBox="0 0 40 40" fill="none" aria-hidden="true"><circle cx="17.5" cy="17.5" r="10.5" stroke="currentColor" stroke-width="2"/><path d="m25.5 25.5 7 7M13.5 17.5h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
  };

  /* ---------- utilidades ---------- */
  function plano(s) { // sin tildes y en minúscula, carácter a carácter (misma longitud)
    var out = '';
    for (var i = 0; i < s.length; i++) out += s[i].normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().charAt(0) || s[i];
    return out;
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function el(tag, cls, html) { var e = D.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function track(nombre, params) {
    try { var a = W.zxAnalytics; if (a && typeof a.track === 'function') a.track(nombre, params); } catch (e) { /* nada */ }
  }
  var CLAVE = 'zx-buscar-recientes';
  function leerRecientes() { try { var v = JSON.parse(localStorage.getItem(CLAVE) || '[]'); return Array.isArray(v) ? v.filter(function (x) { return typeof x === 'string'; }).slice(0, 5) : []; } catch (e) { return []; } }
  function guardarReciente(q) {
    q = (q || '').trim(); if (q.length < 2) return;
    try { var v = leerRecientes().filter(function (x) { return plano(x) !== plano(q); }); v.unshift(q); localStorage.setItem(CLAVE, JSON.stringify(v.slice(0, 5))); } catch (e) { /* nada */ }
  }
  function borrarRecientes() { try { localStorage.removeItem(CLAVE); } catch (e) { /* nada */ } }
  function luminancia(color) {
    var m = /rgba?\(([^)]+)\)/.exec(color || ''); if (!m) return 1;
    var p = m[1].split(',').map(parseFloat); if (p.length > 3 && p[3] < .5) return null;
    return (0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]) / 255;
  }
  function fondoOscuro(nodo) {
    for (var n = nodo; n && n.nodeType === 1; n = n.parentElement) {
      var l = luminancia(getComputedStyle(n).backgroundColor);
      if (l !== null) return l < .4;
    }
    return false;
  }
  function paginaOscura() {
    var t = H.getAttribute('data-theme') || H.getAttribute('data-tema');
    if (t) return /dark|oscuro/.test(t);
    var cs = D.querySelector('meta[name="color-scheme"]');
    if (cs && /^\s*dark\s*$/.test(cs.content)) return true;
    return fondoOscuro(D.body);
  }

  /* ---------- pastilla ---------- */
  var hueco = D.getElementById('zx-buscar');
  if (!hueco) {
    var fila = D.querySelector('.cabecera__fila');
    if (!fila) return;
    hueco = el('div'); hueco.id = 'zx-buscar';
    fila.insertBefore(hueco, fila.querySelector('nav') || null);
  }
  var atajoTxt = MAC ? '⌘K' : 'Ctrl K';
  var pastilla = el('button', 'zxb-pastilla',
    SVG.lupa + '<span class="zxb-pastilla__txt">' + esc(TX.buscar) + '</span><kbd>' + atajoTxt + '</kbd>');
  pastilla.type = 'button';
  pastilla.setAttribute('aria-haspopup', 'dialog');
  pastilla.setAttribute('aria-label', TX.etiqueta + ' (' + atajoTxt + ')');
  pastilla.setAttribute('aria-keyshortcuts', (MAC ? 'Meta+K' : 'Control+K') + ' /');
  if (fondoOscuro(hueco)) pastilla.setAttribute('data-tema', 'oscuro');
  hueco.appendChild(pastilla);

  /* ---------- estado ---------- */
  var raiz, caja, input, eco, resto, lista, estado, cerrarBtn;
  var abierto = false, opener = null, activa = -1, opciones = [];
  var pf = null, pfPromesa = null, pfError = false;
  var terminos = null, terminosPromesa = null, rutasExisten = null;
  var seq = 0, temporizador = 0, temporizadorAnalitica = 0, sugerencia = '', ultimoTermino = '';

  function cargarPagefind() {
    if (pfPromesa) return pfPromesa;
    pfPromesa = import('/pagefind/pagefind.js').then(function (m) {
      pf = m;
      return Promise.resolve(m.options({ excerptLength: 22 })).then(function () { m.init(); return m; });
    }).catch(function () { pfError = true; return null; });
    return pfPromesa;
  }
  function cargarTerminos() {
    if (terminosPromesa) return terminosPromesa;
    terminosPromesa = fetch('/buscador/terminos-' + LANG + '.json').then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d) return null;
        // Prioridad para completar una palabra: las búsquedas populares, los temas
        // con página propia (el nombre del archivo: cobrar, turno, devoluciones…),
        // y después las palabras del sitio por frecuencia.
        var formas = {};
        (d.p || []).forEach(function (x) { var k = plano(x); if (!formas[k]) formas[k] = x; });
        var vistos = {}, palabras = [];
        function poner(x) { var k = plano(x); if (k.length > 2 && !vistos[k]) { vistos[k] = 1; palabras.push([k, formas[k] || x]); } }
        TX.populares.forEach(function (x) { if (x.indexOf(' ') === -1) poner(x); });
        (d.r || []).forEach(function (r) {
          var m = /\/([a-z0-9-]+)(?:\.html|\/)$/.exec(r);
          if (m && m[1].indexOf('-') === -1 && !/^(index|docs|en)$/.test(m[1])) poner(m[1]);
        });
        (d.p || []).forEach(poner);
        (d.t || []).forEach(function (x) { if (x.indexOf(' ') === -1) poner(x); });
        var frases = TX.populares.concat(ATAJOS.map(function (a) { return a[0]; }), d.t || [])
          .filter(function (x) { return x.indexOf(' ') !== -1; });
        terminos = { p: palabras, f: frases.map(function (x) { return [plano(x), x]; }) };
        rutasExisten = d.r || null;
        if (abierto) alEscribir(true);
        return terminos;
      }).catch(function () { return null; });
    return terminosPromesa;
  }

  /* ---------- ventana ---------- */
  function construir() {
    raiz = el('div', 'zxb'); raiz.hidden = true;
    raiz.innerHTML =
      '<div class="zxb__velo" data-cerrar></div>' +
      '<div class="zxb__caja" role="dialog" aria-modal="true" aria-label="' + esc(TX.etiqueta) + '">' +
        '<div class="zxb__campo">' + SVG.lupa +
          '<div class="zxb__entrada">' +
            '<span class="zxb__fantasma" aria-hidden="true"><span class="zxb__eco"></span><span class="zxb__resto"></span></span>' +
            '<input class="zxb__input" id="zxb-q" type="text" role="combobox" aria-autocomplete="both" aria-expanded="true"' +
            ' aria-haspopup="listbox" aria-controls="zxb-lista" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"' +
            ' enterkeyhint="search" maxlength="120" aria-label="' + esc(TX.etiqueta) + '" placeholder="' + esc(TX.placeholder) + '">' +
          '</div>' +
          '<button type="button" class="zxb__cerrar" data-cerrar aria-label="' + esc(TX.cerrar) + '">esc</button>' +
          '<button type="button" class="zxb__cerrar-movil" data-cerrar>' + esc(TX.cancelar) + '</button>' +
        '</div>' +
        '<div class="zxb__cuerpo"><div class="zxb__lista" id="zxb-lista" role="listbox" aria-label="' + esc(TX.resultados) + '"></div></div>' +
        '<div class="zxb-sr" role="status" aria-live="polite" aria-atomic="true"></div>' +
        '<div class="zxb__pie" aria-hidden="true">' +
          '<span><kbd>↑</kbd><kbd>↓</kbd>' + esc(TX.mover) + '</span>' +
          '<span><kbd>↵</kbd>' + esc(TX.abrir) + '</span>' +
          '<span><kbd>tab</kbd>' + esc(TX.completar) + '</span>' +
          '<span class="zxb__fin"><kbd>esc</kbd>' + esc(TX.salir) + '</span>' +
        '</div>' +
      '</div>';
    D.body.appendChild(raiz);
    caja = raiz.querySelector('.zxb__caja');
    input = raiz.querySelector('.zxb__input');
    eco = raiz.querySelector('.zxb__eco');
    resto = raiz.querySelector('.zxb__resto');
    lista = raiz.querySelector('.zxb__lista');
    estado = raiz.querySelector('[role="status"]');
    cerrarBtn = raiz.querySelector('.zxb__cerrar');

    raiz.addEventListener('click', function (e) {
      if (e.target.closest('[data-cerrar]')) { cerrar(); return; }
      if (e.target.closest('.zxb__borrar')) { borrarRecientes(); render(); input.focus(); return; }
      var op = e.target.closest('[role="option"]');
      if (op) { e.preventDefault(); elegir(opciones.indexOf(op), e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1); }
    });
    lista.addEventListener('mousemove', function (e) {
      var op = e.target.closest('[role="option"]');
      if (op && opciones.indexOf(op) !== activa) marcar(opciones.indexOf(op), false);
    });
    input.addEventListener('input', function () { alEscribir(false); });
    input.addEventListener('keydown', teclas);
    input.addEventListener('select', pintarFantasma);
    caja.addEventListener('keydown', function (e) { if (e.key === 'Tab') atrapar(e); if (e.key === 'Escape') { e.preventDefault(); cerrar(); } });
  }

  function abrir(q) {
    if (!raiz) construir();
    if (abierto) { if (q != null) { input.value = q; alEscribir(true); } input.focus(); return; }
    abierto = true;
    opener = D.activeElement && D.activeElement !== D.body ? D.activeElement : pastilla;
    raiz.setAttribute('data-tema', paginaOscura() ? 'oscuro' : 'claro');
    input.placeholder = W.matchMedia && W.matchMedia('(max-width: 640px)').matches ? TX.etiqueta : TX.placeholder;
    raiz.classList.remove('zxb--saliendo');
    raiz.hidden = false;
    H.style.overflow = 'hidden';
    pastilla.setAttribute('aria-expanded', 'true');
    cargarPagefind(); cargarTerminos();
    input.value = q != null ? q : '';
    alEscribir(true);
    input.focus({ preventScroll: true });
    if (input.value) input.setSelectionRange(input.value.length, input.value.length);
  }

  function cerrar() {
    if (!abierto) return;
    abierto = false;
    clearTimeout(temporizador);
    enviarBusqueda();
    pastilla.setAttribute('aria-expanded', 'false');
    var rm = W.matchMedia && W.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var fin = function () { if (!abierto) { raiz.hidden = true; raiz.classList.remove('zxb--saliendo'); } };
    if (rm) fin(); else { raiz.classList.add('zxb--saliendo'); setTimeout(fin, 120); }
    H.style.overflow = '';
    var destino = opener && D.contains(opener) ? opener : pastilla;
    try { destino.focus({ preventScroll: true }); } catch (e) { pastilla.focus(); }
  }

  function atrapar(e) {
    if (!e.shiftKey && sugerencia && D.activeElement === input) { e.preventDefault(); aceptar(); return; }
    var f = Array.prototype.filter.call(caja.querySelectorAll('input, button'), function (n) { return n.offsetParent !== null; });
    if (!f.length) return;
    var i = f.indexOf(D.activeElement);
    if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
  }

  /* ---------- autocompletado en gris ---------- */
  function calcularSugerencia(v) {
    if (!terminos || !v || /\s$/.test(v)) return '';
    var q = plano(v);
    var esFrase = v.trim().indexOf(' ') !== -1;
    if (esFrase) {
      for (var i = 0; i < terminos.f.length; i++) if (terminos.f[i][0].indexOf(q) === 0 && terminos.f[i][0].length > q.length) return terminos.f[i][1];
    }
    var m = /(\S+)$/.exec(v); if (!m || m[1].length < 2) return '';
    var ult = plano(m[1]), base = v.slice(0, v.length - m[1].length);
    // Si lo escrito ya es una palabra completa del sitio, no se le propone otra.
    for (var e = 0; e < terminos.p.length; e++) if (terminos.p[e][0] === ult) return '';
    for (var j = 0; j < terminos.p.length; j++) {
      var t = terminos.p[j];
      if (t[0].length > ult.length && t[0].indexOf(ult) === 0) {
        var forma = t[1];
        if (/^[A-ZÁÉÍÓÚÑ]/.test(m[1]) && /^[a-záéíóúñ]/.test(forma)) forma = forma.charAt(0).toUpperCase() + forma.slice(1);
        return base + forma;
      }
    }
    return '';
  }
  function pintarFantasma() {
    var v = input.value;
    var vale = sugerencia && plano(sugerencia).indexOf(plano(v)) === 0 && sugerencia.length > v.length &&
      input.selectionStart === v.length && input.selectionEnd === v.length && input.scrollWidth <= input.clientWidth + 1;
    eco.textContent = vale ? v : '';
    resto.innerHTML = vale ? esc(sugerencia.slice(v.length)) + '<kbd class="zxb__tab">tab</kbd>' : '';
  }
  function aceptar() {
    if (!sugerencia) return false;
    input.value = sugerencia;
    sugerencia = '';
    alEscribir(true);
    input.setSelectionRange(input.value.length, input.value.length);
    return true;
  }

  /* ---------- teclado ---------- */
  function teclas(e) {
    if (e.isComposing) return;
    var k = e.key;
    if (k === 'ArrowDown' || (k === 'n' && e.ctrlKey)) { e.preventDefault(); marcar(activa + 1 >= opciones.length ? 0 : activa + 1, true); }
    else if (k === 'ArrowUp' || (k === 'p' && e.ctrlKey)) { e.preventDefault(); marcar(activa <= 0 ? opciones.length - 1 : activa - 1, true); }
    else if (k === 'Home' && e.ctrlKey) { e.preventDefault(); marcar(0, true); }
    else if (k === 'End' && e.ctrlKey) { e.preventDefault(); marcar(opciones.length - 1, true); }
    else if (k === 'ArrowRight' && sugerencia && input.selectionStart === input.value.length) { if (aceptar()) e.preventDefault(); }
    else if (k === 'Enter') {
      e.preventDefault();
      if (activa >= 0) elegir(activa, e.metaKey || e.ctrlKey);
    }
  }
  function marcar(i, desplazar) {
    if (!opciones.length) { activa = -1; input.removeAttribute('aria-activedescendant'); return; }
    if (activa >= 0 && opciones[activa]) opciones[activa].setAttribute('aria-selected', 'false');
    activa = Math.max(0, Math.min(i, opciones.length - 1));
    var op = opciones[activa];
    op.setAttribute('aria-selected', 'true');
    input.setAttribute('aria-activedescendant', op.id);
    if (desplazar) op.scrollIntoView({ block: 'nearest' });
  }
  function elegir(i, nuevaPestana) {
    var op = opciones[i]; if (!op) return;
    var q = op.getAttribute('data-q');
    if (q != null) { input.value = q; alEscribir(true); input.focus(); return; }
    var url = op.getAttribute('href');
    var termino = input.value.trim();
    if (termino) { guardarReciente(termino); enviarBusqueda(); }
    track('select_content', { content_type: op.getAttribute('data-tipo') || 'search_result', item_id: url, search_term: termino });
    if (nuevaPestana || op.target === '_blank') { W.open(url, '_blank', 'noopener'); return; }
    var mismo = url.split('#')[0] === (location.pathname + location.search) && url.indexOf('#') !== -1;
    cerrar();
    if (mismo) location.hash = url.split('#')[1]; else location.href = url;
  }

  /* ---------- búsqueda ---------- */
  function alEscribir(inmediato) {
    var v = input.value;
    sugerencia = calcularSugerencia(v);
    pintarFantasma();
    clearTimeout(temporizador);
    if (!v.trim()) { seq++; render(); return; }
    renderAtajos(v.trim(), null);
    temporizador = setTimeout(function () { buscar(v.trim()); }, inmediato ? 0 : 120);
  }

  function atajosPara(q) {
    var qs = plano(q).split(/\s+/).filter(Boolean);
    if (!qs.length || plano(q).replace(/\s/g, '').length < 2) return [];
    var out = [];
    ATAJOS.forEach(function (a) {
      var palabras = plano(a[0] + ' ' + a[4]).split(/\s+/);
      var ok = qs.every(function (t) { return palabras.some(function (p) { return p.indexOf(t) === 0; }); });
      if (!ok) return;
      var url = a[3][0];
      if (rutasExisten && url.charAt(0) === '/') {
        url = a[3].filter(function (r) { return r.indexOf('#') !== -1 || rutasExisten.indexOf(r) !== -1; })[0] || a[3][a[3].length - 1];
      }
      out.push({ nombre: a[0], detalle: a[1], icono: ICONOS[a[2]], url: url });
    });
    return out.slice(0, 4);
  }

  function buscar(q) {
    var mio = ++seq;
    var esperando = setTimeout(function () { if (mio === seq) renderAtajos(q, 'cargando'); }, pf ? 90 : 0);
    cargarPagefind().then(function (m) {
      if (mio !== seq) return null;
      if (!m) { clearTimeout(esperando); renderAtajos(q, 'error'); return null; }
      return m.search(q).then(function (r) {
        if (mio !== seq || !r) return null;
        var top = r.results.slice(0, 10);
        return Promise.all(top.map(function (x) { return x.data(); })).then(function (datos) {
          clearTimeout(esperando);
          if (mio !== seq) return;
          renderResultados(q, datos, r);
          programarAnalitica(q, r.results.length);
        });
      });
    }).catch(function () { clearTimeout(esperando); if (mio === seq) renderAtajos(q, 'error'); });
  }

  function programarAnalitica(q, n) {
    clearTimeout(temporizadorAnalitica);
    temporizadorAnalitica = setTimeout(function () { enviarBusqueda(q, n); }, 900);
  }
  var pendiente = null;
  function enviarBusqueda(q, n) {
    if (q != null) pendiente = { q: q, n: n };
    clearTimeout(temporizadorAnalitica);
    if (!pendiente || pendiente.q === ultimoTermino) { pendiente = null; return; }
    ultimoTermino = pendiente.q;
    track('search', { search_term: pendiente.q });
    if (!pendiente.n) track('search_no_results', { search_term: pendiente.q });
    pendiente = null;
  }

  /* ---------- pintado ---------- */
  var nOp = 0;
  function opcion(cls, attrs, html) {
    var a = el('a', cls, html);
    a.id = 'zxb-o-' + (++nOp);
    a.setAttribute('role', 'option');
    a.setAttribute('aria-selected', 'false');
    a.tabIndex = -1;
    for (var k in attrs) if (attrs[k] != null) a.setAttribute(k, attrs[k]);
    return a;
  }
  function grupo(titulo, n, extra) {
    var g = el('div', 'zxb-grupo'); g.setAttribute('role', 'group');
    var id = 'zxb-g-' + (++nOp);
    var cab = el('div', 'zxb-grupo__cab', '<span id="' + id + '">' + esc(titulo) + '</span>' +
      (n != null ? '<span class="zxb-grupo__n" aria-hidden="true">' + n + '</span>' : '') + (extra || ''));
    g.setAttribute('aria-labelledby', id);
    g.appendChild(cab);
    return g;
  }
  function icono(src, ext) {
    return '<span class="zxb-op__ico">' + (src ? '<img src="' + esc(src) + '" alt="" width="36" height="36" decoding="async">' : '') + '</span>';
  }
  function bloqueAtajos(q) {
    var at = atajosPara(q);
    if (!at.length) return null;
    var g = grupo(TX.atajos, null);
    var fila = el('div', 'zxb-atajos');
    at.forEach(function (a) {
      var ext = /^https?:/.test(a.url);
      var o = opcion('zxb-atajo', { href: a.url, 'data-tipo': 'shortcut', target: ext ? '_blank' : null, rel: ext ? 'noopener' : null },
        '<img src="' + esc(a.icono) + '" alt="" width="28" height="28">' +
        '<span>' + esc(a.nombre) + (ext ? ' <small>↗</small>' : '') + '</span>');
      o.setAttribute('aria-label', a.nombre + ' — ' + a.detalle);
      fila.appendChild(o);
    });
    g.appendChild(fila);
    return g;
  }
  function esqueleto() {
    var g = el('div', 'zxb-grupo'); g.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < 3; i++) g.appendChild(el('div', 'zxb-esq', '<i></i><span><i></i><i></i><i></i></span>'));
    return g;
  }
  function montar(nodos, anuncio) {
    lista.textContent = '';
    nodos.forEach(function (n) { if (n) lista.appendChild(n); });
    opciones = Array.prototype.slice.call(lista.querySelectorAll('[role="option"]'));
    activa = -1;
    if (opciones.length) marcar(0, false); else input.removeAttribute('aria-activedescendant');
    lista.parentNode.scrollTop = 0;
    if (anuncio != null && estado.textContent !== anuncio) estado.textContent = anuncio;
  }

  function render() { // campo vacío: recientes y sugerencias
    var nodos = [];
    var rec = leerRecientes();
    if (rec.length) {
      var g = grupo(TX.recientes, rec.length, '<button type="button" class="zxb__borrar">' + esc(TX.borrar) + '</button>');
      rec.forEach(function (q) {
        g.appendChild(opcion('zxb-op zxb-op--simple', { href: '?q=' + encodeURIComponent(q), 'data-q': q },
          '<span class="zxb-op__ico">' + SVG.reloj + '</span><span class="zxb-op__txt"><span class="zxb-op__tit">' + esc(q) + '</span></span><span class="zxb-op__ir">' + SVG.enter + '</span>'));
      });
      nodos.push(g);
    }
    var gs = grupo(TX.sugerencias, TX.populares.length);
    TX.populares.forEach(function (q) {
      gs.appendChild(opcion('zxb-op zxb-op--simple', { href: '?q=' + encodeURIComponent(q), 'data-q': q },
        '<span class="zxb-op__ico">' + SVG.lupa + '</span><span class="zxb-op__txt"><span class="zxb-op__tit">' + esc(q) + '</span></span><span class="zxb-op__ir">' + SVG.enter + '</span>'));
    });
    nodos.push(gs);
    montar(nodos, '');
  }

  function renderAtajos(q, modo) {
    var nodos = [bloqueAtajos(q)];
    if (modo === 'cargando') nodos.push(esqueleto());
    else if (modo === 'error') nodos.push(el('div', 'zxb__vacio', '<b>' + esc(TX.error) + '</b>'));
    else {
      // Mientras llega la búsqueda se conservan los resultados anteriores.
      var previos = lista.querySelectorAll('.zxb-grupo--res');
      Array.prototype.forEach.call(previos, function (n) { nodos.push(n); });
    }
    var sel = activa >= 0 && opciones[activa] ? opciones[activa].getAttribute('href') : null;
    montar(nodos, modo === 'error' ? TX.error : null);
    if (sel) { for (var i = 0; i < opciones.length; i++) if (opciones[i].getAttribute('href') === sel) { marcar(i, false); break; } }
  }

  function rutaDe(d, tipo, seccion) {
    var prod = (d.filters && d.filters.producto && d.filters.producto[0]) || 'Zentrix';
    var partes = [prod];
    if (TX.ruta[tipo]) partes.push(TX.ruta[tipo]);
    if (seccion) partes.push(seccion);
    return partes.join(' › ');
  }
  function mejorSeccion(d) {
    var subs = (d.sub_results || []).filter(function (s) { return s.url && s.url.indexOf('#') !== -1 && s.title && s.title !== (d.meta && d.meta.title); });
    if (!subs.length) return null;
    subs.sort(function (a, b) { return (b.locations || []).length - (a.locations || []).length; });
    var s = subs[0];
    var total = (d.locations || []).length || 1;
    return (s.locations || []).length * 2 >= total ? s : null;
  }

  // ¿El título o la ruta nombran el término? («cobrar» → «Cobrarle a un cliente»)
  function nombra(q, d) {
    var raices = plano(q).split(/\s+/).filter(function (t) { return t.length > 2; })
      .map(function (t) { return t.replace(/[^a-z0-9]/g, '').slice(0, 5); }).filter(Boolean);
    var tit = plano(((d.meta && d.meta.title) || '') + ' ' + d.url.replace(/[\/._-]+/g, ' '));
    return raices.length > 0 && raices.every(function (r) { return new RegExp('(^|[^a-z0-9])' + r).test(tit); });
  }
  function depurar(q, datos) {
    // Pagefind ordena por el texto; se sube lo que nombra el término en el título.
    // Pagefind tolera erratas y a veces devuelve páginas sin ninguna coincidencia
    // visible («xilófono» → una página cualquiera): esas no se muestran.
    var cabezas = plano(q).split(/\s+/).map(function (t) { return t.replace(/[^a-z0-9]/g, '').slice(0, 3); }).filter(Boolean);
    function coincide(ext) {
      var m = (ext || '').match(/<mark>[^<]*/g) || [];
      return m.some(function (x) {
        var w = plano(x.slice(6)).replace(/[^a-z0-9]/g, '');
        return cabezas.some(function (c) { return w.indexOf(c) === 0; });
      });
    }
    datos = datos.filter(function (d) {
      return nombra(q, d) || coincide(d.excerpt) || (d.sub_results || []).some(function (s) { return coincide(s.excerpt); });
    });
    datos = datos.map(function (d, i) { return [nombra(q, d) ? 0 : 1, i, d]; })
      .sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; }).map(function (x) { return x[2]; });
    return datos;
  }
  function renderResultados(q, datos, r) {
    var nodos = [bloqueAtajos(q)];
    // Lo que ya está como acceso directo no se repite abajo.
    var yaArriba = atajosPara(q).map(function (a) { return a.url; });
    datos = depurar(q, datos).filter(function (d) { return yaArriba.indexOf(d.url) === -1; });
    if (!datos.length && yaArriba.length) { montar(nodos, yaArriba.length + ' ' + (yaArriba.length === 1 ? TX.n1 : TX.nN)); return; }
    if (!datos.length) {
      nodos.push(el('div', 'zxb__vacio', SVG.vacio + '<b>' + esc(TX.nada) + ' «' + esc(q) + '»</b>' +
        esc(TX.nadaPista) + ' <a href="mailto:' + TX.correo + '">' + TX.correo + '</a>.'));
      montar(nodos, TX.nada + ' ' + q);
      return;
    }
    var orden = [], grupos = {};
    datos.forEach(function (d) {
      var tipo = (d.filters && d.filters.tipo && d.filters.tipo[0]) || 'pagina';
      if (!grupos[tipo]) { grupos[tipo] = []; orden.push(tipo); }
      grupos[tipo].push(d);
    });
    orden.forEach(function (tipo) {
      var g = grupo(TX.tipos[tipo] || TX.tipos.pagina, grupos[tipo].length);
      g.classList.add('zxb-grupo--res');
      grupos[tipo].forEach(function (d) {
        var prod = (d.filters && d.filters.producto && d.filters.producto[0]) || 'Zentrix';
        var sec = nombra(q, d) ? null : mejorSeccion(d);
        var url = sec ? sec.url : d.url;
        var ext = sec ? sec.excerpt : d.excerpt;
        var tit = (d.meta && d.meta.title) || url;
        g.appendChild(opcion('zxb-op', { href: url, 'data-tipo': 'search_result' },
          icono(ICONOS[prod]) +
          '<span class="zxb-op__txt"><span class="zxb-op__tit">' + esc(tit) + '</span>' +
          '<span class="zxb-op__ruta">' + esc(rutaDe(d, tipo, sec && sec.title)) + '</span>' +
          (ext ? '<span class="zxb-op__ext">' + ext + '</span>' : '') + '</span>' +
          '<span class="zxb-op__ir">' + SVG.enter + '</span>'));
      });
      nodos.push(g);
    });
    var n = r.results.length;
    montar(nodos, n + ' ' + (n === 1 ? TX.n1 : TX.nN));
  }

  /* ---------- atajos globales ---------- */
  function editable(t) {
    return t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
  }
  D.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && !e.altKey && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      if (abierto) cerrar(); else abrir();
    } else if (e.key === '/' && !abierto && !e.metaKey && !e.ctrlKey && !e.altKey && !editable(e.target)) {
      e.preventDefault(); abrir();
    }
  });
  pastilla.addEventListener('click', function () { abrir(); });

  /* ---------- API para otros campos (el buscador de la 404 y el de /soporte/) ---------- */
  W.zxBuscar = { abrir: function (q) { abrir(q != null ? String(q).slice(0, 120) : null); } };

  /* ---------- ?q= (SearchAction) ---------- */
  try {
    var q0 = new URLSearchParams(location.search).get('q');
    if (q0 && q0.trim()) abrir(q0.trim().slice(0, 120));
  } catch (e) { /* nada */ }
})();
