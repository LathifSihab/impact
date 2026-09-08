/**
 * Keep every host except the production domain out of the index.
 *
 * Staging carries canonical tags pointing at www.wemakeimpact.be, so if a
 * *.netlify.app deploy gets crawled it competes with the real domain. This is
 * host-based rather than a checklist item, so nothing has to be remembered on
 * launch day: the moment the site answers on the production domain it becomes
 * indexable, and every preview stays hidden.
 *
 * The method guard is not optional. This function is registered on '/*', so it
 * also saw form submissions: it called context.next(), which resolves a POST
 * against the static file tree, got Netlify's "Page not found", and handed that
 * back — so every submission returned 404 with this function's own header on
 * it, long before Netlify's form processing was reached. Returning nothing
 * means "not handling this request", which lets it continue down the normal
 * pipeline. A robots header on a form POST was never meaningful anyway; only
 * documents a crawler can fetch need it.
 */
const PRODUCTION_HOSTS = ['www.wemakeimpact.be', 'wemakeimpact.be'];

export default async (request: Request, context: { next: () => Promise<Response> }) => {
  if (request.method !== 'GET' && request.method !== 'HEAD') return;

  const host = new URL(request.url).hostname;
  if (PRODUCTION_HOSTS.includes(host)) return;   // nothing to add, so do not intercept

  const response = await context.next();
  response.headers.set('X-Robots-Tag', 'noindex, nofollow');
  return response;
};

export const config = { path: '/*' };
