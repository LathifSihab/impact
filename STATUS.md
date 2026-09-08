# IMPACT — status against the brief

8 September 2026. Every "done" below was checked against the repo, not from memory.
Staging: https://demo-impact-c399e3.netlify.app (carries `noindex` until cutover).

**Legend:** ✅ done · 🟡 partly · ⛔ not started · 🔒 blocked on the client

---

## Open items — the whole list, most urgent first

### Blocked on the client (we cannot start these)

| # | Item | Blocks | Why it is urgent |
|---|---|---|---|
| 1 | **~~Mollie~~ → Stripe onboarding started** | selling anything | **Changed 8 Sep.** Ticket Tailor settles through Stripe, PayPal or Square — not Mollie — and Bancontact comes through Stripe. So the recommended stack does not need Mollie for tickets at all, and Stripe onboarding is the faster, better-trodden path. This was the worst blocker on the list; the fix was a research question, not a waiting game. See `PLAN.md` §4b |
| 2 | **The 1–2 September events** — title, dates, location, age range, price, capacity | the CMS, the webshop, launch | Without them there is nothing to sell, and the event pages have structure but no real edition. |
| 3 | **Parental consent for the minors on camera**, in writing, per clip | launch | All four clips are now on the homepage. This is the one item that can stop a launch outright. |
| 4 | **Domain + DNS access**, and Wix account access | cutover, SEO carry-over | The Wix URL list must be exported *before* the subscription lapses or existing Google positions are lost. |
| 5 | **Privacy policy + algemene voorwaarden** | the waitlist and newsletter collecting real data | Legally required. The footer links are currently removed because there is no text. |
| 6 | **Which accounting system**, and who owns the login | the accounting integration | We will not custom-build against a guess. |
| 7 | Photo library as a Drive folder · **landscape 16:9 video** · logo + partner logos as SVG · expert portraits · FAQ answers · her own NL copy · transcripts for the clips | polish, and one photographic grade | Everything on staging is cropped out of the branddeck. The header video is still our generated placeholder — the four clips she sent are 480×848 portrait. |

### Our decision to make, and it changes what we build

| # | Item | Blocks | Note |
|---|---|---|---|
| 8 | **Backend: self-hosted Payload + Neon, or a ticketing platform** | the CMS, the waitlist automation, payments, participants | **Evaluated 8 Sep — recommendation: split it.** Ticket Tailor for money, tickets, waitlists and participants (native per-event waitlist with a `WAITLIST_SIGNUP.CREATED` webhook, free for free tickets, Bancontact); Payload + SSR for pages and content, in October. Full comparison and reasoning in `PLAN.md` §4b. **Needs your sign-off, then it stops blocking 10, 11, 16, 17, 19, 20.** |

### Ours to do, no input needed

| # | Item | Note |
|---|---|---|
| 9 | **Analytics** — Plausible, goals, UTM plumbing | **Zero analytics on the site today.** GA4/GTM (`G-7BPTJHC9RB` / `GT-M6JH3H9D`) was started and interrupted, never installed. |
| 10 | ~~Store the signups~~ → **move them to the real sink** | 🟢 Interim done: all 22 forms now post to Netlify Forms with full attribution (`page`, `locale`, `landing_page`, `referrer`, `utm_*`, `gclid`, `fbclid`). Free tier is 100/month. What remains is pointing them at whatever wins item 8, and syncing to Brevo (item 20). |
| 11 | **The automated "registration opened" email** | Marked `TODO(17 Sep)` at the exact two lines in `web/src/pages/api/waitlist.ts` where it lands. |
| 12 | **Astro page parity** — 3 of 10 pages ported (`index`, `events`, `events/[slug]`) | over, samenwerken, social-impact, journal, media, contact, hosted-experiences still exist only as static HTML. |
| 13 | **`feat/astro-cms` has diverged** — 14 commits behind main, 16 ahead | The reel, preloader, sticky nav, mobile-nav fixes and every responsive fix are on `main` only. Rebase before doing more Astro work, or the branch will need the whole craft pass again. |
| 14 | A purpose-built 1200×630 OG share image | Currently reusing a content photo. |
| 15 | The Wix 301 redirect map | Needs item 4 first. |
| 16 | **On-demand rendering, so a new event does not need a rebuild** | The brief's own words: *"without needing a rebuild each time — this needs to be genuinely self-serve"*. The Astro app is `output: 'static'`; event pages come from `getStaticPaths()`. This is an architecture change (server or hybrid output, event routes `prerender = false`), not a content task, and it should be settled with item 8 rather than after it. |
| 17 | **A CMS-driven page type** | The brief says "events/**pages**/waitlists". Only events are modelled. Without this she can add an event but not, say, a new landing page for a campaign. |
| 18 | **The rest of the SEO starter package** | Search Console + Bing verification and sitemap submission (needs item 4), target queries per page, a Google Business Profile for local search, and a content plan. The technical foundation is done; this is the other half. |
| 19 | **Participant management** | The brief asks to manage *"registrations, events and participants"*. Waitlist entries and participants are different objects — a participant has attendance, a guardian, dietary and medical notes, a payment state. Not modelled anywhere yet. |
| 20 | **Brevo lists, tags and the automation** | "Usable for targeted comms/automations later" means segmented on arrival — per event, per locale, per source — not one flat list to be untangled afterwards. |

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
| Self-serve **new pages**, not just events | ⛔ | The brief says "events/pages/waitlists". Only events are modelled — there is no CMS-driven page type at all (item 17) |
| Separate waitlist per event, **where relevant** | 🟡 | `status` is modelled as waitlist / open / full / past and the page branches on it, so "where relevant" is right in principle. But the `open` branch has no purchase flow behind it, because there are no payments yet (item 1) |
| Self-serve: add events **without a rebuild** | ⛔ | Overstated in the previous version of this file. `astro.config.mjs` is `output: 'static'` and `[slug].astro` uses `getStaticPaths()`, so **every new event needs a rebuild and redeploy** — the exact thing the brief rules out. Needs on-demand rendering (item 16) |
| Automatic targeted email when registration opens | ⛔ | Item 11 |

## Backend & data

| Item | State | Note |
|---|---|---|
| Wix decision — *"that call is entirely yours"* | ✅ | **Build no backend on Wix.** It is a closed platform: its data layer cannot be queried by our stack, its automations cannot be triggered from our forms, and anything built there has to be rebuilt when the subscription ends. Since the year is already paid, keep it running as the 301 redirect source until it lapses — that is the one thing it is genuinely useful for. Reasoning in `PLAN.md` §2 |
| Privacy-friendly analytics | ⛔ | Item 9. The brief lists seven things by name; five are stock Plausible (visits, unique visitors, traffic source, actions, signup conversion). Two are not: **page/section engagement** needs custom events fired per section, and **which campaign/page/waitlist drove each signup** has to be stored *on the signup record* and joined in the backoffice — analytics alone cannot answer it, so items 9 and 10 have to be built as one thing |
| All signups in one place | 🟡 | Interim sink live: all 22 forms post to Netlify Forms, in four collections, each submission carrying the campaign and page that produced it. Not yet the permanent home (item 8) and not yet segmented into Brevo (item 20) |
| CMS / backoffice — *"a big priority... from day one"* | ⛔ | Items 8, 17, 19. Content models are written and mirrored to the Payload schema, so the modelling work is not lost whichever backend wins. Nothing is deployed |

## Integrations

| Item | State | Note |
|---|---|---|
| Payments | ⛔ 🔒 | Item 1. Zero files in the repo reference Mollie or Stripe yet — deliberately, until KYC exists |
| Accounting | ⛔ 🔒 | Item 6 |
| **Technically solid SEO foundation** | ✅ | Titles, descriptions, canonicals, hreflang, OG/Twitter, JSON-LD, sitemap, robots, staging noindex |
| **Full SEO starter package** | 🟡 | Marked done in the previous version of this file, which was wrong. The technical foundation is one half of it. Still missing: Search Console + Bing verification and sitemap submission, target queries per page, a Google Business Profile for local search, and a content plan (item 18) |
| Webshop + events live by end of September | ⛔ 🔒 | Needs items 1, 2 and 8 |

---

## Sharing the staging link

Safe to share now. Signups are recorded in **Netlify → Forms** (four collections:
newsletter, waitlist, contact, hosted-experience), each carrying the page and
campaign that produced it. Until 8 September they were silently discarded — if
the link was shared before then, anything submitted in that window is gone.

## If you read one thing

Items **1, 2, 8 and 16** decide whether anything ships in September. 16 is new to
this list: "self-serve without a rebuild" is a requirement the current
architecture cannot satisfy, and it is cheaper to settle alongside the backend
choice than to retrofit afterwards. Everything else here is work we can schedule
ourselves — items 9–20 are ours and none of them are blocked. They are just not
done.

Full blocker list with owners and consequences, plus the Dutch message to send:
`ASKS.md`. Content live on staging that still needs her yes: `SIGN-OFF.md`. How to
test any of it: `TESTING.md`.
