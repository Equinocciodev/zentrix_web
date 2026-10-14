"""Soporte, contacto y legal unificados: /soporte/ (/en/support/), el selector de motivo de
/contacto/ (/en/contact/) y el índice /legal/ (/en/legal/).

El contenido de cada app es el que tenían /work/soporte/ y /sales/soporte/ (y sus versiones en
inglés), reorganizado en una sola página. Esas rutas viejas redirigen aquí (ver REDIRECCIONES en
generar.py), con sus anclas antiguas traducidas por ALIAS.

Las anclas de borrado de cuenta son estables: las declaran las fichas de Google Play y App Store.
    ES: /soporte/#eliminar-cuenta-work   /soporte/#eliminar-cuenta-sales
    EN: /en/support/#delete-account-work /en/support/#delete-account-sales
"""
from urllib.parse import quote

from sitio import MONO, TRAZA_URL, TRAZA_ICONO, SVG_EXTERNO

WA = 'https://wa.me/584123469712'
WA_TXT = '+58 412-346 9712'

# Las monogramas de la suite (orden del mega-menú). (clave del monograma, ancla, nombre, ruta ES)
SUITE = [('work', 'work', 'Zentrix Work', '/work/'), ('sales', 'sales', 'Zentrix Sales', '/sales/'),
         ('ai', 'ai', 'Zentrix AI', '/ai/'), ('logistica', 'logistics', 'Zentrix Logistics', '/logistics/'),
         ('cloud', 'cloud', 'Zentrix Cloud', '/cloud/'), ('labs', 'labs', 'Zentrix Labs', '/labs/'),
         ('software', 'software', 'Zentrix Software', '/software/')]

# Anclas de las páginas viejas → anclas de /soporte/ (las usa la página de redirección).
ALIAS = {
    'work_es': {'eliminar-datos': 'eliminar-cuenta-work', 'preguntas': 'preguntas-work', 'ficha-t': 'ficha-work'},
    'sales_es': {'eliminar-datos': 'eliminar-cuenta-sales', 'ficha-t': 'ficha-sales', 'demo': 'motivo', 'soporte': 'sales'},
    'work_en': {'eliminar-datos': 'delete-account-work', 'preguntas': 'preguntas-work', 'ficha-t': 'ficha-work'},
    'sales_en': {'delete-data': 'delete-account-sales', 'eliminar-datos': 'delete-account-sales', 'ficha-t': 'ficha-sales',
                 'demo': 'motivo', 'soporte': 'sales'},
}


def mailto(correo, asunto):
    return f'mailto:{correo}?subject={quote(asunto)}'


def mono(clave, tam=40):
    return f'<img src="{MONO}/{clave}_icono.svg" alt="" width="{tam}" height="{tam}" loading="lazy" decoding="async">'


# ── Textos de cada app (de las páginas de soporte anteriores) ──────────────
WORK_FAQ = {
    'es': [
        ('sin-cuenta', 'No tengo cuenta. ¿Cómo me registro?',
         'No hay registro: la app es solo para el personal de las empresas que usan Zentrix Work, y la cuenta la crea tu encargado. Si eres cliente de la tienda, lo que buscas es la app de clientes de esa empresa.'),
        ('pin', 'Olvidé mi PIN',
         'En la pantalla del PIN, toca <strong>¿Olvidaste tu PIN?</strong> Vuelves a entrar con tu correo y tu contraseña y creas un PIN nuevo. <strong>No pierdes tu turno ni el trabajo que tenías a medias.</strong>'),
        ('contrasena', 'Olvidé mi contraseña',
         'Es la misma contraseña de tu cuenta de la empresa. Pídele a tu encargado que te la restablezca, o escríbenos.'),
        ('no-suena', 'No me suenan los pedidos',
         'Revisa que estés <strong>encendido</strong> en una tienda: apagado, la app no suena nunca. Si estás encendido, mira que las notificaciones de Zentrix Work estén permitidas y que el teléfono no esté en «No molestar». Al encenderte, la app te avisa si algo de eso está mal.'),
        ('no-enciende', 'No me deja encenderme',
         'El servidor comprueba que estés en la tienda, que tengas permiso en ella y que esa tarea esté habilitada. El mensaje que ves en pantalla dice cuál de esas falló. Si crees que es un error, díselo a tu encargado.'),
        ('se-apago', 'Se me apagó el turno solo',
         'Pasa cuando la app lleva mucho rato sin saber de ti: el teléfono sin señal o la app sin usar. Es a propósito, para que tu teléfono no siga sonando si te fuiste. Vuelve a encenderte y sigues.'),
        ('telefono-perdido', 'Perdí el teléfono o cambié de teléfono',
         'Avísale a tu encargado para que cierre tu acceso en el teléfono viejo. En el nuevo, instala la app y entra con tu correo y tu contraseña. Lo que la app guardaba en el teléfono viejo no se copia al nuevo, a propósito.'),
        ('dejo-empresa', 'Dejé de trabajar en la empresa',
         'Tu acceso se cierra desde el sistema de la empresa y la app deja de funcionar en tu teléfono. Puedes desinstalarla. Para pedir que se borren tus datos, mira <a href="#eliminar-cuenta-work">eliminar tu cuenta o tus datos</a>.'),
    ],
    'en': [
        ('sin-cuenta', 'I don’t have an account. How do I sign up?',
         'There is no sign-up: the app is only for the staff of companies that use Zentrix Work, and your manager creates your account. If you are a customer of the store, what you are looking for is that company’s customer app.'),
        ('pin', 'I forgot my PIN',
         'On the PIN screen, tap <strong>Forgot your PIN?</strong> You sign in again with your email and password and create a new PIN. <strong>You don’t lose your shift or any work you had in progress.</strong>'),
        ('contrasena', 'I forgot my password',
         'It is the same password as your company account. Ask your manager to reset it, or write to us.'),
        ('no-suena', 'My orders don’t make a sound',
         'Make sure you are <strong>clocked in</strong> at a store: when you are clocked out, the app never makes a sound. If you are clocked in, check that notifications for Zentrix Work are allowed and that the phone is not on “Do Not Disturb.” When you clock in, the app warns you if any of that is wrong.'),
        ('no-enciende', 'It won’t let me clock in',
         'The server checks that you are at the store, that you have permission there and that the task is enabled. The message on screen tells you which of those failed. If you think it is a mistake, tell your manager.'),
        ('se-apago', 'My shift ended on its own',
         'This happens when the app has not heard from you for a long time: the phone has no signal or the app has not been used. It is on purpose, so your phone doesn’t keep ringing if you have left. Clock in again and carry on.'),
        ('telefono-perdido', 'I lost my phone or got a new one',
         'Let your manager know so they can close your access on the old phone. On the new one, install the app and sign in with your email and password. What the app stored on the old phone is not copied to the new one, on purpose.'),
        ('dejo-empresa', 'I no longer work at the company',
         'Your access is closed from the company’s system and the app stops working on your phone. You can uninstall it. To ask for your data to be deleted, see <a href="#delete-account-work">delete your account or your data</a>.'),
    ],
}

TX = {
    'es': {
        'ante': 'Soporte', 'h1': '¿En qué te ayudamos?',
        'lead': 'Preguntas frecuentes, acceso, manuales y tus datos, de todas las apps de Zentrix en un solo lugar. Si no lo encuentras, te responde una persona en menos de un día hábil.',
        'buscar_l': 'Buscar en el sitio', 'buscar_ph': 'Busca: PIN, contraseña, cuenta…', 'buscar_b': 'Buscar',
        'elige': 'Elige tu producto', 'chips_l': 'Ir al soporte de cada producto', 'eliminar_atajo': 'Eliminar tu cuenta',
        'eliminar_atajo_t': 'Instrucciones de Zentrix Work y Zentrix Sales para pedir el borrado de tu cuenta y tus datos.',
        'work_lead': 'Para casi todo, tu primer contacto es <strong>tu encargado de tienda</strong>: es quien te da de alta, te habilita las tareas y puede cortar el acceso si pierdes el teléfono. Para lo demás, escríbenos.',
        'work_mail_s': 'Soporte — Zentrix Work',
        'work_mail_p': 'Pon en el asunto <em>Soporte — Zentrix Work</em> y cuéntanos tu correo de la app, tu tienda y qué pasó. Si puedes, agrega una captura.',
        'preguntas': 'Preguntas rápidas', 'manual': 'Manual', 'acceso': 'Acceso y contraseña',
        'work_manual': 'El <a href="{docs}">manual del operador</a> explica paso a paso el turno, los pedidos, la preparación, la entrega y las devoluciones.',
        'eliminar_t': 'Eliminar tu cuenta o tus datos',
        'work_del_p': 'La app no permite crear cuentas, así que tampoco se borran desde ella: la cuenta la crea tu empresa y la cierra tu empresa. Para pedirlo:',
        'work_del_1': 'Escribe a <a href="{m}">soporte@zentrix.company</a> con el asunto <em>Solicitud de datos — Zentrix Work</em>, o díselo a tu encargado.',
        'work_del_s': 'Solicitud de datos — Zentrix Work',
        'work_del_2': 'Indica tu nombre y el correo de tu cuenta, y si quieres <strong>ver</strong>, <strong>corregir</strong> o <strong>eliminar</strong> tus datos.',
        'del_3': 'Te respondemos en un máximo de <strong>30 días hábiles</strong>.',
        'work_del_f': 'Lo que se borra, lo que se conserva por obligación legal y por cuánto tiempo está en la <a href="{priv}#c7">política de privacidad, cláusula 7</a>. <strong>Cerrar sesión o desinstalar la app no borra nada del servidor.</strong>',
        'sales_lead': 'Te contesta una persona del equipo de Zentrix, en español y en menos de un día hábil.',
        'sales_mail_s': 'Soporte — Zentrix Sales', 'tel_wa': 'Teléfono y WhatsApp',
        'sales_calle_t': 'Si usas Zentrix Sales en la calle',
        'sales_calle': '<p>La cuenta te la crea y te la entrega tu empresa: la aplicación no permite registrarse y no hay forma de darse de alta desde aquí. Si no puedes entrar, si algo no te carga o si un pedido no llegó, escríbenos con tu correo de vendedor y el nombre de tu empresa.</p>'
                       '<p>Desde la app también puedes escribirnos: en <strong>Perfil › Acerca de › Reportar un problema</strong>. Cuéntanos qué pasó y con qué cliente por su código, no por su nombre.</p>',
        'sales_manual': 'Antes de escribir, mira el <a href="{docs}">manual del vendedor</a>: explica pantalla por pantalla qué hace cada cosa.',
        'sales_emp_t': 'Si tu empresa ya usa Zentrix Sales',
        'sales_emp': 'Altas y bajas de vendedores, permisos, empresas y almacenes, o la integración con tu ERP. Escríbenos desde el correo de la empresa y dinos qué necesitas cambiar.',
        'sales_del_p': 'Qué recoge la aplicación, para qué y cuánto tiempo se guarda está en la <a href="{priv}">política de privacidad</a>. Para pedir el acceso, la corrección o la eliminación de tus datos:',
        'sales_del_1': 'Escribe a <a href="{m}">hola@zentrix.company</a> con el asunto <em>Solicitud de datos — Zentrix Sales</em>.',
        'sales_del_s': 'Solicitud de datos — Zentrix Sales',
        'sales_del_2': 'Indica tu nombre, tu correo de vendedor o tu RIF si eres cliente de una empresa que usa la app, y qué quieres: <strong>ver</strong>, <strong>corregir</strong> o <strong>eliminar</strong>.',
        'sales_del_f': 'Lo que se conserva por obligación legal, y por cuánto tiempo, está en la <a href="{priv}#c7">cláusula 7 de la política</a>. <strong>Cerrar sesión no elimina datos del servidor:</strong> solo retira las credenciales del teléfono.',
        'ficha': 'Datos de la app', 'f_app': 'Aplicación', 'f_desc': 'Descarga', 'f_resp': 'Responsable', 'f_dir': 'Dirección legal',
        'f_correo': 'Correo de soporte', 'f_tel': 'Teléfono', 'f_resp_t': 'Tiempo de respuesta', 'f_docs': 'Documentos',
        'work_app': 'Zentrix Work (<code>com.leiros.guuaowork</code>), para Android.',
        'sales_app': 'Zentrix Sales (<code>com.leiros.vendoo</code>). Android 7.0 o superior e iOS 15 o superior.',
        'dir': '10302 NW South River Drive, Medley, FL 33178, Estados Unidos',
        'tel': '+58 412-346 9712, también por <a href="' + WA + '">WhatsApp</a>', 'menos_dia': 'Menos de un día hábil.',
        'priv': 'Política de privacidad', 'term_w': 'Términos de uso', 'term_s': 'Términos de servicio',
        'man_w': 'Manual', 'man_s': 'Manual del vendedor',
        'otros_ante': 'Resto de la suite', 'otros_t': 'Sin app publicada todavía.',
        'otros_p': 'Estos productos no tienen app que instalar: se trabajan como proyecto con tu equipo. Para cualquier duda, escríbenos desde contacto.',
        'otros_cta': 'Escribir', 'prox': 'Próximamente', 'traza_l': 'Tiene sitio y soporte propios en traza.technology.',
        'contactar_ante': 'Contacto', 'contactar_t': '¿No encuentras lo que buscas?',
        'contactar_p': 'Te responde una persona, en español, en menos de un día hábil. Si es sobre una app, dinos cuál y desde qué correo entras.',
        'contactar_s': 'Soporte — Zentrix', 'todas': 'Todas las formas de contacto',
    },
    'en': {
        'ante': 'Support', 'h1': 'How can we help?',
        'lead': 'Common questions, access, manuals and your data for every Zentrix app, in one place. If you can’t find it, a person replies within one business day.',
        'buscar_l': 'Search the site', 'buscar_ph': 'Search: PIN, password, delete account…', 'buscar_b': 'Search',
        'elige': 'Pick your product', 'chips_l': 'Go to each product’s support', 'eliminar_atajo': 'Delete your account',
        'eliminar_atajo_t': 'Zentrix Work and Zentrix Sales instructions to request deletion of your account and data.',
        'work_lead': 'For almost everything, your first point of contact is <strong>your store manager</strong>: they set up your account, enable your tasks and can cut off access if you lose your phone. For anything else, write to us.',
        'work_mail_s': 'Support — Zentrix Work',
        'work_mail_p': 'Put <em>Support — Zentrix Work</em> in the subject line and tell us the email you use in the app, your store and what happened. If you can, add a screenshot.',
        'preguntas': 'Quick questions', 'manual': 'Manual', 'acceso': 'Access and password',
        'work_manual': 'The <a href="{docs}">operator manual</a> (in Spanish) explains shifts, orders, picking, delivery and returns step by step.',
        'eliminar_t': 'Delete your account or your data',
        'work_del_p': 'The app does not let you create accounts, so they are not deleted from it either: your company creates the account and your company closes it. To ask for this:',
        'work_del_1': 'Write to <a href="{m}">soporte@zentrix.company</a> with the subject <em>Data request — Zentrix Work</em>, or tell your manager.',
        'work_del_s': 'Data request — Zentrix Work',
        'work_del_2': 'Include your name and your account email, and whether you want to <strong>see</strong>, <strong>correct</strong> or <strong>delete</strong> your data.',
        'del_3': 'We respond within <strong>30 business days</strong> at most.',
        'work_del_f': 'What is deleted, what is kept because of a legal obligation and for how long is explained in the <a href="{priv}#c7">privacy policy, section 7</a>. <strong>Signing out or uninstalling the app does not delete anything from the server.</strong>',
        'sales_lead': 'A person on the Zentrix team replies in under one business day. Our working language is Spanish.',
        'sales_mail_s': 'Support — Zentrix Sales', 'tel_wa': 'Phone and WhatsApp',
        'sales_calle_t': 'If you use Zentrix Sales out in the field',
        'sales_calle': '<p>Your account is created and handed to you by your employer: the app has no sign-up and there is no way to register from here. If you cannot get in, if something will not load, or if an order never arrived, write to us with your rep email address and your company’s name.</p>',
        'sales_manual': 'Before writing, check the <a href="{docs}">field rep manual</a> (in Spanish): it explains what each screen does.',
        'sales_emp_t': 'If your company already runs Zentrix Sales',
        'sales_emp': 'Adding or removing reps, permissions, companies and warehouses, or the integration with your ERP. Write from the company address and tell us what you need changed.',
        'sales_del_p': 'What the app collects, what for and how long it is kept is in the <a href="{priv}">privacy policy</a>. To request access to, correction or deletion of your data:',
        'sales_del_1': 'Write to <a href="{m}">hola@zentrix.company</a> with the subject <em>Data request — Zentrix Sales</em>.',
        'sales_del_s': 'Data request — Zentrix Sales',
        'sales_del_2': 'Include your name, your rep email (or your tax ID if you are a customer of a company that uses the app) and what you want: <strong>access</strong>, <strong>correction</strong> or <strong>deletion</strong>.',
        'sales_del_f': 'What is kept because of a legal obligation, and for how long, is in <a href="{priv}#c7">clause 7 of the policy</a>. <strong>Signing out does not delete data from the server.</strong>',
        'ficha': 'About the app', 'f_app': 'Application', 'f_desc': 'Download', 'f_resp': 'Responsible for the app', 'f_dir': 'Legal address',
        'f_correo': 'Support email', 'f_tel': 'Telephone', 'f_resp_t': 'Response time', 'f_docs': 'Documents',
        'work_app': 'Zentrix Work (<code>com.leiros.guuaowork</code>), for Android.',
        'sales_app': 'Zentrix Sales (<code>com.leiros.vendoo</code>). Android 7.0 or later and iOS 15 or later.',
        'dir': '10302 NW South River Drive, Medley, FL 33178, United States',
        'tel': '+58 412-346 9712, also on <a href="' + WA + '">WhatsApp</a>', 'menos_dia': 'Under one business day.',
        'priv': 'Privacy policy', 'term_w': 'Terms of use', 'term_s': 'Terms of service',
        'man_w': 'Manual', 'man_s': 'Field rep manual',
        'otros_ante': 'The rest of the suite', 'otros_t': 'No published app yet.',
        'otros_p': 'These products have no app to install: we run them as a project with your team. For any question, write to us from the contact page.',
        'otros_cta': 'Write to us', 'prox': 'Coming soon', 'traza_l': 'It has its own site and support at traza.technology.',
        'contactar_ante': 'Contact', 'contactar_t': 'Can’t find what you’re looking for?',
        'contactar_p': 'A person replies, in Spanish or English, within one business day. If it is about an app, tell us which one and the email you sign in with.',
        'contactar_s': 'Support — Zentrix', 'todas': 'Every way to reach us',
    },
}

SCRIPT_SOPORTE = '''<script>
(function () {
  var f = document.getElementById('ayuda-buscar');
  if (f) f.addEventListener('submit', function (e) {
    var q = (f.q.value || '').trim();
    if (q && window.zxBuscar && window.zxBuscar.abrir) { e.preventDefault(); window.zxBuscar.abrir(q); }
  });
  function abre() {
    var id = decodeURIComponent(location.hash.slice(1)), e = id && document.getElementById(id);
    if (e && e.tagName === 'DETAILS') e.open = true;
  }
  window.addEventListener('hashchange', abre); abre();
})();
</script>'''


def _ficha(lang, prod, G):
    t = TX[lang]
    L = G.Lx
    tiendas = G.TIENDAS[prod]
    descargas = [f'<a href="{tiendas["play"]}" data-zx-store="play">Google Play</a>']
    if tiendas.get('appstore'):
        descargas.append(f'<a href="{tiendas["appstore"]}" data-zx-store="appstore">App Store</a>')
    if prod == 'work':
        filas = [(t['f_app'], t['work_app']), (t['f_desc'], ' · '.join(descargas)), (t['f_resp'], 'GUUAO LLC'),
                 (t['f_correo'], '<a href="mailto:soporte@zentrix.company">soporte@zentrix.company</a>'),
                 (t['f_docs'], f'<a href="{L("/work/privacidad/", lang)}">{t["priv"]}</a> · <a href="{L("/work/terminos/", lang)}">{t["term_w"]}</a> · <a href="{L("/work/docs/", lang)}">{t["man_w"]}</a>')]
    else:
        filas = [(t['f_app'], t['sales_app']), (t['f_desc'], ' · '.join(descargas)), (t['f_resp'], 'GUUAO LLC'),
                 (t['f_dir'], t['dir']), (t['f_correo'], '<a href="mailto:hola@zentrix.company">hola@zentrix.company</a>'),
                 (t['f_tel'], t['tel']), (t['f_resp_t'], t['menos_dia']),
                 (t['f_docs'], f'<a href="{L("/sales/privacidad/", lang)}">{t["priv"]}</a> · <a href="{L("/sales/terminos/", lang)}">{t["term_s"]}</a> · <a href="{L("/sales/docs/", lang)}">{t["man_s"]}</a>')]
    dl = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in filas)
    return (f'<h3 id="ficha-{prod}">{t["ficha"]}</h3>'
            f'<div class="ficha"><dl>{dl}</dl></div>')


def _cabeza_prod(clave, nombre, linea, href):
    return (f'<div class="ayuda-prod__cabeza">{mono(clave, 56)}'
            f'<div><h2 id="{clave}-t">{nombre}</h2><p class="ayuda-prod__linea">{linea} · <a href="{href}">{nombre} →</a></p></div></div>')


def cuerpo_soporte(lang, G):
    """Cuerpo de /soporte/ (o /en/support/). G es el módulo generar (heroe, Lx, TIENDAS…)."""
    t = TX[lang]
    en = lang == 'en'
    L = G.Lx
    ruta = L('/soporte/', lang)
    del_w = 'delete-account-work' if en else 'eliminar-cuenta-work'
    del_s = 'delete-account-sales' if en else 'eliminar-cuenta-sales'
    otros, contactar = ('others', 'reach-us') if en else ('otros', 'contactar')
    lineas = {c: (d_en if en else d_es) for c, _, _, d_es, d_en in G.PRODUCTOS}

    # Héroe con el buscador (Pagefind, el de la cabecera: buscador.js expone window.zxBuscar).
    form = (f'<form class="ayuda-buscar" id="ayuda-buscar" role="search" action="{ruta}" method="get">'
            f'<label class="sr" for="ayuda-q">{t["buscar_l"]}</label>'
            f'<input id="ayuda-q" name="q" type="search" placeholder="{t["buscar_ph"]}" autocomplete="off" enterkeyhint="search">'
            f'<button class="boton boton--principal" type="submit">{t["buscar_b"]}</button></form>')
    h = G.heroe(t['ante'], t['h1'], t['lead'], form, G.arte_iconos(['ayuda', 'libro', 'escudo', 'correo']), 'heroe--ayuda')

    chips = []
    for clave, ancla, nombre, _ in SUITE:
        chips.append(f'<li><a class="ayuda-chip" href="#{ancla}">{mono(clave, 28)}<span>{nombre.replace("Zentrix ", "")}</span></a></li>')
    chips.append(f'<li><a class="ayuda-chip ayuda-chip--externo" href="{TRAZA_URL}" target="_blank" rel="noopener">'
                 f'<img src="{TRAZA_ICONO}" alt="" width="28" height="28" loading="lazy" decoding="async"><span>Traza{SVG_EXTERNO}'
                 f'<span class="sr">{G.T[lang]["externo"]}</span></span></a></li>')
    selector = f'''<section class="seccion ayuda-selector" aria-labelledby="elige-t">
  <div class="envoltura">
    <h2 class="ayuda-selector__t" id="elige-t">{t['elige']}</h2>
    <ul class="ayuda-chips" aria-label="{t['chips_l']}">{''.join(chips)}</ul>
    <p class="ayuda-atajo"><a href="#{del_w}">{t['eliminar_atajo']}: Zentrix Work</a> · <a href="#{del_s}">{t['eliminar_atajo']}: Zentrix Sales</a></p>
  </div>
</section>'''

    faq = ''.join(f'<details id="{i}"><summary><h3>{q}</h3></summary><p>{a}</p></details>' for i, q, a in WORK_FAQ[lang])
    work = f'''<section class="seccion seccion--gris ayuda-prod" id="work" aria-labelledby="work-t">
  <div class="envoltura"><div class="doc">
    {_cabeza_prod('work', 'Zentrix Work', lineas['work'], L('/work/', lang))}
    <p>{t['work_lead']}</p>
    <p class="correo-grande"><a href="{mailto('soporte@zentrix.company', t['work_mail_s'])}">soporte@zentrix.company</a></p>
    <p>{t['work_mail_p']}</p>
    <h3 id="preguntas-work">{t['preguntas']}</h3>
    <div class="preguntas">{faq}</div>
    <h3 id="manual-work">{t['manual']}</h3>
    <p>{t['work_manual'].format(docs=L('/work/docs/', lang))}</p>
    <h3 id="{del_w}" class="ayuda-borrar">{t['eliminar_t']} — Zentrix Work</h3>
    <p>{t['work_del_p']}</p>
    <ol class="pasos">
      <li>{t['work_del_1'].format(m=mailto('soporte@zentrix.company', t['work_del_s']))}</li>
      <li>{t['work_del_2']}</li>
      <li>{t['del_3']}</li>
    </ol>
    <p>{t['work_del_f'].format(priv=L('/work/privacidad/', lang))}</p>
    {_ficha(lang, 'work', G)}
  </div></div>
</section>'''

    calle_id, emp_id = ('rep', 'company') if en else ('vendedor', 'empresa')
    sales = f'''<section class="seccion ayuda-prod" id="sales" aria-labelledby="sales-t">
  <div class="envoltura"><div class="doc">
    {_cabeza_prod('sales', 'Zentrix Sales', lineas['sales'], L('/sales/', lang))}
    <p>{t['sales_lead']}</p>
    <p class="correo-grande"><a href="{mailto('hola@zentrix.company', t['sales_mail_s'])}">hola@zentrix.company</a></p>
    <p>{t['tel_wa']}: <a href="{WA}">{WA_TXT}</a>.</p>
    <h3 id="{calle_id}">{t['sales_calle_t']}</h3>
    {t['sales_calle']}
    <h3 id="manual-sales">{t['manual']}</h3>
    <p>{t['sales_manual'].format(docs=L('/sales/docs/', lang))}</p>
    <h3 id="{emp_id}">{t['sales_emp_t']}</h3>
    <p>{t['sales_emp']}</p>
    <h3 id="{del_s}" class="ayuda-borrar">{t['eliminar_t']} — Zentrix Sales</h3>
    <p>{t['sales_del_p'].format(priv=L('/sales/privacidad/', lang))}</p>
    <ol class="pasos">
      <li>{t['sales_del_1'].format(m=mailto('hola@zentrix.company', t['sales_del_s']))}</li>
      <li>{t['sales_del_2']}</li>
      <li>{t['del_3']}</li>
    </ol>
    <p>{t['sales_del_f'].format(priv=L('/sales/privacidad/', lang))}</p>
    {_ficha(lang, 'sales', G)}
  </div></div>
</section>'''

    tarjetas = []
    for clave, ancla, nombre, href in SUITE[2:]:
        linea = lineas[clave]
        contacto = L('/contacto/', lang).split('#')[0] + f'?motivo=soporte&amp;producto={ancla}#motivo'
        tarjetas.append(f'<li class="ayuda-otro" id="{ancla}">{mono(clave, 48)}<div><h3>{nombre}</h3>'
                        f'<p>{linea}. <a href="{L(href, lang)}">{nombre} →</a></p>'
                        f'<a class="ayuda-otro__cta" href="{contacto}">{t["otros_cta"]}</a></div></li>')
    resto = f'''<section class="seccion seccion--gris" id="{otros}" aria-labelledby="{otros}-t">
  <div class="envoltura">
    <div class="cabeza">
      <span class="antetitulo">{t['otros_ante']}</span>
      <h2 id="{otros}-t">{t['otros_t']}</h2>
      <p>{t['otros_p']}</p>
    </div>
    <ul class="ayuda-otros">{''.join(tarjetas)}</ul>
    <p class="ayuda-traza"><a href="{TRAZA_URL}" target="_blank" rel="noopener">Traza{SVG_EXTERNO}<span class="sr">{G.T[lang]['externo']}</span></a> — {t['traza_l']}</p>
  </div>
</section>'''

    botones = (f'<a class="boton boton--principal" href="{mailto("soporte@zentrix.company", t["contactar_s"])}">soporte@zentrix.company</a>'
               f'<a class="boton boton--alterno" href="{WA}">WhatsApp {WA_TXT}</a>'
               f'<a class="boton boton--alterno" href="{L("/contacto/", lang)}">{t["todas"]}</a>')
    cierre = G.BQ.cierre(contactar + '-t', t['contactar_t'], t['contactar_p'], botones).replace(
        '<section ', f'<section id="{contactar}" ', 1)
    return '\n\n'.join([h, selector, work, sales, resto, cierre, SCRIPT_SOPORTE])


# ── /legal/ ─────────────────────────────────────────────────────────────────
LEGAL_TX = {
    'es': {'ante': 'Legal', 'h1': 'Privacidad y términos.',
           'lead': 'Cada app tiene su propia política de privacidad y sus términos, porque cada una trata datos distintos. Aquí están todas, y la del sitio web.',
           'priv_t': 'Políticas de privacidad', 'term_t': 'Términos',
           'items_priv': [('/work/privacidad/', 'work', 'Zentrix Work', 'Qué recoge la app del equipo de tienda, para qué y por cuánto tiempo.'),
                          ('/sales/privacidad/', 'sales', 'Zentrix Sales', 'Qué recoge la app de fuerza de ventas, para qué y por cuánto tiempo.'),
                          ('/privacidad/', None, 'Sitio web y cookies', 'Qué mide zentrix.company, con consentimiento, y cómo retirarlo.')],
           'items_term': [('/work/terminos/', 'work', 'Zentrix Work', 'Términos de uso de la app.'),
                          ('/sales/terminos/', 'sales', 'Zentrix Sales', 'Términos de servicio de la app.')],
           'datos_t': 'Tus datos', 'datos_p': 'Para ver, corregir o eliminar tu cuenta o tus datos de una app, sigue las instrucciones de su página de soporte:',
           'del_w': 'Eliminar tu cuenta de Zentrix Work', 'del_s': 'Eliminar tu cuenta de Zentrix Sales',
           'nota': ''},
    'en': {'ante': 'Legal', 'h1': 'Privacy and terms.',
           'lead': 'Each app has its own privacy policy and terms, because each one handles different data. Here they all are, plus the one for this website.',
           'priv_t': 'Privacy policies', 'term_t': 'Terms',
           'items_priv': [('/work/privacidad/', 'work', 'Zentrix Work', 'What the store team app collects, why and for how long.'),
                          ('/sales/privacidad/', 'sales', 'Zentrix Sales', 'What the field sales app collects, why and for how long.'),
                          ('/privacidad/', None, 'Website and cookies', 'What zentrix.company measures, with consent, and how to withdraw it.')],
           'items_term': [('/work/terminos/', 'work', 'Zentrix Work', 'Terms of use of the app.'),
                          ('/sales/terminos/', 'sales', 'Zentrix Sales', 'Terms of service of the app.')],
           'datos_t': 'Your data', 'datos_p': 'To see, correct or delete your account or your data in an app, follow the instructions on its support page:',
           'del_w': 'Delete your Zentrix Work account', 'del_s': 'Delete your Zentrix Sales account',
           'nota': '<p class="apagado">The English texts are courtesy translations; the Spanish version is the binding one.</p>'},
}


def cuerpo_legal(lang, G):
    t = LEGAL_TX[lang]
    en = lang == 'en'
    L = G.Lx
    priv_id, term_id = ('privacy', 'terms') if en else ('privacidad', 'terminos')

    def lista(items):
        lis = []
        for r, clave, nombre, linea in items:
            ico = mono(clave, 40) if clave else '<img src="/favicon.svg" alt="" width="40" height="40" loading="lazy" decoding="async">'
            lis.append(f'<li><a class="legal-item" href="{L(r, lang)}">{ico}<span><b>{nombre}</b><small>{linea}</small></span>'
                       f'<span class="mega__flecha" aria-hidden="true">→</span></a></li>')
        return f'<ul class="legal-lista">{"".join(lis)}</ul>'
    h = G.heroe(t['ante'], t['h1'], t['lead'], '', G.arte_iconos(['escudo', 'documento', 'escudo', 'documento']))
    return f'''{h}

<section class="seccion" aria-labelledby="{priv_id}">
  <div class="envoltura"><div class="doc">
    <h2 id="{priv_id}">{t['priv_t']}</h2>
    {lista(t['items_priv'])}
    <h2 id="{term_id}">{t['term_t']}</h2>
    {lista(t['items_term'])}
    {t['nota']}
  </div></div>
</section>

<section class="seccion seccion--gris" aria-labelledby="datos-t">
  <div class="envoltura"><div class="doc">
    <h2 id="datos-t" style="margin-top:0">{t['datos_t']}</h2>
    <p>{t['datos_p']}</p>
    <ul>
      <li><a href="{L('/soporte/#eliminar-cuenta-work', lang)}">{t['del_w']}</a></li>
      <li><a href="{L('/soporte/#eliminar-cuenta-sales', lang)}">{t['del_s']}</a></li>
    </ul>
  </div></div>
</section>'''


# ── /contacto/: selector de motivo ──────────────────────────────────────────
MOTIVO_TX = {
    'es': {'ante': 'Escríbenos', 'h2': '¿Sobre qué nos escribes?',
           'p': 'Elige el motivo y, si quieres, el producto: preparamos el asunto del correo o del WhatsApp para que llegue a la persona adecuada.',
           'motivo': 'Motivo', 'producto': 'Producto', 'ninguno': 'Varios o ninguno en concreto',
           'motivos': [('demo', 'Ventas o demostración'), ('soporte', 'Soporte de una app'), ('alianzas', 'Alianzas'), ('prensa', 'Prensa')],
           'correo': 'Escribir por correo', 'wa': 'Escribir por WhatsApp',
           'notas': {'demo': 'Demostración con tus datos: tu catálogo, tu tarifa y tu ruta. Integración con tu ERP: con Odoo®, nativa; con los demás, a medida.',
                     'soporte': 'Si ya usas una app, mira antes el <a href="/soporte/">centro de soporte</a>: preguntas frecuentes, acceso y cómo eliminar tu cuenta.',
                     'alianzas': 'Partners, integradores y proveedores: cuéntanos qué propones.',
                     'prensa': 'Para entrevistas, notas y material de marca.'},
           'asuntos': {'demo': 'Demostración — {p}', 'soporte': 'Soporte — {p}', 'alianzas': 'Alianzas — Zentrix', 'prensa': 'Prensa — Zentrix'},
           'cuerpos': {'demo': 'Nombre:\nEmpresa:\nTeléfono (opcional):\n{extra}Cuéntanos cómo trabaja hoy tu equipo:\n',
                       'soporte': 'Correo con el que entras a la app:\nEmpresa o tienda:\nQué pasó:\n',
                       'alianzas': 'Nombre:\nEmpresa:\nQué propones:\n', 'prensa': 'Nombre:\nMedio:\nQué necesitas:\n'},
           'extra_sales': 'Vendedores en la calle (opcional):\n'},
    'en': {'ante': 'Write to us', 'h2': 'What are you writing about?',
           'p': 'Pick a reason and, if you like, a product: we fill in the email or WhatsApp subject so it reaches the right person.',
           'motivo': 'Reason', 'producto': 'Product', 'ninguno': 'Several or none in particular',
           'motivos': [('demo', 'Sales or a demo'), ('soporte', 'Support for an app'), ('alianzas', 'Partnerships'), ('prensa', 'Press')],
           'correo': 'Write by email', 'wa': 'Write on WhatsApp',
           'notas': {'demo': 'A demo on your own data: your catalog, your price list and your route. ERP integration: native with Odoo®, custom with the rest.',
                     'soporte': 'If you already use an app, check the <a href="/en/support/">support center</a> first: common questions, access and how to delete your account.',
                     'alianzas': 'Partners, integrators and suppliers: tell us what you have in mind.',
                     'prensa': 'For interviews, articles and brand material.'},
           'asuntos': {'demo': 'Demo — {p}', 'soporte': 'Support — {p}', 'alianzas': 'Partnerships — Zentrix', 'prensa': 'Press — Zentrix'},
           'cuerpos': {'demo': 'Name:\nCompany:\nPhone (optional):\n{extra}Tell us how your team works today:\n',
                       'soporte': 'Email you sign in to the app with:\nCompany or store:\nWhat happened:\n',
                       'alianzas': 'Name:\nCompany:\nWhat you have in mind:\n', 'prensa': 'Name:\nPublication:\nWhat you need:\n'},
           'extra_sales': 'Field reps (optional):\n'},
}


def selector_motivo(lang):
    """Selector de motivo y producto de /contacto/: solo cambia el asunto y el texto del correo o
    del WhatsApp (assets/js/contacto.js). Sin JavaScript, los enlaces llevan el motivo por defecto."""
    t = MOTIVO_TX[lang]
    radios = ''.join(
        f'<label class="motivo__op"><input type="radio" name="motivo" value="{v}"{" checked" if i == 0 else ""}><span>{n}</span></label>'
        for i, (v, n) in enumerate(t['motivos']))
    opciones = f'<option value="">{t["ninguno"]}</option>' + ''.join(
        f'<option value="{ancla}">{nombre}</option>' for _, ancla, nombre, _ in SUITE)
    asunto = t['asuntos']['demo'].format(p='Zentrix')
    cuerpo = t['cuerpos']['demo'].format(extra='')
    href_m = f'mailto:hola@zentrix.company?subject={quote(asunto)}&amp;body={quote(cuerpo)}'
    href_w = f'{WA}?text={quote(asunto)}'
    datos = {'asuntos': t['asuntos'], 'cuerpos': t['cuerpos'], 'extra_sales': t['extra_sales']}
    import json
    datos_json = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    notas = ''.join(f'<p class="motivo__nota" data-motivo="{k}"{"" if k == "demo" else " hidden"}>{v}</p>' for k, v in t['notas'].items())
    return f'''<section class="seccion seccion--gris" id="motivo" aria-labelledby="motivo-t">
  <div class="envoltura">
    <div class="cabeza revela">
      <span class="antetitulo">{t['ante']}</span>
      <h2 id="motivo-t">{t['h2']}</h2>
      <p>{t['p']}</p>
    </div>
    <form class="motivo" id="motivo-form" onsubmit="return false">
      <fieldset class="motivo__grupo"><legend>{t['motivo']}</legend><div class="motivo__ops">{radios}</div></fieldset>
      <label class="campo motivo__producto">{t['producto']}<select name="producto">{opciones}</select></label>
      {notas}
      <div class="botones">
        <a class="boton boton--principal" id="motivo-correo" href="{href_m}">{t['correo']}</a>
        <a class="boton boton--alterno motivo__wa" id="motivo-wa" href="{href_w}">{t['wa']}</a>
      </div>
      <script type="application/json" id="motivo-datos">{datos_json}</script>
    </form>
  </div>
</section>
<script src="/assets/js/contacto.js?v=2" defer></script>'''
