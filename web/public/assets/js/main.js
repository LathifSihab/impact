/* IMPACT demo — small local state only: nav, fundamentals scroll, faq, forms. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- hero reveal, on load only ----
     The headline is one text block (no <br>): we measure where the browser broke
     the lines and wrap each in a span, so the reveal is line-by-line while the
     line count stays a property of the type block, not of the markup. */
  function splitLines(el) {
    var text = el.textContent.trim();
    el.textContent = '';
    text.split(/\s+/).forEach(function (word, i) {
      var w = document.createElement('span');
      w.className = 'w';
      w.textContent = (i ? ' ' : '') + word;
      el.appendChild(w);
    });
    var lines = [], current = null, top = null;
    Array.prototype.forEach.call(el.querySelectorAll('.w'), function (w) {
      var t = Math.round(w.offsetTop);
      if (top === null || t !== top) { current = []; lines.push(current); top = t; }
      current.push(w.textContent);
    });
    el.innerHTML = lines.map(function (l) {
      return '<span class="line"><span class="line-in">' + l.join('').trim() + '</span></span>';
    }).join(' ');
  }

  var split = document.querySelector('[data-split]');
  if (split && !reduced) {
    try { splitLines(split); } catch (e) { /* leave the headline as authored */ }
  }

  var hero = document.querySelector('[data-reveal-root]');
  if (hero) requestAnimationFrame(function () { hero.classList.add('is-revealed'); });

  /* ---- hero video: progressive, poster-first ----
     The poster <img> carries data-video-* paths. We probe the webm; if it exists we
     insert a muted, looping, playsinline <video> over the poster. Nothing is
     downloaded when prefers-reduced-motion is set or when the file is absent. */
  var poster = document.querySelector('[data-hero-poster]');
  if (poster && !reduced && poster.dataset.videoWebm) {
    var v = document.createElement('video');
    v.muted = true; v.loop = true; v.autoplay = true; v.playsInline = true;
    v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
    v.setAttribute('aria-hidden', 'true');
    v.preload = 'auto';
    v.poster = poster.currentSrc || poster.getAttribute('src');
    [[poster.dataset.videoWebm, 'video/webm'], [poster.dataset.videoMp4, 'video/mp4']]
      .forEach(function (pair) {
        if (!pair[0]) return;
        var s = document.createElement('source');
        s.src = pair[0]; s.type = pair[1];
        v.appendChild(s);
      });
    // if none of the sources resolve — no file shipped yet — drop back to the still
    v.addEventListener('error', function () { v.remove(); }, true);
    v.addEventListener('loadeddata', function () { v.classList.add('is-ready'); });
    // the poster now sits inside a <picture>, so mount the video on the hero itself
    var heroEl = poster.closest('.hero');
    var mount = heroEl || poster.parentNode;
    var pictureEl = poster.closest('picture') || poster;
    mount.insertBefore(v, pictureEl.nextSibling);
    var play = v.play();
    if (play && play.catch) play.catch(function () { v.remove(); });
  }

  /* ---- nav dropdowns: hover with delay on desktop, click/focus for keyboard ---- */
  var items = document.querySelectorAll('.nav-main > li');
  var openTimer = null;
  function closeAll() {
    items.forEach(function (li) {
      li.classList.remove('is-open');
      var t = li.querySelector('a.top');
      if (t && t.hasAttribute('aria-expanded')) t.setAttribute('aria-expanded', 'false');
    });
  }
  items.forEach(function (li) {
    if (!li.querySelector('.dropdown')) return;
    var top = li.querySelector('a.top');
    top.setAttribute('aria-expanded', 'false');
    li.addEventListener('mouseenter', function () {
      clearTimeout(openTimer);
      openTimer = setTimeout(function () {
        closeAll(); li.classList.add('is-open'); top.setAttribute('aria-expanded', 'true');
      }, 120);
    });
    li.addEventListener('mouseleave', function () {
      clearTimeout(openTimer); li.classList.remove('is-open'); top.setAttribute('aria-expanded', 'false');
    });
    top.addEventListener('click', function (e) {
      if (top.getAttribute('href') === '#') e.preventDefault();
      var open = li.classList.contains('is-open');
      closeAll();
      if (!open) { li.classList.add('is-open'); top.setAttribute('aria-expanded', 'true'); }
    });
    li.addEventListener('focusin', function () { closeAll(); li.classList.add('is-open'); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(); closeMobile(); } });
  document.addEventListener('click', function (e) { if (!e.target.closest('.nav-main')) closeAll(); });

  /* ---- mobile menu ---- */
  var menu = document.getElementById('mobile-menu');
  var burgerEl = document.querySelector('.burger');
  function closeMobile() {
    if (!menu) return;
    menu.classList.remove('is-open');
    if (burgerEl) { burgerEl.setAttribute('aria-expanded', 'false'); burgerEl.focus(); }
    document.body.style.overflow = '';
    Array.prototype.forEach.call(document.body.children, function (el) {
      if (el !== document.getElementById('dome')) el.removeAttribute('inert');
    });
  }
  var burger = document.querySelector('.burger');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      menu.classList.add('is-open');
      burger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
      Array.prototype.forEach.call(document.body.children, function (el) {
        if (el !== menu && el.tagName !== 'SCRIPT') el.setAttribute('inert', '');
      });
      var c = menu.querySelector('.close'); if (c) c.focus();
    });
    menu.querySelector('.close').addEventListener('click', closeMobile);
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) closeMobile(); });
  }

  /* ---- fundamentals horizontal scroll → progress bar ---- */
  var track = document.querySelector('.fund-track');
  if (track) {
    var bar = document.querySelector('[data-progress]');
    var counter = document.querySelector('[data-counter]');
    var total = track.children.length;
    var update = function () {
      var max = track.scrollWidth - track.clientWidth;
      var p = max > 0 ? track.scrollLeft / max : 0;
      if (bar) {
        var travel = bar.parentElement.clientWidth - bar.clientWidth;
        bar.style.transform = 'translateX(' + (p * travel) + 'px)';
      }
      if (counter) {
        var i = Math.min(total, Math.round(p * (total - 1)) + 1);
        counter.textContent = ('0' + i).slice(-2) + ' / ' + ('0' + total).slice(-2);
      }
    };
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    track.setAttribute('tabindex', '0');
    var step = function () { return track.children[0].offsetWidth + 20; };
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { track.scrollBy({ left: step(), behavior: reduced ? 'auto' : 'smooth' }); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { track.scrollBy({ left: -step(), behavior: reduced ? 'auto' : 'smooth' }); e.preventDefault(); }
    });
    update();

    var prev = document.querySelector('[data-strip-prev]');
    var next = document.querySelector('[data-strip-next]');
    if (prev) prev.addEventListener('click', function () {
      track.scrollBy({ left: -step(), behavior: reduced ? 'auto' : 'smooth' });
    });
    if (next) next.addEventListener('click', function () {
      track.scrollBy({ left: step(), behavior: reduced ? 'auto' : 'smooth' });
    });
  }

  /* ---- FAQ: one open at a time ---- */
  var faqs = document.querySelectorAll('.faq');
  faqs.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      faqs.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  /* ---- forms ---- */
  function setError(field, msg) {
    var el = field.querySelector('.err');
    if (el) el.textContent = msg || '';
  }
  var mail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  /* Post a form to its endpoint and hand back the parsed JSON.
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

  /* ---- counters: count up once, when the row scrolls into view ---- */
  var fmt = new Intl.NumberFormat('nl-BE');
  function countUp(el) {
    var target = Number(el.dataset.count || 0);
    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';
    var render = function (v) { el.textContent = prefix + fmt.format(v) + suffix; };
    if (reduced) { render(target); return; }
    var dur = 1400, t0 = null;
    var step = function (t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 3); // ease-out cubic
      render(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  var counterRows = document.querySelectorAll('[data-counters]');
  if (counterRows.length) {
    if (!('IntersectionObserver' in window)) {
      counterRows.forEach(function (row) { row.querySelectorAll('[data-count]').forEach(countUp); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.querySelectorAll('[data-count]').forEach(countUp);
          io.unobserve(entry.target);
        });
      }, { threshold: 0.35 });
      counterRows.forEach(function (row) { io.observe(row); });
    }
  }

  /* ---- journal category filter ---- */
  var group = document.querySelector('[data-filter-group]');
  var list = document.querySelector('[data-filter-list]');
  if (group && list) {
    group.addEventListener('click', function (e) {
      var btn = e.target.closest('.chip');
      if (!btn) return;
      group.querySelectorAll('.chip').forEach(function (c) { c.classList.toggle('is-on', c === btn); });
      var want = btn.dataset.filter;
      Array.prototype.forEach.call(list.children, function (card) {
        card.hidden = !(want === 'all' || card.dataset.cat === want);
      });
    });
  }

  /* ---- generic demo forms (contact, hosted aanvraag) ---- */
  document.querySelectorAll('[data-demo-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.querySelectorAll('.field').forEach(function (f) { setError(f, ''); });
      var ok = true;
      var email = form.elements.email;
      form.querySelectorAll('input[type="text"]').forEach(function (i) {
        if (i.value.trim().length < 2) { setError(i.closest('.field'), 'Dit veld is verplicht.'); ok = false; }
      });
      if (email && !mail.test(email.value.trim())) {
        setError(email.closest('.field'), 'Vul een geldig e-mailadres in.'); ok = false;
      }
      var msg = form.querySelector('.form-msg');
      if (!ok) { if (msg) { msg.className = 'form-msg error'; msg.textContent = 'Vul de ontbrekende velden aan.'; } return; }
      if (msg) { msg.className = 'form-msg ok'; msg.textContent = 'Bedankt — je bericht is klaar om verzonden te worden. ()'; }
    });
  });

  /* ---- newsletter dome (Capital Belgium pattern) ----
     Exit-intent on desktop, 60% scroll on mobile, once per visitor, suppressed
     90 days after a dismiss or a signup. localStorage, so no consent banner. */
  var dome = document.getElementById('dome');
  if (dome) {
    var KEY = 'impact.dome.until';
    var panel = dome.querySelector('.dome-panel');
    var closeBtn = dome.querySelector('.dome-close');
    var lastFocus = null;
    var suppressed = function () {
      try { return Number(localStorage.getItem(KEY) || 0) > Date.now(); } catch (e) { return false; }
    };
    var suppress = function (days) {
      try { localStorage.setItem(KEY, String(Date.now() + days * 864e5)); } catch (e) {}
    };
    var focusables = function () {
      return dome.querySelectorAll('button, input, a[href]');
    };
    function openDome() {
      if (suppressed() || !dome.hidden) return;
      lastFocus = document.activeElement;
      dome.hidden = false;
      document.body.style.overflow = 'hidden';
      Array.prototype.forEach.call(document.body.children, function (el) {
        if (el !== dome && el.tagName !== 'SCRIPT') el.setAttribute('inert', '');
      });
      var first = dome.querySelector('input');
      if (first) first.focus();
      if (window.plausible) window.plausible('dome_shown');
    }
    function closeDome(reason) {
      if (dome.hidden) return;
      dome.hidden = true;
      document.body.style.overflow = '';
      Array.prototype.forEach.call(document.body.children, function (el) { el.removeAttribute('inert'); });
      suppress(90);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
      if (window.plausible && reason) window.plausible(reason);
    }
    closeBtn.addEventListener('click', function () { closeDome('dome_dismissed'); });
    dome.addEventListener('click', function (e) { if (e.target === dome) closeDome('dome_dismissed'); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeDome('dome_dismissed');
      if (e.key === 'Tab' && !dome.hidden) {
        var f = focusables(), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
        else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
      }
    });
    var domeForm = dome.querySelector('[data-dome-form]');
    if (domeForm) domeForm.addEventListener('submit', function () {
      suppress(365);
      if (window.plausible) window.plausible('dome_signup');
      setTimeout(function () { closeDome(); }, 1800);
    });

    if (!suppressed()) {
      if (window.matchMedia('(min-width: 821px)').matches) {
        document.addEventListener('mouseout', function (e) {
          if (!e.relatedTarget && e.clientY <= 0) openDome();
        });
      } else {
        window.addEventListener('scroll', function onScroll() {
          var p = window.scrollY / (document.body.scrollHeight - window.innerHeight);
          if (p >= 0.6) { openDome(); window.removeEventListener('scroll', onScroll); }
        }, { passive: true });
      }
    }
  }

  /* ---- participant clips: autoplay muted when scrolled into view ----
     Autoplay is only permitted while muted, so the clips start silent and carry
     a hint; the native controls remain, so sound is one click away. One plays at
     a time, loading starts near the viewport rather than on page load, and it
     stays off under reduced motion or a metered connection. */
  var clips = Array.prototype.slice.call(document.querySelectorAll('.vcard video'));
  if (clips.length && 'IntersectionObserver' in window) {
    var saveData = !!(navigator.connection && navigator.connection.saveData);
    var mayAutoplay = !reduced && !saveData;
    var playing = null;

    clips.forEach(function (v) {
      v.muted = true;                 // required for autoplay to be allowed
      v.setAttribute('muted', '');
      v.loop = true;
      var hint = v.parentNode.querySelector('.vhint');
      // once the visitor unmutes, stop treating this clip as ambient
      v.addEventListener('volumechange', function () {
        if (!v.muted) {
          v.parentNode.classList.remove('is-live');
          if (hint) hint.remove();
        }
      });
      v.addEventListener('play', function () {
        if (playing && playing !== v) playing.pause();
        playing = v;
        // the hint only makes sense while this clip is actually running silent
        if (v.muted) v.parentNode.classList.add('is-live');
      });
      v.addEventListener('pause', function () { v.parentNode.classList.remove('is-live'); });
      if (hint) {
        hint.addEventListener('click', function () {
          v.muted = false;
          v.play();
          hint.remove();
        });
      }
    });

    // start fetching a little before it is needed
    var preloader = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) e.target.preload = 'auto';
      });
    }, { rootMargin: '300px' });
    clips.forEach(function (v) { preloader.observe(v); });

    if (mayAutoplay) {
      var watcher = new IntersectionObserver(function (entries) {
        // the most visible card wins, so two never play at once
        var best = null;
        entries.forEach(function (e) {
          if (e.isIntersecting && e.intersectionRatio >= 0.6) {
            if (!best || e.intersectionRatio > best.intersectionRatio) best = e;
          } else if (!e.isIntersecting) {
            e.target.pause();
          }
        });
        if (best) {
          var v = best.target;
          if (v.paused && v.muted) {
            var p = v.play();
            if (p && p.catch) p.catch(function () { /* blocked: the poster stays */ });
          }
        }
      }, { threshold: [0, 0.6, 0.9] });
      clips.forEach(function (v) { watcher.observe(v); });

      document.addEventListener('visibilitychange', function () {
        if (document.hidden && playing) playing.pause();
      });
    }
  }

  /* ---- mobile bottom action bar on the event page ---- */
  if (document.querySelector('.mobile-cta')) document.body.classList.add('has-mobile-cta');
})();
