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
