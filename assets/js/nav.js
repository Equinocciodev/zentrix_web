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

/* Idioma: se recuerda la elección (ES/EN) y, en la portada española, se sugiere el inglés
   con un aviso discreto a quien navega en inglés o ya lo eligió. Nunca se redirige solo. */
(function () {
  'use strict';
  var CLAVE = 'zx-idioma';
  function leer() { try { return localStorage.getItem(CLAVE); } catch (e) { return null; } }
  function guardar(v) { try { localStorage.setItem(CLAVE, v); } catch (e) { /* sin almacenamiento */ } }
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-idioma]') : null;
    if (a) guardar(a.getAttribute('data-idioma'));
  });
  if (location.pathname !== '/' && location.pathname !== '/index.html') return;
  var pref = leer();
  var navegador = (navigator.languages && navigator.languages[0]) || navigator.language || '';
  if (pref === 'es' || (pref !== 'en' && !/^en\b/i.test(navegador))) return;
  var aviso = document.createElement('div');
  aviso.className = 'aviso-idioma';
  aviso.setAttribute('role', 'region');
  aviso.setAttribute('aria-label', 'Language');
  aviso.setAttribute('lang', 'en');
  aviso.innerHTML = '<p>This site is also available in English.</p>' +
    '<a class="boton boton--principal" href="/en/" data-idioma="en" hreflang="en">View in English</a>' +
    '<button type="button" class="aviso-idioma__cerrar" lang="es">Seguir en español</button>';
  aviso.querySelector('button').addEventListener('click', function () { guardar('es'); aviso.remove(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && aviso.isConnected) { guardar('es'); aviso.remove(); } });
  var montar = function () { document.body.appendChild(aviso); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', montar); else montar();
})();
