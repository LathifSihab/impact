# IMPACT — demo website

Static demo of the approved hi-fi design (`../IMPACT Hi-Fi Design.dc.html`, homepage structure 1a
from the wireframes). Three pages, no build step — open `index.html` in a browser, or serve the
folder with any static server.

- `index.html` — homepage, full 9-section flow
- `over.html` — one OVER page with sections Founders / Onze fundamenten (six long-form) / Voor wie / Team & experts
- `events.html` — Upcoming Events, Onze Formats, per-format sections (Camps, Days, Retreats, Community) and Alle events
- `event.html` — IMPACT Camp: Basketball Edition 2027, with the waitlist flow
- `hosted-experiences.html` — shared page under both EVENTS and SAMENWERKEN
- `samenwerken.html` — Partner worden / Experts & coaches / Voor bedrijven / Onze partners
- `social-impact.html` — IMPACT FOR ALL (Onze aanpak, Onze impact, Steun onze missie)
- `journal.html` — archive with category filter (Past events, Stories, Insights, Social impact, Partnerships, News)
- `media.html` — aftermovies, beeldarchief, pers, downloads
- `contact.html` — contact form and routing shortcuts
- `assets/css/style.css` — all design tokens live in `:root`
- `assets/js/main.js` — nav dropdowns, mobile menu, fundamentals scroll progress, FAQ, form validation
- `assets/img/` — photography cropped from the client brochure (`brief/IMPACT_FOLDER.pdf`)
- `assets/impact-brochure.pdf` — the client brochure, linked from the utility bar and every "Download brochure" CTA
- `../tools/inject.py` — the utility bar, nav, mobile menu and footer live here in one place; run
  `python tools/inject.py` from the project root after editing them and they are rewritten into every
  page between its `<!--NAV-->` / `<!--FOOTER-->` markers. `<body data-nav="...">` marks the active item.

Navigation and sitemap follow `brief/IMPACT WEBSITE-4.pdf`: utility bar (Brochure · Media · Journal ·
Contact), main nav OVER / EVENTS / SAMENWERKEN / SOCIAL IMPACT with the UPCOMING EVENTS button, and the
deliberate split between Formats (kinds of experience) and Events (bookable editions).

## Partner & host section
Built from `../IMPACT Homepage Wireframes.dc.html` (option 1a), which is the template for this block:
a white band with a hairline top *and* bottom, a `[ PARTNERS & HOSTS ]` label left with a note right,
and one endless track of evenly spaced logo slots (44px tall, hatched placeholder, each a link to
the partner). It pauses on hover and is gated behind `prefers-reduced-motion`. The same band is reused
on `samenwerken.html` above the full partner overview and on `hosted-experiences.html` as
`[ HOSTS & LOCATIES ]`. Each slot now holds a **real partner logo**, extracted from the
`.slider > .slide-track > .slide` markup on wemakeimpact.be (it lives in a `filesusr.com` HTML embed
iframe, which is why it is invisible to a plain page scrape). Nine partners, each linking to its own
site in a new tab: Talenco Group, SNM Event Agency, ODTH, Les Plumes, Foodmaker, Boshi, Decathlon,
Één Pot Nat, Flourish by Magnolia. Files in `assets/brand/partners/` — alpha-trimmed and capped at
120px tall; greyscale at rest, full colour on hover, as on the live strip.

The loop is seamless by construction: the track holds two identical `.mq-set`s and each cell carries its
spacing as `margin-right` (never a flex `gap`), so one set is exactly half the track and
`translateX(-50%)` lands the duplicate precisely where the original started — no jump, whatever the
number of logos. Spacing and cell width are tokens on `.marquee` (`--mq-gap` 90px / `--mq-cell` 170px,
stepping down to 64/150 on tablet and 40/120 on mobile), so one set is always wider than the viewport
and no empty run can appear. 42s linear, paused on hover, disabled under `prefers-reduced-motion`. The same nine fill the
`Onze partners` grid on `samenwerken.html`.

Two notes on the source data: the live slider's `alt` attributes are shifted one slide against their
`href`s (Talenco's link carries `alt="Foodmaker"`, and so on), so I paired each logo with its own brand
by looking at the artwork; and the Foodmaker slide's link on the live site points at a wixstatic image
URL instead of a site, so it links to foodmaker.be here — worth confirming with the client. Wireframe option 1b's two counter-running rows was not approved and is not used.

## Brand assets & founders (from the live site)
- `assets/brand/impact-logo.png` — the real `[IMPACT]` wordmark, pulled from wemakeimpact.be
  (`cb0c7c_59a6953d…~mv2.png`, 647×145, transparent). It replaces the typographic `[ ]` stand-in in the
  nav, the mobile menu and the footer; height is set in one CSS rule (`.logo img`). A vector (SVG)
  version is still worth requesting from the client for print and for retina crispness.
- `assets/brand/favicon.ico` + `favicon-32.png` + `favicon-180.png` — generated from the live site's
  `[]` beeldmerk (`favicon-source.png`, 64×64), linked from every page.
- `assets/img/founders/` — three photos from wemakeimpact.be/founders, cropped to 4:5 and 3:2.
- The Founders section on `over.html` now carries the real founders, Jean-Marc Mwema and Mirte Rens,
  with their own texts condensed from wemakeimpact.be/founders and the "And so this happened" duo story.

## Counters
`[data-counters]` rows count up once, when the row scrolls into view (IntersectionObserver at 0.35
threshold, 1400ms ease-out cubic, `Intl.NumberFormat('nl-BE')`, `font-variant-numeric: tabular-nums` so
nothing jitters). Under `prefers-reduced-motion` the final value renders immediately. Each number is
`<div class="n" data-count="24" data-prefix="€">` — set `data-count`, optional `data-prefix` /
`data-suffix`, and the markup fallback text is what non-JS visitors see.

The values (24 jongeren, 16 tickets, 8 partners, €12.500) are **demo placeholders**, deliberately modest
for an organisation with one edition behind it, and both counter rows say so in the note underneath. The
handoff asks for empty `000` until IMPACT confirms real figures — swap `data-count` and delete the note.

## Page headers
Every page now opens with the same hero treatment as the homepage: a full-bleed photo behind the text,
the handoff's dark gradient scrim, white display type, and the staggered on-load reveal (opacity + 28px
rise, 800ms ease-out, 90ms apart) — label, headline, intro, then the anchor-nav pills.

`.hero--page` is the inner-page variant of `.hero`: `min-height:560px` instead of 760px, growing taller
when the copy needs it (over.html runs to 651px for its four-line headline), fluid type via
`clamp(32px,5.4vw,72px)`, and a heavier scrim — `rgba(0,0,0,.84)` at the bottom against the homepage's
.72 — because these headers carry more copy over brighter frames. The anchor-nav pills switch to a white
outline on the dark ground. The old flat `.page-hero` and `.si-hero` rules are gone.

Photos used: over → the founders, events → the basketball court, samenwerken → hands/connection,
journal → a participant in motion, media → the archive jump shot, contact → arriving on location,
social-impact → two participants.

Two notes: the Social Impact page's hero was the hi-fi's two-column layout (headline left, 4:5 photo
right) and is now an image hero like the rest, so that page deviates from the design sheet — flag it with
the client if the original composition matters. And Journal's category chips moved out of the hero to sit
directly above the article grid, where they stay legible and tappable.

## Fundamentals row — auto-advance
The row is still a native horizontal scroller (wheel, drag, arrow keys, snap points); on top of that it
advances one card every **3s** and loops indefinitely: once the last card is reached it holds that same
3s, sweeps back to the first card and carries on. Timing is a `setTimeout` chain rather than an interval,
so the rewind finishes before the next step and every card gets its own full 3s. It only runs while the
row is at least 25% on screen, pauses on hover, on focus and when the tab is hidden, and **hands control
to the visitor permanently** on the first `pointerdown` / `wheel` / `touchstart` / `keydown`. Under
`prefers-reduced-motion: reduce` it never starts. The progress bar and `01 / 06` counter are driven by
the row's real scroll position, so they follow either way.

Two details worth knowing: if the next card would land within 80px of the end, it goes straight to the
end instead — otherwise the final stop is a sliver of a step that holds for 3s twice in a row. And the
track now sets `scroll-padding-left` to match its `padding-left`; without it the browser snapped the
first card flush against the viewport edge on load, eating the 72px page margin and starting the counter
at `02 / 06`.

Note: the hi-fi handoff says "do not build a custom carousel with autoplay" for this row. This was added
on request — it is autoplay in the sense the note warns about, so it is worth a second look with the
client. The implementation is deliberately the mildest version: no custom carousel, no cloned slides, no
hijacked scrolling, and it stops for good the moment anyone touches it. Removing it is deleting one block
in `assets/js/main.js` (marked "Auto-advance").

## Responsive
Audited on all 10 pages at 1440 / 1280 / 1024 / 834 / 768 / 430 / 390 / 375, plus an iPhone-sized
touch emulation. Result: no page scrolls horizontally at any of those widths, and nothing overflows the
viewport except the two elements that are meant to (the partner marquee and the fundamentals row).

Breakpoints: 1180px (page margin 72→40, section padding 120→72, grids narrow) and 820px (mobile — page
margin 20, section padding 48, nav collapses to the burger + full-screen overlay menu, every multi-column
grid stacks, event rows and format rows become cards, counters go 2x2, the event page's sticky waitlist
releases and the fixed bottom CTA bar takes over).

Three things the audit found and fixed:
1. **Headings did not scale.** Section headlines carried inline `style="font-size:60px"` etc., which no
   media query can override, so "Talent is everywhere. Opportunity isn't." and "Join the IMPACT
   community" ran off the right edge on phones. Those are now fluid utility classes
   (`.d-l--60/52/48/44/40`, `.pull-quote`) built on `clamp()`.
2. **Sub-pixel overflow on the event page.** The `margin:-0.5px` border-collapse trick on `.fund-cell`
   and `.expert-slot` pushed the document 1px wider than the viewport at =1024px; both grids now clip it
   with `overflow:hidden`.
3. **Touch targets.** Text links, the logo, marquee logos, filter chips, anchor-nav pills, footer links
   and the contact `select` were below the 44px minimum the brief asks for. A `max-width:820px` block
   raises them; text links grow upward (`align-items:flex-end`) so the underline stays tight to the text.
   Links inline inside a sentence stay at text size, which is the standard exemption.

## Brief compliance
Checked against all three documents in `brief/`. What changed after that pass:

From **IMPACT - Ecosysteem & bredere visie-3.pdf**
- Days: schools can book a one-off day *or a longer traject with several contact moments*; a Day needs
  no overarching medium — the fundamenten are the starting point.
- Camps: future editions can run on a different medium (Theater Edition, Multisport Edition …); the site
  now says explicitly that this is not a sports camp with workshops bolted on.
- Community: framed as more than a newsletter list — contact with peers, coaches, experts, knowledge and
  opportunities, and eventually the connective tissue between formats.
- Hosted Experiences: **not a fifth pillar** but another way of organising Days and Camps. The host owns
  ticketing, communication, marketing, location and the main programme; IMPACT adds team, experts and
  tailored content and works on a fixed fee. Added the City Pirates × IMPACT example.
- IMPACT FOR ALL: the four ways to contribute now match the brief exactly (finance a ticket, sponsor
  tickets at an activation, contribute to the fund, open up places as a partner) — two of the previous
  four were invented. Added that part of the fund is deliberately spent outside IMPACT's own
  activations, and the "one-off participation vs. durable follow-up" framing.
- Experts: the poule is described as the brief does, and the role slots now name the brief's expertise
  domains (movement, mentale vaardigheden, communicatie, voeding, ondernemerschap, persoonlijke
  ontwikkeling) instead of invented job titles.
- New `#systeem` section on over.html: the brief's own "logica achter het geheel" — brand → six
  fundamenten → life stages → formats & concrete activations, with the early-phase caveat.

From **IMPACT_FOLDER.pdf** (the brochure)
- The six fundamenten on over.html now carry the client's real copy, including each one's "Waar we op
  werken" list and the brochure's English one-liners. The invented Q&A columns are gone.
- New `#why` section: "Because young people deserve better tools." with the brochure's own text.
- Samenwerken opens with the brochure's partnership copy ("Let's build something meaningful …").
- Days described as the brochure does: workshops, schooldagen, talks, community events, hosted.
- Contact shows the phone number attributed to Mirte Rens, as in the brochure.

From **IMPACT WEBSITE-4.pdf**
- Homepage now has the testimonial teaser the sitemap asks for ("+ aantal testimonials"), as three
  clearly-marked pending slots — no invented quotes.
- The event page has the Partners block its content list requires.
- Journal's social category is labelled `IMPACT FOR ALL`, the name the brief uses.

### One conflict for the client to settle
The middle age band differs between sources: `IMPACT WEBSITE-4.pdf` and the approved hi-fi say
**15–18**, while the ecosystem brief and the brochure both say **14–18**. The site keeps **15–18**
(website brief + approved design). If the client confirms 14–18, it is a find-and-replace across
`index.html`, `over.html`, `events.html` and the age-group cards.

## Notes
- Copy is taken verbatim from the hi-fi design (Dutch body, English headlines). Placeholders that the
  design deliberately leaves empty stay empty: the IMPACT FOR ALL counters render as grey `000`,
  FAQ answers and the day schedule say "wordt aangeleverd door IMPACT".
- Type is Figtree via Google Fonts, the agreed stand-in for the brand font. Swapping it is one
  `--font` change.
- The hero uses a still instead of the aftermovie video, which has not been supplied.
- Team & experts renders the two founders as wide media cards (`.team-cards` / `.team-card`: portrait
  left, name + role + one line right), so a two-item row fills the full content width instead of leaving
  half of it empty. They collapse to one card per row at 1180px and stack image-over-text at 820px.
- Team & experts lists only the two real founders (with their own portraits, cropped per person as
  `mirte-45.jpg` / `jean-marc-45.jpg`); the expert poule is shown as four bordered role slots tied to a
  fundament, with no invented names, until IMPACT confirms people.
- Forms are client-side only — validation runs, nothing is sent or stored.
- Motion respects `prefers-reduced-motion`; pills are the only rounded element.
