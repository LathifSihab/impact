/* IMPACT demo — small local state only: nav, fundamentals scroll, faq, forms. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- hero reveal, on load only ---- */
  var hero = document.querySelector('[data-reveal-root]');
  if (hero) requestAnimationFrame(function () { hero.classList.add('is-revealed'); });

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
  function closeMobile() {
    if (!menu) return;
    menu.classList.remove('is-open');
    document.body.style.overflow = '';
  }
  var burger = document.querySelector('.burger');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      menu.classList.add('is-open');
      document.body.style.overflow = 'hidden';
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
    var step = function () { return track.children[0].offsetWidth + 24; };
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { track.scrollBy({ left: step(), behavior: reduced ? 'auto' : 'smooth' }); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { track.scrollBy({ left: -step(), behavior: reduced ? 'auto' : 'smooth' }); e.preventDefault(); }
    });
    update();

    /* Auto-advance: one card every 3s while the row is on screen. When the last
       card has been shown it holds that full 3s, sweeps back to the first card and
       carries on, so the row loops indefinitely. Timing is a setTimeout chain
       rather than an interval, so the rewind can finish before the next step and
       every card gets its own 3s. It hands control to the visitor for good on the
       first real interaction, pauses on hover/focus, and never runs under
       prefers-reduced-motion — the row stays a native scroller either way. */
    var AUTO_DELAY = 3000;
    var REWIND_SETTLE = 700;
    var timer = null, paused = false, surrendered = reduced, onScreen = false;

    function schedule(delay) {
      if (surrendered) return;
      stop();
      timer = setTimeout(function () {
        timer = null;
        schedule(tick());
      }, delay);
    }
    // returns the delay to use before the next step
    function tick() {
      if (paused || surrendered || !onScreen) return AUTO_DELAY;
      var max = track.scrollWidth - track.clientWidth;
      if (max <= 0) return AUTO_DELAY;
      if (track.scrollLeft >= max - 4) {          // all cards shown → start over
        track.scrollTo({ left: 0, behavior: 'smooth' });
        return AUTO_DELAY + REWIND_SETTLE;
      }
      // if the next card would land within a sliver of the end, go straight to the
      // end instead — otherwise the last stop is a 48px nudge that holds for 3s twice
      var next = track.scrollLeft + step();
      track.scrollTo({ left: next >= max - 80 ? max : next, behavior: 'smooth' });
      return AUTO_DELAY;
    }
    function start() { if (!timer && !surrendered) schedule(AUTO_DELAY); }
    function stop() { if (timer) { clearTimeout(timer); timer = null; } }
    function surrender() { surrendered = true; stop(); }

    ['pointerdown', 'wheel', 'touchstart', 'keydown'].forEach(function (ev) {
      track.addEventListener(ev, surrender, { passive: true });
    });
    track.addEventListener('mouseenter', function () { paused = true; });
    track.addEventListener('mouseleave', function () { paused = false; });
    track.addEventListener('focusin', function () { paused = true; });
    track.addEventListener('focusout', function () { paused = false; });
    document.addEventListener('visibilitychange', function () { paused = document.hidden; });

    if (!surrendered) {
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          onScreen = entries[0].isIntersecting;
          if (onScreen) start(); else stop();
        }, { threshold: 0.25 }).observe(track);
      } else {
        onScreen = true; start();
      }
    }
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

  var waitlist = document.getElementById('waitlist-form');
  if (waitlist) {
    var min = parseInt(waitlist.dataset.ageMin, 10);
    var max = parseInt(waitlist.dataset.ageMax, 10);
    waitlist.addEventListener('submit', function (e) {
      e.preventDefault();
      var fields = waitlist.querySelectorAll('.field');
      fields.forEach(function (f) { setError(f, ''); });
      var ok = true;
      var naam = waitlist.elements.naam, leeftijd = waitlist.elements.leeftijd, email = waitlist.elements.email;
      if (naam.value.trim().length < 2) { setError(naam.closest('.field'), 'Vul de voornaam van de deelnemer in.'); ok = false; }
      var age = Number(leeftijd.value);
      if (!leeftijd.value.trim() || Number.isNaN(age)) { setError(leeftijd.closest('.field'), 'Vul een leeftijd in.'); ok = false; }
      else if (age < min || age > max) { setError(leeftijd.closest('.field'), 'Deze editie is voor ' + min + '–' + max + ' jaar.'); ok = false; }
      if (!mail.test(email.value.trim())) { setError(email.closest('.field'), 'Vul een geldig e-mailadres in.'); ok = false; }
      if (!ok) return; // values are never cleared on error
      var card = waitlist.closest('.wl-card');
      card.innerHTML = '<h2>Je staat op de wachtlijst</h2><p class="body">We sturen een bevestiging naar ' +
        email.value.trim().replace(/[<>&]/g, '') +
        '. Zodra de datum van deze editie bevestigd is, krijg je als eerste bericht — nog zonder verplichting.</p>' +
        '<p class="meta" style="margin-top:18px">Demo: er wordt niets verzonden of opgeslagen.</p>';
      card.scrollIntoView({ block: 'center', behavior: reduced ? 'auto' : 'smooth' });
    });
  }

  var news = document.getElementById('newsletter-form');
  if (news) {
    news.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = news.querySelector('.form-msg');
      var v = news.elements.email.value.trim();
      if (!mail.test(v)) { msg.className = 'form-msg error'; msg.textContent = 'Vul een geldig e-mailadres in.'; return; }
      msg.className = 'form-msg ok';
      msg.textContent = 'Bedankt — je staat op de lijst. (Demo: er wordt niets verzonden.)';
      news.elements.email.value = '';
    });
  }

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
      if (msg) { msg.className = 'form-msg ok'; msg.textContent = 'Bedankt — je bericht is klaar om verzonden te worden. (Demo: er wordt niets verstuurd.)'; }
    });
  });

  /* ---- mobile bottom action bar on the event page ---- */
  if (document.querySelector('.mobile-cta')) document.body.classList.add('has-mobile-cta');
})();
