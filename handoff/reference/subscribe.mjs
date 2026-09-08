/**
 * Newsletter and waitlist signups from the site's own forms.
 *
 *   POST /.netlify/functions/subscribe
 *
 * Accepts what the forms already send — the visitor's fields plus the
 * attribution main.js attaches — validates it server-side, and puts the contact
 * in Brevo tagged so it can be segmented later.
 *
 * Three decisions worth keeping:
 *
 * Tags, not a list per event. `event:<slug>`, `locale:<nl|en>`, `source:<page>`.
 * Tags survive an account migration; a pile of list IDs does not, and the Brevo
 * account will move from DRP to IMPACT before the first real subscriber.
 *
 * Validation is repeated here even though the browser already did it. The
 * browser check is a courtesy to the visitor; this one is the only one that
 * counts, because anything can POST to this URL.
 *
 * Without BREVO_API_KEY it still returns 200 and logs. The forms keep working
 * before the account exists, and Netlify Forms remains the audit copy either
 * way — so a signup is never lost between the two.
 *
 * Environment:
 *   BREVO_API_KEY           optional; absent = log only
 *   BREVO_LIST_NEWSLETTER   numeric list id
 *   BREVO_LIST_WAITLIST     numeric list id
 *   BREVO_DOI_TEMPLATE_ID   optional; set it and newsletter signups use double
 *                           opt-in instead of subscribing directly
 *   BREVO_DOI_REDIRECT      where Brevo sends them after they confirm
 */
const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json' },
  });

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const CAMPAIGN = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content',
                  'utm_term', 'gclid', 'fbclid'];

function read(form) {
  const get = (k) => (form.get(k) ?? '').toString().trim();
  return {
    formName: get('form-name') || 'newsletter',
    email: get('email'),
    naam: get('naam'),
    leeftijd: get('leeftijd'),
    gemeente: get('gemeente'),
    consent: get('consent'),
    event: get('event'),
    ageMin: Number(get('ageMin') || 0),
    ageMax: Number(get('ageMax') || 0),
    honeypot: get('bot-field'),
    locale: get('locale') || 'nl',
    page: get('page'),
    landingPage: get('landing_page'),
    referrer: get('referrer'),
    campaign: Object.fromEntries(
      CAMPAIGN.map((k) => [k, get(k)]).filter(([, v]) => v),
    ),
  };
}

function validate(d) {
  const errors = {};
  if (!EMAIL.test(d.email)) errors.email = 'Vul een geldig e-mailadres in.';

  if (d.formName === 'waitlist') {
    if (d.naam.length < 2) errors.naam = 'Vul de voornaam van de deelnemer in.';
    const age = Number(d.leeftijd);
    if (!d.leeftijd || Number.isNaN(age)) {
      errors.leeftijd = 'Vul een leeftijd in.';
    } else if (d.ageMin && d.ageMax && (age < d.ageMin || age > d.ageMax)) {
      errors.leeftijd = `Deze editie is voor ${d.ageMin}–${d.ageMax} jaar.`;
    }
    // this form collects a child's name and age, so the guardian's consent is a
    // server-side requirement and not a checkbox the client can skip
    if (!d.consent) errors.consent = 'Bevestig dit om je in te schrijven.';
  }
  return errors;
}

function tagsFor(d) {
  const tags = [`locale:${d.locale}`];
  if (d.event) tags.push(`event:${d.event}`);
  if (d.formName) tags.push(`form:${d.formName}`);
  if (d.campaign.utm_campaign) tags.push(`campaign:${d.campaign.utm_campaign}`);
  if (d.campaign.utm_source) tags.push(`source:${d.campaign.utm_source}`);
  return tags;
}

async function toBrevo(d) {
  const key = process.env.BREVO_API_KEY;
  if (!key) return { stored: false, reason: 'BREVO_API_KEY not set' };

  const isWaitlist = d.formName === 'waitlist';
  const listId = isWaitlist
    ? process.env.BREVO_LIST_WAITLIST
    : process.env.BREVO_LIST_NEWSLETTER;

  // Brevo accepts a `tags` array and silently discards it — verified against the
  // live account: POST returns 201 and PUT returns 204, and the contact comes
  // back with tags: [] either way. So the segmentation this file was designed
  // around (locale, form, event, campaign) is carried as attributes instead.
  // Same information, and it is what the backoffice has to join on to answer
  // "which campaign drove this signup". The attributes must exist on the
  // account or Brevo drops them just as quietly — see setup/03-brevo.md.
  const attributes = {
    FIRSTNAME: d.naam || undefined,
    GEMEENTE: d.gemeente || undefined,
    LEEFTIJD: d.leeftijd || undefined,
    LANDING_PAGE: d.landingPage || undefined,
    REFERRER: d.referrer || undefined,
    LOCALE: d.locale || undefined,
    FORM: d.formName || undefined,
    EVENT: d.event || undefined,
    ...Object.fromEntries(
      Object.entries(d.campaign).map(([k, v]) => [k.toUpperCase(), v]),
    ),
  };

  const doi = process.env.BREVO_DOI_TEMPLATE_ID;
  // Double opt-in for the newsletter when a template is configured. Not for the
  // waitlist: that consent was given explicitly, by an adult, on a form that
  // will not submit without the tick — a second confirmation there costs
  // signups without adding a record we do not already hold.
  if (doi && !isWaitlist) {
    const res = await fetch('https://api.brevo.com/v3/contacts/doubleOptinConfirmation', {
      method: 'POST',
      headers: { 'api-key': key, 'content-type': 'application/json' },
      body: JSON.stringify({
        email: d.email,
        attributes,
        includeListIds: listId ? [Number(listId)] : undefined,
        templateId: Number(doi),
        redirectionUrl: process.env.BREVO_DOI_REDIRECT || undefined,
      }),
    });
    return { stored: res.ok, status: res.status, doubleOptIn: true };
  }

  const res = await fetch('https://api.brevo.com/v3/contacts', {
    method: 'POST',
    headers: { 'api-key': key, 'content-type': 'application/json' },
    body: JSON.stringify({
      email: d.email,
      attributes,
      listIds: listId ? [Number(listId)] : undefined,
      updateEnabled: true,          // signing up twice is normal, not an error
      tags: tagsFor(d),
    }),
  });
  return { stored: res.ok, status: res.status, doubleOptIn: false };
}

export default async (request) => {
  if (request.method !== 'POST') return json(405, { ok: false, error: 'POST only' });

  let form;
  try {
    const type = request.headers.get('content-type') || '';
    form = type.includes('application/json')
      ? new URLSearchParams(Object.entries(await request.json()))
      : new URLSearchParams(await request.text());
  } catch {
    return json(400, { ok: false, error: 'unreadable body' });
  }

  const d = read(form);

  // the honeypot is empty for a human and filled by a bot that completes every
  // field; answer 200 so the bot learns nothing from the difference
  if (d.honeypot) return json(200, { ok: true });

  const errors = validate(d);
  if (Object.keys(errors).length) return json(422, { ok: false, errors });

  let result;
  try {
    result = await toBrevo(d);
  } catch (err) {
    console.error('[subscribe] brevo failed', err);
    result = { stored: false, reason: 'upstream error' };
  }

  // Log regardless. Netlify Forms holds the audit copy, so a Brevo outage
  // degrades to "not segmented yet" rather than "lost".
  console.info('[subscribe]', JSON.stringify({ ...d, honeypot: undefined, result }));

  const message = d.formName === 'waitlist'
    ? 'Je staat op de wachtlijst.'
    : result.doubleOptIn
      ? 'Bijna klaar — bevestig je inschrijving via de mail die we net stuurden.'
      : 'Bedankt — je staat op de lijst.';

  return json(200, { ok: true, message });
};

export const config = { path: '/.netlify/functions/subscribe' };
