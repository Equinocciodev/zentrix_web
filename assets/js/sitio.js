/* zentrix.company — movimiento del sitio.
   Solo añade clases y anima cifras: sin este archivo el contenido se lee igual.
   Con prefers-reduced-motion no anima nada. */
(function () {
  'use strict';
  var reducido = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var elementos = document.querySelectorAll('.revela, [data-anima]');
  var cifras = document.querySelectorAll('[data-cuenta]');

  function contar(el) {
    var fin = parseInt(el.getAttribute('data-cuenta'), 10);
    if (isNaN(fin) || fin < 1) return;
    var inicio = null;
    var duracion = 1400;
    function paso(t) {
      if (inicio === null) inicio = t;
      var x = Math.min((t - inicio) / duracion, 1);
      var e = 1 - Math.pow(1 - x, 3);
      el.textContent = String(Math.round(fin * e));
      if (x < 1) window.requestAnimationFrame(paso);
    }
    el.textContent = '0';
    window.requestAnimationFrame(paso);
  }

  // Las animaciones infinitas solo corren en las secciones que se ven: fuera de la pantalla se pausan
  // (.zx-fuera en sitio.css). Menos trabajo de pintado mientras se lee, se toca o se escribe (INP).
  if (!reducido && 'IntersectionObserver' in window) {
    var vigia = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) { e.target.classList.toggle('zx-fuera', !e.isIntersecting); });
    }, { rootMargin: '200px 0px' });
    document.querySelectorAll('main > section, main > div > section, .pie').forEach(function (s) { vigia.observe(s); });
  }

  if (reducido || !('IntersectionObserver' in window)) {
    elementos.forEach(function (el) { el.classList.add('visible'); });
    return;
  }

  var observador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (entrada) {
      if (!entrada.isIntersecting) return;
      var el = entrada.target;
      el.classList.add('visible');
      el.querySelectorAll('[data-cuenta]').forEach(contar);
      if (el.hasAttribute('data-cuenta')) contar(el);
      observador.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

  elementos.forEach(function (el) { observador.observe(el); });
  cifras.forEach(function (el) {
    if (!el.closest('.revela, [data-anima]')) observador.observe(el);
  });
})();
