# IMPACT — website

Redesign and rebuild of wemakeimpact.be for **IMPACT**, a Belgian youth development
brand for ages 8–25. Built by [DRP BuildLab](https://drpbuildlab.com).

**→ To run and test it, start with [TESTING.md](TESTING.md).**

## What is in this repo

| Path | What it is |
|---|---|
| `site/` | The static craft-pass site. 10 pages, hand-written HTML/CSS/JS, no build step. **This is what staging serves and what the client reviews.** |
| `web/` | The Astro 5 app that replaces it — **on the `feat/astro-cms` branch**, not on `main`, until it reaches page parity and the backend choice is settled. `git checkout feat/astro-cms` |
| `i18n/en.json` | Every translatable string, keyed by the Dutch original. English copy is edited here, not in markup |
| `tools/` | The scripts that maintain both: shared nav/footer, SEO head, image variants, deck harvesting, the placeholder video, content seeding |
| `brief/` | Client briefs, the 18 branddeck slides, reference captures, and `brief/docs/` — the build documentation that drives the current phase |
| `PLAN.md` | Stack decision, the events/waitlist architecture, staged timeline |
| `ASKS.md` | Open blockers by phase, and the message to send the client |
| `SIGN-OFF.md` | Content live on staging that IMPACT has not confirmed yet |
| `TESTING.md` | How to test everything end to end |

## The short version of the stack

Astro on Netlify · **Payload 3** on Neon Postgres for content *and* registrations in
one admin · Brevo for newsletter, double opt-in and the per-event "registration
opened" campaign · Mollie for payments · Plausible for cookieless analytics.
**No Wix backend** — the subscription lapses and becomes a 301 source. Reasoning in
[PLAN.md](PLAN.md) §2–4.

## Where the phases stand

- **Craft pass (10 Sep)** — done. Colour and type corrected from the branddeck, the
  headline construction rebuilt, photo-strip / stat-block / tier-table /
  newsletter-dome / CTA cards built, real camp photography in, a placeholder hero
  video, accessibility and responsive pass. See `site/README.md`.
- **CMS (17 Sep)** — in progress on **`feat/astro-cms`**. The Astro app builds, content
  models mirror the Payload schema, event pages generate per entry, and the form
  endpoints validate and capture attribution. Held on a branch because the backend
  choice is still open: self-hosted Payload versus a ticketing platform that already
  does waitlists, payments and participant management (see the options table in the
  handover notes). Nothing built so far is specific to either — only the loader behind
  `src/content.config.ts` changes.
- **Sellable (24 Sep)** and **launch (30 Sep)** — blocked on the client. See
  [ASKS.md](ASKS.md).

## Maintaining the static site

```bash
python tools/inject.py          # shared utility bar, nav, mobile menu, newsletter band, footer
python tools/seo.py             # titles, canonical, hreflang, OG, JSON-LD, sitemap.xml, robots.txt
python tools/i18n.py --extract  # pick up any new Dutch strings into i18n/en.json
python tools/i18n.py            # regenerate site/en/ from the Dutch pages
```

Run all four after editing a page. The Dutch pages are the source; `site/en/` is
generated and should never be edited by hand.

Run both after editing their templates. `site/README.md` documents the design system
and every decision the craft pass took.

## Content still owed by the client

Brand font · logo and beeldmerk as SVG · partner logos as SVG · the aftermovie /
banner video master · the photo library · the September events with dates, price and
capacity · FAQ answers · the 2027 day programme · expert portraits · testimonial
consent · privacy policy and terms. Full list with owners and consequences in
[ASKS.md](ASKS.md).

## Rebuilding

```bash
python tools/build.py
```

inject → seo → fingerprint → i18n → check. Always this, never the individual
tools: fingerprint has to run before i18n or the English pages keep the previous
asset hash, and check is what catches a lost closing tag before it ships.
