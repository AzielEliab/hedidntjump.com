import { handleRequest } from "../workers/hedidntjump-stats/src/index.js";
import { buildStats } from "../workers/hedidntjump-stats/src/identity.js";

export async function onRequest(context) {
  const url = new URL(context.request.url);
  url.pathname = "/api/stats";
  const res = await handleRequest(new Request(url, context.request), context.env);
  let counters = { views: 0, downloads: 0, items: {} };
  try {
    counters = await res.json();
  } catch {
    /* static pointer still documents counters_url */
  }
  const live = Number.isFinite(Number(counters.views));
  return new Response(JSON.stringify(buildStats(counters, { live })), {
    status: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "access-control-allow-origin": "*",
      "cache-control": "public, max-age=60",
    },
  });
}
