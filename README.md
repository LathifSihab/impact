# Handoff: IMPACT website — homepage, event page, social impact

## Overview
Redesign of the website for **IMPACT** (wemakeimpact.be), a Belgian youth development brand for ages 8–25. The current site is built around a single activation (IMPACT Camp: Basketball Edition). The redesign repositions the site around IMPACT as a brand and organisation, with an architecture that scales as new formats (Days, Camps, Retreats, Community, Hosted Experiences) and new editions are added, without reworking the site logic.

Three pages are designed in this bundle: the homepage (full 9-section flow), a single event page with a waitlist flow, and the Social Impact / IMPACT FOR ALL page. A design system sheet documents colour, type, buttons, grid, photography and motion.

Language: Dutch body copy, English headlines. That mix is intentional and comes from the client's own brochure.

## About the Design Files
The files in this bundle are **design references created in HTML** — prototypes that show the intended look, structure and behaviour. They are **not production code to copy directly**. They are authored as a single streaming component format with inline styles, which is a design-tool convention, not an app architecture.

The task is to **recreate these designs in the target codebase's existing environment** — React, Vue, Astro, Webflow, a CMS theme, whatever the project uses — following that codebase's established patterns, component library and styling approach. If no environment exists yet, pick the most appropriate stack for a content-driven marketing site with a CMS behind it (events, journal articles, formats and partners all need to be editable by the client without a developer).

Do not port the inline styles verbatim. Translate them into the codebase's token/utility system using the values in **Design Tokens** below.

## Fidelity
**High-fidelity.** Colours, type scale, spacing, radii and hover states are final and should be recreated faithfully. Two exceptions, both flagged in the design:

1. **Typography is a substitution.** No brand font files were supplied. Everything is set in **Figtree** (Google Fonts) as a stand-in for the geometric sans used on the current site. The *scale* is final; the family is expected to be swapped when the real brand font arrives. Keep the family in one place so the swap is a single change.
2. **All photography is a marked placeholder.** Every image slot is a warm gradient block labelled with the intended subject and crop. No stock photography, no AI-generated imagery. Real photography from IMPACT is required before launch.

A low-fidelity wireframe file is also included (`IMPACT Homepage Wireframes.dc.html`) showing two homepage structures; option **1a** was approved and is what the hi-fi implements.

## Screens / Views

### 1. Homepage
**Purpose:** a visitor understands what IMPACT is, feels the brand, discovers the formats, and either joins a waitlist or subscribes. The homepage deliberately does not explain everything — it creates curiosity and routes people onward.

**Layout:** single column, full-bleed sections stacked. Content grid is 12 columns, 1296px max content width, 72px page margin, 24px gutter. Section padding 120px top/bottom on desktop. Sections alternate white `#FFFFFF` and sand `#F5F1EA`; two sections are black `#111111` (Formats, footer). No horizontal rules between sections — the background change does the separating.

**Sections in order:**

| # | Section | Notes |
|---|---|---|
| — | Utility bar | Black `#111`, 11px 72px padding. Left: BROCHURE / MEDIA / JOURNAL / CONTACT. Right: IG / LI / TT, divider, NL / EN. Labels 10px/700, letter-spacing .16em, `rgba(255,255,255,.7)`, active language `#fff`. |
| — | Main nav | White, 22px 72px. Left: logo mark `[ ]` in `#D91F26`, 30px/800 — links to home. Centre: OVER / EVENTS / SAMENWERKEN / SOCIAL IMPACT, 12px/700, letter-spacing .12em. Right: primary pill "UPCOMING EVENTS". Nav items have dropdowns (see Information Architecture). |
| 01 | Hero | 760px tall, full-bleed video (16:9 aftermovie, muted autoplay loop). Overlay: `linear-gradient(to top, rgba(0,0,0,.72) 0%, rgba(0,0,0,.25) 48%, rgba(0,0,0,.1) 100%)`. Content bottom-left, 72px margin, 72px bottom padding. Headline "BUILDING / FOUNDATIONS / FOR THE NEW / GENERATION" in 4 lines, 88px/0.92, 800, letter-spacing -.03em, white. Below: intro paragraph (17px/1.6, max 520px, `rgba(255,255,255,.9)`) left, two pills right — primary "Ontdek IMPACT", secondary outline-white "Bekijk events". |
| 02 | Six fundamentals | White. Label `[ 02 — ONZE FUNDAMENTEN ]`. Headline "SIX FOUNDATIONS. / ONE STRONGER GENERATION." 56px/1.0. Supporting paragraph right-aligned in the header row, max 380px. Below: **horizontal scroll** row of 6 cards, each 432px wide, 24px gap, first card flush to the 72px margin, row overflows the right edge of the viewport. Card: 520px image (4:5) with the number 01–06 top-left at 46px/800 `rgba(255,255,255,.85)`, then title 26px/1.08/800 and body 14.5px/1.65 `#6B665E`. Under the row: a progress bar (200px red segment on a 560px `#EAE6DF` track) with "01 / 06", and the text link "MEER OVER ONZE FUNDAMENTEN →" right. |
| 03 | Voor wie | Sand. Three equal white cards, 24px gap. Each: 440px portrait (4:5), then age range 44px/800, a red 12.5px/600 tagline, body copy, and two outline pills (format tags). Ranges 8–14, 15–18, 18–25. |
| 04 | Upcoming events | White. Rows on a 200px / 1fr / 220px / 150px / 230px grid, 30px vertical padding, 1px `#EAE6DF` top border. Per row: 16:9 thumb, format label (red, 9.5px/700, .18em), title 30px/800, date + place stacked, age, and a right-aligned secondary pill "Zet me op de wachtlijst" with a small status line under it. Max 3–4 rows as a teaser; "ALLE EVENTS →" in the section header. Closing note explains the waitlist. |
| 05 | Formats | Black. Rows on 70px / 340px / 1fr / 150px / 40px. Format name as "IMPACT [Camps]" with the bracketed word in red — this bracket construction comes from the client's brochure and should be preserved. Description `rgba(255,255,255,.62)`, meta label, arrow right. Five rows: Camps, Days, Retreats, Community, Hosted. |
| 06 | Social impact | White, two columns 1.05fr / .95fr, 64px gap. Left: label, "IMPACT FOR ALL" (34px/800, FOR ALL in red), then "Talent is everywhere. / Opportunity isn't." at 60px/1.0, body copy, a four-up counter row, two pills. Right: 600px portrait (4:5) plus a pull-quote with a 3px red left border. |
| 07 | Journal | Sand. Four equal cards, 24px gap: 260px image (3:2), red category label, title 20px/1.2, meta line. Categories: PAST EVENT, STORY, INSIGHT, PARTNER. |
| 08 | Newsletter | White, two columns. Left: label, "JOIN THE / IMPACT COMMUNITY" 60px/0.98, body. Right: a single email field as a 2px black bottom-bordered row with the primary pill "Inschrijven" inline right, plus a small reassurance line. This is a full section, not a footer strip. |
| — | Partner marquee | White, 34px 0, top border. Label `[ PARTNERS & HOSTS ]`. Two-width flex row animated `translateX(0 → -50%)`, 30s linear infinite. Logo slots 46px tall, 1px `#EAE6DF` border. **Carried over from the current site at the client's explicit request** — each logo links to the partner. |
| 09 | Footer | Black. Grid 1.5fr + 5 × 1fr. First cell: red `[ ]` mark, tagline, social links. Then five link columns: IMPACT, EVENTS, SAMENWERKEN, SOCIAL IMPACT, INFO. Bottom bar: contact line left, Privacy · Algemene voorwaarden right. |

### 2. Event page — IMPACT Camp: Basketball Edition 2027
**Purpose:** give a parent enough information and confidence to join the waitlist. Conversion-focused.

**Layout:** nav → 620px hero → sticky black meta bar → two-column body (1fr / 400px, 72px gap, 110px section padding) → past-edition gallery → contact band.

- **Hero:** 620px, 16:9 photo, `linear-gradient(to top, rgba(0,0,0,.75), rgba(0,0,0,.15))` overlay. Three pills top (CAMP in red, 8–14 JAAR and WACHTLIJST OPEN in `rgba(255,255,255,.16)` with a `rgba(255,255,255,.4)` border), then "IMPACT [CAMP]" 34px/800 `rgba(255,255,255,.8)`, title "BASKETBALL / EDITION 2027" 82px/0.94, standfirst 18px/1.6 max 620px.
- **Meta bar:** black, 26px 72px, five key/value pairs (Format, Datum, Locatie, Leeftijd, Prijs) 64px apart; key 9.5px/600/.18em `rgba(255,255,255,.5)`, value 17px/700 white. Primary pill right. This bar is what makes the page feel bookable.
- **Left column:** Wat is het (46px/1.02 headline + 16px/1.75 body) → Programma (5 day rows, 110px / 1fr grid, 1px top borders) → Welke fundamenten (2-up grid of 6 bordered cells, number in red + name + English one-liner) → Experts & coaches (4-up portraits 4:5) → FAQ (accordion rows, 17px/600 question, red `+`, 1px `#EAE6DF` borders).
- **Right column (sticky, `top:24px`):** waitlist card on `#FAF8F5` with a 1px `#EAE6DF` border, 34px 32px padding. Heading "Deze editie is nog niet bevestigd" 28px/1.1, explanation, four fields (label 9.5px/600/.16em over a 1px `#DDD7CD` bottom border), full-width primary pill, and a note linking to IMPACT FOR ALL for financial support. Under it, a "Praktisch" card with key/value rows.
- **Past edition:** sand, "THIS WAS BASKETBALL EDITION 2026" with a 2fr/1fr/1fr image row and a link to the Journal recap. Closes the loop the client asked for: finished events move to Journal.
- **Contact band:** black, headline left, two pills right (Contacteer ons, Download brochure).

### 3. Social Impact — IMPACT FOR ALL
**Purpose:** explain why the social pillar exists, who it helps, and how to contribute. Navigation label is SOCIAL IMPACT (a new visitor does not know what IMPACT FOR ALL means); the page title is IMPACT FOR ALL.

Sections: hero (two columns, "Talent is everywhere. Opportunity isn't." at 76px/0.96 left, 520px 4:5 photo right, 19px/1.7 mission paragraph across 820px below) → Hoe het werkt (sand; three white cards numbered 01–03 in red 40px/800, plus a pull-quote block with a 3px red left border about the club-membership example) → counters (white, 2px black top rule, four-up at 76px/800) → Draag bij (**the one full-red section on this page**, four ways to contribute on 2px white top rules, two pills) → story (photo left, 40px/1.15 quote right, attribution, link to Journal) → contact band (black).

## Interactions & Behavior
- **Hero headline reveal, on load only.** Each of the four headline lines plus the intro and the button row animate `opacity 0→1` and `translateY(28px)→0`, 800ms, `ease-out`, staggered 90ms. Nothing else animates on scroll. Must respect `prefers-reduced-motion: reduce` (render final state, no transform).
- **Partner marquee:** continuous `translateX` loop, 30s linear infinite, duplicated track. Pause on hover is acceptable. Also gate behind `prefers-reduced-motion`.
- **Primary pill hover:** background `#D91F26 → #A8121A`, translateY(-1px), 150ms ease.
- **Secondary pill hover:** fills — border stays `#111`, background `#111`, label white.
- **Text link hover:** colour `#111 → #D91F26`, bottom border follows, arrow translates 4px right, 150ms.
- **Fundamentals row:** native horizontal overflow. Trackpad and wheel-horizontal, drag on touch, plus keyboard arrows when focused. Progress bar reflects scroll position. Do not build a custom carousel with autoplay.
- **Event rows (homepage 04):** whole row is a link to the event page; the waitlist pill is a separate target that jumps to the waitlist form anchor.
- **FAQ:** accordion, one open at a time is fine; `+` rotates to `×`. Use `<details>`/`<summary>` or a button with `aria-expanded`.
- **Waitlist form:** fields Voornaam deelnemer, Leeftijd, E-mailadres ouder, Gemeente (optional). Validation: name required (min 2), age required numeric within the event's range (reject with "Deze editie is voor 8–14 jaar"), email required and format-checked, gemeente optional. Submit → inline success state replacing the form ("Je staat op de wachtlijst") plus a confirmation email. Errors inline under the field in `#D91F26`, 12px. Never clear entered values on error.
- **Newsletter form:** email only, same inline success/error pattern.
- **Nav dropdowns:** open on hover on desktop with a ~120ms delay and on focus/click for keyboard; close on Escape and on outside click.
- **Sticky waitlist panel:** `position: sticky; top: 24px`, releases before the footer. Below 1024px it stops being sticky and moves inline after the "Wat is het" block; a fixed bottom action bar with the primary CTA takes over.

### Responsive
Designed desktop-first here at 1440, but the client brief is mobile-first — build mobile properly rather than compressing this.
- Page margin 72px → 40px (tablet) → 20px (mobile). Section padding 120px → 72px → 48px.
- Hero headline 88px → 56px → 40px; keep the four-line break at all sizes, it is part of the composition. Hero height 760px → 88vh on mobile.
- Nav collapses to the logo, a hamburger and the UPCOMING EVENTS pill. Full-screen black overlay menu: the four main items at ~34px, dropdown children indented beneath, utility links and socials at the bottom.
- Fundamentals stay a horizontal scroll on mobile, card ~78vw, snap points on.
- Voor wie: 3 columns → 1 column stacked, image 16:9 instead of 4:5.
- Events: table rows → stacked cards, thumb on top, CTA full width.
- Formats: rows → stacked, number and name on one line, description under.
- Journal: 4-up → 2-up tablet → 1-up mobile, or a snapped horizontal scroll.
- Counters: 4-up → 2×2.
- Touch targets minimum 44px; pills are already 48–52px tall.

## State Management
Marketing site, so state is local and small:
- `mobileNavOpen`, `openDropdown` (nav item id or null)
- `fundamentalsScrollIndex` (derived from scroll offset, drives the progress bar)
- `openFaqId`
- `waitlistForm`: `{ values, errors, status: 'idle' | 'submitting' | 'success' | 'error' }`
- `newsletterForm`: same shape

**Data fetching / CMS.** Everything repeating should be CMS-driven, not hardcoded: Events (title, format, edition year, date or "volgt", location, age range, status `waitlist | open | full | past`, hero image, gallery, programme days, experts, fundamentals covered, price, FAQ, partners), Formats, Fundamentals (number, name, EN one-liner, NL body, image), Age groups, Journal articles (category, title, image, body, related event), Partners (logo, url), IMPACT FOR ALL figures, Team & experts. The homepage event teaser is a query for the next 3–4 events with status `waitlist` or `open`, sorted by date; past events fall out of Events and are surfaced as Journal entries.

## Design Tokens

### Colour
| Token | Hex | Use |
|---|---|---|
| `--white` | `#FFFFFF` | base, content sections |
| `--sand` | `#F5F1EA` | alternating section background |
| `--sand-card` | `#FAF8F5` | waitlist card, callouts |
| `--black` | `#111111` | type, dark sections, footer |
| `--red` | `#D91F26` | CTA, labels, active nav, hover |
| `--red-dark` | `#A8121A` | primary button hover |
| `--grey-warm` | `#8D877D` | meta, captions |
| `--grey-body` | `#6B665E` | body copy on light |
| `--grey-muted` | `#A09A90` | fine print |
| `--border` | `#EAE6DF` | hairlines on white |
| `--border-sand` | `#DDD7CD` | hairlines on sand, outline pills |
| `--placeholder` | `#E2DDD4` | unconfirmed counter numbers |

Red is an accent only: CTAs, labels, hover, active nav, and exactly **one** full-colour section per page (Draag bij on the Social Impact page). Never a red section background on the homepage.

Dark-section text: white, `rgba(255,255,255,.62)` for body, `rgba(255,255,255,.5)` for meta, `rgba(255,255,255,.14)` for rules.

### Typography
Family: **Figtree** (400, 500, 600, 700, 800) — placeholder for the brand font. Small monospace numerics use the system mono stack.

| Role | Size / line-height | Weight | Letter-spacing | Case |
|---|---|---|---|---|
| Display XL (hero) | 88 / 0.92 | 800 | -0.03em | upper |
| Display L (section) | 52–60 / 1.0 | 800 | -0.03em | upper |
| Display M (page title) | 40–46 / 1.02 | 800 | -0.03em | upper or sentence |
| Heading | 26 / 1.08 | 800 | -0.015em | upper |
| Subheading | 20–22 / 1.2 | 700 | -0.01em | sentence |
| Intro | 17–19 / 1.6–1.7 | 400 | 0 | sentence |
| Body | 14.5–16 / 1.65–1.75 | 400 | 0 | sentence |
| Meta | 12.5–13.5 / 1.5 | 400–600 | 0 | sentence |
| Label / bracket | 10 / 1.0 | 700 | 0.20em | upper |
| Pill label | 11.5–13 / 1.0 | 700 | 0.06–0.10em | sentence or upper |
| Tag | 9.5 / 1.0 | 700 | 0.14–0.18em | upper |

Bracket labels are written `[ 02 — ONZE FUNDAMENTEN ]` with spaces inside the brackets. Format names are written `IMPACT [Camps]`. Both come from the client's brochure.

### Spacing
8px base. Used steps: 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 40, 44, 48, 54, 56, 60, 64, 70, 72, 80, 90, 96, 100, 110, 120. Section padding 120 desktop / 72 tablet / 48 mobile. Page margin 72 / 40 / 20. Grid gutter 24. Max content width 1296.

### Radius
Pills `999px` (carried over from the current site at the client's request). **Everything else is square** — cards, images, inputs, image slots all have `border-radius: 0`. That contrast is the whole visual idea: soft buttons, hard editorial blocks. Do not round cards.

### Borders & shadows
Hairlines 1px. Emphasis rules 2px `#111` or 2px `rgba(255,255,255,.55)` on red. Quote and callout accents 3px `#D91F26` left border. **No shadows anywhere.** No glassmorphism, no gradients other than the photo overlays and the placeholder fills.

### Motion
`--dur-fast: 150ms` (hover), `--dur-reveal: 800ms` (hero lines), `--ease: ease-out`, stagger `90ms`, marquee `30s linear infinite`.

## Assets
- **Logo:** the red bracket mark `[ ]` is rendered as type in these mockups (Figtree 800, `#D91F26`). The real logo and beeldmerk must be supplied as SVG and substituted — do not ship the typographic stand-in.
- **Photography:** none supplied. Every image slot is a labelled gradient placeholder stating subject and crop. Required: hero aftermovie (16:9 video), 6 fundamentals portraits (4:5), 3 age-group portraits (4:5), event hero (16:9), event thumbs (16:9), 4 expert portraits (4:5), journal images (3:2), 2 IMPACT FOR ALL portraits (4:5), 2026 gallery images. Treatment: warm grade, slightly desaturated, open blacks, no filters, no duotone. People in action or in conversation, not posed group shots. Portraits of minors need consent.
- **Partner logos:** needed as SVG (mono works best in the marquee).
- **Icons:** none used. Arrows are the text characters `→` and `+`. Keep it that way unless the client supplies an icon set.
- **Fonts:** Figtree via Google Fonts, to be replaced by the brand font.

## Information Architecture
Utility nav: BROCHURE · MEDIA · JOURNAL · CONTACT (+ socials, language).
Main nav: OVER · EVENTS · SAMENWERKEN · SOCIAL IMPACT, plus the UPCOMING EVENTS button. Logo links home; there is deliberately no "Home" item.

- **OVER** (one page, dropdown jumps to sections): Founders · Onze fundamenten · Team & experts
- **EVENTS**: Upcoming Events · Camps · Days · Retreats · Hosted Experiences · Alle events
- **SAMENWERKEN**: Partner worden · Hosted Experiences · Experts & coaches · Voor bedrijven · Onze partners
- **SOCIAL IMPACT**: → IMPACT FOR ALL page

Hosted Experiences appears under both EVENTS and SAMENWERKEN and resolves to the same page — a participant reads it as a type of event, a club reads it as a way to work with IMPACT.

Keep **Formats** (kinds of experience) and **Events** (concrete, bookable editions) distinct everywhere in copy, URLs and CMS models. Past events leave the events list and become Journal entries ("THIS WAS …").

## Content still to be supplied by the client
Brand font · logo and beeldmerk in vector · photography and the aftermovie · the 3–5 waitlist events with date, location and age range · the Basketball Edition 2027 day schedule · expert names and portraits · FAQ answers · IMPACT FOR ALL figures and one participant story with consent · partner logos in vector · the brochure PDF · per-fundamental long copy.

Nothing in these mockups invents statistics, testimonials, partnerships or claims. The IMPACT FOR ALL counters render as light grey `000` placeholders on purpose — they must stay empty until real figures are confirmed.

## Files
- `IMPACT Hi-Fi Design.dc.html` — the approved hi-fi designs. Four cards side by side: `2a` design system sheet, `2b` homepage, `2c` event page, `2d` Social Impact.
- `IMPACT Homepage Wireframes.dc.html` — low-fi homepage structures; `1a` (Editorial stack) was approved, `1b` (Bracket index) was not.
- `support.js` — runtime for the two HTML files above. Needed only to view them; not part of the implementation.
- `brief/IMPACT WEBSITE-4.pdf` — client briefing: structure, navigation, homepage flow, design requirements (Dutch).
- `brief/IMPACT - Ecosysteem & bredere visie-3.pdf` — brand vision, fundamentals, formats, IMPACT FOR ALL (Dutch).
- `brief/IMPACT_FOLDER.pdf` — brand brochure; source of the English headlines and the bracket typography.

Open the two HTML files in a browser to read the designs. The canvas pans and zooms.
