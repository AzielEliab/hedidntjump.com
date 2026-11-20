// Pages _redirects does not support domain-level redirects, so www → apex
// is applied here. Path and query are preserved. The hash never reaches the server.

export const WWW_HOST = "www.hedidntjump.com";
export const APEX_ORIGIN = "https://hedidntjump.com";

export function canonicalRedirectUrl(requestUrl, hostHeader) {
  const url = new URL(requestUrl);
  const headerHost = String(hostHeader || "")
    .split(":")[0]
    .trim()
    .toLowerCase();
  const urlHost = url.hostname.toLowerCase();
  if (headerHost !== WWW_HOST && urlHost !== WWW_HOST) return null;
  return new URL(url.pathname + url.search, APEX_ORIGIN).toString();
}

export async function onRequest(context) {
  const request = context.request;
  const target = canonicalRedirectUrl(request.url, request.headers.get("host"));
  if (!target) return context.next();
  return Response.redirect(target, 301);
}
