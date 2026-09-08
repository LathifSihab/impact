# 7. What is broken right now — do these in order

Checked live on 8 September 2026 against
`https://demo-impact-c399e3.netlify.app`. Each step says how to prove it worked,
so you never have to guess.

Four things are wrong. Steps 1 and 2 are almost certainly **one** cause.

---

## Step 1 — Push the commit (2 min)

The site changes are committed on this machine but never sent to GitHub, so
Netlify has been rebuilding the *old* code every time.

```bash
git push
```

**Proof it worked** — wait for the deploy to finish, then:

```bash
curl -s https://demo-impact-c399e3.netlify.app/ | grep canonical
```

You want `demo-impact-c399e3.netlify.app`. If you still see
`www.wemakeimpact.be`, the deploy has not finished — wait and repeat.

---

## Step 2 — Redeploy so the functions can see the variables (5 min)

Environment variables set in Netlify's UI do **not** reach already-deployed
functions. They are read at deploy time. Nothing you set has taken effect yet.

This is why `tt-webhook` answers `503 not configured` even though you set
`TICKET_TAILOR_WEBHOOK_SECRET`, and almost certainly why signups are not
reaching Brevo either. One cause, two symptoms.

1. Netlify → **Site configuration → Environment variables**.
2. Check every variable is there, spelled exactly as in `.env.example`.
3. For each one, open it and check **Scopes / deploy contexts**. A variable
   scoped to *Production* only does nothing on a branch or preview URL. When in
   doubt choose **All deploy contexts**.
4. Netlify → **Deploys → Trigger deploy → Deploy site**. Wait for green.

**Proof it worked:**

```bash
curl -s -X POST https://demo-impact-c399e3.netlify.app/.netlify/functions/tt-webhook \
  -H 'content-type: application/json' -d '{}'
```

| You get | Meaning |
|---|---|
| `401 bad signature` | **Correct.** The secret is loaded and unsigned messages are refused |
| `503 not configured` | The variable still is not reaching the function — recheck 2 and 3 |
| `404` | The functions did not deploy at all |

---

## Step 3 — Find out why Brevo signups vanish (10 min)

The endpoint answers `200 {"ok":true}` but **no contact is created**. That 200
is by design: a Brevo outage must not lose a signup, so the visitor always gets
a friendly answer and the failure is logged instead. A 200 here does not mean
it worked.

Confirmed with the API key from `.env`, from this machine:

- The key is valid — `/v3/account` answers.
- Lists are correct — **3 = Newsletter**, **4 = Waitlist**, matching `.env`.
- Both lists hold **0 contacts**, after several test signups.

So the key works from here but not from Netlify. Two candidates:

**a) The IP allowlist is still on.** Brevo → **Security → Authorised IPs**. If
you added *your own* IP, that fixed your machine and not the site. Netlify's
servers send from addresses that change constantly and cannot be listed. The
restriction has to be **off**.

**b) `BREVO_API_KEY` is not reaching the function** — same cause as step 2.
Do step 2 first, then retest.

**Proof it worked:**

```bash
curl -s -X POST https://demo-impact-c399e3.netlify.app/.netlify/functions/subscribe \
  -d 'form-name=newsletter&email=YOUR@EMAIL&locale=nl'
```

Then Brevo → **Contacts → Newsletter**. The address must appear, tagged
`locale:nl` and `form:newsletter`. If the list is still empty, it failed —
Netlify → **Logs → Functions → subscribe** shows the real reason.

---

## Step 4 — Fix the sender address (5 min)

`.env` has `BREVO_SENDER_EMAIL=lathif.sihab95@gmail.com`, but the only verified
sender on the Brevo account is `lathif.sihab-dewantoro@drpbuildlab.com`.

Brevo refuses to send from an unverified address, so any mail using that value
fails. Either verify the gmail (Brevo → **Senders & IP → Senders → Add**) or
change the variable to the address that is already verified.

Long term this must become an address on `wemakeimpact.be` — mail sent from a
gmail address on behalf of a brand lands in spam far more often.

---

## Then clean up

The test signups used `source:drp-selftest` and `event:selftest` tags. Once
anything succeeds, delete those contacts in Brevo so they never reach a real
mailing.

---

## Still blocked on the client, not on you

Ticket Tailor has **no events yet** — the API answers correctly and returns an
empty list. Nothing about ticketing can be finished until the September event
details arrive. That is item 2 in `ASKS.md`.
