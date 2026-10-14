/* zentrix.company — analítica con consentimiento.
   GA4 (gtag.js) en la propiedad de GUUAO (G-H0HG8XPTES), filtrable por site=zentrix.
   - No se pide nada a Google hasta que la persona acepta. Rechazar no envía nada.
   - Consent Mode v2: analytics_storage denegado hasta aceptar; ad_storage,
     ad_user_data y ad_personalization siempre denegados.
   - Sin elección guardada, «Do Not Track» o «Global Privacy Control» cuentan como rechazo.
   - El enlace #zx-cookies del pie reabre las preferencias.
   - window.zxAnalytics.track(nombre, params): encola antes del consentimiento y descarta si se rechaza.
   Sin datos personales: los enlaces se miden sin consulta (?…) ni texto de formularios. */
(function () {
  'use strict';
  if (window.zxAnalytics) return;

  var ID = 'G-H0HG8XPTES';
  var CLAVE = 'zx-consent';           // 'granted' | 'denied'
  var VERSION = 1;                    // si cambia, se vuelve a preguntar
  var doc = document;
  var html = doc.documentElement;
  var en = /^en/i.test(html.getAttribute('lang') || '');
  var lang = en ? 'en' : 'es';

  var T = en ? {
    titulo: 'Cookies and analytics',
    texto: 'With your permission we measure visits with Google Analytics to improve the site. No advertising, no personal data.',
    aceptar: 'Accept', rechazar: 'Reject', mas: 'Learn more', mas_url: '/en/privacy/#cookies',
    senal: 'Your browser asks not to be tracked (Do Not Track / Global Privacy Control), so we measure nothing unless you accept here.',
    cerrar: 'Close'
  } : {
    titulo: 'Cookies y analítica',
    texto: 'Si lo permites, medimos las visitas con Google Analytics para mejorar el sitio. Sin publicidad y sin datos personales.',
    aceptar: 'Aceptar', rechazar: 'Rechazar', mas: 'Más información', mas_url: '/privacidad/#cookies',
    senal: 'Tu navegador pide no ser rastreado (Do Not Track / Global Privacy Control), así que no medimos nada salvo que aceptes aquí.',
    cerrar: 'Cerrar'
  };

  /* ---------- estado ---------- */
  function leer() {
    try {
      var v = JSON.parse(window.localStorage.getItem(CLAVE) || 'null');
      if (v && v.v === VERSION && (v.estado === 'granted' || v.estado === 'denied')) return v.estado;
    } catch (e) { /* almacenamiento bloqueado */ }
    return null;
  }
  function guardar(estado) {
    try { window.localStorage.setItem(CLAVE, JSON.stringify({ v: VERSION, estado: estado, t: Date.now() })); } catch (e) { /* nada */ }
  }
  var nav = window.navigator || {};
  var senal = nav.globalPrivacyControl === true || nav.doNotTrack === '1' || nav.doNotTrack === 'yes' ||
    window.doNotTrack === '1' || nav.msDoNotTrack === '1';

  var guardado = leer();
  var estado = guardado || (senal ? 'denied' : null);   // null = sin decidir
  var cola = [];
  var cargado = false;

  /* ---------- gtag ---------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  var forzado = doc.currentScript && doc.currentScript.getAttribute('data-grupo');

  function seccion() {
    if (forzado) return forzado;
    var p = location.pathname.replace(/^\/en(\/|$)/, '/').split('/').filter(Boolean);
    if (!p.length) return 'portada';
    var s = p[0].replace(/\.html$/, '');
    var mapa = { logistica: 'logistics', privacy: 'privacidad', '404': 'error' };
    s = mapa[s] || s;
    if (p.length > 1) {
      var sub = p[1].replace(/\.html$/, '');
      if (sub === 'en' && p[2]) sub = p[2].replace(/\.html$/, '');
      if (/^(docs|privacidad|privacy|soporte|support|terminos|terms|contacto|contact)$/.test(sub)) {
        var n = { privacy: 'privacidad', support: 'soporte', terms: 'terminos', contact: 'contacto' };
        return s + '/' + (n[sub] || sub);
      }
    }
    return s;
  }

  function enviar(nombre, params) {
    var p = {};
    for (var k in params) if (Object.prototype.hasOwnProperty.call(params, k)) p[k] = params[k];
    p.site = 'zentrix';
    p.language = lang;
    if (!p.content_group) p.content_group = seccion();
    gtag('event', nombre, p);
  }

  function cargar() {
    if (cargado) return;
    cargado = true;
    gtag('consent', 'default', {
      analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'
    });
    gtag('consent', 'update', { analytics_storage: 'granted' });
    gtag('set', 'ads_data_redaction', true);
    gtag('js', new Date());
    gtag('config', ID, {
      send_page_view: false,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      content_group: seccion(),
      site: 'zentrix'
    });
    var s = doc.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    doc.head.appendChild(s);
    while (cola.length) { var e = cola.shift(); enviar(e[0], e[1]); }
  }

  /* Carga diferida: tras la primera interacción o cuando el navegador esté ocioso. */
  function cuandoOcioso(fn) {
    var hecho = false;
    function una() {
      if (hecho) return;
      hecho = true;
      ['pointerdown', 'keydown', 'scroll', 'touchstart'].forEach(function (t) { window.removeEventListener(t, una, true); });
      fn();
    }
    ['pointerdown', 'keydown', 'scroll', 'touchstart'].forEach(function (t) { window.addEventListener(t, una, { capture: true, passive: true }); });
    if (window.requestIdleCallback) window.requestIdleCallback(una, { timeout: 4000 });
    else window.setTimeout(una, 2500);
  }

  function track(nombre, params) {
    if (typeof nombre !== 'string' || !nombre) return;
    params = params && typeof params === 'object' ? params : {};
    if (estado === 'denied') return;
    if (estado === 'granted' && cargado) { enviar(nombre, params); return; }
    if (cola.length < 50) cola.push([nombre, params]);
  }

  function decidir(nuevo) {
    var antes = estado;
    estado = nuevo;
    guardar(nuevo);
    if (nuevo === 'granted') {
      cargar();
    } else {
      cola.length = 0;
      if (cargado) {
        gtag('consent', 'update', { analytics_storage: 'denied' });
        if (antes === 'granted') borrarCookies();
      }
    }
  }

  /* Al retirar el consentimiento se borran las cookies _ga de este dominio. */
  function borrarCookies() {
    try {
      var host = location.hostname, dominios = ['', host, '.' + host.replace(/^www\./, '')];
      doc.cookie.split(';').forEach(function (c) {
        var n = c.split('=')[0].trim();
        if (!/^_ga/.test(n)) return;
        dominios.forEach(function (d) {
          doc.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
        });
      });
    } catch (e) { /* nada */ }
  }

  /* ---------- banner ---------- */
  var caja = null, previo = null;

  function estilos() {
    if (doc.getElementById('zx-ck-css')) return;
    var st = doc.createElement('style');
    st.id = 'zx-ck-css';
    st.textContent =
      '.zx-ck{position:fixed;z-index:2147483000;left:16px;right:16px;bottom:16px;max-width:560px;margin:0 auto;' +
      'background:#090D12;color:#fff;border:1px solid rgba(255,255,255,.14);border-radius:16px;' +
      'box-shadow:0 12px 40px rgba(9,13,18,.35);padding:20px 20px 18px;' +
      'font:400 .9375rem/1.5 Inter,"Inter reserva",system-ui,-apple-system,"Segoe UI",sans-serif;box-sizing:border-box}' +
      '.zx-ck *{box-sizing:border-box}' +
      '.zx-ck::before{content:"";position:absolute;left:20px;top:0;width:40px;height:3px;border-radius:0 0 3px 3px;background:#C7FA46}' +
      '.zx-ck__t{margin:0 0 6px;font-size:1rem;font-weight:700;letter-spacing:-.01em;color:#fff}' +
      '.zx-ck__p{margin:0;color:#AEB6C2}' +
      '.zx-ck__p a{color:#A6B6FF;text-decoration:underline;text-underline-offset:2px}' +
      '.zx-ck__s{margin:10px 0 0;font-size:.8125rem;color:#AEB6C2}' +
      '.zx-ck__b{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}' +
      '.zx-ck button{appearance:none;font:inherit;font-weight:600;font-size:.9375rem;min-height:44px;padding:10px 16px;' +
      'border-radius:12px;cursor:pointer;border:2px solid transparent;transition:background-color .15s,color .15s}' +
      '.zx-ck__si{background:#244DFF;color:#fff}.zx-ck__si:hover{background:#1B3EE0}' +
      '.zx-ck__no{background:#fff;color:#090D12}.zx-ck__no:hover{background:#E6E9EF}' +
      '.zx-ck button:focus-visible,.zx-ck a:focus-visible{outline:3px solid #C7FA46;outline-offset:2px}' +
      '.zx-ck__x{position:absolute;top:8px;right:8px;width:36px;min-height:36px!important;padding:0!important;' +
      'background:transparent;color:#AEB6C2;border-radius:10px!important;font-size:1.25rem!important;line-height:1}' +
      '.zx-ck__x:hover{color:#fff;background:rgba(255,255,255,.08)}' +
      '@media (min-width:768px){.zx-ck{left:24px;right:auto;bottom:24px;margin:0}}' +
      '@media (prefers-reduced-motion:no-preference){.zx-ck{animation:zx-ck-in .25s ease-out}}' +
      '@keyframes zx-ck-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}' +
      '@media print{.zx-ck{display:none}}';
    doc.head.appendChild(st);
  }

  function cerrar(devolverFoco) {
    if (!caja) return;
    caja.remove();
    caja = null;
    doc.removeEventListener('keydown', alEscape, true);
    if (devolverFoco && previo && previo.focus) { try { previo.focus(); } catch (e) { /* nada */ } }
    previo = null;
  }

  function alEscape(e) {
    if (e.key === 'Escape' && caja && caja.getAttribute('data-reabierto') === '1') { e.preventDefault(); cerrar(true); }
  }

  function mostrar(reabierto) {
    if (caja) { caja.querySelector('button').focus(); return; }
    estilos();
    caja = doc.createElement('section');
    caja.className = 'zx-ck';
    caja.setAttribute('role', 'region');
    caja.setAttribute('aria-labelledby', 'zx-ck-t');
    caja.setAttribute('lang', lang);
    if (reabierto) caja.setAttribute('data-reabierto', '1');
    caja.innerHTML =
      '<h2 class="zx-ck__t" id="zx-ck-t"></h2>' +
      '<p class="zx-ck__p"><span></span> <a></a></p>' +
      (senal && !guardado ? '<p class="zx-ck__s"></p>' : '') +
      '<div class="zx-ck__b"><button type="button" class="zx-ck__no"></button><button type="button" class="zx-ck__si"></button></div>' +
      (reabierto ? '<button type="button" class="zx-ck__x"><span aria-hidden="true">×</span></button>' : '');
    caja.querySelector('h2').textContent = T.titulo;
    caja.querySelector('.zx-ck__p span').textContent = T.texto;
    var a = caja.querySelector('.zx-ck__p a');
    a.textContent = T.mas;
    a.href = T.mas_url;
    var s = caja.querySelector('.zx-ck__s');
    if (s) s.textContent = T.senal;
    var no = caja.querySelector('.zx-ck__no'), si = caja.querySelector('.zx-ck__si');
    no.textContent = T.rechazar;
    si.textContent = T.aceptar;
    if (estado) (estado === 'granted' ? si : no).setAttribute('aria-pressed', 'true');
    no.addEventListener('click', function () { decidir('denied'); cerrar(reabierto); });
    si.addEventListener('click', function () { decidir('granted'); cerrar(reabierto); });
    var x = caja.querySelector('.zx-ck__x');
    if (x) { x.setAttribute('aria-label', T.cerrar); x.addEventListener('click', function () { cerrar(true); }); }
    doc.body.appendChild(caja);
    if (reabierto) {
      doc.addEventListener('keydown', alEscape, true);
      (estado === 'granted' ? si : no).focus();
    }
  }

  /* ---------- clics ---------- */
  function limpia(u) {
    if (/^mailto:/i.test(u.href)) return 'mailto:' + u.href.slice(7).split('?')[0];
    // De Google Play se conserva solo el id de la app; del sitio, el ancla.
    var extra = u.host === location.host ? u.hash : (u.hostname === 'play.google.com' && u.searchParams.get('id') ? '?id=' + u.searchParams.get('id') : '');
    return u.protocol + '//' + u.host + u.pathname + extra;
  }

  function tipoDe(u) {
    var h = u.hostname.replace(/^www\./, '');
    if (u.protocol === 'mailto:') return 'correo';
    if (u.protocol === 'tel:') return 'telefono';
    if (h === 'wa.me' || /(^|\.)whatsapp\.com$/.test(h)) return 'whatsapp';
    if (h === 'play.google.com' || h === 'apps.apple.com' || h === 'itunes.apple.com') return 'tienda';
    if (h === 'traza.technology' || /\.traza\.technology$/.test(h)) return 'traza';
    if (u.host === location.host && (/\/(contacto|contact)(\/|\.html|$)/.test(u.pathname) || /^#(contacto|contact|demo)$/.test(u.hash))) return 'contacto';
    return null;
  }

  doc.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    if (a.id === 'zx-cookies' || a.hasAttribute('data-zx-abrir')) { e.preventDefault(); previo = a; mostrar(true); return; }
    var u;
    try { u = new URL(a.getAttribute('href'), location.href); } catch (err) { return; }

    // Cambio de idioma: el selector del pie, o un enlace con lang y hreflang iguales a otro idioma.
    var hl = (a.getAttribute('hreflang') || '').slice(0, 2).toLowerCase();
    var al = (a.getAttribute('lang') || '').slice(0, 2).toLowerCase();
    if (hl && hl !== lang && (a.closest('.pie__idioma, [data-zx-idioma]') || al === hl)) {
      track('language_change', { language_from: lang, language_to: hl, link_url: limpia(u) });
      return;
    }

    var tipo = tipoDe(u);
    if (!tipo) return;
    track('click', {
      link_type: tipo,
      link_url: limpia(u),
      link_domain: u.protocol === 'mailto:' ? 'mailto' : u.hostname,
      outbound: u.protocol !== 'http:' && u.protocol !== 'https:' ? true : u.host !== location.host
    });
  }, true);

  /* ---------- API ---------- */
  window.zxAnalytics = {
    track: track,
    consent: function () { return estado; },
    open: function () { mostrar(true); }
  };

  /* Solo se conservan los parámetros de campaña (utm_*); el resto de la consulta no se envía. */
  function utm() {
    try {
      var q = new URLSearchParams(location.search), o = new URLSearchParams();
      q.forEach(function (v, k) { if (/^utm_[a-z_]+$/.test(k)) o.append(k, v.slice(0, 100)); });
      var t = o.toString();
      return t ? '?' + t : '';
    } catch (e) { return ''; }
  }

  /* page_view queda en cola hasta que haya consentimiento. */
  track('page_view', {
    page_location: location.protocol + '//' + location.host + location.pathname + utm(),
    page_title: doc.title,
    content_group: seccion()
  });

  function iniciar() {
    if (estado === 'granted') cuandoOcioso(cargar);
    else if (estado === null) cuandoOcioso(function () { mostrar(false); });
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
