# He Didn't Jump - complete Grok handoff

An Aziel Eliab Project
Repository: https://github.com/AzielEliab/hedidntjump.com
Domain owned by user: hedidntjump.com

## Task for Grok
Upload this complete snapshot to the existing repository. Preserve the website's wording, the 21 entries in their present order, five Volume I-V links, the Aziel Eliab credit, the five original PDFs, and all reader images. Do not rewrite or regenerate content.

The complete static site is in dist/. docs/ is an identical GitHub Pages copy (plus CNAME). Serve either as the web root. Links begin with / and therefore require root hosting, not a /repository-name/ subdirectory.

Live view and download pills call a Cloudflare Worker + KV stub:

- Client: `/stats.js` → `/api/stats` and `/api/hit?type=view|download&id=...`
- Live Nodes pill (read-only): `/stats.js` → `/api/mesh` (Worker proxy of aziel-runtime `GET /v1/mesh`) or a client fetch of that runtime URL. Display is always **Live Nodes · N / mesh on**. GET never enables. Not a Softwares catalog.
- Worker: `workers/hedidntjump-stats/` (CORS for hedidntjump.com, *.pages.dev, localhost)
- Deploy: `npx wrangler deploy` from that folder. Default host is set in `<meta name="hdj-stats-api">`.
- FOIA paper: `/foia.html` (Nadeau columns + Aziel’s FOIA Binary editorial + hash-chained denial ledger). Rubye / Aziel project paper: `/rubye.html`.
- Ledger upload: `POST /api/foia/upload` (Zioncheck FOIA denials only). Create R2 bucket `hedidntjump-foia-denials` and bind `DENIALS` before public uploads work — see `workers/hedidntjump-stats/README.md`.

Drop historic plates over the placeholders at `/assets/arctic-building.webp`, `/assets/marion-rubye.webp`, and `/assets/marion-gravestone.webp`. Optional all-volumes zip: `scripts/make-all-volumes-zip.sh` (otherwise the landing control downloads each PDF).

## Local preview
python3 -m http.server 8000 --directory dist
Open http://localhost:8000

## GitHub Pages sync
scripts/sync_docs.sh

## Validate the handoff
python3 verify_handoff.py

## Upload
Use the user's authorized GitHub connection with Contents write access. Clone AzielEliab/hedidntjump.com. Copy dist/, this README.md, verify_handoff.py and FILE_MANIFEST.json into the checkout. Keep existing unrelated files. Inspect the diff, commit, and push without force. If GitHub rejects integration access, fix the integration permissions; no token is included in this package.

Suggested commands, run separately after authorized authentication:
git clone https://github.com/AzielEliab/hedidntjump.com.git
cd hedidntjump.com
# Copy the package files into this checkout, then:
python3 verify_handoff.py
git add dist README.md verify_handoff.py FILE_MANIFEST.json
git commit -m "Upload complete Marion Zioncheck website"
git push origin main

GitHub upload does not activate the custom domain. For a static host, serve dist/ with no compilation. Keep hedidntjump.com DNS and existing hosting changes separate from this source upload. The existing Sites deployment remains the current hosted version until the owner changes it.

## Acceptance checks
- Landing page opens with portrait, styling and favicon.
- Exactly 21 case entries open and close, in existing order.
- Volume I-V controls open matching readers.
- Reader page totals are 20, 20, 21, 15, 14.
- Previous/next, page selector, direct page links and PDF downloads work.
- Reader URL with invalid volume/page falls back safely.
- No clipping at phone and desktop widths.
- Every file matches FILE_MANIFEST.json.

## Status at handoff
The previous GitHub upload attempt was rejected with HTTP 403: Resource not accessible by integration. No successful upload was reported. Do not assume files already exist remotely.
The current Sites URL is https://hedidntjump.fey-cup-1329.chatgpt.site and is owner-private. The domain attachment was pending DNS validation at the last check.

The source materials retain their original rights. This package grants no new license to collected documents or photographs.
