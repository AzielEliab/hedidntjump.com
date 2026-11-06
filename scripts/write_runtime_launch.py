#!/usr/bin/env python3
"""Cite Softwares+runtime launch readiness on HDJ machine surfaces.

HDJ stays a Zioncheck archive. This is a cross-link cite of aziel-runtime
2.0.0-rc1 (Dual re-lock main 16b543b5 / version_id 21b64dc5), not a Softwares clone.
Stale pin 31ccb56b/d7b63ac1 is replaced. Worker version_id was declared, not
observed by a live Worker GET in this writer.

Does not invent Plane B LIVE, Framagit URLs, , or a global
Receipts paper-tab. Does not change hashed /ingest-as-receipt.json.
Does not add visible 1 Chronicles 15:20 chrome.
Live origin is Cloudflare Pages project hedidntjump (docs/), not GH Pages alone.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
LASTMOD = "2026-10-01"  # keep equal to write_sitemap.LASTMOD
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"

GIT_SHA = "16b543b5961f03813076e38ff19d883d46845c48"
GIT_SHORT = "16b543b5"
VERSION_ID = "21b64dc5"
STALE_GIT_SHA = "31ccb56b6c01647f434a9981c9843602c5967899"
STALE_GIT_SHORT = "31ccb56b"
STALE_VERSION_ID = "d7b63ac1"
VERSION = "2.0.0-rc1"
PIN_NOTE = (
    "Dual re-lock. Git object 16b543b5961f03813076e38ff19d883d46845c48 "
    "resolved from GitHub AzielEliab/aziel-runtime (prefix 16b543b5). "
    "Worker version_id 21b64dc5 is the declared Dual pin replacing stale "
    "31ccb56b/d7b63ac1. This file does not claim a live Worker GET observed "
    "version_id 21b64dc5."
)
COS_TIP_CANDIDATE = "a536ec66"
AUTHORED_FROM = "6b2a02fa7e8f93325bd3bb5facf6195b33e9a094"
RUNTIME_GITHUB = "https://github.com/AzielEliab/aziel-runtime"
RUNTIME_WORKER = "https://aziel-runtime.vibelock.workers.dev/"
RUNTIME_GLAMA = "https://glama.ai/mcp/servers/AzielEliab/aziel-runtime"
RUNTIME_SOFTWARE = f"{RUNTIME_WORKER.rstrip('/')}/v1/software"
RUNTIME_DOWNLOAD = f"{RUNTIME_WORKER.rstrip('/')}/download"
RUNTIME_MCP = f"{RUNTIME_WORKER.rstrip('/')}/mcp"
RUNTIME_MESH = f"{RUNTIME_WORKER.rstrip('/')}/v1/mesh"
RUNTIME_CITE = f"{RUNTIME_WORKER.rstrip('/')}/cite.json"
PAGES_PROJECT = "hedidntjump"
PAGES_PREVIEW = "https://hedidntjump.pages.dev"


def dumps(obj: object) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def launch_cite() -> dict:
    return {
        "spec": "SOFTWARES-RUNTIME-LAUNCH-1.0",
        "author": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "this_host": "hedidntjump.com",
        "this_host_role": "Marion Zioncheck archive — sister cite",
        "softwares_clone": False,
        "softwares_tab": False,
        "visible_1520": False,
        "lamb_lens": {
            "shelf": "https://www.azielcorpuslibrary.net/corpus",
            "note": "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net.",
        },
        "no_lie": "NO-LIE / NO-REWRITE",
        "no_lie_rule": (
            "receipts that still hash; copies not all on one tunnel; "
            "verify without voice; no rewrite key; network never lies even to stay alive."
        ),
        "runtime_sot": {
            "status": "LIVE",
            "product": "aziel-runtime",
            "version": VERSION,
            "branch": "main",
            "git_sha": GIT_SHA,
            "git_short": GIT_SHORT,
            "version_id": VERSION_ID,
            "replaces_stale": f"{STALE_GIT_SHORT}/{STALE_VERSION_ID}",
            "git_object_resolved": True,
            "worker_version_observed": False,
            "pin_note": PIN_NOTE,
            "github": RUNTIME_GITHUB,
            "worker": RUNTIME_WORKER,
            "one_line": (
                "Aziel Runtime is a node-meshed orchestration suite of MCP-connected software "
                "designed to route catalog Softwares through the FragGate door, mint receipts, "
                "and coordinate mesh presence."
            ),
            "glama": RUNTIME_GLAMA,
            "glama_note": "Prefer Try on Glama for Aziel Runtime MCP. Worker is secondary execution / OpenAPI.",
            "mcp_primary": RUNTIME_GLAMA,
            "software": RUNTIME_SOFTWARE,
            "download": RUNTIME_DOWNLOAD,
            "mcp": RUNTIME_MCP,
            "mesh": RUNTIME_MESH,
            "cite": RUNTIME_CITE,
            "library_front_door": "https://www.azielcorpuslibrary.net/runtime",
        },
        "readiness": {
            "human_ui": True,
            "mcp": True,
            "mesh": True,
            "vpn": True,
            "radios": "on",
            "download": True,
            "note": (
                "Human UI + MCP + mesh/VPN/radios + /download are launch-ready on aziel-runtime. "
                "HDJ cites those surfaces; it does not host Softwares, MCP, mesh radios, or /download."
            ),
        },
        "hdj": {
            "live_origin": "cloudflare-pages",
            "pages_project": PAGES_PROJECT,
            "pages_preview": PAGES_PREVIEW,
            "custom_domain": f"{APEX}/",
            "www": f"{WWW}/",
            "deploy_root": "docs/",
            "github_pages": "secondary-not-alone",
            "receipts_chrome": "Aziel-page-only. Not global paper-tabs Pg.11.",
            "mission": "Zioncheck archive",
            "mcp_local": False,
        },
        "shelves_honesty": {
            "plane_b_codeberg": "pass",
            "plane_b_archive_org": "pass",
            "plane_b_framagit": "SLOT",
            "plane_b_framagit_refuse": "CNS-NO-FORGE-MIRROR",
            "plane_b_framagit_url": None,
            "plane_b_live": False,
            "plane_c": "SLOT",
            "no_live_invent": True,
        },
        "live_nodes": {
            "sot": RUNTIME_MESH,
            "plane": "human-mesh-users-uses",
            "counts": "human mesh users + cited human uses",
            "software_nodes_excluded": True,
            "instance_nodes_excluded": True,
            "invent_users": False,
            "runtime_pr": "https://github.com/AzielEliab/aziel-runtime/pull/151",
            "runtime_git_short": GIT_SHORT,
            "runtime_version_id": VERSION_ID,
            "pin_note": PIN_NOTE,
            "hub": f"{APEX}/mesh",
            "note": (
                "Public Live Nodes cite GET /v1/mesh live_nodes + live_nodes_note. "
                "Softwares stay on software_nodes and do not feed this pill."
            ),
        },
        "spore": {
            "sot": "https://aziel-runtime.vibelock.workers.dev/v1/survival",
            "spec": "SPORE-1.0",
            "role": "failsafe",
            "last_resort": True,
            "replaces_cold_shelves": False,
            "re_cold_store": "RE-COLD-STORE",
            "destinations": [],
            "runtime_pr": "https://github.com/AzielEliab/aziel-runtime/pull/152",
            "runtime_git_short": "231b02f",
            "runtime_version_id": "a8f7fdc9",
            "hub": f"{APEX}/survival",
            "note": (
                "SPORE-1.0 last-resort failsafe + RE-COLD-STORE honest hook from "
                "Worker GET /v1/survival (Worker a8f7fdc9). "
                "Softwares blurbs unchanged."
            ),
        },
        "ingest_tip_unchanged": HDJ_INGEST_TIP,
        "note": (
            "Announce/sync only. Cite aziel-runtime / Try on Glama. "
            "Do not clone Softwares onto this Zioncheck archive."
        ),
    }


LLMS_BLOCK = f"""## SOFTWARES-RUNTIME-LAUNCH-1.0

Sister-archive cite of Aziel Runtime launch readiness. HDJ stays the Marion Zioncheck archive.

Runtime SoT LIVE: `{RUNTIME_GITHUB}` main `{GIT_SHORT}` / version_id `{VERSION_ID}` / `{VERSION}`.
Replaces stale pin `{STALE_GIT_SHORT}` / `{STALE_VERSION_ID}`. Git object resolved from GitHub. Worker version_id was declared by Dual and was not observed by a live Worker GET in this door.
Prefer [Try on Glama]({RUNTIME_GLAMA}). Worker (secondary): {RUNTIME_WORKER}
Human UI + MCP + mesh/VPN/radios + `/download` are launch-ready on aziel-runtime. This host cites; it does not host Softwares, MCP, mesh radios, or `/download`. GET never enables radios beyond suite-presence.
Live Nodes cite `{RUNTIME_MESH}`: human mesh users + cited human uses. Softwares (`software_nodes`) never feed that pill.
Identity Aziel Eliab only. Person @id: {PERSON_ID}. No visible 1 Chronicles 15:20.
Lamb Lens ingest: https://www.azielcorpuslibrary.net/corpus (not this host). NO-LIE / NO-REWRITE stays in force.

Live origin of this archive is Cloudflare Pages project `{PAGES_PROJECT}` (deploy root `docs/`). Preview {PAGES_PREVIEW}. GitHub Pages is not the live origin alone.
Receipts chrome stays Aziel-page-only (AboutAziel). Do not add Receipts as paper-tabs Pg.11.
Shelves honesty unchanged: Plane B Framagit SLOT (`CNS-NO-FORGE-MIRROR`, URL null); Codeberg + archive.org PASS still SLOT; Plane C SLOT. No LIVE invent.
HDJ ingest tip unchanged: `{HDJ_INGEST_TIP}`
"""

AI_BLOCK = f"""SOFTWARES-RUNTIME-LAUNCH-1.0 (sister cite):
- Runtime SoT LIVE: main {GIT_SHORT} / version_id {VERSION_ID} / {VERSION}
- Replaces stale pin {STALE_GIT_SHORT} / {STALE_VERSION_ID}. Git object resolved from GitHub. Worker version_id was declared by Dual and was not observed by a live Worker GET in this door.
- GitHub: {RUNTIME_GITHUB}
- Prefer Try on Glama: {RUNTIME_GLAMA}
- Worker (secondary): {RUNTIME_WORKER}
- Softwares catalog: {RUNTIME_SOFTWARE}
- Counted /download: {RUNTIME_DOWNLOAD}
- MCP: {RUNTIME_MCP}
- Mesh/VPN/radios cite: {RUNTIME_MESH} (GET never enables radios beyond suite-presence)
- Live Nodes = human mesh users + cited human uses. Softwares ≠ Live Nodes.
- Human UI + MCP + mesh/VPN/radios + /download ready on aziel-runtime. HDJ cites; does not host.
- Identity Aziel Eliab only. Person @id: {PERSON_ID}. No visible 15:20.
- Lamb Lens: https://www.azielcorpuslibrary.net/corpus
- NO-LIE / NO-REWRITE
- Live origin: Cloudflare Pages project {PAGES_PROJECT} (docs/). Preview {PAGES_PREVIEW}. Not GH Pages alone.
- Receipts chrome: Aziel-page-only (not paper-tabs Pg.11)
- Shelves: Plane B Framagit SLOT CNS-NO-FORGE-MIRROR; Codeberg+archive PASS still SLOT; Plane C SLOT; no LIVE invent
- Ingest tip unchanged: `{HDJ_INGEST_TIP}`
"""


def upsert_section(text: str, heading: str, block: str) -> str:
    if heading in text:
        return re.sub(
            rf"{re.escape(heading)}\n[\s\S]*?(?=\n## |\Z)",
            block.rstrip() + "\n\n",
            text,
            count=1,
        )
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def write_launch_json() -> None:
    body = dumps(launch_cite())
    for tree in TREES:
        path = tree / "runtime-launch.json"
        path.write_text(body, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


def patch_cite() -> None:
    extra = {
        "runtime_launch": launch_cite(),
        "runtime_sot": {
            "status": "LIVE",
            "product": "aziel-runtime",
            "version": VERSION,
            "branch": "main",
            "git_sha": GIT_SHA,
            "git_short": GIT_SHORT,
            "version_id": VERSION_ID,
            "replaces_stale": f"{STALE_GIT_SHORT}/{STALE_VERSION_ID}",
            "git_object_resolved": True,
            "worker_version_observed": False,
            "pin_note": PIN_NOTE,
            "github": RUNTIME_GITHUB,
            "worker": RUNTIME_WORKER,
            "glama": RUNTIME_GLAMA,
            "mcp_primary": RUNTIME_GLAMA,
            "one_line": (
                "Aziel Runtime is a node-meshed orchestration suite of MCP-connected software "
                "designed to route catalog Softwares through the FragGate door, mint receipts, "
                "and coordinate mesh presence."
            ),
        },
        "softwares_clone": False,
        "live_origin": {
            "kind": "cloudflare-pages",
            "project": PAGES_PROJECT,
            "preview": PAGES_PREVIEW,
            "custom_domain": f"{APEX}/",
            "deploy_root": "docs/",
            "github_pages": "secondary-not-alone",
        },
    }
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(extra)
        data["author"] = "Aziel Eliab"
        data["identity"] = "Aziel Eliab"
        data["person_id"] = PERSON_ID
        data["runtime_origin"] = RUNTIME_WORKER
        data["runtime_glama"] = RUNTIME_GLAMA
        data["runtime_glama_note"] = (
            "This archive has no local MCP. Prefer Try on Glama for Aziel Runtime MCP. Worker is secondary."
        )
        data["mcp_local"] = False
        data["mcp_note"] = (
            "Sister MCP door is aziel-runtime on Glama — not hosted on hedidntjump.com."
        )
        q = list(data.get("query_urls") or [])
        for u in (
            f"{APEX}/runtime-launch.json",
            f"{WWW}/runtime-launch.json",
        ):
            if u not in q:
                q.append(u)
        data["query_urls"] = q
        path.write_text(dumps(data), encoding="utf-8")
        print("cite", path.relative_to(ROOT))


def patch_llms() -> None:
    for tree in TREES:
        for name in ("llms.txt", "llms-full.txt"):
            path = tree / name
            text = path.read_text(encoding="utf-8")
            text = upsert_section(text, "## SOFTWARES-RUNTIME-LAUNCH-1.0", LLMS_BLOCK)
            if name == "llms.txt" and "runtime-launch.json" not in text.split("## Marion")[0]:
                text = text.replace(
                    f"- [{APEX}/cite.json]({APEX}/cite.json)\n",
                    (
                        f"- [{APEX}/cite.json]({APEX}/cite.json)\n"
                        f"- [{APEX}/runtime-launch.json]({APEX}/runtime-launch.json) — Softwares+runtime launch cite\n"
                    ),
                    1,
                )
            if "- [runtime-launch]" not in text and "Optional" in text:
                text = text.replace(
                    "- [ai.txt]",
                    (
                        f"- [runtime-launch]({APEX}/runtime-launch.json) — Softwares+runtime launch cite (aziel-runtime {VERSION})\n"
                        "- [ai.txt]"
                    ),
                    1,
                )
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("llms", path.relative_to(ROOT))
        ai = tree / "ai.txt"
        text = ai.read_text(encoding="utf-8")
        if "SOFTWARES-RUNTIME-LAUNCH-1.0" in text:
            text = re.sub(
                r"\nSOFTWARES-RUNTIME-LAUNCH-1.0[\s\S]*?(?=\nLIVE-NODES|\nBAN-SURVIVAL|\nIdentity lock|\nPublisher name|\nCOLD-MULTI-SHELF|\Z)",
                "\n" + AI_BLOCK.strip() + "\n\n",
                text,
                count=1,
            )
        elif "COLD-MULTI-SHELF-1.0" in text:
            text = text.replace(
                "COLD-MULTI-SHELF-1.0",
                AI_BLOCK.strip() + "\n\nCOLD-MULTI-SHELF-1.0",
                1,
            )
        else:
            text = text.rstrip() + "\n\n" + AI_BLOCK
        if f"{WWW}/runtime-launch.json" not in text:
            text = text.replace(
                "- https://www.hedidntjump.com/cite.json\n",
                (
                    "- https://www.hedidntjump.com/cite.json\n"
                    "- https://www.hedidntjump.com/runtime-launch.json\n"
                ),
                1,
            )
        ai.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("ai", ai.relative_to(ROOT))


def patch_mcp() -> None:
    note = (
        "Static Zioncheck archive has no local MCP tools/list. "
        f"Aziel Runtime {VERSION} SoT LIVE main {GIT_SHORT} / version_id {VERSION_ID}. "
        "Prefer Try on Glama."
    )
    payload = {
        "mcpServers": {
            "aziel-runtime": {
                "description": "Aziel Runtime MCP (not hosted on hedidntjump.com). Glama is primary.",
                "url": RUNTIME_GLAMA,
                "mcp": RUNTIME_MCP,
                "glama": RUNTIME_GLAMA,
                "primary": "glama",
                "version": VERSION,
                "git_sha": GIT_SHA,
                "version_id": VERSION_ID,
                "note": note,
            }
        }
    }
    body = dumps(payload)
    for tree in TREES:
        for rel in ("mcp.json", ".well-known/mcp.json"):
            path = tree / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            print("mcp", path.relative_to(ROOT))


def patch_headers() -> None:
    block = """
/runtime-launch.json
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age=3600
"""
    for tree in TREES:
        path = tree / "_headers"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "/runtime-launch.json" not in text:
            text = text.rstrip() + "\n" + block
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("headers", path.relative_to(ROOT))


def patch_redirects() -> None:
    line = "/runtime-launch.json /runtime-launch.json 200\n"
    for tree in TREES:
        path = tree / "_redirects"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "/runtime-launch.json /runtime-launch.json 200" not in text:
            text = text.rstrip() + "\n" + line
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("redirects", path.relative_to(ROOT))


def sitemap_entry(loc: str, host: str, priority: str = "0.4") -> str:
    return (
        "  <url>\n"
        f"    <loc>{host}{loc}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def patch_sitemap() -> None:
    for tree in TREES:
        path = tree / "sitemap.xml"
        text = path.read_text(encoding="utf-8")
        if f"{APEX}/runtime-launch.json</loc>" not in text:
            text = text.replace(
                "</urlset>",
                sitemap_entry("/runtime-launch.json", APEX, "0.4") + "</urlset>",
                1,
            )
        path.write_text(text, encoding="utf-8")
        print("sitemap", path.relative_to(ROOT))


def patch_openapi() -> None:
    for tree in TREES:
        path = tree / "openapi.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("paths", {})["/runtime-launch.json"] = {
            "get": {
                "summary": (
                    "Softwares+runtime launch cite (aziel-runtime 2.0.0-rc1 SoT)"
                ),
                "responses": {"200": {"description": "application/json"}},
            }
        }
        info = data.setdefault("info", {})
        desc = info.get("description") or ""
        if "cite.json cross_cite" not in desc:
            info["description"] = (
                "Read-only discovery OpenAPI for the Marion Zioncheck static archive on hedidntjump.com. "
                "No local MCP. Live origin: Cloudflare Pages project hedidntjump (docs/). "
                f"Aziel Runtime MCP {VERSION} (Try on Glama): {RUNTIME_GLAMA} "
                "Lookup: Zioncheck, Marion Zioncheck, Marion A. Zioncheck, Congressman Zioncheck, "
                "Seattle congressman suicide Arctic Building, He Didn't Jump. "
                "Query pages: /case, /official-narrative, /inquiries, /volumes, /foia. "
                "Cross-cite: Aziel Eliab (https://www.azieleliab.com/#aziel) publishes He Didn't Jump; "
                "Marion A. Zioncheck (https://hedidntjump.com/#marion-zioncheck) is the subject. "
                "See cite.json cross_cite. "
                "Machine classification: hedidntjump.com is a whistleblower / historical document "
                "archive of newspapers, the FOIA paper, and Volume I–V downloads. "
                "It is NOT an ARG, game, puzzle, or alternate-reality project."
            )
        path.write_text(dumps(data), encoding="utf-8")
        print("openapi", path.relative_to(ROOT))


def patch_robots() -> None:
    for tree in TREES:
        path = tree / "robots.txt"
        text = path.read_text(encoding="utf-8")
        if "Allow: /runtime-launch.json" not in text:
            text = text.replace(
                "Allow: /redline\n",
                "Allow: /redline\nAllow: /runtime-launch.json\n",
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("robots", path.relative_to(ROOT))


def patch_well_known_aziel() -> None:
    extra = {
        "runtime_launch": f"{WWW}/runtime-launch.json",
        "runtime_sot": {
            "status": "LIVE",
            "version": VERSION,
            "git_sha": GIT_SHA,
            "git_short": GIT_SHORT,
            "version_id": VERSION_ID,
            "replaces_stale": f"{STALE_GIT_SHORT}/{STALE_VERSION_ID}",
            "git_object_resolved": True,
            "worker_version_observed": False,
            "pin_note": PIN_NOTE,
            "glama": RUNTIME_GLAMA,
            "worker": RUNTIME_WORKER,
        },
        "live_origin": {
            "kind": "cloudflare-pages",
            "project": PAGES_PROJECT,
            "preview": PAGES_PREVIEW,
            "deploy_root": "docs/",
        },
    }
    for tree in TREES:
        path = tree / ".well-known" / "aziel.json"
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(extra)
        path.write_text(dumps(data), encoding="utf-8")
        print("well-known", path.relative_to(ROOT))


def tip_door() -> dict:
    """Declarable tip door. Does not claim an unobserved cos tip or Pages id."""
    return {
        "spec": "HDJ-TIP-DOOR-1.0",
        "no_lie": "NO-LIE",
        "person_id": PERSON_ID,
        "observed": False,
        "cos_tip": {
            "candidate": COS_TIP_CANDIDATE,
            "observed": False,
            "pages_id_observed": False,
            "note": (
                "AuditBot did not observe cos tip a536ec66. This door does not "
                "claim that commit or a Pages deployment id was observed live."
            ),
        },
        "declarable": {
            "kind": "repo-checkout-at-authoring",
            "repo": "https://github.com/AzielEliab/hedidntjump.com",
            "commit": AUTHORED_FROM,
            "observed_as_pages_deploy": False,
            "note": (
                "Git checkout this door was authored from. Not a live Pages "
                "observation. Not a claim that Pages is serving this commit."
            ),
        },
        "runtime_sot_pin": {
            "git_sha": GIT_SHA,
            "git_short": GIT_SHORT,
            "version_id": VERSION_ID,
            "replaces_stale": f"{STALE_GIT_SHORT}/{STALE_VERSION_ID}",
            "git_object_resolved": True,
            "worker_version_observed": False,
            "note": PIN_NOTE,
        },
        "unseal_seo": "HELD",
        "cap7_public_icann": False,
        "paid_sat": "HELD",
        "visible_1520": False,
    }


def write_tip_door() -> None:
    body = dumps(tip_door())
    entry = (
        "  <url>\n"
        "    <loc>https://hedidntjump.com/tip.json</loc>\n"
        "    <lastmod>2026-10-30</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>0.3</priority>\n"
        "  </url>\n"
    )
    who_line = (
        f"Softwares pin (Dual re-lock): main {GIT_SHORT} / version_id {VERSION_ID} "
        f"(git {GIT_SHA}). Replaces stale pin {STALE_GIT_SHORT} / {STALE_VERSION_ID}. "
        "Git object resolved from GitHub. Worker version_id was declared by Dual and "
        "was not observed by a live Worker GET in this door. "
        "pull/151 remains the historical hub-cite PR and is not this git object.\n"
    )
    for tree in TREES:
        for rel in ("tip.json", ".well-known/tip.json"):
            path = tree / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            print("tip", path.relative_to(ROOT))
        redirects = tree / "_redirects"
        redir = redirects.read_text(encoding="utf-8")
        for line in (
            "/tip.json /tip.json 200\n",
            "/.well-known/tip.json /.well-known/tip.json 200\n",
        ):
            if line not in redir:
                redir = redir.rstrip() + "\n" + line
        redirects.write_text(redir if redir.endswith("\n") else redir + "\n", encoding="utf-8")
        headers = tree / "_headers"
        head = headers.read_text(encoding="utf-8")
        if "/tip.json\n" not in head:
            head = head.rstrip() + (
                "\n\n/tip.json\n"
                "  Content-Type: application/json; charset=utf-8\n"
                "  Cache-Control: public, max-age=3600\n"
                "\n/.well-known/tip.json\n"
                "  Content-Type: application/json; charset=utf-8\n"
                "  Cache-Control: public, max-age=3600\n"
            )
            headers.write_text(head if head.endswith("\n") else head + "\n", encoding="utf-8")
        robots = tree / "robots.txt"
        robots_txt = robots.read_text(encoding="utf-8")
        if "Allow: /tip.json" not in robots_txt:
            robots_txt = robots_txt.replace(
                "Allow: /ai.txt\n",
                "Allow: /ai.txt\nAllow: /tip.json\nAllow: /.well-known/tip.json\n",
                1,
            )
            robots.write_text(robots_txt, encoding="utf-8")
        sitemap = tree / "sitemap.xml"
        sm = sitemap.read_text(encoding="utf-8")
        if "https://hedidntjump.com/tip.json" not in sm:
            sm = sm.replace("</urlset>", entry + "</urlset>", 1)
            sitemap.write_text(sm, encoding="utf-8")
        openapi = tree / "openapi.json"
        spec = json.loads(openapi.read_text(encoding="utf-8"))
        spec.setdefault("paths", {})["/tip.json"] = {
            "get": {
                "summary": (
                    "HDJ tip door. Cos tip a536ec66 was not observed. NO-LIE."
                ),
                "responses": {"200": {"description": "application/json"}},
            }
        }
        spec["paths"]["/.well-known/tip.json"] = {
            "get": {
                "summary": "Same HDJ tip door as /tip.json",
                "responses": {"200": {"description": "application/json"}},
            }
        }
        openapi.write_text(dumps(spec), encoding="utf-8")
        for name in ("who-is", "who-is-aziel-eliab.txt"):
            path = tree / name
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if "Softwares pin (Dual re-lock):" in text:
                text = re.sub(
                    r"Softwares pin \(Dual re-lock\):[^\n]*\n",
                    who_line,
                    text,
                    count=1,
                )
            else:
                needle = (
                    "Runtime lock: https://github.com/AzielEliab/aziel-runtime/pull/151 "
                    "(main 31ccb56 / Worker d7b63ac1)\n"
                )
                if needle in text:
                    text = text.replace(needle, needle + who_line, 1)
                else:
                    text = text.rstrip() + "\n" + who_line
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        cite = tree / "cite.json"
        data = json.loads(cite.read_text(encoding="utf-8"))
        data["tip_door"] = f"{APEX}/tip.json"
        data["cos_tip"] = {
            "candidate": COS_TIP_CANDIDATE,
            "observed": False,
            "pages_id_observed": False,
        }
        q = list(data.get("query_urls") or [])
        for url in (f"{APEX}/tip.json", f"{WWW}/.well-known/person.jsonld"):
            if url not in q:
                q.append(url)
        data["query_urls"] = q
        cite.write_text(dumps(data), encoding="utf-8")


def main() -> None:
    write_launch_json()
    patch_cite()
    patch_llms()
    patch_mcp()
    patch_headers()
    patch_redirects()
    patch_sitemap()
    patch_openapi()
    patch_robots()
    patch_well_known_aziel()
    write_tip_door()
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"SoT LIVE main `[^`]+` / version_id `[^`]+`",
        f"SoT LIVE main `{GIT_SHORT}` / version_id `{VERSION_ID}`",
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")
    print("readme", path.relative_to(ROOT))
    print("runtime launch cite written; ingest tip unchanged; no Softwares clone")


if __name__ == "__main__":
    main()
