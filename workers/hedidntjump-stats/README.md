# hedidntjump-stats

Cloudflare Worker + KV counters and the Zioncheck FOIA denial ledger for [hedidntjump.com](https://hedidntjump.com).

## Endpoints

| Method | Path | Action |
| --- | --- | --- |
| `GET` | `/api/stats` or `/stats` | Read totals. Does not increment. |
| `GET`/`POST` | `/api/hit?type=view\|download&id=...` | Increment and return totals. |
| `GET` | `/api/foia/ledger` | Public hash-chained receipt list + running count. |
| `POST` | `/api/foia/upload` | Multipart `file` + `attestation=zioncheck-foia-denial`. Hard-gated. |
| `GET` | `/api/foia/file/:index` | Bytes of an accepted denial. |

`POST` hit may send JSON `{ "type": "download", "id": "volume-1" }`.

CORS is open to `hedidntjump.com`, `*.pages.dev`, and `localhost`.

## FOIA content gate

Uploads are **rejected** unless every check passes:

1. Attestation field equals `zioncheck-foia-denial`.
2. File is PDF or image (JPEG/PNG/WebP/GIF/TIFF), sniffed from magic bytes, max 8 MB.
3. Readable text contains **FOIA** language (`foia`, `freedom of information`, `5 u.s.c.`, `§ 552`).
4. Readable text contains **Zioncheck / Marion Zioncheck**.
5. Readable text contains **denial** language (`denied`, `denial`, `withhold`, `exemption`, `no records`, …).

Unrelated images, memes, random PDFs, non-denials, and non-Zioncheck FOIA letters never enter the public ledger. Images without extractable text are rejected unless Workers AI (binding `AI`) can transcribe FOIA/Zioncheck/denial language.

Accepted files: SHA-256 of bytes → append `prev_hash → this_hash` in KV (`foia:tip`, `foia:receipt:N`) → store object in R2 `DENIALS`.

## Bindings ZionBot / Aziel must set

| Binding | Type | Purpose |
| --- | --- | --- |
| `STATS` | KV | View/download counters **and** `foia:*` chain keys. Already bound. |
| `DENIALS` | R2 | Accepted denial files. Create: `npx wrangler r2 bucket create hedidntjump-foia-denials` |
| `AI` | Workers AI (optional) | Image transcription for scans without a text layer. |

`wrangler.jsonc` names the R2 bucket `hedidntjump-foia-denials`. Create that bucket on the same account **before** `wrangler deploy`, or deploy will fail on the missing bucket.

## Deploy

```bash
cd workers/hedidntjump-stats
npx wrangler r2 bucket create hedidntjump-foia-denials
# optional OCR:
#   add to wrangler.jsonc: "ai": { "binding": "AI" }
npx wrangler deploy
```

Expected workers.dev host:

`https://hedidntjump-stats.vibelock.workers.dev`

The static site reads that URL from `<meta name="hdj-stats-api">`. `/foia.html` uses the same host for the ledger.

KV namespace for counters is already bound as `STATS`.

## Tests

```bash
cd workers/hedidntjump-stats
node --test
```

## Local

```bash
npx wrangler dev
```

Then open the archive with the meta tag pointed at `http://localhost:8787`.
