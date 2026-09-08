# 6. Verify it actually works

Setting a variable and seeing no error is not evidence. Each check below proves
one thing genuinely reaches its destination.

Do these **after** a redeploy. Every one of them will fail against a build that
predates the variable.

---

## A. The endpoints are alive

Paste into a terminal:

```bash
curl -i -X POST https://demo-impact-c399e3.netlify.app/.netlify/functions/subscribe \
  -d "form-name=newsletter&email=test+check@example.be&locale=nl"
```

| You see | It means |
|---|---|
| `200` and `{"ok":true,…}` | Working |
| `404` | Functions are not deployed. Redeploy; check `netlify/functions/` exists |
| `422` | Working — it rejected the address. Check the email you typed |

## B. Brevo is receiving

Do A above with a real address you can check, then:

1. Brevo → **Contacts** → the `Newsletter` list.
2. The address should be there within seconds.
3. Open the contact. It should carry **tags**: `locale:nl`, `form:newsletter`.

**If it is not there**, the request still returned `200` — by design, because a
signup must never be lost just because Brevo is having a bad day. Look in
Netlify → **Functions → subscribe → logs**. A line reading
`"reason":"BREVO_API_KEY not set"` means the variable is missing or the site was
not redeployed after adding it.

## C. Attribution is attached

This is the "which campaign brought this signup" requirement, and it is worth
proving once because it is invisible when it silently does not work.

1. Open, in a fresh private window:
   `https://demo-impact-c399e3.netlify.app/?utm_source=instagram&utm_campaign=test-run`
2. Accept the cookie banner.
3. Click through to **another** page — do not sign up on the landing page.
4. Subscribe to the newsletter there.
5. In Brevo, open that contact.

You should see `UTM_SOURCE = instagram` and `UTM_CAMPAIGN = test-run`, **even
though you signed up on a different page**. That is the point: someone arrives on
a campaign link, browses, and converts later — and the campaign still gets the
credit.

## D. The Ticket Tailor webhook

```bash
curl -i -X POST https://demo-impact-c399e3.netlify.app/.netlify/functions/tt-webhook \
  -H "content-type: application/json" -d '{}'
```

| You see | It means |
|---|---|
| `401 bad signature` | **Correct.** The endpoint is live and refusing unsigned messages |
| `503 not configured` | `TICKET_TAILOR_WEBHOOK_SECRET` is missing, or no redeploy |
| `404` | Functions are not deployed |
| `200` | Wrong — tell DRP immediately. It should never accept an unsigned message |

For a real end-to-end test you need an event with a waitlist. Join your own
waitlist with a real address, then check Ticket Tailor → the event → waitlist
signups, and Brevo → `Waitlist` list. Ticket Tailor also shows recent webhook
deliveries and their responses under **Settings → API → Webhooks**, which is the
fastest place to see whether ours answered `200`.

## E. Plausible is counting

1. Open the site in a private window.
2. **Accept** the cookie banner — nothing is recorded if you decline, which is
   the intended behaviour and the most common reason for "it is not working".
3. Click through two or three pages.
4. Plausible → **Realtime**. You should be there within about 30 seconds.
5. Subscribe to the newsletter, then check **Goals** for `newsletter_signup`.

If Realtime stays empty: view source on the page and search for
`plausible-domain`. Missing means the variable is not set or the site was not
redeployed. Present, but nothing recorded, means the banner was declined.

## F. Nothing leaked

```bash
git log -p --all | grep -iE "xkeysib-|sk_[0-9]{4,}_|whsec_" | head
```

No output is the answer you want. Anything at all: tell DRP, and rotate that key.

---

## Done looks like

- [ ] A `subscribe` returns `200`
- [ ] B contact appears in Brevo with tags
- [ ] C campaign survives a page change
- [ ] D webhook answers `401` to an unsigned message
- [ ] E a visit appears in Plausible Realtime after accepting
- [ ] F no key anywhere in git history

Once A–F pass, everything DRP can control is connected. What remains is the
September events, and that is IMPACT's to supply.
