/**
 * Ticket Tailor webhook receiver.
 *
 *   POST /.netlify/functions/tt-webhook
 *
 * Point the WAITLIST_SIGNUP.CREATED subscription here. Not at a page: a page
 * returns HTML with a 200, so Ticket Tailor records a successful delivery and
 * every signup is discarded silently — no error, no retry, nothing to notice.
 *
 * What it does today: verifies the signature, normalises the payload, and
 * mirrors the contact into Brevo tagged with its event so the "all signups in
 * one place" requirement holds from the first one. It deliberately does not
 * write to a database, because there is not one yet — when there is, that is one
 * more call in `store()` below and nothing else changes.
 *
 * Environment (Netlify → Site configuration → Environment variables):
 *   TICKET_TAILOR_WEBHOOK_SECRET   required, or every request is rejected
 *   BREVO_API_KEY                  optional; without it the mirror is skipped
 *   BREVO_LIST_WAITLIST            optional; numeric list id
 */
import crypto from 'node:crypto';

const json = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json' },
  });

/**
 * Ticket Tailor signs with an HMAC over `timestamp.body`, sent as
 * `tl-signature: t=<unix>,v1=<hex>`.
 *
 * Two things here are not optional. The comparison is timing-safe, because a
 * plain === leaks the signature one byte at a time to anyone willing to measure.
 * And the timestamp is checked, because a valid signature is valid forever
 * otherwise — an attacker who captures one request can replay it indefinitely.
 */
function verify(rawBody, header, secret) {
  if (!header || !secret) return false;

  const parts = Object.fromEntries(
    header.split(',').map((p) => p.trim().split('=').map((s) => s.trim())),
  );
  const timestamp = parts.t;
  const signature = parts.v1;
  if (!timestamp || !signature) return false;

  const age = Math.abs(Date.now() / 1000 - Number(timestamp));
  if (!Number.isFinite(age) || age > 300) return false;   // five minutes

  const expected = crypto
    .createHmac('sha256', secret)
    .update(`${timestamp}.${rawBody}`)
    .digest('hex');

  const a = Buffer.from(expected, 'utf8');
  const b = Buffer.from(signature, 'utf8');
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

/** Everything downstream should depend on this shape, not on Ticket Tailor's. */
function normalise(payload) {
  const p = payload?.payload ?? payload ?? {};
  return {
    source: 'ticket-tailor',
    kind: payload?.event ?? 'unknown',
    email: p.email ?? p.buyer_details?.email ?? null,
    firstName: p.first_name ?? p.buyer_details?.first_name ?? null,
    lastName: p.last_name ?? p.buyer_details?.last_name ?? null,
    eventId: p.event_id ?? p.event?.id ?? null,
    eventName: p.event?.name ?? null,
    receivedAt: new Date().toISOString(),
  };
}

async function mirrorToBrevo(entry) {
  const key = process.env.BREVO_API_KEY;
  if (!key || !entry.email) return { mirrored: false, reason: 'not configured' };

  const tags = ['source:ticket-tailor'];
  if (entry.eventId) tags.push(`event:${entry.eventId}`);

  const res = await fetch('https://api.brevo.com/v3/contacts', {
    method: 'POST',
    headers: { 'api-key': key, 'content-type': 'application/json' },
    body: JSON.stringify({
      email: entry.email,
      attributes: {
        FIRSTNAME: entry.firstName ?? undefined,
        LASTNAME: entry.lastName ?? undefined,
        EVENT: entry.eventName ?? entry.eventId ?? undefined,
      },
      listIds: process.env.BREVO_LIST_WAITLIST
        ? [Number(process.env.BREVO_LIST_WAITLIST)]
        : undefined,
      // an existing contact must be updated, not rejected: someone joining a
      // second waitlist is normal and must not 400
      updateEnabled: true,
      tags,
    }),
  });

  return { mirrored: res.ok, status: res.status };
}

async function store(entry) {
  // TODO: write to the permanent store once the backend exists. Until then the
  // function log is the record, and Ticket Tailor itself holds the authoritative
  // list — this mirror exists so our own reporting is not blind.
  console.info('[tt-webhook]', JSON.stringify(entry));
}

export default async (request) => {
  if (request.method !== 'POST') return json(405, { error: 'POST only' });

  const secret = process.env.TICKET_TAILOR_WEBHOOK_SECRET;
  if (!secret) {
    // Fail closed. An unconfigured endpoint that accepts anything is worse than
    // one that accepts nothing, because it looks like it is working.
    console.error('[tt-webhook] TICKET_TAILOR_WEBHOOK_SECRET is not set');
    return json(503, { error: 'not configured' });
  }

  const raw = await request.text();
  if (!verify(raw, request.headers.get('tl-signature'), secret)) {
    return json(401, { error: 'bad signature' });
  }

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    return json(400, { error: 'invalid json' });
  }

  const entry = normalise(payload);
  await store(entry);
  const brevo = await mirrorToBrevo(entry);

  // 200 quickly and unconditionally once the signature is good: a webhook that
  // errors on a downstream failure gets retried, and retries duplicate contacts.
  return json(200, { ok: true, ...brevo });
};

export const config = { path: '/.netlify/functions/tt-webhook' };
