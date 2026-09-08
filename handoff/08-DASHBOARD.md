# The dashboard — spec

This is the screen the client opens after logging in, and the one that decides
whether the demo lands. It answers three questions in one place: **who is
visiting, who signed up, and what sold.**

Nothing in the project does this today. The data exists across four systems and
nothing joins it.

---

## Build it in four tiers, in this order

Each tier is independently demonstrable. If you run out of time, an earlier tier
still stands on its own — which is the point of the ordering. **Do not build
them in parallel and finish none.**

| Tier | Panel | Source | Risk |
|---|---|---|---|
| 1 | Content overview | Your own Postgres | None |
| 2 | Signups | Brevo API | Low — contract verified, see below |
| 3 | Ticket sales | Ticket Tailor API | Medium — some endpoints unverified |
| 4 | Traffic & conversion | Plausible Stats API | **Check the plan first** |

---

## Tier 1 — Content overview

From Supabase alone. No external calls, no keys, cannot fail in a demo.

- Count per content type: events, journal, partners, experts, tiers, figures
- Events broken down by `status`: waitlist / open / full / past
- Recently edited: last 10 records with type, title and `updated_at`
- **Blocked on consent** — a distinct panel, not a footnote: experts and figures
  with `confirmed = false`, testimonials with `consentOnFile = false`. These are
  real people's names awaiting permission to publish. Making that visible is
  genuinely useful to the client and costs nothing.

## Tier 2 — Signups

The brief's *"all signups in one place, usable for targeted comms"* and
*"which campaign/page/waitlist drove each signup"*. Contracts are verified —
see [04-INTEGRATIONS.md](04-INTEGRATIONS.md).

**Read from Brevo server-side.** The API key is secret and must never reach the
browser: a SvelteKit server route or server load function, never a client fetch.

```
GET https://api.brevo.com/v3/contacts?limit=50&offset=0
GET https://api.brevo.com/v3/contacts/lists/{listId}/contacts   # 3=Newsletter, 4=Waitlist
GET https://api.brevo.com/v3/contacts/{urlEncodedEmail}
Header: api-key: <BREVO_API_KEY>
```

Each contact carries the attribution as attributes: `EVENT`, `FORM`, `LOCALE`,
`GEMEENTE`, `LEEFTIJD`, `UTM_SOURCE`, `UTM_MEDIUM`, `UTM_CAMPAIGN`, `GCLID`,
`FBCLID`, `LANDING_PAGE`, `REFERRER`.

Show: a table filterable by list, event and campaign; counts per event; counts
per `UTM_SOURCE`. That last one is the brief's attribution question, answered.

**Two traps, both verified the hard way:**
- **`totalSubscribers` on a list is unreliable.** It read `0` while a contact was
  demonstrably in that list. Count contacts, do not trust the counter.
- **Tags are always empty** on this account — Brevo discards them silently. Read
  attributes, never tags.

## Tier 3 — Ticket sales

**Verified working** (tested 8 September, HTTP Basic with the API key as
username and an empty password):

```
GET https://api.tickettailor.com/v1/events?limit=5
GET https://api.tickettailor.com/v1/event_series
GET https://api.tickettailor.com/v1/orders
```

All three currently return `{"data":[],"links":{...}}` — **no events have been
entered yet.** That is a client dependency, not a fault, and it means you cannot
test this tier against real data until they arrive. Build it to render an empty
state honestly rather than looking broken.

**Not verified:** endpoints for issued tickets and per-event waitlist entries.
They exist in Ticket Tailor's product but I did not confirm the paths. **Check
their API reference before writing against them — do not guess a path from the
pattern of the three above.**

Show: events with date and status, orders with totals, tickets sold against
capacity, waitlist size per event. Joining waitlist size to the Brevo `EVENT`
attribute is where this becomes more than two lists side by side.

## Tier 4 — Traffic & conversion

**Check this before promising it.** Plausible's Stats API needs an API key and,
on some plans, a paid tier. I did not verify what this account has. If the Stats
API is not available, the fallback is a **shared-link embed** in an iframe —
less integrated, five minutes' work, and still shows real numbers.

Goals already firing on the site, no dashboard configuration needed beyond
naming them:

```
newsletter_signup    props: source
waitlist_join        props: event
dome_shown / dome_signup / dome_dismissed
section_view         props: section, page
```

Show: visitors and unique visitors, top sources, and conversion rate per goal.
`section_view` answers the brief's *"page/section engagement"*, which stock
analytics cannot.

**Analytics is consent-gated**, so these numbers are lower than reality by
however many visitors declined. Say so on the screen — an unexplained gap
between Plausible and Brevo counts looks like a bug and will be raised as one.

---

## Architecture notes

**Every external call is server-side.** Three secret keys are involved. A single
client-side fetch leaks one permanently.

**Cache the external reads.** Brevo, Ticket Tailor and Plausible all rate-limit,
and a dashboard that refetches three APIs on every navigation will trip them
during a demo. Cache in memory for 60 seconds, or mirror into Postgres on a
schedule. In-memory is enough for two days.

**Each panel fails independently.** If Ticket Tailor times out, that panel shows
an error and the rest of the dashboard still renders. A dashboard where one dead
API blanks the page is worse than four separate screens.

**Empty states are a real design case here, not an edge case.** Ticket Tailor has
no events, testimonials are empty by design, and the site has low traffic. Every
panel will be empty or near-empty on day one. "No events entered yet" reads as
correct; a spinner or a zero with no explanation reads as broken.

---

## What to say in the demo

The honest framing, which is also the impressive one:

> One screen for content, signups, sales and traffic — pulled live from the four
> systems that actually hold them, rather than a number typed into a slide.

Do not imply the dashboard *controls* Ticket Tailor or Brevo. It reads them.
Writing back — creating an event in Ticket Tailor from here, for instance — is a
later phase and a much larger one.
