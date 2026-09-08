# Setup — do these in order

You are wiring four services to the site. Nothing here needs code. Everything
here needs an account, a key, and the key pasted into the right box in Netlify.

Work through them in this order. Each one takes 10–20 minutes and they stack:
step 2 is where every key from steps 3–5 ends up, so do it before them.

| # | File | What it does | Time |
|---|---|---|---|
| 1 | [01-rotate-leaked-keys.md](01-rotate-leaked-keys.md) | Replace the two keys that were pasted into chat | 5 min |
| 2 | [02-netlify-environment-variables.md](02-netlify-environment-variables.md) | Learn where keys go, and why never in code | 10 min |
| 3 | [03-brevo.md](03-brevo.md) | Email — where newsletter and waitlist signups land | 20 min |
| 4 | [04-ticket-tailor.md](04-ticket-tailor.md) | Ticketing — events, waitlists, the webhook | 20 min |
| 5 | [05-plausible.md](05-plausible.md) | Analytics — visitors, sources, conversions | 10 min |
| 6 | [06-verify.md](06-verify.md) | Prove each one actually works | 15 min |
| 7 | [07-what-is-broken-now.md](07-what-is-broken-now.md) | **Start here today** — the four things currently failing, in order | 25 min |

---

## The one idea behind all of it

**A key is a password.** `BREVO_API_KEY` is a password that lets anything holding
it send email as IMPACT. `TICKET_TAILOR_API_KEY` can read and change the box
office.

So keys are never written in code and never sent in a message. They live in one
place — Netlify's environment variables — where the site reads them at run time.

That has a practical payoff at handover: when IMPACT takes over their own
accounts, somebody edits five boxes in a web page. No code changes, no redeploy,
no developer. That is the whole reason for doing it this way rather than the
quicker way.

---

## Words you will see

**API key** — a password for a program rather than a person.

**Environment variable** — a named box, e.g. `BREVO_API_KEY`, that holds a value
the site reads while running. Set in Netlify, never in the repository.

**Webhook** — the reverse of the site asking a question. Ticket Tailor sends
*us* a message when something happens ("someone joined a waitlist"). It needs a
URL to send it to, and that URL must be an endpoint, not a page.

**Endpoint** — a URL that runs code and answers. Ours look like
`https://…/.netlify/functions/subscribe`. A **page** is a URL that returns HTML.
Sending a webhook to a page fails silently, which is the worst way to fail.

**Deploy context** — Netlify runs the same site in more than one place:
production and previews. A variable can hold a different value in each, so
staging can talk to a test account while production talks to the real one.

---

## What is already built

Nothing in the site is waiting on code. All of it is waiting on keys.

- Both endpoints exist and are tested: 14 checks pass with no key set at all.
- Analytics is written and loads only after the visitor accepts the cookie banner.
- Every form works today; submissions land in Netlify Forms as a backup, and will
  keep doing so after Brevo is connected.

**If you stop half way, nothing breaks.** Each service switches on when its
variable appears and stays inert until then. That is deliberate.

---

## What is still blocked on IMPACT, not on you

Ticket Tailor cannot be finished without **the September events** — titles,
dates, location, age range, price, capacity. That is item 2 in `ASKS.md` and it
is the thing actually holding up the end-of-September date. Everything in this
folder can be done first, so that the day the events arrive it is only data
entry.
