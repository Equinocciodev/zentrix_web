/* Arma el correo del formulario de demostración y abre el cliente de correo. Sin esto, el formulario usa mailto: tal cual. */
(function () {
  var f = document.getElementById('formulario-demo');
  if (!f) return;
  f.addEventListener('submit', function (e) {
    if (!f.reportValidity()) return;
    e.preventDefault();
    var d = new FormData(f), lineas = [];
    d.forEach(function (v, k) { if (String(v).trim()) lineas.push(k + ': ' + v); });
    location.href = 'mailto:' + f.dataset.correo + '?subject=' + encodeURIComponent(f.dataset.asunto + ' — ' + (d.get('empresa') || '')) +
      '&body=' + encodeURIComponent(lineas.join('\n'));
  });
})();
