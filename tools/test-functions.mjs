/**
 * Exercises the Netlify Functions without Netlify.
 *
 *   node tools/test-functions.mjs
 *
 * They are plain handlers taking a Request and returning a Response, so they can
 * be called directly. No network: BREVO_API_KEY is left unset, which is exactly
 * the path the site is on until the account is wired, and the one that has to
 * stay working.
 *
 * The signature test is the point of this file. A webhook endpoint that rejects
 * everything looks identical from the outside to one that is simply not being
 * called — so it is worth proving a correctly signed request gets through
 * before pointing Ticket Tailor at it.
 */
import crypto from 'node:crypto';

let pass = 0;
let fail = 0;

function check(name, got, want) {
  const ok = got === want;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${name}${ok ? '' : `  (got ${got}, want ${want})`}`);
  ok ? pass++ : fail++;
}

const post = (body, headers = {}) =>
  new Request('https://example.test/', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded', ...headers },
    body,
  });

const { default: subscribe } = await import('../netlify/functions/subscribe.mjs');
const { default: ttWebhook } = await import('../netlify/functions/tt-webhook.mjs');

console.log('\nsubscribe');

let r = await subscribe(new Request('https://example.test/'));
check('GET is rejected', r.status, 405);

r = await subscribe(post('form-name=newsletter&email=nope'));
check('invalid email is 422', r.status, 422);

r = await subscribe(post('form-name=newsletter&email=ouder@example.be&locale=nl'));
check('valid newsletter is 200 with no Brevo key', r.status, 200);
check('and reports success', (await r.json()).ok, true);

r = await subscribe(post('form-name=newsletter&email=bot@example.be&bot-field=filled'));
check('honeypot answers 200 and tells the bot nothing', r.status, 200);

r = await subscribe(post(
  'form-name=waitlist&email=ouder@example.be&naam=Sam&leeftijd=11&ageMin=8&ageMax=14'));
check('waitlist without consent is 422', r.status, 422);
check('and names the consent field', Object.keys((await r.json()).errors).join(), 'consent');

r = await subscribe(post(
  'form-name=waitlist&email=ouder@example.be&naam=Sam&leeftijd=30&ageMin=8&ageMax=14&consent=ja'));
check('age outside the edition is 422', r.status, 422);

r = await subscribe(post(
  'form-name=waitlist&email=ouder@example.be&naam=Sam&leeftijd=11&ageMin=8&ageMax=14&consent=ja'));
check('complete waitlist entry is 200', r.status, 200);

console.log('\ntt-webhook');

delete process.env.TICKET_TAILOR_WEBHOOK_SECRET;
r = await ttWebhook(post('{}'));
check('unconfigured fails closed, not open', r.status, 503);

process.env.TICKET_TAILOR_WEBHOOK_SECRET = 'test-secret';

r = await ttWebhook(post('{}'));
check('no signature is 401', r.status, 401);

r = await ttWebhook(post('{}', { 'tl-signature': 't=1,v1=deadbeef' }));
check('bad signature is 401', r.status, 401);

const body = JSON.stringify({
  event: 'WAITLIST_SIGNUP.CREATED',
  payload: { email: 'ouder@example.be', first_name: 'Sam', event_id: 'ev_123' },
});
const now = Math.floor(Date.now() / 1000);
const sign = (ts) =>
  crypto.createHmac('sha256', 'test-secret').update(`${ts}.${body}`).digest('hex');

r = await ttWebhook(post(body, { 'tl-signature': `t=${now},v1=${sign(now)}` }));
check('a correctly signed request is accepted', r.status, 200);

const old = now - 600;
r = await ttWebhook(post(body, { 'tl-signature': `t=${old},v1=${sign(old)}` }));
check('a valid signature from 10 minutes ago is replayed and rejected', r.status, 401);

console.log(`\n${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
