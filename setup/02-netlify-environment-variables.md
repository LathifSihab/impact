# 2. Netlify environment variables

This is where every key from steps 3, 4 and 5 goes. Read it once, then keep the
tab open — you will come back to it after each service.

## Where

1. [app.netlify.com](https://app.netlify.com) → the site
   (`demo-impact-c399e3`).
2. **Site configuration** in the left sidebar.
3. **Environment variables**.
4. **Add a variable** → *Add a single variable*.

For each one you give a **Key** (the name, exactly as written below — they are
case-sensitive) and a **Value** (what you copied).

## Scopes, and the one setting that matters

Netlify asks which **deploy contexts** the value applies to. Unless a file here
says otherwise, choose **All deploy contexts** (or *Same value for all*).

There is one exception, `PUBLIC_SITE_URL`, explained at the bottom.

## The full list

You will not have all of these yet. Add each as you get it; nothing breaks while
one is missing.

| Key | From | Step |
|---|---|---|
| `BREVO_API_KEY` | Brevo | 3 |
| `BREVO_LIST_NEWSLETTER` | Brevo, a number like `4` | 3 |
| `BREVO_LIST_WAITLIST` | Brevo, a number like `5` | 3 |
| `BREVO_SENDER_EMAIL` | the address mail is sent from | 3 |
| `BREVO_DOI_TEMPLATE_ID` | optional, turns on double opt-in | 3 |
| `TICKET_TAILOR_API_KEY` | Ticket Tailor | 4 |
| `TICKET_TAILOR_WEBHOOK_SECRET` | Ticket Tailor, when creating the webhook | 4 |
| `PUBLIC_TICKET_TAILOR_BOX_OFFICE` | your box office address | 4 |
| `PUBLIC_PLAUSIBLE_DOMAIN` | Plausible | 5 |

**`PUBLIC_` is not decoration.** A name starting `PUBLIC_` is safe for the
browser to see — a domain name, a box office address. Everything else is secret
and stays on the server. Never rename a secret to start with `PUBLIC_`.

## After adding or changing any variable

Netlify only reads them when the site builds. So:

**Deploys → Trigger deploy → Deploy site.**

Skip this and you will swear the variable is not working. It is; the running copy
of the site simply predates it.

## About `PUBLIC_SITE_URL`

Leave this one alone for now. It controls which domain the site claims to be, and
it is currently correct.

It matters at launch: a canonical tag pointing at a domain the site is not served
from keeps the real domain out of Google. When IMPACT's domain goes live it is
set to `https://www.wemakeimpact.be`, and DRP rebuilds the site once.

- [ ] I know where the environment variables page is
- [ ] I know a variable does nothing until the site is redeployed
