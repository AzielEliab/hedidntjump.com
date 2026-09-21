# He Didn't Jump - complete Grok handoff

An Aziel Eliab Project
Repository: https://github.com/AzielEliab/hedidntjump.com
Domain owned by user: hedidntjump.com

## Task for Grok
Upload this complete snapshot to the existing repository. Preserve the website's wording, the 21 entries in their present order, five Volume I-V links, the Aziel Eliab credit, the five original PDFs, and all reader images. Do not rewrite or regenerate content.

The complete static site is in dist/. docs/ is the Cloudflare Pages deploy root (project `hedidntjump`, plus CNAME). Live origin is that Pages project — not GitHub Pages alone. Preview: https://hedidntjump.pages.dev. Serve either tree as the web root. Links begin with / and therefore require root hosting, not a /repository-name/ subdirectory. The landing paper now carries 23 inquiries of the record.

Live view and download pills call a Cloudflare Worker + KV stub:

- Client: `/stats.js` → `/api/stats` and `/api/hit?type=view|download&id=...`
- Worker: `workers/hedidntjump-stats/` (CORS for hedidntjump.com, *.pages.dev, localhost)
- Deploy: `npx wrangler deploy` from that folder. Default host is set in `<meta name="hdj-stats-api">`.
- FOIA paper: `/foia.html` (Nadeau columns + Aziel’s FOIA Binary editorial + hash-chained denial ledger). Rubye / Aziel project paper: `/rubye.html`.
- Ledger upload: `POST /api/foia/upload` (Zioncheck FOIA denials only). Create R2 bucket `hedidntjump-foia-denials` and bind `DENIALS` before public uploads work — see `workers/hedidntjump-stats/README.md`.

Drop historic plates over the placeholders at `/assets/arctic-building.webp`, `/assets/marion-rubye.webp`, and `/assets/marion-gravestone.webp`. Optional all-volumes zip: `scripts/make-all-volumes-zip.sh` (otherwise the landing control downloads each PDF).

## Local preview
python3 -m http.server 8000 --directory dist
Open http://localhost:8000

## Cloudflare Pages sync (docs/ deploy root)
scripts/sync_docs.sh

GitHub Pages may still build from docs/; it is not the live origin alone. Custom domain DNS stays on Cloudflare Pages project `hedidntjump`.

BAN-SURVIVAL-1.0 hub pull: `/survival` (short TTL) cites runtime `GET https://aziel-runtime.vibelock.workers.dev/v1/survival` — mutual backup, live doors, platforms all LIVE, calling name Aziel Runtime, Cap-7 `resolves_to_hub: false`. MirageGrid Cap-7 Worker LIVE `https://miragegrid.vibelock.workers.dev`. HDJ stays the Zioncheck archive.

LIVE-NODES-HUB-CITE-1.0 hub pull: `/mesh` (short TTL) cites runtime `GET https://aziel-runtime.vibelock.workers.dev/v1/mesh` — Live Nodes = human mesh users + cited human uses. Softwares (`software_nodes`) never feed that pill. Runtime lock https://github.com/AzielEliab/aziel-runtime/pull/151 (main `31ccb56` / Worker `d7b63ac1`). HDJ stays the Zioncheck archive.


Sister cite: Aziel Runtime 2.0.0-rc1 SoT LIVE main `31ccb56` / version_id `d7b63ac1`. Prefer [Try on Glama](https://glama.ai/mcp/servers/AzielEliab/aziel-runtime). Machine field: `/runtime-launch.json`.

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

GitHub upload does not activate the custom domain. For a static host, serve dist/ or docs/ with no compilation. Live origin is Cloudflare Pages project `hedidntjump` (docs/). Keep hedidntjump.com DNS on that Pages project. GitHub Pages is secondary, not the live origin alone.

## Acceptance checks
- Landing page opens with portrait, styling and favicon.
- Exactly 23 case entries open and close, in existing order.
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
