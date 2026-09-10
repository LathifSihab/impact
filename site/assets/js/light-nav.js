/* IMPACT — light direction: nav state
   Companion to light.css. main.js already publishes --nav-h and toggles
   `is-scrolled`; this file adds the two flags the overlay nav needs and
   nothing else.

     is-past-hero      the hero has left the top of the screen, so the nav
                       stops overlaying the video and becomes a real bar
     is-scrolling-down the reader is moving away from the top, so the bar
                       gets out of the way

   is-past-hero comes from an IntersectionObserver on a sentinel pinned to the
   hero's last 80px rather than from a scroll threshold: it stays correct when
   the hero is 100svh and the viewport changes height, which a hard-coded
   pixel number does not. */
(function () {
  'use strict';

  var body = document.body;
  if (!body || !body.classList.contains('is-light')) return;

  var root = document.documentElement;
  var hero = document.querySelector('.hero');
  var nav = document.querySelector('.nav');
  if (!nav) return;

  /* ---- is-past-hero ---- */
  if (hero && 'IntersectionObserver' in window) {
    var sentinel = document.createElement('div');
    sentinel.setAttribute('aria-hidden', 'true');
    sentinel.style.cssText = 'position:absolute;left:0;bottom:0;width:1px;height:80px;pointer-events:none';
    hero.appendChild(sentinel);

    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        root.classList.toggle('is-past-hero', !e.isIntersecting && e.boundingClientRect.top < 0);
      });
    }, { threshold: 0 }).observe(sentinel);
  } else if (!hero) {
    // a page with no hero has nothing to overlay: the nav is a bar from the start
    root.classList.add('is-past-hero');
  }

  /* ---- is-scrolling-down ----
     Same hysteresis idea as main.js: a small band so a nav sitting exactly on
     the turn cannot flap on a trackpad, and the bar is always revealed near
     the top of the page regardless of direction. */
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduced) {
    var last = window.scrollY || 0;
    var BAND = 8;      // ignore jitter below this
    var TOP = 120;     // always show the bar this close to the top
    var queued = false;

    function onScroll() {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        var y = window.scrollY || 0;
        var d = y - last;
        if (Math.abs(d) < BAND) return;
        if (y < TOP) root.classList.remove('is-scrolling-down');
        else root.classList.toggle('is-scrolling-down', d > 0);
        last = y;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Opening the mobile menu while the bar is hidden would leave no way back,
     so any menu interaction pins the bar visible. */
  var burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      root.classList.remove('is-scrolling-down');
    });
  }
})();
