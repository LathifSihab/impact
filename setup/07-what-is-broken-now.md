# 7. What is broken right now — do these in order

Re-checked live on 8 September 2026 against
`https://demo-impact-c399e3.netlify.app`, after your push and redeploy.

**Three of the four items are now fixed.** One is left, plus one smaller thing.

Commands here are **PowerShell**, because that is the shell you are in. If you
ever run them in Git Bash instead, `curl -s ... | grep x` is the equivalent —
but do not mix the two: in PowerShell `curl` is a different command that does
not understand `-s`, and `grep` does not exist at all.

---

## ✅ Fixed — no action needed

| What | Proof |
|---|---|
| Canonical + og:url point at staging | `<link rel="canonical" href="https://demo-impact-c399e3.netlify.app/">` |
| Plausible is switched on | `<meta name="plausible-domain">` present in the page |
| Ticket Tailor webhook | now answers `401 bad signature` instead of `503` |
| Ticket Tailor API key | valid; `/v1/events` answers (empty — no events entered yet) |
| Stripe test keys | valid; `/v1/balance` answers with `livemode: false` |
| Brevo list ids | confirmed **3 = Newsletter**, **4 = Waitlist**, matching `.env` |

`401 bad signature` on the webhook is the **correct** answer. It means the
secret is loaded and the endpoint refuses unsigned messages, which is exactly
what it should do to anything that is not Ticket Tailor.

---

## ⛔ Step 1 — Signups still never reach Brevo (15 min)

This is the one real problem left.

The endpoint answers `200 {"ok":true}` and **no contact is created**. Both lists
still show 0 subscribers after several test signups. The only contact on the
account is your own address, which was already there.

**The 200 is not a lie, and not a bug.** The endpoint is built so a Brevo
outage never loses a signup: the visitor always gets a friendly answer, the
failure is written to the log, and Netlify Forms keeps the audit copy. So a
200 here tells you the form worked — it does not tell you Brevo accepted it.

### Why it is one of exactly two things

The webhook now reads its secret correctly, which proves environment variables
*are* reaching the functions after your redeploy. So either:

**a) `BREVO_API_KEY` is missing from Netlify.** Easy to miss — the webhook
variable was set, this one may not have been.

**b) Brevo is still refusing Netlify by IP.** Brevo → **Security → Authorised
IPs**. If you added *your own* address to the list, that fixed your laptop and
not the site. Netlify's servers send from addresses that change constantly and
cannot be listed, so the restriction has to be **off**, not extended.

### How to tell which, in one look

Netlify → **Logs → Functions → subscribe**, then submit a signup. The function
prints its own reason:

| Log line contains | Cause | Fix |
|---|---|---|
| `BREVO_API_KEY not set` | (a) | Add the variable, redeploy |
| `unrecognised IP address` | (b) | Turn the allowlist off |
| `brevo failed` | something else | Send me the line |

### Prove it is fixed

```powershell
$b='https://demo-impact-c399e3.netlify.app/.netlify/functions/subscribe'
Invoke-RestMethod -Method POST $b -Body 'form-name=newsletter&email=YOUR@EMAIL&locale=nl'
```

Then Brevo → **Contacts → Newsletter**. The address must appear, tagged
`locale:nl` and `form:newsletter`. If the list is still empty it failed, and
the log tells you why.

---

## ⛔ Step 2 — The sender address is not verified (5 min)

`.env` has `BREVO_SENDER_EMAIL=lathif.sihab95@gmail.com`, but the only verified
sender on the Brevo account is `lathif.sihab-dewantoro@drpbuildlab.com`.

Brevo refuses to send from an unverified address, so mail using that value
fails even once step 1 works. Either verify the gmail (Brevo → **Senders & IP →
Senders → Add a sender**) or change the variable to the address already
verified.

Before launch this has to become an address on `wemakeimpact.be`. Mail sent on
behalf of a brand from a gmail address lands in spam far more often, and that
domain is open item 4 in `STATUS.md`.

---

## Useful checks, in PowerShell

Whole site and both endpoints at once:

```powershell
$b='https://demo-impact-c399e3.netlify.app'
$h=(Invoke-WebRequest -UseBasicParsing $b/).Content
"plausible : " + [bool]($h -match 'plausible-domain')
"canonical : " + [bool]($h -match 'demo-impact-c399e3')
foreach($p in 'tt-webhook','subscribe'){
  try{ $r=Invoke-WebRequest -UseBasicParsing -Method POST "$b/.netlify/functions/$p" `
         -ContentType 'application/json' -Body '{}'
       "$p : HTTP $($r.StatusCode) $($r.Content)" }
  catch{ $e=$_.Exception.Response
         $sr=New-Object IO.StreamReader($e.GetResponseStream())
         "$p : HTTP $([int]$e.StatusCode) $($sr.ReadToEnd())" }
}
```

Expected today: `plausible : True`, `canonical : True`,
`tt-webhook : HTTP 401 bad signature`, `subscribe : HTTP 422` with the Dutch
email error. Anything else is a regression.

The `try/catch` is not decoration: in PowerShell 5.1 `Invoke-WebRequest` throws
on any non-2xx answer, so without it a 401 or 422 looks like a crash rather
than the correct result.

Brevo lists and their subscriber counts:

```powershell
$k=((Get-Content .env | Select-String '^BREVO_API_KEY=').Line -replace '^BREVO_API_KEY=','').Trim()
(Invoke-RestMethod -Headers @{'api-key'=$k} 'https://api.brevo.com/v3/contacts/lists?limit=20').lists |
  Select-Object id,name,totalSubscribers | Format-Table -Auto
```

---

## Then clean up

The test signups carry the tags `source:drp-selftest` and `event:selftest`.
Once step 1 works, delete those contacts in Brevo so they never reach a real
mailing.

---

## Still blocked on the client, not on you

Ticket Tailor has **no events**. The API answers correctly and returns an empty
list, so nothing about ticketing can be finished until the September event
details arrive — item 2 in `ASKS.md`. The box office is also not linked from
any page on the site yet; that is a separate piece of work, not a broken one.
