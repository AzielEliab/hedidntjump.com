/**
 * Zioncheck-only FOIA denial ledger.
 *
 * Hard gate: accept only image/PDF files that read as a FOIA denial
 * concerning Marion Zioncheck. Nothing else enters the public chain.
 *
 * Bindings (optional until ZionBot deploys them):
 *   STATS   — KV (shared with counters); keys foia:tip, foia:receipt:N
 *   DENIALS — R2 bucket for accepted files
 *   AI      — optional Workers AI for image OCR / vision
 */

export const FOIA_MAX_BYTES = 8 * 1024 * 1024;
export const FOIA_ALLOWED_TYPES = new Set([
  "application/pdf",
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/gif",
  "image/tiff",
]);
export const GENESIS_HASH = "0".repeat(64);

const FOIA_TERMS = [
  "foia",
  "freedom of information",
  "5 u.s.c.",
  "5 usc",
  "§ 552",
  "section 552",
];
const ZION_TERMS = ["zioncheck", "marion a. zioncheck", "marion zioncheck"];
const DENIAL_TERMS = [
  "denied",
  "denial",
  "withhold",
  "withheld",
  "exemption",
  "no records",
  "cannot locate",
  "we are unable",
  "will not release",
  "refused",
  "reject",
];

function norm(text) {
  return String(text || "")
    .toLowerCase()
    .replace(/\u00a0/g, " ")
    .replace(/[“”]/g, '"')
    .replace(/[’]/g, "'");
}

export function extractPdfText(bytes) {
  const latin = new TextDecoder("latin1").decode(bytes);
  const chunks = [];
  const paren = /\((?:\\.|[^\\)]){2,}\)/g;
  let m;
  while ((m = paren.exec(latin))) {
    chunks.push(
      m[0]
        .slice(1, -1)
        .replace(/\\n/g, "\n")
        .replace(/\\r/g, "\n")
        .replace(/\\t/g, " ")
        .replace(/\\(.)/g, "$1"),
    );
  }
  const tj = /\[([^\]]{4,})\]\s*TJ/g;
  while ((m = tj.exec(latin))) {
    chunks.push(m[1].replace(/[()\\]/g, " "));
  }
  return chunks.join(" ");
}

export function extractAscii(bytes) {
  const latin = new TextDecoder("latin1").decode(bytes);
  return latin.replace(/[^\x09\x0a\x0d\x20-\x7e]/g, " ");
}

function hasAny(text, terms) {
  return terms.some((t) => text.includes(t));
}

export function classifyDenialText(text) {
  const body = norm(text);
  const reasons = [];
  const hasFoia = hasAny(body, FOIA_TERMS);
  const hasZion = hasAny(body, ZION_TERMS);
  const hasDenial = hasAny(body, DENIAL_TERMS);

  if (!hasFoia) {
    reasons.push("No FOIA / Freedom of Information / 5 U.S.C. § 552 language was readable in the file.");
  }
  if (!hasZion) {
    reasons.push("No Marion Zioncheck language was readable. Only Zioncheck FOIA denials are accepted.");
  }
  if (!hasDenial) {
    reasons.push("No denial / withhold / exemption / no-records language was readable.");
  }
  if (body.length < 40) {
    reasons.push("The extracted text is too short to verify as a denial letter.");
  }
  return {
    ok: reasons.length === 0,
    reasons,
    hasFoia,
    hasZion,
    hasDenial,
  };
}

export function sniffType(name, declared, bytes) {
  const n = String(name || "").toLowerCase();
  const d = String(declared || "").toLowerCase().split(";")[0].trim();
  if (bytes && bytes.length >= 5 && bytes[0] === 0x25 && bytes[1] === 0x50 && bytes[2] === 0x44 && bytes[3] === 0x46) {
    return "application/pdf";
  }
  if (bytes && bytes.length >= 3 && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) {
    return "image/jpeg";
  }
  if (bytes && bytes.length >= 8 && bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47) {
    return "image/png";
  }
  if (bytes && bytes.length >= 12 && bytes[8] === 0x57 && bytes[9] === 0x45 && bytes[10] === 0x42 && bytes[11] === 0x50) {
    return "image/webp";
  }
  if (FOIA_ALLOWED_TYPES.has(d)) return d;
  if (n.endsWith(".pdf")) return "application/pdf";
  if (n.endsWith(".jpg") || n.endsWith(".jpeg")) return "image/jpeg";
  if (n.endsWith(".png")) return "image/png";
  if (n.endsWith(".webp")) return "image/webp";
  return d || "application/octet-stream";
}

export async function sha256Hex(bytes) {
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function chainHash(prev, contentHash, timestamp, index) {
  const payload = `${prev}\n${contentHash}\n${timestamp}\n${index}`;
  return sha256Hex(new TextEncoder().encode(payload));
}

async function visionText(env, bytes, type) {
  if (!env || !env.AI || typeof env.AI.run !== "function") return "";
  const b64 = btoa(String.fromCharCode(...bytes.subarray(0, Math.min(bytes.length, 1_500_000))));
  try {
    const res = await env.AI.run("@cf/meta/llama-3.2-11b-vision-instruct", {
      messages: [
        {
          role: "user",
          content: [
            {
              type: "text",
              text: "Transcribe every visible word from this document image. Return plain text only.",
            },
            { type: "image_url", image_url: { url: `data:${type};base64,${b64}` } },
          ],
        },
      ],
    });
    if (typeof res === "string") return res;
    if (res && typeof res.response === "string") return res.response;
    if (res && typeof res.description === "string") return res.description;
  } catch {
    return "";
  }
  return "";
}

export async function gatherReadableText(bytes, type, env) {
  let text = extractAscii(bytes);
  if (type === "application/pdf") {
    text += " " + extractPdfText(bytes);
  }
  if (type.startsWith("image/") || (type === "application/pdf" && norm(text).length < 80)) {
    text += " " + (await visionText(env, bytes, type));
  }
  return text;
}

export async function gateUpload({ bytes, type, filename, attestation }, env) {
  const reasons = [];
  if (attestation !== "zioncheck-foia-denial") {
    reasons.push("You must attest that this file is a Denied FOIA regarding Marion Zioncheck only.");
  }
  if (!bytes || !bytes.byteLength) {
    reasons.push("No file was received.");
  } else if (bytes.byteLength > FOIA_MAX_BYTES) {
    reasons.push("File exceeds the 8 MB size limit.");
  }
  if (!FOIA_ALLOWED_TYPES.has(type)) {
    reasons.push("Only PDF or image scans are accepted (PDF, JPEG, PNG, WebP).");
  }
  if (reasons.length) {
    return { ok: false, reasons };
  }

  const text = await gatherReadableText(bytes, type, env);
  const classified = classifyDenialText(text);
  if (!classified.ok) {
    if (type.startsWith("image/") && !classified.hasFoia && !classified.hasZion && !env?.AI) {
      classified.reasons.push(
        "This image had no readable FOIA/Zioncheck denial text, and Workers AI OCR is not bound on this deploy. Upload a text-layer PDF of the Zioncheck denial, or bind AI and redeploy.",
      );
    }
    return { ok: false, reasons: classified.reasons };
  }
  return { ok: true, reasons: [], textSample: norm(text).slice(0, 240) };
}

async function kvGet(kv, key) {
  if (!kv) return null;
  return kv.get(key);
}

async function kvPut(kv, key, value) {
  if (!kv) throw new Error("STATS KV is not bound");
  await kv.put(key, value);
}

export async function readLedger(kv) {
  const tipRaw = await kvGet(kv, "foia:tip");
  const tip = tipRaw ? JSON.parse(tipRaw) : { index: 0, hash: GENESIS_HASH };
  const receipts = [];
  const last = Number(tip.index) || 0;
  const start = Math.max(1, last - 199);
  for (let i = last; i >= start; i -= 1) {
    const raw = await kvGet(kv, "foia:receipt:" + i);
    if (raw) receipts.push(JSON.parse(raw));
  }
  return { count: last, tip: tip.hash, genesis: GENESIS_HASH, receipts };
}

export async function appendDenial(env, { bytes, type, filename }) {
  const kv = env && env.STATS;
  const r2 = env && env.DENIALS;
  if (!kv) {
    return { ok: false, status: 503, error: "ledger_unbound", reasons: ["STATS KV is not bound. See workers/hedidntjump-stats/README.md."] };
  }
  if (!r2) {
    return { ok: false, status: 503, error: "storage_unbound", reasons: ["R2 binding DENIALS is not set. Create a bucket and bind it before public uploads go live."] };
  }

  const contentHash = await sha256Hex(bytes);
  const tipRaw = await kvGet(kv, "foia:tip");
  const tip = tipRaw ? JSON.parse(tipRaw) : { index: 0, hash: GENESIS_HASH };
  const index = (Number(tip.index) || 0) + 1;
  const timestamp = new Date().toISOString();
  const prevHash = tip.hash || GENESIS_HASH;
  const hash = await chainHash(prevHash, contentHash, timestamp, index);
  const objectKey = `denials/${String(index).padStart(5, "0")}-${contentHash.slice(0, 16)}`;

  await r2.put(objectKey, bytes, {
    httpMetadata: { contentType: type },
    customMetadata: { filename: String(filename || "upload").slice(0, 120), contentHash },
  });

  const receipt = {
    index,
    timestamp,
    hash,
    prev_hash: prevHash,
    content_hash: contentHash,
    filename: String(filename || "upload").slice(0, 120),
    type,
    bytes: bytes.byteLength,
    object: objectKey,
  };
  await kvPut(kv, "foia:receipt:" + index, JSON.stringify(receipt));
  await kvPut(kv, "foia:tip", JSON.stringify({ index, hash }));
  return { ok: true, status: 201, receipt };
}

export async function readObject(env, index) {
  const kv = env && env.STATS;
  const r2 = env && env.DENIALS;
  const raw = await kvGet(kv, "foia:receipt:" + Number(index));
  if (!raw || !r2) return null;
  const receipt = JSON.parse(raw);
  const obj = await r2.get(receipt.object);
  if (!obj) return null;
  return { receipt, obj };
}
