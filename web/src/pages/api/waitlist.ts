import type { APIRoute } from 'astro';

export const prerender = false;

/**
 * Waitlist intake.
 *
 * Every row carries event, locale, source and utm_* — that is what makes
 * "which campaign drove this signup" answerable later (doc 04 §3). Today it
 * validates and returns; the Payload write and the Brevo double opt-in land in
 * the 17 September milestone, at the two marked TODOs, without touching the
 * form or the client-side handler.
 *
 * The guardian's consent is checked here and not only in the browser. This form
 * collects a child's first name and age, so the tick is the lawful basis for
 * holding it — and anything at all can POST to this URL, which makes the
 * browser check a courtesy to the visitor and this one the only one that
 * counts. It is stored on the entry too: consent that cannot be evidenced later
 * is the same as no consent. Mirrors netlify/functions/subscribe.mjs, which is
 * what the live site posts to today; the two must not drift.
 */

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

type Errors = Record<string, string>;

export const POST: APIRoute = async ({ request, clientAddress }) => {
  const form = await request.formData();
  const get = (k: string) => String(form.get(k) ?? '').trim();

  const entry = {
    event: get('event'),
    participantName: get('naam'),
    participantAge: Number(get('leeftijd')),
    parentEmail: get('email'),
    municipality: get('gemeente') || null,
    guardianConsent: get('consent') !== '',
    locale: 'nl',
    source: request.headers.get('referer') ?? null,
    utm: Object.fromEntries(
      [...new URL(request.url).searchParams].filter(([k]) => k.startsWith('utm_')),
    ),
    createdAt: new Date().toISOString(),
    ip: clientAddress ?? null,
  };

  const errors: Errors = {};
  if (entry.participantName.length < 2) errors.naam = 'Vul de voornaam van de deelnemer in.';
  if (!Number.isFinite(entry.participantAge)) errors.leeftijd = 'Vul een leeftijd in.';
  if (!EMAIL.test(entry.parentEmail)) errors.email = 'Vul een geldig e-mailadres in.';
  if (!entry.event) errors.event = 'Onbekend event.';
  if (!entry.guardianConsent) errors.consent = 'Bevestig dit om je in te schrijven.';

  // the age range is the event's own, sent with the form and re-checked server-side
  const min = Number(form.get('ageMin') ?? 0);
  const max = Number(form.get('ageMax') ?? 0);
  if (min && max && (entry.participantAge < min || entry.participantAge > max)) {
    errors.leeftijd = `Deze editie is voor ${min}–${max} jaar.`;
  }

  if (Object.keys(errors).length > 0) {
    return new Response(JSON.stringify({ ok: false, errors }), {
      status: 422,
      headers: { 'content-type': 'application/json' },
    });
  }

  // TODO(17 Sep): create a waitlist_entries row in Payload
  // TODO(17 Sep): push the contact to Brevo with tag `event:<slug>`, double opt-in
  console.info('[waitlist]', JSON.stringify(entry));

  return new Response(
    JSON.stringify({
      ok: true,
      message: 'Je staat op de wachtlijst. We sturen een bevestiging naar ' + entry.parentEmail + '.',
    }),
    { status: 200, headers: { 'content-type': 'application/json' } },
  );
};
