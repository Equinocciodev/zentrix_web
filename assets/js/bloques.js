/* zentrix.company — bloques: el brillo que sigue al cursor en tarjetas y teselas (.bq-brillo).
   Solo con ratón y sin prefers-reduced-motion. Sin este archivo el brillo aparece centrado. */
(function () {
  'use strict';
  var mm = window.matchMedia && window.matchMedia.bind(window);
  if (!mm || mm('(prefers-reduced-motion: reduce)').matches || !mm('(hover: hover) and (pointer: fine)').matches) return;
  var pendiente = null, x = 0, y = 0, el = null;
  document.addEventListener('pointermove', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('.bq-brillo') : null;
    if (!t) return;
    el = t;
    x = e.clientX; y = e.clientY;
    if (pendiente) return;
    pendiente = window.requestAnimationFrame(function () {
      pendiente = null;
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (x - r.left) + 'px');
      el.style.setProperty('--my', (y - r.top) + 'px');
    });
  }, { passive: true });
})();
