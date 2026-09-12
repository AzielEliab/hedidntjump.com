/**
 * He Didn't Jump — page-view + download counters.
 * KV binding: STATS
 *
 * GET  /api/stats              → current totals
 * GET  /api/hit?type=view|download&id=...
 * POST /api/hit                → JSON { type, id } or same query string
 *
 * Also accepts /stats and /hit (workers.dev root).
 * CORS: hedidntjump.com, *.pages.dev, localhost.
 */
const ALLOWED_ORIGIN = [
  /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/i,
  /^https:\/\/([a-z0-9-]+\.)?hedidntjump\.com$/i,
  /^https:\/\/[a-z0-9-]+\.pages\.dev$/i,
  /^https:\/\/azieleliab\.github\.io$/i,
];

const VIEW_KEY = "views";
const DOWNLOAD_KEY = "downloads";
const ITEM_PREFIX = "item:";

export function allowedOrigin(origin) {
  if (!origin) return "";
  return ALLOWED_ORIGIN.some((re) => re.test(origin)) ? origin : "";
}

export function corsHeaders(request, extra = {}) {
  const origin = allowedOrigin(request.headers.get("Origin") || "");
  const headers = {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    vary: "Origin",
    ...extra,
  };
  if (origin) headers["access-control-allow-origin"] = origin;
  return headers;
}

function json(request, body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: corsHeaders(request),
  });
}

async function readCount(kv, key) {
  const raw = kv ? await kv.get(key) : null;
  const n = Number.parseInt(raw || "0", 10);
  return Number.isFinite(n) && n > 0 ? n : 0;
}

async function bump(kv, key) {
  const next = (await readCount(kv, key)) + 1;
  if (kv) await kv.put(key, String(next));
  return next;
}

function itemKey(id) {
  const clean = String(id || "site")
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, "-")
    .slice(0, 80);
  return ITEM_PREFIX + (clean || "site");
}

export async function snapshot(kv) {
  const views = await readCount(kv, VIEW_KEY);
  const downloads = await readCount(kv, DOWNLOAD_KEY);
  const items = {};
  if (kv && typeof kv.list === "function") {
    const listed = await kv.list({ prefix: ITEM_PREFIX });
    for (const key of listed.keys || []) {
      items[key.name.slice(ITEM_PREFIX.length)] = await readCount(kv, key.name);
    }
  }
  return { views, downloads, items };
}

async function increment(kv, type, id) {
  if (type === "download") {
    await bump(kv, DOWNLOAD_KEY);
    await bump(kv, itemKey(id || "download"));
  } else {
    await bump(kv, VIEW_KEY);
    await bump(kv, itemKey(id || "landing"));
  }
  return snapshot(kv);
}

async function parseHit(request, url) {
  let type = (url.searchParams.get("type") || "view").toLowerCase();
  let id = url.searchParams.get("id") || "";
  if (request.method === "POST") {
    const ctype = request.headers.get("content-type") || "";
    if (ctype.includes("application/json")) {
      try {
        const body = await request.json();
        if (body && typeof body === "object") {
          if (body.type) type = String(body.type).toLowerCase();
          if (body.id) id = String(body.id);
        }
      } catch {
        /* keep query values */
      }
    }
  }
  if (type !== "download") type = "view";
  return { type, id };
}

function routeName(pathname) {
  const path = pathname.replace(/\/+$/, "") || "/";
  if (path === "/api/stats" || path === "/stats") return "stats";
  if (path === "/api/hit" || path === "/hit") return "hit";
  if (path === "/" || path === "/api") return "stats";
  return "";
}

export async function handleRequest(request, env) {
  const url = new URL(request.url);
  const route = routeName(url.pathname);

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders(request) });
  }

  if (!route) {
    return json(request, { error: "not_found" }, 404);
  }

  const kv = env && env.STATS;
  if (route === "stats") {
    return json(request, await snapshot(kv));
  }

  if (request.method !== "GET" && request.method !== "POST") {
    return json(request, { error: "method_not_allowed" }, 405);
  }

  const { type, id } = await parseHit(request, url);
  return json(request, await increment(kv, type, id));
}

export default {
  async fetch(request, env) {
    return handleRequest(request, env);
  },
};
