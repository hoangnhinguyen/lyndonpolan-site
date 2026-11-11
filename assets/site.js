/* Lyndon Polan — language switch and contact form. */
(function () {
  var html = document.documentElement;

  /* ---- language (EN / FR), remembered between pages ---- */
  function setLang(lang) {
    html.className = lang === 'fr' ? 'fr' : '';
    html.lang = lang;
    try { localStorage.setItem('lang', lang); } catch (e) { /* private mode: just don't remember */ }
    var send = document.getElementById('sendButton');
    if (send) send.value = send.getAttribute('data-' + lang);
  }
  function currentLang() { return html.className === 'fr' ? 'fr' : 'en'; }

  var sw = document.getElementById('langSwitch');
  if (sw) sw.addEventListener('click', function () { setLang(currentLang() === 'en' ? 'fr' : 'en'); });
  setLang(currentLang());

  /* ---- contact form: same EmailJS service the original site used ---- */
  var form = document.getElementById('contactForm');
  if (!form) return;
  var status = document.getElementById('formStatus');
  var button = document.getElementById('sendButton');
  var MSG = {
    en: { sending: 'Sending…', ok: 'Thank you — your message was sent.',
          fail: "Can't send the message. Sorry for this inconvenience, please contact me directly: " },
    fr: { sending: 'Envoi…', ok: 'Merci — votre message a été envoyé.',
          fail: "Impossible d'envoyer le message. Veuillez m'écrire directement : " }
  };
  function say(kind, isError) {
    var m = MSG[currentLang()][kind];
    status.className = 'formStatus' + (isError ? ' error' : '');
    status.textContent = m;
    if (isError) {
      var a = document.createElement('a');
      a.href = 'mailto:' + form.getAttribute('data-fallback');
      a.textContent = form.getAttribute('data-fallback');
      status.appendChild(a);
    }
  }
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var data = new FormData(form);
    data.append('service_id', form.getAttribute('data-service'));
    data.append('template_id', form.getAttribute('data-template'));
    data.append('user_id', form.getAttribute('data-user'));
    button.disabled = true;
    say('sending');
    fetch('https://api.emailjs.com/api/v1.0/email/send-form', { method: 'POST', body: data })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); form.reset(); say('ok'); })
      .catch(function () { say('fail', true); })
      .then(function () { button.disabled = false; });
  });
})();
