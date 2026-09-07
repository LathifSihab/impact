/**
 * Keep every host except the production domain out of the index.
 *
 * Staging carries canonical tags pointing at www.wemakeimpact.be, so if a
 * *.netlify.app deploy gets crawled it competes with the real domain. This is
 * host-based rather than a checklist item, so nothing has to be remembered on
 * launch day: the moment the site answers on the production domain it becomes
 * indexable, and every preview stays hidden.
 */
const PRODUCTION_HOSTS = ['www.wemakeimpact.be', 'wemakeimpact.be'];

export default async (request: Request, context: { next: () => Promise<Response> }) => {
  const response = await context.next();
  const host = new URL(request.url).hostname;

  if (!PRODUCTION_HOSTS.includes(host)) {
    response.headers.set('X-Robots-Tag', 'noindex, nofollow');
  }
  return response;
};

export const config = { path: '/*' };
