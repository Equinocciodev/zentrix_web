/* Cabecera de zentrix.company: menú móvil y mega-menú.
   Sin dependencias. Los <details> ya funcionan sin JS; esto añade: un solo panel abierto a
   la vez, cerrar con Esc o al pulsar fuera, y el botón del menú en pantallas pequeñas. */
(function () {
  'use strict';
  var nav = document.querySelector('.nav');
  if (!nav) return;
  var boton = nav.querySelector('.nav__abrir');
  var megas = Array.prototype.slice.call(nav.querySelectorAll('details.mega'));
  var raiz = document.documentElement;

  function cerrarMegas(excepto) {
    megas.forEach(function (d) { if (d !== excepto) d.open = false; });
  }

  function abrirMenu(abrir) {
    raiz.classList.toggle('nav--abierta', abrir);
    if (boton) {
      boton.setAttribute('aria-expanded', abrir ? 'true' : 'false');
    }
    if (!abrir) cerrarMegas(null);
  }

  megas.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) cerrarMegas(d);
    });
  });

  if (boton) {
    boton.addEventListener('click', function () {
      abrirMenu(!raiz.classList.contains('nav--abierta'));
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var abierto = megas.filter(function (d) { return d.open; })[0];
    if (abierto) {
      abierto.open = false;
      var s = abierto.querySelector('summary');
      if (s) s.focus();
    } else if (raiz.classList.contains('nav--abierta')) {
      abrirMenu(false);
      if (boton) boton.focus();
    }
  });

  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target)) {
      cerrarMegas(null);
      if (raiz.classList.contains('nav--abierta')) abrirMenu(false);
    }
  });

  // Al pasar de móvil a escritorio, el menú desplegado no debe quedarse abierto.
  var mq = window.matchMedia('(min-width: 1100px)');
  var alCambiar = function () { if (mq.matches) abrirMenu(false); };
  if (mq.addEventListener) mq.addEventListener('change', alCambiar); else if (mq.addListener) mq.addListener(alCambiar);
})();

/* Idioma: se recuerda la elección (ES/EN) y, en cualquier página española que tenga versión
   inglesa (<link rel="alternate" hreflang="en">), se sugiere esa misma página en inglés a quien
   navega en inglés o ya lo eligió. Nunca se redirige solo.
   La sugerencia es una píldora pequeña bajo la cabecera, junto al selector ES/EN, y nunca
   coincide con el aviso de cookies: solo aparece cuando ya hay decisión de cookies (en esta
   visita o en una anterior). Cerrarla la recuerda (zx-idioma = es). */
(function () {
  'use strict';
  var CLAVE = 'zx-idioma';
  function leer() { try { return localStorage.getItem(CLAVE); } catch (e) { return null; } }
  function guardar(v) { try { localStorage.setItem(CLAVE, v); } catch (e) { /* sin almacenamiento */ } }
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-idioma]') : null;
    if (a) guardar(a.getAttribute('data-idioma'));
  });
  if ((document.documentElement.getAttribute('lang') || '').slice(0, 2) !== 'es') return;
  var alterna = document.querySelector('link[rel="alternate"][hreflang="en"]');
  if (!alterna) return;  // sin par inglés (la 404, por ejemplo): no se sugiere nada
  var destino;
  try {
    var u = new URL(alterna.getAttribute('href'), location.href);
    // Los capítulos de la documentación tienen las mismas anclas en los dos idiomas.
    destino = u.pathname + (/\/docs\//.test(u.pathname) ? location.hash : '');
  } catch (e) { return; }
  var pref = leer();
  var navegador = (navigator.languages && navigator.languages[0]) || navigator.language || '';
  if (pref === 'es' || (pref !== 'en' && !/^en\b/i.test(navegador))) return;

  var aviso = document.createElement('div');
  aviso.className = 'aviso-idioma';
  aviso.setAttribute('role', 'region');
  aviso.setAttribute('aria-label', 'Language suggestion');
  aviso.setAttribute('lang', 'en');
  aviso.innerHTML =
    '<svg class="aviso-idioma__globo" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false">' +
    '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/>' +
    '<path d="M3 12h18M12 3c2.5 2.7 3.6 5.7 3.6 9s-1.1 6.3-3.6 9c-2.5-2.7-3.6-5.7-3.6-9S9.5 5.7 12 3z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>' +
    '<a class="aviso-idioma__ir" data-idioma="en" lang="en" hreflang="en">View in English <span aria-hidden="true">→</span></a>' +
    '<button type="button" class="aviso-idioma__cerrar" lang="es" aria-label="Cerrar: seguir en español" title="Seguir en español">' +
    '<span aria-hidden="true">×</span></button>';
  aviso.querySelector('a').setAttribute('href', destino);
  function quitar() {
    guardar('es');
    window.removeEventListener('resize', colocar);
    aviso.remove();
  }
  aviso.querySelector('button').addEventListener('click', quitar);
  aviso.addEventListener('keydown', function (e) { if (e.key === 'Escape') { e.stopPropagation(); quitar(); } });

  // Fija bajo la cabecera (no mueve el contenido) y, si el selector ES/EN está a la vista,
  // con la punta bajo el «EN».
  function colocar() {
    var cab = document.querySelector('.cabecera');
    var abajo = cab ? Math.round(cab.getBoundingClientRect().bottom) : 64;
    aviso.style.top = Math.max(abajo, 0) + 10 + 'px';
    var en = document.querySelector('.cabecera .idioma a[hreflang="en"]');
    var r = en && en.offsetParent ? en.getBoundingClientRect() : null;
    var ancho = document.documentElement.clientWidth;
    if (r && r.width) {
      var centro = r.left + r.width / 2;
      aviso.style.right = Math.max(12, Math.round(ancho - centro - 20)) + 'px';
      aviso.classList.add('aviso-idioma--punta');
    } else {
      // En móvil la píldora no lleva punta: si la barra de producto está a la vista, va debajo
      // de ella para no tapar sus enlaces.
      var barra = document.querySelector('.producto-barra');
      var fin = barra ? Math.round(barra.getBoundingClientRect().bottom) : 0;
      if (fin > abajo) aviso.style.top = fin + 10 + 'px';
      aviso.style.right = '';
      aviso.classList.remove('aviso-idioma--punta');
    }
  }
  var hecho = false;
  function montar() {
    if (hecho || leer() === 'es') return;
    hecho = true;
    document.body.appendChild(aviso);
    colocar();
    window.addEventListener('resize', colocar);
  }
  // Primero el consentimiento: si el aviso de cookies está pendiente, se espera a la decisión.
  function cuandoHayaDecision(fn) {
    var a = window.zxAnalytics;
    if (a && typeof a.consent === 'function' && a.consent() === null) {
      document.addEventListener('zx:consent', function () { window.setTimeout(fn, 600); }, { once: true });
    } else {
      fn();
    }
  }
  // Se muestra con la primera interacción (scroll, toque, tecla): así no compite con el
  // contenido principal en la primera pintura ni cuenta como LCP.
  var eventos = ['scroll', 'pointerdown', 'keydown', 'touchstart', 'mousemove'];
  var listo = false;
  var alInteractuar = function () {
    if (listo) return; listo = true;
    eventos.forEach(function (ev) { window.removeEventListener(ev, alInteractuar, true); });
    // analitica.js también es «defer»: se mira el consentimiento cuando ya se ha ejecutado.
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { cuandoHayaDecision(montar); });
    else cuandoHayaDecision(montar);
  };
  eventos.forEach(function (ev) { window.addEventListener(ev, alInteractuar, { capture: true, passive: true }); });
})();

/* Mega-menú: la tarjeta destacada cambia al pasar (o enfocar) cada producto o solución. */
(function () {
  'use strict';
  document.querySelectorAll('details.mega').forEach(function (d) {
    var vistas = d.querySelectorAll('.mega-dest__vista');
    if (!vistas.length) return;
    function ver(id) {
      var hay = false;
      vistas.forEach(function (v) { if (v.getAttribute('data-vista') === id) hay = true; });
      if (!hay) return;
      vistas.forEach(function (v) { v.hidden = v.getAttribute('data-vista') !== id; });
    }
    var inicial = vistas[0].getAttribute('data-vista');
    d.querySelectorAll('[data-ver]').forEach(function (a) {
      var id = a.getAttribute('data-ver');
      a.addEventListener('mouseenter', function () { ver(id); });
      a.addEventListener('focus', function () { ver(id); });
    });
    d.addEventListener('toggle', function () { if (d.open) ver(inicial); });
  });
})();
