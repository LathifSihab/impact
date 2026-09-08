# CMS scope — what to build

The chosen stack, as of 9 September 2026: **SvelteKit + TypeScript, Supabase for
Postgres and auth, deployed on Vercel.** The static site stays on Netlify.

That decoupling is deliberate and worth preserving: building the CMS cannot break
a site that is already live and verified.

---

## Build this

**A backoffice for site content.** Login, list and edit views for the ten content
types in [03-DATA-MODEL.md](03-DATA-MODEL.md), with events first — they are what
the client will click on.

Priority order, by what the client actually edits:

1. **Events** — the demo centrepiece. Full CRUD, `status` prominent
2. **Journal** — Markdown posts, the genuinely recurring content
3. **Partners / experts** — small records with a `confirmed` gate
4. **Figures, tiers, formats, foundations, ageGroups** — rarely change; list and
   edit is plenty
5. **Testimonials** — trivial, but the `consentOnFile` gate is the interesting part

## Do not build this

| Not this | Why |
|---|---|
| Payments, checkout, orders | Ticket Tailor and Stripe own it. Duplicating it creates two systems that both think they own an order, and puts you in PCI scope |
| Registrations, tickets, attendance | Ticket Tailor's backoffice already does this, and the client gets it for free |
| A newsletter sender | Brevo owns sending, segments and automations. The CMS has no business holding an email list |
| Your own auth | Supabase Auth. Do not hand-roll sessions on a system holding minors' names and ages |
| Rendering the public site, at first | It is 20 pages with a Python i18n and SEO pipeline behind them. That is a separate project — see below |

## The scoping rule that makes this survivable

**In the first pass, the CMS manages data. It does not serve the website.**

The static site stays static. What the client needs to see is a login, their real
content in editable forms, and changes that persist. That is a convincing
backoffice. Wiring it to publish the site is the next phase and is a much bigger
job than it looks, because the existing pipeline also does the English
generation, the SEO head blocks, the sitemap and an HTML validity check.

**Be honest about this in the demo.** "A working backoffice with real data in a
real database, not yet the thing that publishes the site" is an impressive
sentence. Letting the client assume otherwise becomes a problem in week three.

---

## Seeding

`reference/content/` holds the real content as JSON and Markdown — 4 events, 4
journal posts, and the full set of partners, experts, formats, foundations, age
groups, tiers and figures. Write a seed script against it. **Do not invent
placeholder content**: the client recognises their own copy, and lorem ipsum in a
demo reads as unfinished.

`testimonials.json` is `[]` on purpose — no parent consent is held. Leave it
empty rather than inventing quotes.

---

## Where the CMS could genuinely beat the alternatives

Two things no off-the-shelf tool gives, both small:

**A joined view.** Signups from Brevo, orders from Ticket Tailor, campaign
attribution from your own data, in one screen. The brief asks for "all signups in
one place" and "which campaign drove each signup" — the data exists across three
systems and nothing joins it today. Read-only, one page, high perceived value.

**A publish gate on consent.** `confirmed` on experts and figures,
`consentOnFile` on testimonials. These are real people's names and real claims. A
CMS that makes the tick explicit and visible is better than a generic one that
treats it as just another boolean.

---

## Known constraints

- The client had not supplied: event details, privacy text, parental consent for
  four on-camera minors, domain access. None block the CMS.
- Content is **Dutch-first**, English generated. The current model has one record
  per locale rather than paired translations — improve this if you touch it.
- Images referenced by path (`assets/img/...`) are not in this handoff. If the
  CMS handles uploads, Supabase Storage is the obvious home, but the existing
  paths must keep resolving for the static site.
