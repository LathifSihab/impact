import type { APIRoute } from 'astro';

export const prerender = false;

/**
 * Newsletter intake. Same attribution fields as the waitlist so both land in one
 * audience with the campaign that produced them (doc 04 §3/§5).
 */

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const POST: APIRoute = async ({ request }) => {
  const form = await request.formData();
  const email = String(form.get('email') ?? '').trim();

  if (!EMAIL.test(email)) {
    return new Response(
      JSON.stringify({ ok: false, errors: { email: 'Vul een geldig e-mailadres in.' } }),
      { status: 422, headers: { 'content-type': 'application/json' } },
    );
  }

  const subscriber = {
    email,
    locale: 'nl',
    source: request.headers.get('referer') ?? null,
    utm: Object.fromEntries(
      [...new URL(request.url).searchParams].filter(([k]) => k.startsWith('utm_')),
    ),
    createdAt: new Date().toISOString(),
  };

  // TODO(17 Sep): create a newsletter_subscribers row in Payload
  // TODO(17 Sep): Brevo contact + double opt-in confirmation mail
  console.info('[newsletter]', JSON.stringify(subscriber));

  return new Response(JSON.stringify({ ok: true, message: 'Bedankt — je staat op de lijst.' }), {
    status: 200,
    headers: { 'content-type': 'application/json' },
  });
};
