"""Wire the forms to the real endpoints.

Client-side validation stays for instant feedback and never clears what was
typed. When a form carries an `action`, the values are POSTed there and the
JSON response drives the result, including field errors the server rejected.
Forms without an `action` (the static demo pages) keep the local success state.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

OLD_START = "  var waitlist = document.getElementById('waitlist-form');"
OLD_END = "  /* ---- counters: count up once, when the row scrolls into view ---- */"

NEW = r"""  /* Post a form to its endpoint and hand back the parsed JSON.
     Returns null when the form has no action — then the caller shows the
     local success state instead. */
  function postForm(form) {
    var action = form.getAttribute('action');
    if (!action) return null;
    var data = new FormData(form);
    return fetch(action, { method: 'POST', body: data, headers: { accept: 'application/json' } })
      .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); });
  }

  function applyServerErrors(form, errors) {
    Object.keys(errors || {}).forEach(function (name) {
      var input = form.elements[name];
      var field = input && input.closest ? input.closest('.field') : null;
      if (field) setError(field, errors[name]);
    });
  }

  function busy(form, on) {
    var btn = form.querySelector('button[type="submit"]');
    if (!btn) return;
    btn.disabled = on;
    btn.dataset.label = btn.dataset.label || btn.textContent;
    btn.textContent = on ? 'Even geduld…' : btn.dataset.label;
  }

  var waitlist = document.getElementById('waitlist-form');
  if (waitlist) {
    var min = parseInt(waitlist.dataset.ageMin, 10);
    var max = parseInt(waitlist.dataset.ageMax, 10);

    function waitlistSuccess(email, message) {
      var card = waitlist.closest('.wl-card');
      card.innerHTML =
        '<h2>Je staat op de wachtlijst</h2><p class="body">' +
        (message ||
          'We sturen een bevestiging naar ' + email.replace(/[<>&]/g, '') +
          '. Zodra de datum van deze editie bevestigd is, krijg je als eerste bericht — nog zonder verplichting.') +
        '</p>';
      card.scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' });
      if (window.plausible) {
        window.plausible('waitlist_join', { props: { event: (waitlist.elements.event || {}).value || '' } });
      }
    }

    waitlist.addEventListener('submit', function (e) {
      e.preventDefault();
      waitlist.querySelectorAll('.field').forEach(function (f) { setError(f, ''); });

      var naam = waitlist.elements.naam;
      var leeftijd = waitlist.elements.leeftijd;
      var email = waitlist.elements.email;
      var ok = true;

      if (naam.value.trim().length < 2) {
        setError(naam.closest('.field'), 'Vul de voornaam van de deelnemer in.'); ok = false;
      }
      var age = Number(leeftijd.value);
      if (!leeftijd.value.trim() || Number.isNaN(age)) {
        setError(leeftijd.closest('.field'), 'Vul een leeftijd in.'); ok = false;
      } else if (age < min || age > max) {
        setError(leeftijd.closest('.field'), 'Deze editie is voor ' + min + '–' + max + ' jaar.'); ok = false;
      }
      if (!mail.test(email.value.trim())) {
        setError(email.closest('.field'), 'Vul een geldig e-mailadres in.'); ok = false;
      }
      if (!ok) return;   // values are never cleared on error

      // the server re-checks the range, so send the event's own bounds with it
      if (!waitlist.querySelector('input[name="ageMin"]')) {
        [['ageMin', min], ['ageMax', max]].forEach(function (pair) {
          if (!Number.isFinite(pair[1])) return;
          var h = document.createElement('input');
          h.type = 'hidden'; h.name = pair[0]; h.value = String(pair[1]);
          waitlist.appendChild(h);
        });
      }

      var sent = postForm(waitlist);
      if (!sent) { waitlistSuccess(email.value.trim()); return; }

      busy(waitlist, true);
      sent.then(function (res) {
        busy(waitlist, false);
        if (res.status === 200 && res.body.ok) {
          waitlistSuccess(email.value.trim(), res.body.message);
        } else {
          applyServerErrors(waitlist, res.body.errors);
        }
      }).catch(function () {
        busy(waitlist, false);
        setError(email.closest('.field'), 'Versturen lukte niet. Probeer het straks opnieuw.');
      });
    });
  }

  /* every newsletter form: footer band, section 08, CTA card, dome */
  document.querySelectorAll('[data-newsletter]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.form-msg');
      var field = form.elements.email;
      var value = field.value.trim();

      function say(kind, text) {
        if (!msg) return;
        msg.className = 'form-msg ' + kind;
        msg.textContent = text;
      }

      if (!mail.test(value)) { say('error', 'Vul een geldig e-mailadres in.'); return; }

      function done(message) {
        say('ok', message || 'Bedankt — je staat op de lijst.');
        field.value = '';
        if (window.plausible) {
          window.plausible('newsletter_signup', { props: { source: document.title } });
        }
      }

      var sent = postForm(form);
      if (!sent) { done(); return; }

      busy(form, true);
      say('', 'Versturen…');
      sent.then(function (res) {
        busy(form, false);
        if (res.status === 200 && res.body.ok) done(res.body.message);
        else say('error', (res.body.errors && res.body.errors.email) || 'Inschrijven lukte niet.');
      }).catch(function () {
        busy(form, false);
        say('error', 'Versturen lukte niet. Probeer het straks opnieuw.');
      });
    });
  });

"""


def patch(path):
    f = ROOT / path
    s = f.read_text(encoding="utf8")
    i, j = s.index(OLD_START), s.index(OLD_END)
    f.write_text(s[:i] + NEW + s[j:], encoding="utf8")
    print("patched", path)


patch("site/assets/js/main.js")
# the Astro app serves the same file from public/
(ROOT / "web/public/assets/js/main.js").write_text(
    (ROOT / "site/assets/js/main.js").read_text(encoding="utf8"), encoding="utf8")
print("mirrored into web/public/assets/js/main.js")
