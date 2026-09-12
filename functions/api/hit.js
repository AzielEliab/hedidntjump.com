import { handleRequest } from "../../workers/hedidntjump-stats/src/index.js";

const WORKER = "https://hedidntjump-stats.vibelock.workers.dev";

export async function onRequest(context) {
  const url = new URL(context.request.url);
  url.pathname = "/api/hit";
  if (context.env && context.env.STATS) {
    return handleRequest(new Request(url, context.request), context.env);
  }
  const target = WORKER + "/api/hit" + url.search;
  const res = await fetch(new Request(target, context.request));
  const headers = new Headers(res.headers);
  const origin = context.request.headers.get("Origin") || "";
  if (origin) headers.set("access-control-allow-origin", origin);
  headers.set("cache-control", "no-store");
  return new Response(res.body, { status: res.status, headers });
}
