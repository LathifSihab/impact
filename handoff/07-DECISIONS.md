# Decisions already made

Each of these was argued through and settled. They are recorded so the next
person does not spend the same hours reaching the same conclusion — or quietly
reverse one without knowing what it cost.

---

**Wix is not the backend.** The client pays for it for another year and asked
whether to hang backend functionality off it. No: it is a closed platform whose
data layer cannot be queried from an external stack and whose automations cannot
be triggered from these forms. Anything built there gets rebuilt when the
subscription ends. It is kept only as the 301 redirect source until it lapses.

**Mollie was dropped for Stripe.** Ticket Tailor settles through Stripe, PayPal
or Square — not Mollie. Bancontact, which matters in Belgium, comes through
Stripe. This was found by reading Ticket Tailor's docs, and it removed what was
recorded as the project's worst blocker.

**Ticket Tailor owns commerce; we own content.** Events, tickets, waitlists,
registrations and participants live there. It has a backoffice the client can log
into today, with no build, and it takes payments, PCI scope, refunds, VAT
invoices and door scanning off the table. The CMS covers site content only.

**This also solved "self-serve without a rebuild."** The brief's hardest
requirement — *add events without needing a rebuild each time* — is satisfied by
where events live, not by rewriting the render mode. She adds an event in Ticket
Tailor and the box office reflects it immediately.

**Payload was planned, then deferred, then replaced.** It was the intended CMS
(self-hosted, Postgres on Neon) and `reference/content.config.ts` mirrors its
models. It was dropped because it needs an always-on Node server and a database
to hand over to a youth organisation. Supabase gives the same Postgres with
managed auth and no server to operate.

**The Astro app is not deployed and should not be.** 6 of 20 pages, no English
routing. It exists in the original repo as `web/`. Its schemas are worth
everything; its pages are not worth porting under time pressure.

**Analytics is Plausible, not GA4.** The brief said "privacy-friendly". GA4 needs
a consent banner and contradicts that. Plausible is loaded behind the banner
anyway, because a banner that lists a category and then ignores the answer is
worse than no banner.

**Segmentation is Brevo attributes, not tags.** Tags were the original design.
Brevo accepts a `tags` array and silently discards it on this account — verified
directly. Fourteen contact attributes were created instead.

**Nothing that identifies an account is hardcoded.** Not the box office slug, not
the Plausible domain, not the site URL. All come from environment variables, so
handover is editing boxes in a UI rather than a code change and a redeploy. Two
API keys were leaked into a chat early on and had to be rotated; the discipline
comes from that.

**Guardian consent is checked server-side.** The waitlist collects a child's
first name and age, so the tick is the lawful basis for holding it, and anything
can POST to that URL. The browser check is a courtesy; the server one is what
counts. It is stored on the record too — consent that cannot be evidenced later
is the same as no consent. An earlier version of the Astro route accepted
submissions without it; that was a defect, fixed 9 September.

**Signup endpoints answer `200` even when the upstream write fails.** Deliberate:
a Brevo outage must never lose a signup. The visitor gets a friendly answer, the
failure goes to the log, and an audit copy is kept elsewhere. If you rebuild
this, keep the property *and* the log — otherwise success and silent failure look
identical, which cost hours here.

**Nothing renders without a consent flag** where a real person is named.
`confirmed` on experts and figures, `consentOnFile` on testimonials. These are
not soft-delete flags; they mean a human verified publication is permitted.

---

## Two mistakes worth not repeating

**A `200` is not proof.** The signup endpoint returned `200` for a full day while
Brevo rejected every call with `401`, because the deployed environment held a
deleted API key. Verify integrations by checking the far side — fetch the
contact, read the log — never by the response code of your own endpoint.

**Environment variables reach serverless functions only at deploy time.** Editing
a value in a hosting UI changes nothing until a new build runs. Two separate
failures here traced back to this one fact.
