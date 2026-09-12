/**
 * He Didn't Jump — page-view + download counters + Zioncheck FOIA ledger.
 * KV binding: STATS
 * R2 binding: DENIALS (FOIA denial files)
 * AI binding: optional Workers AI for image transcription
 *
 * GET  /api/stats              → current totals
 * GET  /api/hit?type=view|download&id=...
 * POST /api/hit                → JSON { type, id } or same query string
 * GET  /api/foia/ledger        → public hash chain
 * POST /api/foia/upload        → gated Zioncheck FOIA-denial upload
 * GET  /api/foia/file/:index   → accepted file bytes
 * GET  /api/mesh or /api/mesh/status
 *      → read-only Live Nodes rollup (proxies aziel-runtime /v1/mesh).
 *        Always mesh: "on". GET never enables. No radio writes.
 *
 * Also accepts /stats and /hit (workers.dev root).
 * CORS: hedidntjump.com, *.pages.dev, localhost.
 */
import { appendDenial, gateUpload, readLedger, readObject, sniffType } from "./foia.js";
const ALLOWED_ORIGIN = [
  /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/i,
  /^https:\/\/([a-z0-9-]+\.)?hedidntjump\.com$/i,
  /^https:\/\/[a-z0-9-]+\.pages\.dev$/i,
  /^https:\/\/azieleliab\.github\.io$/i,
];

const VIEW_KEY = "views";
const DOWNLOAD_KEY = "downloads";
const ITEM_PREFIX = "item:";
const RUNTIME_ORIGIN = "https://aziel-runtime.vibelock.workers.dev";
const MESH_WRITE = /\/(api\/)?mesh\/(enable|disable|join|leave|heartbeat|broadcast|nodes)$/i;

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
    "access-control-expose-headers": "content-type",
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
  if (path === "/api/foia/ledger" || path === "/foia/ledger") return "foia-ledger";
  if (path === "/api/foia/upload" || path === "/foia/upload") return "foia-upload";
  if (/^\/(api\/)?foia\/file\/\d+$/.test(path)) return "foia-file";
  if (MESH_WRITE.test(path)) return "mesh-write";
  if (path === "/api/mesh" || path === "/mesh" || path === "/api/mesh/status" || path === "/mesh/status") {
    return "mesh";
  }
  if (path === "/" || path === "/api") return "stats";
  return "";
}

export function displayMesh(raw, { ok = true } = {}) {
  const src = raw && typeof raw === "object" ? raw : {};
  const nested = src.src && typeof src.src === "object" ? src.src : null;
  const n = Number(
    src.live_nodes ??
      (nested && nested.live_nodes) ??
      (src.rollup && src.rollup.live) ??
      (Array.isArray(src.nodes) ? src.nodes.length : Number.NaN),
  );
  const live = Number.isFinite(n) && n >= 0 ? Math.floor(n) : null;
  return {
    ok,
    author: "Aziel Eliab",
    identity: "Aziel Eliab",
    live_nodes: live,
    mesh: "on",
    spec: "QNM-BUILD-1.0",
    note: "Read-only Live Nodes rollup. GET never enables. Counts only.",
  };
}

function runtimeOrigin(env) {
  const base = env && env.AZIEL_RUNTIME ? String(env.AZIEL_RUNTIME) : RUNTIME_ORIGIN;
  return base.replace(/\/+$/, "");
}

async function handleMesh(request, env) {
  const fetchFn = (env && env.MESH_FETCH) || fetch;
  const url = runtimeOrigin(env) + "/v1/mesh";
  try {
    const res = await fetchFn(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "User-Agent": "Mozilla/5.0",
      },
    });
    if (!res || !res.ok) {
      return json(request, displayMesh(null, { ok: false }), 502);
    }
    let raw = null;
    try {
      raw = await res.json();
    } catch {
      raw = null;
    }
    return json(request, displayMesh(raw));
  } catch {
    return json(request, displayMesh(null, { ok: false }), 502);
  }
}

async function handleFoiaUpload(request, env) {
  if (request.method !== "POST") {
    return json(request, { ok: false, error: "method_not_allowed" }, 405);
  }
  const ctype = request.headers.get("content-type") || "";
  if (!ctype.includes("multipart/form-data")) {
    return json(request, { ok: false, error: "rejected", reasons: ["Send multipart/form-data with a file field named file."] }, 400);
  }
  let form;
  try {
    form = await request.formData();
  } catch {
    return json(request, { ok: false, error: "rejected", reasons: ["The upload could not be read."] }, 400);
  }
  const file = form.get("file");
  if (!file || typeof file.arrayBuffer !== "function") {
    return json(request, { ok: false, error: "rejected", reasons: ["No file field was sent."] }, 400);
  }
  const bytes = new Uint8Array(await file.arrayBuffer());
  const type = sniffType(file.name, file.type, bytes);
  const attestation = String(form.get("attestation") || "");
  const gated = await gateUpload({ bytes, type, filename: file.name, attestation }, env);
  if (!gated.ok) {
    return json(request, { ok: false, error: "rejected", reasons: gated.reasons }, 422);
  }
  const stored = await appendDenial(env, { bytes, type, filename: file.name });
  if (!stored.ok) {
    return json(request, stored, stored.status || 503);
  }
  return json(request, { ok: true, receipt: stored.receipt, count: stored.receipt.index }, 201);
}

async function handleFoiaFile(request, env, pathname) {
  const match = pathname.match(/(\d+)$/);
  const index = match ? Number(match[1]) : 0;
  const found = await readObject(env, index);
  if (!found) {
    return json(request, { ok: false, error: "not_found" }, 404);
  }
  const headers = corsHeaders(request, {
    "content-type": found.receipt.type || "application/octet-stream",
    "content-disposition": `inline; filename="${found.receipt.filename || "denial"}"`,
    "cache-control": "public, max-age=3600",
  });
  return new Response(found.obj.body, { status: 200, headers });
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

  if (route === "mesh-write") {
    return json(request, { ok: false, error: "read_only" }, 404);
  }
  if (route === "mesh") {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return json(request, { ok: false, error: "method_not_allowed" }, 405);
    }
    return handleMesh(request, env);
  }

  const kv = env && env.STATS;
  if (route === "stats") {
    return json(request, await snapshot(kv));
  }
  if (route === "foia-ledger") {
    return json(request, await readLedger(kv));
  }
  if (route === "foia-upload") {
    return handleFoiaUpload(request, env);
  }
  if (route === "foia-file") {
    return handleFoiaFile(request, env, url.pathname.replace(/\/+$/, ""));
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
