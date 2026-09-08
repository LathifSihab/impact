# IMPACT — build plan, stack decision and open asks

Status: 7 September 2026. Written against the client's latest brief (6 audiences, bilingual,
self-serve events + waitlists, CMS, analytics, payments, SEO, webshop).

---

## 1. The timeline needs a decision today

The brief asks for "first full version ready for 10 September" — that is **3 days** — and
"1–2 events live by end of September".

A full version in 3 days is not achievable if "full" includes CMS, bilingual copy, payments,
webshop and automated per-event waitlist mails. What *is* achievable is a genuine, useful
milestone on the 10th, with the revenue-critical parts following inside September. Proposed split:

| Date | Deliverable | State |
|---|---|---|
| **10 Sep** | **Reviewable v1, live on a staging domain.** All 10 pages, real photography, NL copy slots, audience routing, recurring CTAs, newsletter + waitlist capture that really stores signups, privacy analytics, full SEO foundation. | Client can click every flow and start pasting her own copy. |
| **17 Sep** | CMS live (client adds/edits events, journal articles, partners, experts herself). Per-event waitlist with double opt-in. Signups exported/synced into one audience tool with per-event tags. | Client self-serve for content. |
| **24 Sep** | Payments + ticketing on one live event, invoice/accounting hook, EN version wired (needs her EN copy), "registration opened" automation firing to that event's waitlist. | First event sellable. |
| **30 Sep** | 1–2 events live and selling. Webshop if the product list exists by then. | Launch. |

If the 10th must include *everything*, the honest answer is that scope has to shrink — most
likely the webshop and the EN version move to October. Flag which way you want it and I'll
re-cut the plan.

---

## 2. Wix: no. Here's the call.

**Recommendation: do not attach any backend to Wix. Let the subscription run out and use it only
as a 301 redirect source once the new domain is live.**

Why:
- Wix Events/Stores cannot be driven cleanly from an external front-end. There is no supported
  way to run our own pages against their booking data, so we'd end up with two front-ends.
- The self-serve requirement ("add new events/pages/waitlists themselves, no rebuild") is
  exactly what Wix's editor *seems* to solve and then doesn't: waitlist → "registration opened"
  automation per event, with campaign attribution, is not something Wix Automations does at the
  granularity asked for here.
- Data would live in a place we cannot easily model, query or migrate. The brief's own priority
  is "manage data, registrations, events and participants cleanly from day one" — that argues
  for one system we control, not two half-systems.
- The paid year is a sunk cost either way. Keeping it as a redirect preserves the existing SEO
  value, which is worth more than its CMS.

**One exception worth considering:** if the client wants to keep selling through Wix's existing
checkout while we build, we can keep the current Wix camp page alive on a subdomain
(`camp.wemakeimpact.be`) for a few weeks and point the new site's CTAs at it. It buys time
without contaminating the new architecture.

---

## 3. Stack

| Layer | Choice | Why this one |
|---|---|---|
| Front-end | **Astro** (static + islands), deployed on **Netlify** | Ships the current hand-built HTML/CSS almost as-is (no rewrite), zero-JS by default so the photography-heavy pages stay fast, first-class i18n routing for NL/EN, and content collections that map onto a CMS cleanly. |
| CMS / backoffice | **Payload 3** (self-hosted, Postgres on **Neon**) | The client's stated top priority is *one* clean place for content **and** registrations. Payload gives content types (events, journal, partners, experts, formats) *and* the signup/participant tables *and* the admin UI in a single app, with hooks to fire the emails. A headless-CMS-plus-separate-database split would give her two logins and no participant view. |
| Signups & participants | Payload collections: `waitlist_entries`, `newsletter_subscribers`, `registrations`, `orders` | One place, queryable, exportable, with `event`, `source`, `utm_*` and `locale` on every row — which is what makes the campaign attribution in the brief possible. |
| Email | **Brevo** (EU/GDPR, transactional + campaigns + automations in one) | Newsletter, double opt-in, per-event lists/tags, and the "registration opened" campaign to one event's waitlist all live in the tool the client will actually use afterwards. Payload writes the contact + tag; Brevo owns the sending. |
| Payments | **Mollie** | Belgian, Bancontact + iDEAL + card + Apple Pay, straightforward invoicing exports, cheaper than Stripe for BE consumer payments. Stripe stays a drop-in alternative if she prefers its dashboard. |
| Accounting | Whichever she uses — needs confirming (Billit / Teamleader / Yuki / Exact are the common BE options) | Mollie → accounting via the provider's native connector where one exists; otherwise a nightly export of paid orders. Do not custom-build this until we know the system. |
| Analytics | **Plausible** (EU-hosted, cookieless, no consent banner needed) | Gives visits, uniques, sources, per-page engagement, custom goals (CTA clicks, waitlist joins, newsletter signups) and UTM attribution per signup, without a cookie wall on a youth site. |
| Webshop | Payload products + Mollie checkout | Only worth building if there's an actual product list. If it's merch-with-variants at volume, Shopify is the better tool and we embed it — decide when we see the catalogue. |

Everything above is replaceable in isolation. Nothing in it locks the client in the way Wix does.

---

## 4. How the events + waitlist requirement actually gets built

This is the part the brief calls "a big one", so concretely:

1. **Event** is a CMS entry the client creates herself: title, format, edition year, date-or-"volgt",
   location, age range, price, hero image + gallery, programme days, experts, fundamenten covered,
   FAQ, partners, and a `status` field: `waitlist | open | full | past`.
2. Creating an event **auto-creates its page** (`/events/<slug>`) and **its own waitlist** — no
   developer step, no rebuild. Past events drop out of the events list and surface in Journal.
3. `status: waitlist` renders the waitlist form; the row stores `event_id`, `locale`, `source`,
   `utm_*`. Double opt-in via Brevo, so the list stays clean and legal.
4. When she flips `status` to `open`, a Payload hook fires **one targeted campaign to exactly that
   event's waitlist** ("inschrijvingen zijn open"), with a deep link into that event's registration
   flow. She can preview and hold it; it is not a blind send.
5. Registration → Mollie checkout → `registrations` + `orders` rows, confirmation mail, and the
   participant list she can filter and export per event.
6. Everything above is one admin panel: events, waitlists, participants, orders, subscribers.

---

## 4b. Ticketing platform evaluation — recommendation: Ticket Tailor

Researched 8 September 2026. This is the input the backend decision (item 8 in
`STATUS.md`) was waiting on, and it changes the critical path.

| | **Ticket Tailor** | **Eventix / Weeztix** |
|---|---|---|
| Per ticket | £0.22–0.60 (credits, never expire; volume discounts) | ~€0.25 for iDEAL/Bancontact |
| Free tickets | **Free**, up to 5.000/year | booking fee applies |
| Non-profit | **50% discount** for registered charities — worth checking if IMPACT is a vzw | — |
| Bancontact | Yes (via Stripe) | Yes, native |
| **Per-event waitlist** | **Native**, with new/notified tracking | not confirmed |
| Waitlist → email | One click: "Create Broadcast" to that event's waitlist | — |
| API + webhooks | Full API; webhooks for Order, Issued ticket, Event and **WAITLIST_SIGNUP.CREATED** | — |
| Platform risk | Independent, stable | **Acquired by Weezevent, rebranding to Weeztix** |

**Recommendation: Ticket Tailor.** The waitlist is not a workaround on top of a
ticketing tool, it is a first-class object with its own webhook — which is the
single hardest requirement in the brief, and the one we were otherwise going to
build from scratch. Eventix is the more natively Belgian product, but it is
mid-acquisition, and migrating a ticketing platform after launch is the one
migration nobody wants.

### The finding that matters most: this takes Mollie off the critical path

Ticket Tailor settles through **Stripe, PayPal or Square — not Mollie** — and
Bancontact and iDEAL come through Stripe. So for selling event tickets, Mollie
is not required at all.

That was our number one hard blocker, with days of KYC lead time we could not
influence. It becomes: **start Stripe onboarding instead**, which is a faster and
better-trodden path. Mollie stays relevant only if the webshop is later built on
our own stack, and that is an October question, not a September one.

This is the single biggest de-risking available to the 30 September date and it
should be acted on before anything else on the list.

### Honest caveat on "automatic, targeted email"

The brief says the waitlist email should be **automatic**. Ticket Tailor's is
**one click** — you open that event's waitlist and send a broadcast, and it then
tracks who has and has not been notified.

I would ship that for launch, and argue it is better: a fully automatic blast
fires the moment a status flips, which is usually while someone is still editing
the page. If they still want it hands-off afterwards, the `EVENT.UPDATED` webhook
into Brevo makes it genuinely automatic and is perhaps a day's work — in October,
not before launch.

### What this makes the September plan

1. Stripe onboarding started (client) — replaces Mollie on the critical path
2. Ticket Tailor account, the 1–2 September events created, waitlists on
3. Our event pages link into Ticket Tailor's checkout; `WAITLIST_SIGNUP.CREATED`
   webhook mirrors signups into our own store so item 10 stays true
4. Self-serve without a rebuild stays an **October** deliverable, and we say so

## 5. What is already done (this repo)

Front-end foundations that don't depend on any of the decisions above:

- 10 pages, real photography, real brand assets, the nine real partner logos, founders' own copy.
- **Audience router** on the homepage: the six visitor types, each with one obvious next step.
- **Recurring CTAs**: every page ends in a contextual dark CTA band; the newsletter is now a
  full-width band above the footer on every page (and its own section 08 on the homepage), not a
  footer afterthought.
- **Video-ready hero**: drop `assets/video/hero.webm` + `.mp4` in and the homepage upgrades itself
  from poster to muted looping video — the foodmaker.be pattern, gated behind
  `prefers-reduced-motion` and behind a HEAD check so a missing file costs nothing.
- **SEO foundation**: managed per-page titles/descriptions, canonical, `hreflang` (nl-BE + en +
  x-default), Open Graph + Twitter cards, JSON-LD (Organization, WebSite, Event on the event page,
  BreadcrumbList elsewhere), `sitemap.xml`, `robots.txt`. All generated by `tools/seo.py` so it
  stays consistent as pages are added.
- **DRP BuildLab credit**, hyperlinked, in the footer of every page.
- Content is structured as slots, not prose — the client can replace copy per block without
  touching layout.

---

## 6. What we need from the client to hit these dates

Blocking (needed before 10 Sep):
1. **The banner video file.** She says she likes the current site's banner video — the live site
   serves no video today, so we need the actual file (and the aftermovie), ideally 16:9 masters.
2. **Photo library access** — a drive folder, not attachments. Everything on the demo today is
   cropped out of the brochure PDF.
3. **The 1–2 events for September**: title, format, dates, location, age range, price, capacity.
   Without these there is nothing to sell by month end.
4. **Domain + DNS access** for `wemakeimpact.be`, and confirmation of whether the new site takes
   the apex domain on launch day.
5. **Logo and beeldmerk as SVG**, plus partner logos as SVG. We're using rasters off the live site.
6. **Which accounting system** she uses, and who owns that login.
7. **Brand font** — everything is set in Figtree as the agreed stand-in.

Needed by 17 Sep:
8. NL copy per block (she writes it — the structure is ready), and the EN version if EN ships in September.
9. Brevo (or existing newsletter tool) account + who owns it; existing subscriber list to import.
10. Mollie account in the company's name, KYC completed — this takes days, start now.
11. FAQ answers, expert names + portraits, IMPACT FOR ALL figures, the participant story with consent.

Also worth flagging: the middle age band is **15–18** in the website brief and hi-fi but **14–18**
in the ecosystem brief and brochure. One line to change once she confirms.

---

## 7. Things in the brief I'd push back on gently

- **"Full SEO starter package"**: the technical foundation is done, but ranking for a new domain
  needs content and links. Worth setting expectations that September is foundation + indexing,
  not results.
- **Webshop by end September**: only if a product catalogue exists. Selling event tickets is a
  different flow and is the one that matters for the launch.
- **Six audiences on one homepage**: the router handles it, but every audience wanting a homepage
  block is how homepages die. The router sends them one click deep instead — that is deliberate.

---

## 8. Not accessible to me

- The Canva branddeck link (`canva.link/impactsponsordeck2026`) needs an authorised Canva
  connector; it is not readable from here. Export it to PDF and drop it in `brief/` and I'll fold
  it into the design.
- The screenshot referenced as "attached" did not come through — resend it and I'll build the
  pattern she likes into the layout.
