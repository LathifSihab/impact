# IMPACT — status against the brief

8 September 2026. Every "done" below was checked against the repo, not from memory.
Staging: https://demo-impact-c399e3.netlify.app (carries `noindex` until cutover).

**Legend:** ✅ done · 🟡 partly · ⛔ not started · 🔒 blocked on the client

---

## Open items — the whole list, most urgent first

### Blocked on the client (we cannot start these)

| # | Item | Blocks | Why it is urgent |
|---|---|---|---|
| 1 | **Mollie account + KYC started** | selling anything | Days of lead time entirely outside our control. Not started as far as we know. Nothing else on this list can rescue a late KYC. |
| 2 | **The 1–2 September events** — title, dates, location, age range, price, capacity | the CMS, the webshop, launch | Without them there is nothing to sell, and the event pages have structure but no real edition. |
| 3 | **Parental consent for the minors on camera**, in writing, per clip | launch | All four clips are now on the homepage. This is the one item that can stop a launch outright. |
| 4 | **Domain + DNS access**, and Wix account access | cutover, SEO carry-over | The Wix URL list must be exported *before* the subscription lapses or existing Google positions are lost. |
| 5 | **Privacy policy + algemene voorwaarden** | the waitlist and newsletter collecting real data | Legally required. The footer links are currently removed because there is no text. |
| 6 | **Which accounting system**, and who owns the login | the accounting integration | We will not custom-build against a guess. |
| 7 | Photo library as a Drive folder · **landscape 16:9 video** · logo + partner logos as SVG · expert portraits · FAQ answers · her own NL copy · transcripts for the clips | polish, and one photographic grade | Everything on staging is cropped out of the branddeck. The header video is still our generated placeholder — the four clips she sent are 480×848 portrait. |

### Our decision to make, and it changes what we build

| # | Item | Blocks | Note |
|---|---|---|---|
| 8 | **Backend: self-hosted Payload + Neon, or a ticketing platform** (Ticket Tailor / Eventix) | the CMS, the waitlist automation, payments, participants | Still open. The second option removes most of the September risk from our scope. Nothing built so far commits us either way. |

### Ours to do, no input needed

| # | Item | Note |
|---|---|---|
| 9 | **Analytics** — Plausible, goals, UTM plumbing | **Zero analytics on the site today.** GA4/GTM (`G-7BPTJHC9RB` / `GT-M6JH3H9D`) was started and interrupted, never installed. |
| 10 | **Store the signups** | The endpoints validate and capture `event`, `locale`, `source`, `utm_*` — nothing is written anywhere yet. |
| 11 | **The automated "registration opened" email** | Marked `TODO(17 Sep)` at the exact two lines in `web/src/pages/api/waitlist.ts` where it lands. |
| 12 | **Astro page parity** — 3 of 10 pages ported (`index`, `events`, `events/[slug]`) | over, samenwerken, social-impact, journal, media, contact, hosted-experiences still exist only as static HTML. |
| 13 | **`feat/astro-cms` has diverged** — 14 commits behind main, 16 ahead | The reel, preloader, sticky nav, mobile-nav fixes and every responsive fix are on `main` only. Rebase before doing more Astro work, or the branch will need the whole craft pass again. |
| 14 | A purpose-built 1200×630 OG share image | Currently reusing a content photo. |
| 15 | The Wix 301 redirect map | Needs item 4 first. |

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
| Bilingual NL + EN | ✅ | 10 Dutch + 10 English pages, working switch in the utility bar *and* the mobile menu, per-locale canonicals, both locales in the sitemap. **English is our translation, not her voice — she should review `i18n/en.json`** |
| Their own photography | ✅ | 18 crops harvested from the branddeck plus the brochure shoot. Her full library is item 7 🔒 |
| Their own video | 🟡 | All four participant clips live in a scroll-driven cinema reel, autoplaying muted, one at a time. The **landscape 16:9 header video is still a placeholder** we generated 🔒 |
| Horizontal image strips | ✅ | Fundamentals strip, partner marquee, media archive grid |
| Partner / collaboration page | ✅ | Tiers €2.000–€7.000, reach figures, nine partner logos as a 3×3, five ways to work together, three closing CTA cards |
| DRP BuildLab credit | ✅ | Hyperlinked in the footer of all 20 pages, in the homepage marquee, and as its own row under the partner grid |
| Responsive | ✅ | **20 pages × 15 widths, 320px to 1920px**: no horizontal overflow, no clipped content, no sliced words, no labels that do not fit. Repeatable via `tools/audit_responsive.html` |
| Sticky nav | ✅ | Spacious at the top, compacts past 50px, on both desktop and mobile |
| Preloader | ✅ | Kinetic wordmark into a split-curtain tear, 1.88s, once per session |

## Conversion

| Item | State | Note |
|---|---|---|
| Recurring CTAs | ✅ | Every page ends in a contextual CTA band or a three-card row |
| Newsletter visibility | ✅ | Band above the footer on every page, its own homepage section, card rows, and the exit-intent dome |
| SEO foundation | ✅ | Per-page titles/descriptions, canonical, hreflang both locales, OG + Twitter, JSON-LD, sitemap with 20 URLs, robots.txt, staging `noindex` by host |
| SEO results | 🟡 | Foundation only. A new domain needs content and links — September is indexing, not ranking |

## Events & waitlists — 🟡 the core is built, the automation is not

| Item | State | Note |
|---|---|---|
| Every event gets its own page | ✅ *(on `feat/astro-cms`)* | 4 event files generate 4 pages |
| Separate waitlist per event | ✅ *(branch)* | Renders from the event's own status and age range; the server re-checks the range |
| Self-serve: add events without a rebuild | 🟡 | The template proves out — but the CMS she edits in does not exist (item 8) |
| Automatic targeted email when registration opens | ⛔ | Item 11 |

## Backend & data

| Item | State | Note |
|---|---|---|
| Wix decision | ✅ | **No backend on Wix.** Let it lapse, keep it as a 301 source. Reasoning in `PLAN.md` §2 |
| Privacy-friendly analytics | ⛔ | Item 9 |
| All signups in one place | 🟡 | Item 10 |
| CMS / backoffice | ⛔ | Item 8 |

## Integrations

| Item | State | Note |
|---|---|---|
| Payments | ⛔ 🔒 | Item 1. Zero files in the repo reference Mollie or Stripe yet — deliberately, until KYC exists |
| Accounting | ⛔ 🔒 | Item 6 |
| SEO starter package | ✅ technical | See above |
| Webshop + events live by end of September | ⛔ 🔒 | Needs items 1, 2 and 8 |

---

## If you read one thing

Items **1, 2 and 8** decide whether anything ships in September. Everything else on
this page is work we can do on our own schedule. Items 9–13 are ours and none of
them are blocked — they are just not done.

Full blocker list with owners and consequences, plus the Dutch message to send:
`ASKS.md`. Content live on staging that still needs her yes: `SIGN-OFF.md`. How to
test any of it: `TESTING.md`.
