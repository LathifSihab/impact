# 7. Integration status — verified live

Last checked **8 September 2026** against
`https://demo-impact-c399e3.netlify.app`, end to end, with real requests.

**Everything in this folder now works.** This file records what was proven, how
it was proven, and the one thing that is still waiting on the client.

Commands are **PowerShell**. If you use Git Bash instead the `curl … | grep …`
form works, but do not mix them: in PowerShell `curl` is a different command
that ignores `-s`, and `grep` does not exist.

---

## Verified working

| What | How it was proven |
|---|---|
| Newsletter signup → Brevo | posted through the live endpoint; contact appeared in list **3** |
| Waitlist signup → Brevo | same contact then appeared in **3,4** — both branches pick the right list |
| Server-side validation | a waitlist post missing name and consent returned `422` with the Dutch errors |
| Ticket Tailor webhook | answers `401 bad signature` to unsigned messages |
| Ticket Tailor API | key valid; `/v1/events` answers (empty — no events entered yet) |
| Stripe test keys | valid; `/v1/balance` answers with `livemode: false` |
| Canonical + og:url | point at the staging domain, not production |
| Plausible | `<meta name="plausible-domain">` present; script loads after consent |
| Local test suite | `node tools/test-functions.mjs` — 14 passed, 0 failed |

`401 bad signature` is the **correct** answer from the webhook. It proves the
secret is loaded and that anything which is not Ticket Tailor is refused.

---

## What went wrong, and what it teaches

Two failures cost most of the debugging. Both are worth remembering, because
neither announced itself.

**Netlify held a deleted API key.** The Brevo key was rotated correctly in Brevo
and in `.env`, but Netlify still had the old one. The site kept answering
`200 {"ok":true}` while Brevo rejected every call with `401`.

**A 200 from `/subscribe` does not mean Brevo accepted it.** That is deliberate:
a Brevo outage must never lose a signup, so the visitor always gets a friendly
answer, the real result goes to the log, and Netlify Forms keeps the audit copy.

So there is only one way to know a signup landed:

```powershell
$k=((Get-Content .env | Select-String '^BREVO_API_KEY=').Line -replace '^BREVO_API_KEY=','').Trim()
Invoke-RestMethod -Headers @{'api-key'=$k} 'https://api.brevo.com/v3/contacts/YOUR%40EMAIL'
```

`listIds` on the contact is the proof. **Do not trust `totalSubscribers` on the
list** — Brevo updates that counter lazily and it still read `0` while a contact
was demonstrably in the list.

And when something does fail, the answer is in **Netlify → Logs → Functions →
subscribe**, which prints the upstream status:

| Log line | Meaning | Fix |
|---|---|---|
| `"status":401` | Brevo rejected the key | Netlify holds a wrong or deleted key — update it, then redeploy |
| `"reason":"BREVO_API_KEY not set"` | the variable never reached the function | Add it in Netlify, then redeploy |
| `"stored":true` | it worked | — |

**Environment variables reach functions only at deploy time.** After editing any
variable: **Deploys → Trigger deploy → Deploy site**, and wait for green.

---

## Tags do not work on this account — attributes carry the segmentation

Brevo accepts a `tags` array and silently throws it away. Verified directly:
`POST /v3/contacts` returns `201`, `PUT /v3/contacts/{email}` returns `204`, and
the contact comes back with `tags: []` either way.

The site therefore writes the same information as **contact attributes**, which
do persist. These were created on the account on 8 September 2026:

`LOCALE` · `FORM` · `EVENT` · `GEMEENTE` · `LEEFTIJD` · `LANDING_PAGE` ·
`REFERRER` · `UTM_SOURCE` · `UTM_MEDIUM` · `UTM_CAMPAIGN` · `UTM_CONTENT` ·
`UTM_TERM` · `GCLID` · `FBCLID`

**An attribute that does not exist on the account is dropped exactly as quietly
as a tag** — Brevo still answers `201`. If a new field is ever added to a form,
create the attribute first: Brevo → **Contacts → Settings → Attributes**, type
*text*.

This is also what open item 10 in `STATUS.md` needs — "which campaign, page or
waitlist drove this signup" has to live on the signup record to be joinable
later. It now does.

---

## Still to do

**Delete the test contact.** `agro.dude95@gmail.com` is on both lists from
testing. Remove it in Brevo before any real mailing goes out.

**Fix the sender address.** `.env` has
`BREVO_SENDER_EMAIL=lathif.sihab95@gmail.com`, but the only verified sender on
the account is `lathif.sihab-dewantoro@drpbuildlab.com`. Brevo refuses to send
from an unverified address. Either verify the gmail (Brevo → **Senders, domains,
IPs**) or point the variable at the verified one. Before launch it has to become
an address on `wemakeimpact.be` — brand mail sent from a gmail address lands in
spam far more often.

---

## The full sweep, in one command

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

Expected: `True`, `True`, `tt-webhook : HTTP 401 bad signature`,
`subscribe : HTTP 422` with the Dutch email error. Anything else is a
regression.

The `try/catch` is not decoration: PowerShell 5.1 throws on any non-2xx answer,
so without it the correct `401` and `422` look like crashes.

---

## Still blocked on the client, not on you

Ticket Tailor has **no events**. The API answers correctly and returns an empty
list, so nothing about ticketing can be finished until the September event
details arrive — item 2 in `ASKS.md`. Separately, the box office is not linked
from any page yet; that is unbuilt work, not a fault.
