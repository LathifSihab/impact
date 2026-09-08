/* Consent layer — built, tested, and deliberately invisible until it has
 * something to ask about.
 *
 * The site sets no advertising or analytics cookies today. A banner now would
 * ask permission for nothing, and cookie banners cost signups — so USES below
 * is empty and nothing renders. The moment a category is added to it, the
 * banner appears on the next page load and the gating below starts applying,
 * with no further work and nothing to remember on the day.
 *
 * To switch on privacy-friendly analytics:
 *
 *   1. add 'analytics' to USES
 *   2. wherever the tracker is loaded, wrap it:
 *        window.impactConsent.whenGranted('analytics', function () { ...load... });
 *
 * The same applies to 'embeds' for anything third-party that stores state — a
 * hosted checkout, a video embed, a social feed.
 *
 * What is deliberately NOT gated: the preloader's sessionStorage flag and the
 * newsletter dome's "don't show me again" value. Both are strictly necessary
 * for something the visitor asked for, both are first-party, neither identifies
 * anyone, and consenting to "do not nag me again" would be absurd.
 */
(function () {
  'use strict';

  /* ---- what this site currently uses. Empty means: no banner. ---- */
  var USES = [];

  var KEY = 'impact.consent';
  var VERSION = 1;                 // bump to re-ask after a material change
  var html = document.documentElement;
  var isEN = (html.lang || 'nl').slice(0, 2) === 'en';

  var COPY = {
    nl: {
      title: 'Mogen we meten hoe de site gebruikt wordt?',
      body: 'We gebruiken geen advertentiecookies en verkopen niets door. ' +
            'Je keuze geldt voor deze browser en je kan ze altijd aanpassen.',
      accept: 'Alles aanvaarden',
      reject: 'Alleen noodzakelijk',
      prefs: 'Voorkeuren',
      save: 'Bewaar mijn keuze',
      close: 'Sluiten',
      policy: 'Privacyverklaring',
      cats: {
        analytics: ['Statistieken',
                    'Hoeveel mensen de site bezoeken en welke pagina’s ze lezen. ' +
                    'Geen cookies, geen profielen.'],
        embeds: ['Externe inhoud',
                 'Onderdelen van andere diensten, zoals een ticketvenster of een video. ' +
                 'Die kunnen zelf gegevens opslaan.']
      }
    },
    en: {
      title: 'May we measure how the site is used?',
      body: 'We use no advertising cookies and sell nothing on. Your choice applies ' +
            'to this browser and you can change it at any time.',
      accept: 'Accept all',
      reject: 'Essential only',
      prefs: 'Preferences',
      save: 'Save my choice',
      close: 'Close',
      policy: 'Privacy statement',
      cats: {
        analytics: ['Statistics',
                    'How many people visit and which pages they read. ' +
                    'No cookies, no profiles.'],
        embeds: ['External content',
                 'Parts of other services, such as a ticket window or a video. ' +
                 'Those can store data themselves.']
      }
    }
  }[isEN ? 'en' : 'nl'];

  var POLICY = isEN ? '/en/privacy.html' : '/privacy.html';

  /* ---- stored decision ---- */
  function read() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (!raw || raw.v !== VERSION) return null;
      // a decision made before a new category existed is not a decision about it
      for (var i = 0; i < USES.length; i++) {
        if ((raw.asked || []).indexOf(USES[i]) === -1) return null;
      }
      return raw;
    } catch (e) { return null; }
  }

  function write(granted) {
    try {
      localStorage.setItem(KEY, JSON.stringify({
        v: VERSION, ts: Date.now(), asked: USES.slice(), granted: granted
      }));
    } catch (e) { /* storage blocked: the choice holds for this page only */ }
  }

  var decision = read();
  var listeners = [];

  function granted(cat) {
    return !!decision && decision.granted.indexOf(cat) > -1;
  }

  function settle(list) {
    decision = { v: VERSION, ts: Date.now(), asked: USES.slice(), granted: list };
    write(list);
    listeners.forEach(function (l) { if (granted(l.cat)) l.fn(); });
    listeners = listeners.filter(function (l) { return !granted(l.cat); });
  }

  /* ---- public API ---- */
  window.impactConsent = {
    granted: granted,
    whenGranted: function (cat, fn) {
      if (USES.indexOf(cat) === -1) return;   // not in use: never runs, never asks
      if (granted(cat)) { fn(); return; }
      listeners.push({ cat: cat, fn: fn });
    },
    open: function () { render(true); }
  };

  /* the footer entry point only makes sense once there is something to change */
  var opener = document.querySelector('[data-consent-open]');
  if (opener && USES.length) {
    opener.hidden = false;
    opener.addEventListener('click', function () { render(true); });
  }

  if (!USES.length) return;         // dormant: nothing to ask, so nothing to draw
  if (decision) {
    listeners = [];
    USES.forEach(function (c) { if (granted(c)) { /* consumers ran already */ } });
    return;
  }

  /* ---- the banner ---- */
  var el = null;
  var lastFocus = null;

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function render(showPrefs) {
    if (el) { el.remove(); el = null; }
    lastFocus = document.activeElement;

    var rows = USES.map(function (cat) {
      var c = COPY.cats[cat] || [cat, ''];
      return '<div class="consent-cat">' +
             '<input type="checkbox" id="consent-' + esc(cat) + '" value="' + esc(cat) + '" checked>' +
             '<label for="consent-' + esc(cat) + '"><b>' + esc(c[0]) + '</b>' +
             '<span>' + esc(c[1]) + '</span></label></div>';
    }).join('');

    el = document.createElement('div');
    el.className = 'consent' + (showPrefs ? ' consent--prefs' : '');
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'false');
    el.setAttribute('aria-label', COPY.title);
    el.innerHTML =
      '<div class="consent-inner">' +
        '<div class="consent-text">' +
          '<h2>' + esc(COPY.title) + '</h2>' +
          '<p>' + esc(COPY.body) + ' <a href="' + POLICY + '">' + esc(COPY.policy) + '</a></p>' +
          '<div class="consent-cats">' + rows + '</div>' +
        '</div>' +
        '<div class="consent-actions">' +
          '<button type="button" class="pill pill--primary pill--sm" data-all>' + esc(COPY.accept) + '</button>' +
          '<button type="button" class="pill pill--ghost pill--sm" data-none>' + esc(COPY.reject) + '</button>' +
          '<button type="button" class="linkish" data-prefs>' + esc(COPY.prefs) + '</button>' +
          '<button type="button" class="pill pill--primary pill--sm" data-save>' + esc(COPY.save) + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(el);

    function done(list) {
      settle(list);
      el.remove(); el = null;
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    el.querySelector('[data-all]').addEventListener('click', function () { done(USES.slice()); });
    el.querySelector('[data-none]').addEventListener('click', function () { done([]); });
    el.querySelector('[data-prefs]').addEventListener('click', function () {
      el.classList.add('consent--prefs');
      var first = el.querySelector('.consent-cat input');
      if (first) first.focus();
    });
    el.querySelector('[data-save]').addEventListener('click', function () {
      done(Array.prototype.filter
        .call(el.querySelectorAll('.consent-cat input'), function (i) { return i.checked; })
        .map(function (i) { return i.value; }));
    });

    // no focus trap and aria-modal="false" on purpose: this is a banner, not a
    // wall. The page stays readable and operable while the choice is pending,
    // which is both kinder and what a regulator expects of a genuine choice.
    var firstBtn = el.querySelector('button');
    if (firstBtn) firstBtn.focus();
  }

  render(false);
})();
