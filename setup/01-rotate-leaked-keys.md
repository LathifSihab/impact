# 1. Rotate the two leaked keys

**Do this first, before anything else.** Five minutes.

## What happened

Two live keys were pasted into a chat message:

- a Brevo API key, beginning `xkeysib-39f2…`
- a Ticket Tailor API key, beginning `sk_17818_339850_…`

A chat transcript is stored somewhere you do not control. That is enough to treat
both keys as public, regardless of who has actually seen them.

## Why it matters more than it feels like it does

Nothing has gone wrong, and probably nothing will. But those two keys can:

- **Brevo** — send email as IMPACT, to IMPACT's contact list. A spammer with this
  key does not just send mail; they burn the sending reputation of
  `wemakeimpact.be`, and rebuilding that takes months.
- **Ticket Tailor** — read the box office, orders and customer details, and
  change them.

Rotating means the old key stops working. Anyone holding it now holds nothing.

## Brevo

1. Log in to [brevo.com](https://www.brevo.com).
2. Top-right, your account name → **SMTP & API** (sometimes shown as *API keys*).
3. Find the key starting `xkeysib-39f2…` → **Delete**. Confirm.
4. **Generate a new API key**. Name it something you will recognise later —
   `impact-website` is fine.
5. It is shown **once**. Copy it somewhere safe for the next ten minutes.
   Step 2 is where it goes.

## Ticket Tailor

1. Log in to [tickettailor.com](https://www.tickettailor.com).
2. **Settings → Box office settings → API** (the page in your screenshot).
3. **API keys** tab → find `sk_17818_339850_…` → revoke or delete it.
4. Create a new key. Copy it.

## Then

Do not paste either new key into a chat, an email, a ticket, or a code file.
They go into Netlify, and only Netlify. That is step 2.

- [ ] Brevo key deleted and replaced
- [ ] Ticket Tailor key revoked and replaced
- [ ] Both new keys copied somewhere temporary

> If you ever paste a key somewhere by accident again, the fix is always the
> same and always cheap: rotate it. That is why the plan says every key must be
> rotatable. It costs two minutes; deciding whether a leak "probably mattered"
> costs far more.
