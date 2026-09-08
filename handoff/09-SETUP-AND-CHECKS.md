# Standing it up, and proving it works

Two halves: how to get the project running, and how to verify each piece rather
than assume it. The second half matters more than it sounds — on this project a
signup endpoint returned `200` for a full day while storing nothing.

Commands are **PowerShell**, because that is the shell in use. In Git Bash the
`curl ... | grep ...` form works, but do not mix them: PowerShell's `curl` is a
different command that ignores `-s`, and `grep` does not exist there.

---

## Part 1 — Setup

### 1. Supabase

1. Create the project. Note the **project URL**, the **anon key** and the
   **service-role key**.
2. Run the schema — tables from [03-DATA-MODEL.md](03-DATA-MODEL.md).
3. Seed from `reference/content/` — 4 events, 4 journal posts, and the full sets
   of partners, experts, formats, foundations, age groups, tiers, figures. **Use
   the real content, not placeholders**: the client recognises their own copy,
   and lorem ipsum reads as unfinished.
4. Enable **Row Level Security** on every table, then add policies. RLS off on a
   table reachable with the anon key means the whole table is public.
5. Create one admin user in Supabase Auth for the demo.

### 2. Environment variables

Names and purpose in `reference/env.example.txt`. **No values are in this
handoff** — they live in the hosting platform's environment settings.

| Variable | Where it may be read | Notes |
|---|---|---|
| `PUBLIC_SUPABASE_URL` | browser + server | safe to expose |
| `PUBLIC_SUPABASE_ANON_KEY` | browser + server | safe to expose, **only if RLS is on** |
| `SUPABASE_SERVICE_ROLE_KEY` | **server only** | bypasses RLS entirely |
| `BREVO_API_KEY` | **server only** | can send mail as IMPACT |
| `TICKET_TAILOR_API_KEY` | **server only** | can read and change the box office |
| `PLAUSIBLE_API_KEY` | **server only** | if the plan includes the Stats API |

An API key is a password. One leaked into a chat transcript early in this project
and had to be rotated. If a key reaches the browser bundle it is public
permanently — rotate it, do not reason about whether anyone saw it.

### 3. Vercel

Connect the repo, add the variables above, deploy. Confirm the secret ones are
**not** prefixed `PUBLIC_`, and confirm the built client bundle does not contain
them:

```powershell
# after a build, from the project root
Select-String -Path .svelte-kit\output\client\**\*.js -Pattern 'xkeysib|sk_1782|service_role' -List
```

Any hit is a leaked secret. Fix before deploying anywhere the client can reach.

---

## Part 2 — Checks

### Auth

- [ ] Logged out, visiting `/admin` (or wherever the CMS lives) redirects to login
- [ ] A wrong password fails
- [ ] Logged in, a page reload keeps the session
- [ ] **Try to read a table with the anon key while logged out.** It must return
      nothing. If it returns rows, RLS is off or a policy is wrong

### Content editing — the one the client will actually try

- [ ] The four seeded events appear in the list
- [ ] Open one, change the title, save, reload — the change persisted
- [ ] Change `status` from `waitlist` to `open` and back
- [ ] A required field left empty is refused, with the message visible next to
      the field, not in a console
- [ ] A record with `confirmed = false` is visibly marked as not publishable

### Dashboard, per tier

**Tier 1 — content.** Counts match what is in the database. Change a record and
the "recently edited" panel reflects it.

**Tier 2 — signups.** Verify against Brevo directly, not against your own UI:

```powershell
$k = '<BREVO_API_KEY>'   # from your local env, never committed
(Invoke-RestMethod -Headers @{'api-key'=$k} 'https://api.brevo.com/v3/contacts/lists?limit=20').lists |
  Select-Object id,name | Format-Table -Auto
```

Lists `3 = Newsletter` and `4 = Waitlist` must appear. Then submit a signup
through the **live site** and confirm the dashboard shows it with its `EVENT` and
`UTM_SOURCE`:

```powershell
Invoke-RestMethod -Method POST 'https://demo-impact-c399e3.netlify.app/.netlify/functions/subscribe' `
  -Body 'form-name=waitlist&email=YOU@EXAMPLE.COM&naam=Test&leeftijd=12&consent=on&event=selftest&locale=nl&utm_source=cms-check'
```

Then look up the contact and read `listIds` — **not** the list's
`totalSubscribers`, which is unreliable and read `0` while a contact was in the
list. **Delete the test contact afterwards** so it never reaches a real mailing.

**Tier 3 — ticket sales.**

```powershell
$tt = '<TICKET_TAILOR_API_KEY>'
$pair = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${tt}:"))
(Invoke-RestMethod -Headers @{Authorization="Basic $pair"} 'https://api.tickettailor.com/v1/events?limit=5').data.Count
```

`0` is the **correct** answer today — no events have been entered. The check is
that the panel renders "no events yet" rather than a spinner or a broken layout.

**Tier 4 — traffic.** Numbers appear, and the screen says they are
consent-limited. If the Stats API is unavailable on this plan, a shared-link
embed showing real figures is an acceptable pass.

### Resilience — do this before the demo, not after

- [ ] **Break one key deliberately** (change a character in `BREVO_API_KEY`) and
      reload. That panel shows an error; **every other panel still renders.** Put
      the key back
- [ ] Load the dashboard twice in ten seconds — no rate-limit error
- [ ] Open it at 390px wide. The client will pull out a phone
- [ ] Click every nav item. A 404 or an unstyled error page in a demo costs more
      than a missing feature

### Do not regress these

The live site keeps running on Netlify throughout. Before calling anything done:

```powershell
$b='https://demo-impact-c399e3.netlify.app'
$h=(Invoke-WebRequest -UseBasicParsing "$b/").Content
"plausible : " + [bool]($h -match 'plausible-domain')
"canonical : " + [bool]($h -match 'demo-impact-c399e3')
try { Invoke-WebRequest -UseBasicParsing -Method POST "$b/.netlify/functions/tt-webhook" `
        -ContentType 'application/json' -Body '{}' }
catch { "tt-webhook : HTTP " + [int]$_.Exception.Response.StatusCode }
```

Expected: `True`, `True`, and `tt-webhook : HTTP 401` — which is correct, it means
the endpoint is refusing unsigned messages. PowerShell 5.1 throws on any non-2xx
response, so without the `try/catch` a correct `401` looks like a crash.
