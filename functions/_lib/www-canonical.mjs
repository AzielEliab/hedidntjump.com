// Pages _redirects does not support domain-level redirects, so www → apex
// is applied here. Path and query are preserved. The hash never reaches the server.

export const WWW_HOST = "www.hedidntjump.com";
export const APEX_ORIGIN = "https://hedidntjump.com";

function normalizeHost(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/:\d+$/, "")
    .replace(/\.+$/, "");
}

export function canonicalRedirectUrl(requestUrl, hostHeader) {
  let url;
  try {
    url = new URL(requestUrl);
  } catch {
    return null;
  }
  const headerHost = normalizeHost(hostHeader);
  const urlHost = normalizeHost(url.hostname);
  if (headerHost !== WWW_HOST && urlHost !== WWW_HOST) return null;
  // Never resolve the request path against the apex: "//evil.com" or "/\\evil.com"
  // would be read as a new authority. Start from the fixed apex origin and only
  // set path and query, collapsing any run of leading slashes or backslashes.
  const target = new URL(APEX_ORIGIN);
  target.pathname = "/" + url.pathname.replace(/^[\/\\]+/, "");
  target.search = url.search;
  if (target.origin !== APEX_ORIGIN) return APEX_ORIGIN + "/";
  return target.toString();
}

export async function onRequest(context) {
  const request = context.request;
  const target = canonicalRedirectUrl(request.url, request.headers.get("host"));
  if (!target) return context.next();
  return Response.redirect(target, 301);
}
