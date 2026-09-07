# IMPACT — status against the brief

7 September 2026. Every "done" below was checked against the repo, not from memory.
Staging: https://demo-impact-c399e3.netlify.app (carries `noindex` until cutover).

**Legend:** ✅ done · 🟡 partly · ⛔ not started · 🔒 blocked on the client

---

## Audiences — ✅ done

Six routes on the homepage, each one click from its next step, in both languages.

| Visitor | Next step |
|---|---|
| Young people / parents | Events → waiting list |
| Companies, sponsors, partners | Partner with us → For companies |
| Clubs / organisations | Hosted Experiences |
| Coaches / experts | Partner with us → Experts & coaches |
| Supporters of the social mission | IMPACT FOR ALL → Contribute |
| First-time visitors | About IMPACT |

## Visual direction

| Item | State | Note |
|---|---|---|
| Bilingual NL + EN | ✅ | 10 Dutch + 10 English pages, working switch, per-locale canonicals, both locales in the sitemap. **English is our translation, not her voice — she should review `i18n/en.json`** |
| Their own photography | ✅ | 18 crops harvested from the branddeck (real camp photography) + the brochure shoot. Their full library is still outstanding 🔒 |
| Their own video | 🟡 | 4 participant clips live, autoplaying muted on scroll. The **landscape 16:9 header video is still a placeholder** we generated — the four clips they sent are 480×848 portrait 🔒 |
| Horizontal image strips | ✅ | Fundamentals strip on red, partner marquee, media archive grid |
| Partner / collaboration page | ✅ | Partnership tiers €2.000–€7.000, reach figures, nine real partner logos, five ways to work together, three closing CTA cards |
| DRP BuildLab in the footer, hyperlinked | ✅ | On all 20 pages |
| Current site checked for tone | ✅ | Logo, favicon, founders and all nine partner logos pulled from the live site; brand deck is the visual authority |

## Conversion

| Item | State | Note |
|---|---|---|
| Recurring CTAs | ✅ | Every page ends in a contextual CTA band or a three-card row — 8 pages carry one, plus per-section links |
| Newsletter visibility | ✅ | Full-width band above the footer on every page, its own section on the homepage, three-card row on key pages, and the Capital-style dome (exit-intent desktop / 60% scroll mobile, once per visitor) |
| SEO foundation | ✅ | Per-page titles/descriptions, canonical, hreflang both locales, OG + Twitter, JSON-LD (Organization, WebSite, Event, BreadcrumbList), sitemap with 20 URLs, robots.txt, staging `noindex` by host |
| SEO results | 🟡 | Foundation only. Ranking a new domain needs content and links — September is indexing, not results |

## Events & waitlists — 🟡 the core is built, the automation is not

| Item | State | Note |
|---|---|---|
| Every event gets its own page | ✅ *(on `feat/astro-cms`)* | 4 events generate 4 pages from content files |
| Separate waitlist per event | ✅ *(branch)* | Form renders from the event's own status and age range; server re-checks the range |
| Self-serve: add events without a rebuild | 🟡 | The template exists and proves out — **but the CMS she edits in does not** (backend decision open) |
| Automatic targeted email when registration opens | ⛔ | Marked `TODO(17 Sep)` at the exact two lines where it lands |

## Backend & data

| Item | State | Note |
|---|---|---|
| Wix decision | ✅ | **No backend on Wix.** Let it lapse, keep it as a 301 source. Reasoning in `PLAN.md` §2 |
| Privacy-friendly analytics | ⛔ | Zero analytics on the site today. Plausible is the choice; not installed |
| All signups in one place | 🟡 | Endpoints validate and capture `event`, `locale`, `source`, `utm_*` — the attribution that answers "which campaign drove this signup" — but nothing is **stored** yet |
| CMS / backoffice | ⛔ | Content models written and mirrored to the Payload schema; no CMS deployed. **Decision needed:** self-hosted Payload vs a ticketing platform that already does waitlists, payments and participants |

## Integrations

| Item | State | Note |
|---|---|---|
| Payments | ⛔ 🔒 | Mollie chosen. **KYC not started — this is the single biggest risk to selling in September** |
| Accounting | ⛔ 🔒 | Cannot start: we do not know which system they use |
| SEO starter package | ✅ technical | See above |
| Webshop + events live by end of September | ⛔ 🔒 | Needs the events, Mollie, and the backend decision |

---

## The three things that decide the rest

1. **Mollie KYC has not started.** Days of lead time, entirely outside our control. Without it there is no selling in September, whatever else we build.
2. **The backend call is still open** — Payload vs a ticketing platform. The second removes the waitlist automation, payments and participant management from our scope, which is precisely the work threatening 24 and 30 September. Nothing built so far is specific to either.
3. **No September events have been supplied.** Title, dates, location, age range, price, capacity. Without them there is nothing to sell.

Full blocker list with owners and consequences: `ASKS.md`. Content live on staging
that still needs her yes: `SIGN-OFF.md`.
