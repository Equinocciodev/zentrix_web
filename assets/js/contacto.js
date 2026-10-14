/* Selector de motivo de /contacto/ y /en/contact/: el motivo y el producto solo cambian el asunto
   (y el texto de partida) del correo y del WhatsApp. Sin JavaScript, los enlaces llevan el motivo
   por defecto. ?motivo=demo|soporte|alianzas|prensa y ?producto=work|sales|… lo preseleccionan
   (lo usan las redirecciones de /sales/contacto/ y los enlaces de /soporte/). */
(function () {
  var f = document.getElementById('motivo-form');
  var datos = document.getElementById('motivo-datos');
  if (!f || !datos) return;
  var D;
  try { D = JSON.parse(datos.textContent); } catch (e) { return; }
  var correo = document.getElementById('motivo-correo');
  var wa = document.getElementById('motivo-wa');
  var sel = f.querySelector('select[name="producto"]');
  var CORREO = { demo: 'hola@zentrix.company', soporte: 'soporte@zentrix.company', alianzas: 'hola@zentrix.company', prensa: 'hola@zentrix.company' };

  function motivo() {
    var r = f.querySelector('input[name="motivo"]:checked');
    return r ? r.value : 'demo';
  }
  function pintar() {
    var m = motivo();
    var p = sel.value;
    var nombre = p ? sel.options[sel.selectedIndex].text : 'Zentrix';
    var asunto = (D.asuntos[m] || '').replace('{p}', nombre);
    var cuerpo = (D.cuerpos[m] || '').replace('{extra}', m === 'demo' && p === 'sales' ? D.extra_sales : '');
    correo.href = 'mailto:' + CORREO[m] + '?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent(cuerpo);
    wa.href = 'https://wa.me/584123469712?text=' + encodeURIComponent(asunto);
    var notas = f.querySelectorAll('.motivo__nota');
    for (var i = 0; i < notas.length; i++) notas[i].hidden = notas[i].getAttribute('data-motivo') !== m;
    sel.closest('.motivo__producto').hidden = m === 'alianzas' || m === 'prensa';
  }
  try {
    var q = new URLSearchParams(location.search);
    var m0 = q.get('motivo'), p0 = q.get('producto');
    if (m0) { var r = f.querySelector('input[name="motivo"][value="' + m0.replace(/[^a-z]/g, '') + '"]'); if (r) r.checked = true; }
    if (p0) { var v = p0.replace(/[^a-z]/g, ''); if (sel.querySelector('option[value="' + v + '"]')) sel.value = v; }
  } catch (e) { /* nada */ }
  f.addEventListener('change', pintar);
  pintar();
})();
