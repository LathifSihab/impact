# 3. Brevo — where signups land

Brevo is the email tool. Newsletter subscribers and event waitlist entries end up
there, so IMPACT can mail them later.

About 20 minutes. Free up to 300 sends a day, which is far more than needed now.

---

## Before you start: whose account?

Create it under **DRP for now**, and create **IMPACT's own account before the
first real subscriber**.

The reason is legal rather than technical. Under GDPR IMPACT is the *controller*
of their subscribers' data and DRP is a *processor* working on their behalf. Real
people's consent records sitting in an agency's account is a position that is
awkward to explain and awkward to migrate. Prototyping there is fine. Collecting
real subscribers there is not.

Note it as a to-do; it is in `PRIVACY-INVENTORY.md` §6 as a question for her
lawyer.

---

## Step 1 — Account

1. Sign up at [brevo.com](https://www.brevo.com), free plan.
2. Verify the email address they send you.
3. Brevo will ask what you use it for — "newsletter" is fine, it only changes
   which onboarding tips you see.

## Step 2 — Two lists

A **list** is a group of contacts. We use exactly two, and they must stay
separate: someone who wants event news has not agreed to a monthly newsletter,
and treating those as the same thing is the kind of shortcut that produces spam
complaints.

1. **Contacts → Lists → Create a list**.
2. Name it `Newsletter`. Create.
3. Create a second, `Waitlist`.

## Step 3 — Find the list IDs

The site refers to lists by **number**, not name, because a renamed list would
otherwise break the connection silently.

1. **Contacts → Lists**.
2. Click `Newsletter`.
3. Look at the address bar. It ends in a number, e.g.
   `…/contact/list/4` → the ID is **4**.
4. Do the same for `Waitlist`.

If the number is not in the URL, the list overview usually shows an ID column, or
hovering the list name reveals it. Write both down.

## Step 4 — API key

1. Top-right account menu → **SMTP & API** → **API keys**.
2. **Generate a new API key**, name it `impact-website`.
3. Copy it. It is shown once.

## Step 5 — Sender address

Brevo will not send from an address it cannot verify.

1. **Senders, Domains & Dedicated IPs → Senders → Add a sender**.
2. Use `hello@wemakeimpact.be` if you can receive mail there. Otherwise use an
   address you control for now and change it later.
3. Confirm the verification email.

> Later, and worth flagging to IMPACT: verifying the whole **domain**
> (SPF/DKIM records in DNS) rather than a single address is what stops IMPACT's
> mail landing in spam. It needs DNS access, which is `ASKS.md` item 3.

## Step 6 — Into Netlify

Back to [step 2](02-netlify-environment-variables.md) and add:

| Key | Value |
|---|---|
| `BREVO_API_KEY` | the key from step 4 |
| `BREVO_LIST_NEWSLETTER` | the number, e.g. `4` |
| `BREVO_LIST_WAITLIST` | the number, e.g. `5` |
| `BREVO_SENDER_EMAIL` | the verified address |

Then **Trigger deploy → Deploy site**.

---

## Optional: double opt-in

Double opt-in means a subscriber gets an email and must click a link before they
are really on the list. It is slightly fewer subscribers and considerably better
ones, and it produces a consent record with a timestamp — which is exactly what
you want to be able to show if anyone ever asks.

**We recommend it for the newsletter.** It is deliberately *not* used for the
event waitlist: that consent is already explicit, given by an adult, on a form
that will not submit without ticking a box.

To switch it on:

1. **Campaigns → Templates → New template**, a short "confirm your subscription"
   email containing Brevo's confirmation link.
2. Save it and note its **template ID** (a number).
3. Add to Netlify: `BREVO_DOI_TEMPLATE_ID` = that number.
4. Redeploy.

The site changes its own success message accordingly — no code change needed.

- [ ] Account created
- [ ] Two lists created, both IDs written down
- [ ] API key generated
- [ ] Sender address verified
- [ ] Four variables in Netlify, site redeployed
- [ ] Decided about double opt-in

## Contact attributes — create them before a form sends them

Brevo silently discards anything it does not recognise. Send it a `tags` array
and it answers `201` and stores nothing; send an attribute that is not defined
on the account and it does exactly the same. Nothing errors, and the data is
simply gone.

Tags were the original plan and do not work on this account, verified against
the live API. So the segmentation is carried as attributes, which do persist.

These exist already, created 8 September 2026:

`LOCALE` · `FORM` · `EVENT` · `GEMEENTE` · `LEEFTIJD` · `LANDING_PAGE` ·
`REFERRER` · `UTM_SOURCE` · `UTM_MEDIUM` · `UTM_CAMPAIGN` · `UTM_CONTENT` ·
`UTM_TERM` · `GCLID` · `FBCLID`

**If a new field is ever added to a form, create the attribute first** — Brevo →
**Contacts → Settings → Attributes**, type *text*. Otherwise the form will look
like it works and that field will never arrive.
