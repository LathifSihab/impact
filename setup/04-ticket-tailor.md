# 4. Ticket Tailor — events, waitlists, the webhook

Ticket Tailor sells the tickets and holds the waitlists. It was chosen over
building it ourselves because its waitlist is a real feature with its own
webhook, which is the hardest single requirement in the brief — the reasoning is
in `PLAN.md` §4b.

About 20 minutes. You already have an account.

---

## Before you start

**Check whether IMPACT is a vzw** (a Belgian non-profit). Ticket Tailor gives
registered charities **50% off** per ticket, permanently. It is worth five
minutes of asking before you finish setting up, because it halves the running
cost for the life of the account.

Free tickets are free anyway, up to 5,000 a year.

---

## Step 1 — Fix the webhook you already made

Your current webhook is wrong in two ways, and both fail quietly.

| | You have | It should be |
|---|---|---|
| Event | `ORDER.CREATED` | `WAITLIST_SIGNUP.CREATED` |
| URL | `https://demo-impact-c399e3.netlify.app/en/` | `https://demo-impact-c399e3.netlify.app/.netlify/functions/tt-webhook` |

**Why the URL matters.** `/en/` is a page. Ticket Tailor would send its message
there, the server would answer with the English homepage and a "200 OK", and
Ticket Tailor would record a successful delivery. Every waitlist signup would be
thrown away, and nothing anywhere would report an error. The `.netlify/functions/`
address is code that actually reads the message.

**Why the event matters.** `ORDER.CREATED` fires when somebody buys a ticket.
Useful later. But the requirement in the brief is the waitlist — people who want
to be told when registration opens — and that is `WAITLIST_SIGNUP.CREATED`.

To fix:

1. **Settings → Box office settings → API → Webhooks**.
2. Delete the existing `ORDER.CREATED` entry, or edit it.
3. **Create new webhook**:
   - Event: `WAITLIST_SIGNUP.CREATED`
   - URL: `https://demo-impact-c399e3.netlify.app/.netlify/functions/tt-webhook`
4. Save.

## Step 2 — The signing secret

When you create the webhook, Ticket Tailor shows a **signing secret** (it may be
called a webhook secret or signing key).

This is how our endpoint knows a message genuinely came from Ticket Tailor and
not from someone who guessed the URL. Without it the endpoint refuses everything,
on purpose — an endpoint that accepts anything is worse than one that accepts
nothing, because it looks like it is working.

1. Copy the secret.
2. Netlify → `TICKET_TAILOR_WEBHOOK_SECRET` = that value.
3. Also add `TICKET_TAILOR_API_KEY` = the new key from step 1 of this folder.
4. **Trigger deploy → Deploy site.**

## Step 3 — Box office address

**Settings → Box office settings → Basic settings.** Your public box office has
an address like `https://www.tickettailor.com/events/drpbuildlab`.

Netlify → `PUBLIC_TICKET_TAILOR_BOX_OFFICE` = the last part (`drpbuildlab`), or
the whole URL — tell me which you used and I will match it.

## Step 4 — The events

**This is the part that is blocked, and not on you.**

To create an event Ticket Tailor needs: title, date, time, location, capacity,
price, and the age range. `ASKS.md` item 2 says none of that has arrived.

When it does:

1. **Events → Create event**.
2. Fill in the details.
3. Turn on the **waitlist** for it — usually under the event's ticket settings,
   as "waiting list" or "notify me".
4. Repeat for the second event.

Then tell me the event names and I will link the site's event pages to them.

## Step 5 — Connect Stripe

Ticket Tailor takes the money through **your** Stripe account, so the money goes
directly to IMPACT and never through us.

1. **Settings → Payment methods** (or *Payment gateways*).
2. Connect Stripe. It walks you through creating or linking an account.
3. Make sure **Bancontact** is enabled — it is how most Belgians pay.

> There is nothing for DRP to build here. Our code never sees a Stripe key; the
> connection lives entirely inside Ticket Tailor. The `STRIPE_*` rows in the
> variable registry only apply if a separate webshop is built later.

- [ ] Charity discount checked
- [ ] Webhook fixed: `WAITLIST_SIGNUP.CREATED` → the functions URL
- [ ] Signing secret in Netlify, site redeployed
- [ ] API key in Netlify
- [ ] Box office address noted
- [ ] Stripe connected, Bancontact on
- [ ] Events created — **waiting on IMPACT**
