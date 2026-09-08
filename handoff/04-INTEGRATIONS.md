# Integrations — the live contracts

Three third-party services are wired and verified. **They keep running in the
original repo on Netlify.** Do not rebuild them in the CMS; understand them, and
read from them if useful.

Source for the two endpoints: `reference/subscribe.mjs`, `reference/tt-webhook.mjs`.

---

## Brevo — email and the signup store

Every newsletter and waitlist signup lands here, already segmented.

**Endpoint:** `POST /.netlify/functions/subscribe` (form-encoded or JSON)

Accepts: `form-name` (`newsletter` | `waitlist`), `email`, `naam`, `leeftijd`,
`gemeente`, `consent`, `event`, `ageMin`, `ageMax`, `locale`, `page`,
`landing_page`, `referrer`, `utm_*`, `gclid`, `fbclid`, `bot-field` (honeypot).

**Lists:** `3` = Newsletter, `4` = Waitlist.

**Contact attributes** — these carry the segmentation and were created on the
account on 8 September 2026:

```
LOCALE  FORM  EVENT  GEMEENTE  LEEFTIJD  LANDING_PAGE  REFERRER
UTM_SOURCE  UTM_MEDIUM  UTM_CAMPAIGN  UTM_CONTENT  UTM_TERM  GCLID  FBCLID
```

### Three behaviours that cost real debugging time

1. **Tags do not work on this account.** Brevo accepts a `tags` array and
   silently discards it — `POST` returns `201`, `PUT` returns `204`, and the
   contact comes back with `tags: []` either way. All segmentation is carried as
   attributes instead. This was originally designed around tags; it does not work.

2. **An attribute that does not exist is discarded just as quietly**, also with
   a `201`. Create the attribute on the account *before* a form sends the field,
   or it silently vanishes. Brevo → Contacts → Settings → Attributes, type text.

3. **`totalSubscribers` on a list is not reliable.** It read `0` while a contact
   was demonstrably in that list. Verify by fetching the contact and reading its
   `listIds`, never by the list counter.

**Sender:** only `lathif.sihab-dewantoro@drpbuildlab.com` is verified. Brevo
refuses to send from an unverified address. Before launch this should become an
address on `wemakeimpact.be`.

**The "registration opened" email** the brief asks for is now a Brevo segment
filter on the `EVENT` attribute — everyone waiting for a given edition, in a
given locale. For a single launch, sending that campaign by hand is
indistinguishable from automating it.

---

## Ticket Tailor — events, tickets, waitlists, participants

**This owns the commerce half of the product and should keep owning it.**
Payments settle through Stripe, PayPal or Square — *not* Mollie, which is why
the original Mollie plan was abandoned. Bancontact, which matters in Belgium,
comes through Stripe.

- API: `https://api.tickettailor.com/v1/`, HTTP Basic, the API key as username
  with an empty password.
- `/v1/events` currently returns `{"data":[]}` — **no events have been entered
  yet.** This is a client dependency, not a fault.
- Native per-event waitlists, with a `WAITLIST_SIGNUP.CREATED` webhook.

**Webhook:** `POST /.netlify/functions/tt-webhook`, HMAC-signed. It answers
`401 bad signature` to anything unsigned and `503` if the secret is not
configured. It has a replay guard: a valid signature older than a few minutes is
refused.

**Point the webhook at the function, never at a page.** A page returns HTML with
a `200`, so Ticket Tailor records a successful delivery and every signup is
discarded silently — no error, no retry, nothing to notice.

**The box office widget:** the site links to the box office from `/events`, with
the address read from an environment variable at build time and the widget
mounted only after marketing consent. Ticket Tailor's own embed snippet hardcodes
the account slug and a ref — do not paste it; that would put an account id in
twenty files and make handover a code change.

---

## Plausible — privacy-friendly analytics

Loads only after the visitor accepts the analytics category. No cookies, no
consent banner legally required — but it is gated anyway, because a banner that
lists a category and then ignores the answer is worse than no banner.

Custom goals already fired by the site:

```
newsletter_signup    props: source
waitlist_join        props: event
dome_shown / dome_signup / dome_dismissed
section_view         props: section, page      ← the brief's "section engagement"
```

`section_view` exists because stock Plausible counts pageviews, not whether
anyone reached a given part of a page.

---

## Stripe

Test keys verified working (`/v1/balance` answers, `livemode: false`). **No
Stripe code exists in the project and none should be written**: Ticket Tailor
processes payments, and you connect Stripe inside its dashboard. Building a
checkout would duplicate it and create two systems that both think they own an
order.

---

## Environment variables

Names and purpose in `reference/env.example.txt`. **No values are in this
handoff.** Every value lives in the deploying platform's environment settings.

The principle, worth keeping: nothing that identifies an account is hardcoded, so
handover is editing boxes in a UI rather than a code change and a redeploy.

Note which are build-time versus runtime. `PUBLIC_SITE_URL`,
`PUBLIC_PLAUSIBLE_DOMAIN` and `PUBLIC_TICKET_TAILOR_BOX_OFFICE` are read by the
Python build and baked into committed HTML — setting them in a hosting UI does
nothing. The rest are read by the serverless functions at runtime, and only take
effect on a new deploy.
