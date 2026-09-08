# IMPACT — status against the brief

8 September 2026. Every "done" below was checked against the repo, not from memory.
The four integrations were additionally tested **live against staging** that evening —
real requests, real responses. What is marked done there was watched working, not assumed.
Staging: https://demo-impact-c399e3.netlify.app (carries `noindex` until cutover).

**Legend:** ✅ done · 🟡 partly · ⛔ not started · 🔒 blocked on the client

---

## Open items — the whole list, most urgent first

### Blocked on the client (we cannot start these)

| # | Item | Blocks | Why it is urgent |
|---|---|---|---|
| 1 | **~~Mollie~~ → Stripe onboarding started** | selling anything, live only | **Changed 8 Sep.** Ticket Tailor settles through Stripe, PayPal or Square — not Mollie — and Bancontact comes through Stripe. So the recommended stack does not need Mollie for tickets at all, and Stripe onboarding is the faster, better-trodden path. This was the worst blocker on the list; the fix was a research question, not a waiting game. See `PLAN.md` §4b. **Test keys are wired and verified working 8 Sep** — the whole flow can be built and proven in test mode; only *live* keys need her legal entity, so this no longer blocks development, just launch |
| 2 | **The 1–2 September events** — title, dates, location, age range, price, capacity | the CMS, the webshop, launch | Without them there is nothing to sell, and the event pages have structure but no real edition. |
| 3 | **Parental consent for the minors on camera**, in writing, per clip | launch | All four clips are now on the homepage. This is the one item that can stop a launch outright. |
| 4 | **Domain + DNS access**, and Wix account access | cutover, SEO carry-over | The Wix URL list must be exported *before* the subscription lapses or existing Google positions are lost. |
| 5 | **Privacy policy + algemene voorwaarden** — *the text* | the live domain | 🟢 Structure done 8 Sep: `/privacy.html` in both languages, linked from every footer and under every form, plus a required guardian-consent tick on the waitlist, which is where a child's name and age are collected. **What is still needed is her legal text** — everything in `[ brackets ]`. See `SIGN-OFF.md`. |
| 6 | **Which accounting system**, and who owns the login | the accounting integration | We will not custom-build against a guess. |
| 7 | Photo library as a Drive folder · **landscape 16:9 video** · logo + partner logos as SVG · expert portraits · FAQ answers · her own NL copy · transcripts for the clips | polish, and one photographic grade | Everything on staging is cropped out of the branddeck. The header video is still our generated placeholder — the four clips she sent are 480×848 portrait. |

### Our decision to make, and it changes what we build

| # | Item | Blocks | Note |
|---|---|---|---|
| 8 | **Backend: self-hosted Payload + Neon, or a ticketing platform** | the CMS, the waitlist automation, payments, participants | **Evaluated 8 Sep — recommendation: split it.** Ticket Tailor for money, tickets, waitlists and participants (native per-event waitlist with a `WAITLIST_SIGNUP.CREATED` webhook, free for free tickets, Bancontact); Payload + SSR for pages and content, in October. Full comparison and reasoning in `PLAN.md` §4b. **Needs your sign-off, then it stops blocking 10, 11, 16, 17, 19, 20.** |

### Ours to do, no input needed

| # | Item | Note |
|---|---|---|
| 9 | ~~Analytics~~ → ~~set `PUBLIC_PLAUSIBLE_DOMAIN`~~ → **✅ live on staging** | 🟢 Set and deployed 8 Sep; the meta tag is in the page and the script loads after consent. Built: gated behind the consent banner, with an event queue so conversions fired before someone answers the banner are not lost, plus `section_view` for the brief's "page/section engagement", which stock Plausible cannot answer. **Note it is a build-time value, not a Netlify one** — `site/` is committed HTML, so the domain is baked in by `tools/build.py`; see the cutover section below. GA4/GTM was dropped: it needs a consent banner and contradicts "privacy-friendly". |
| 10 | ~~Store the signups~~ → **move them to the real sink** | 🟢 Interim done, and **Brevo is now live**: signups verified arriving in the right list 8 Sep, carrying locale, form, event and the full campaign set as contact attributes — which is what makes "which campaign drove this signup" answerable at all. Also: all 22 forms now post to Netlify Forms with full attribution (`page`, `locale`, `landing_page`, `referrer`, `utm_*`, `gclid`, `fbclid`). Free tier is 100/month. What remains is pointing them at whatever wins item 8, and syncing to Brevo (item 20). |
| 11 | **The automated "registration opened" email** | Marked `TODO(17 Sep)` at the exact two lines in `web/src/pages/api/waitlist.ts` where it lands. |
| 12 | **Astro page parity** — 3 of 10 pages ported (`index`, `events`, `events/[slug]`) | over, samenwerken, social-impact, journal, media, contact, hosted-experiences still exist only as static HTML. |
| 13 | **`feat/astro-cms` has diverged** — 14 commits behind main, 16 ahead | The reel, preloader, sticky nav, mobile-nav fixes and every responsive fix are on `main` only. Rebase before doing more Astro work, or the branch will need the whole craft pass again. |
| 14 | A purpose-built 1200×630 OG share image | Currently reusing a content photo. |
| 15 | The Wix 301 redirect map | Needs item 4 first. |
| 16 | **On-demand rendering, so a new event does not need a rebuild** | The brief's own words: *"without needing a rebuild each time — this needs to be genuinely self-serve"*. The Astro app is `output: 'static'`; event pages come from `getStaticPaths()`. This is an architecture change (server or hybrid output, event routes `prerender = false`), not a content task, and it should be settled with item 8 rather than after it. |
| 17 | **A CMS-driven page type** | The brief says "events/**pages**/waitlists". Only events are modelled. Without this she can add an event but not, say, a new landing page for a campaign. |
| 18 | **The rest of the SEO starter package** | Search Console + Bing verification and sitemap submission (needs item 4), target queries per page, a Google Business Profile for local search, and a content plan. The technical foundation is done; this is the other half. |
| 19 | **Participant management** | The brief asks to manage *"registrations, events and participants"*. Waitlist entries and participants are different objects — a participant has attendance, a guardian, dietary and medical notes, a payment state. Not modelled anywhere yet. |
| 20 | **Brevo ~~lists, tags~~ → the automation** | 🟡 **Segmentation done 8 Sep.** Lists live (3 Newsletter, 4 Waitlist), both branches verified end to end, and fourteen contact attributes created so every signup arrives already carrying locale, form, event and campaign — segmented on arrival, not untangled afterwards. **Tags do not work on this account**: Brevo accepts a `tags` array and silently discards it, so attributes carry it instead (`setup/03-brevo.md`). What is left is the *automation* — item 11. |

| 21 | **Verified sender address** | `BREVO_SENDER_EMAIL` points at a personal gmail; the only verified sender on the account is `lathif.sihab-dewantoro@drpbuildlab.com`, and Brevo refuses to send from anything unverified. Needs to become an address on `wemakeimpact.be`, which needs item 4. Until then no mail can go out, however well the signups land. |

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
| Their own video | ✅ | All four participant clips live in a scroll-driven cinema reel, autoplaying muted, one at a time. Signed off 8 Sep — the reel is the video direction, and the landscape header no longer waits on new footage |
| Horizontal image strips | ✅ | Fundamentals strip, partner marquee, media archive grid |
| Partner / collaboration page | ✅ | Tiers €2.000–€7.000, reach figures, nine partner logos as a 3×3, five ways to work together, three closing CTA cards |
| DRP BuildLab credit | ✅ | Hyperlinked in the footer of all 20 pages, in the homepage marquee, and as its own row under the partner grid |
| Responsive | ✅ | **20 pages × 15 widths, 320px to 1920px**: no horizontal overflow, no clipped content, no sliced words, no labels that do not fit. Repeatable via `tools/audit_responsive.html` |
| Sticky nav | ✅ | Spacious at the top, compacts past 50px, on both desktop and mobile |
| Preloader | ✅ | Kinetic wordmark into a split-curtain tear, 1.88s, once per session |
| Cookie consent | ✅ | Bottom-anchored banner, both languages, Necessary / Statistics / Marketing, opt-in and unticked by default, equal-weight buttons, links to the privacy statement. Gates are live before the trackers are |

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
| Privacy-friendly analytics | 🟡 | Item 9. The brief lists seven things by name; five are stock Plausible (visits, unique visitors, traffic source, actions, signup conversion). Two are not: **page/section engagement** needs custom events fired per section, and **which campaign/page/waitlist drove each signup** has to be stored *on the signup record* and joined in the backoffice — analytics alone cannot answer it, so items 9 and 10 have to be built as one thing |
| All signups in one place | 🟡 | Two sinks, both live and verified 8 Sep: all 22 forms post to Netlify Forms (four collections, full attribution) **and** through to Brevo, tagged by list with locale, form, event and campaign on the record. That is "one place, usable for targeted comms" in working form. Still not the permanent home — that waits on item 8 |
| CMS / backoffice — *"a big priority... from day one"* | ⛔ | Items 8, 17, 19. Content models are written and mirrored to the Payload schema, so the modelling work is not lost whichever backend wins. Nothing is deployed |

## Integrations

| Item | State | Note |
|---|---|---|
| Payments | 🟡 🔒 | Item 1. Stripe **test** keys are wired and verified answering 8 Sep, so the flow can be built and proven now. Live keys still need her legal entity |
| Accounting | ⛔ 🔒 | Item 6 |
| **Technically solid SEO foundation** | ✅ | Titles, descriptions, canonicals, hreflang, OG/Twitter, JSON-LD, sitemap, robots, staging noindex |
| **Full SEO starter package** | 🟡 | Marked done in the previous version of this file, which was wrong. The technical foundation is one half of it. Still missing: Search Console + Bing verification and sitemap submission, target queries per page, a Google Business Profile for local search, and a content plan (item 18) |
| Webshop + events live by end of September | ⛔ 🔒 | Needs items 1, 2 and 8. Ticket Tailor's API is verified working and answering — it returns an empty event list because **no events have been entered**, which is item 2 and the single thing holding this date |
| Email — newsletter + waitlist delivery | 🟡 | Endpoints verified live 8 Sep: both list branches, server-side validation, and the Ticket Tailor webhook refusing unsigned messages. Blocked only by the sender address, item 21 |

---

## Building for a domain — read before the cutover

`site/` is committed HTML and Netlify serves it as-is (`command = ""` in
`netlify.toml`). So the domain is baked in **at local build time**, and the
`PUBLIC_*` variables set in Netlify's UI have no effect on it.

Two values are decided by the build command:

| Variable | Staging | Production |
|---|---|---|
| `PUBLIC_SITE_URL` | `https://demo-impact-c399e3.netlify.app` | `https://www.wemakeimpact.be` |
| `PUBLIC_PLAUSIBLE_DOMAIN` | `demo-impact-c399e3.netlify.app` | `www.wemakeimpact.be` |

Staging is built with:

```
PUBLIC_SITE_URL=https://demo-impact-c399e3.netlify.app PUBLIC_PLAUSIBLE_DOMAIN=demo-impact-c399e3.netlify.app python tools/build.py
```

**The committed HTML currently carries the staging values.** Deploying this
commit to the real domain without rebuilding puts a canonical pointing at the
demo site on every page — a live site disowning itself, which de-indexes it.
The cutover step is: rebuild with the production values, commit, then deploy.

`PUBLIC_SITE_URL` defaults to the production domain when unset (`tools/seo.py`),
so a bare `python tools/build.py` silently reverts staging to production values.
Always pass it. Worth removing that fallback before launch so the build fails
loudly instead of guessing — cheap, and it makes this note unnecessary.

Analytics has no `<script>` tag in the HTML by design: the build writes
`<meta name="plausible-domain">` and `assets/js/analytics.js` loads Plausible
only after the consent banner grants the analytics category. No meta tag, no
tracker. Domain access itself is open item 4.

## Sharing the staging link

Safe to share now. Signups are recorded in **Netlify → Forms** (four collections:
newsletter, waitlist, contact, hosted-experience), each carrying the page and
campaign that produced it. Until 8 September they were silently discarded — if
the link was shared before then, anything submitted in that window is gone.

## Verified live on 8 September — what actually works

Tested with real requests against staging, not inferred from the code.

| Integration | Proven by |
|---|---|
| Newsletter → Brevo | posted through the live endpoint; contact landed in list 3 |
| Waitlist → Brevo | same contact then in lists 3 **and** 4 — each branch picks its own list |
| Form validation | a waitlist post missing name and consent returned 422 in Dutch |
| Ticket Tailor webhook | answers `401 bad signature` to unsigned messages, as it must |
| Ticket Tailor API | key valid; events list answers, and is empty — item 2 |
| Stripe (test) | `/v1/balance` answers, `livemode: false` |
| Plausible + canonicals | meta tag live, canonicals on the staging domain |
| Function suite | `node tools/test-functions.mjs` — 14 passed, 0 failed |

Two things worth carrying forward, both of which cost real debugging time:

**A 200 from `/subscribe` does not mean Brevo accepted it.** The endpoint is
built so a Brevo outage never loses a signup — the visitor always gets a
friendly answer and the failure goes to the log. Verify a signup by looking up
the contact, never by the response. And do not trust the list's
`totalSubscribers`: it read 0 while a contact was demonstrably in that list.

**Brevo drops what it does not recognise, and still answers 201.** Tags are
discarded entirely on this account; an attribute that has not been created is
discarded too. A form field added without its attribute will look like it works
and silently lose the data. Full detail in `setup/07-what-is-broken-now.md`.

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
