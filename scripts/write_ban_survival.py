#!/usr/bin/env python3
"""Pull BAN-SURVIVAL SoT + MirageGrid Cap-7 Worker onto HDJ machine surfaces.

Short-TTL hub pull. HDJ stays the Zioncheck archive. Not a Softwares clone.
Does not invent case facts, hosted Cap-7 /mcp, or HDJ as a live exec door.
Does not add visible 1 Chronicles 15:20 chrome.
Person @id stays https://www.azieleliab.com/#aziel.
"""
from __future__ import annotations

import json
import re
import ssl
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
LASTMOD = "2026-09-18"
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"
TTL_SECONDS = 60
SOT_URL = "https://aziel-runtime.vibelock.workers.dev/v1/survival"
CAP7_URL = "https://miragegrid.vibelock.workers.dev/bridge"
MIRAGE_WORKER = "https://miragegrid.vibelock.workers.dev"
LAMB_LENS = "https://www.azielcorpuslibrary.net/corpus"
UA = "Mozilla/5.0"

LIVE_DOOR_IDS = ("workers-dev", "library-runtime", "author-runtime", "godlock-runtime")
PUBLIC_PAIR = ("azgrid", "azbooth")
AZNET_SIDE = ("azcloak", "azvault", "azshift", "azflag", "azstandby")


def dumps(obj: object) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def fetch_json(url: str) -> dict[str, Any] | None:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": UA},
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 — writer falls back to pinned SoT
        print("fetch miss", url, type(exc).__name__, exc)
        return None


def pin_sot() -> dict[str, Any]:
    """Pinned 2026-09-18 pull of /v1/survival. Used only if live fetch misses."""
    return {
        "spec": "BAN-SURVIVAL-1.0",
        "mode": "LIVE",
        "mutual_backup": True,
        "person_id": PERSON_ID,
        "live_doors": [
            {
                "id": "workers-dev",
                "origin": "https://aziel-runtime.vibelock.workers.dev",
                "via": "workers.dev",
                "status": "live",
                "independent": False,
            },
            {
                "id": "library-runtime",
                "origin": "https://www.azielcorpuslibrary.net/runtime",
                "via": "service-binding",
                "status": "live",
                "independent": False,
            },
            {
                "id": "author-runtime",
                "origin": "https://www.azieleliab.com/runtime",
                "via": "service-binding",
                "status": "live",
                "independent": False,
            },
            {
                "id": "godlock-runtime",
                "origin": "https://godlock.uk/runtime",
                "via": "service-binding",
                "status": "live",
                "independent": False,
            },
        ],
        "platforms": {
            "spec": "BAN-PLATFORMS-1.0",
            "all_live": True,
            "native_app_store": False,
            "calling_name": "Aziel Runtime",
        },
        "calling_name": {
            "spec": "BAN-CALLING-NAME-1.0",
            "rotated": False,
            "calling_name": "Aziel Runtime",
            "calling_slug": "aziel-runtime",
            "identity": "Aziel Eliab",
            "identity_unchanged": True,
        },
        "cap7_aznet": {
            "factory": "miragegrid",
            "resolves_to_hub": False,
            "public_icann": False,
            "cite": {"status": "live"},
            "aznet_verify": {"status": "live"},
            "hosted_endpoints": {"status": "slot"},
            "shuffle": {
                "layout": "live",
                "public_worker_shuffle": "slot",
            },
        },
    }


def pin_cap7() -> dict[str, Any]:
    return {
        "resolves_to_hub": False,
        "public_icann": False,
        "app_worker": {"status": "live-app"},
        "honesty": {
            "app_worker": "LIVE",
            "public_pair_https": "LIVE",
            "aznet_side_https": "SLOT",
        },
        "public_pair": list(PUBLIC_PAIR),
        "aznet_side": list(AZNET_SIDE),
        "cap7": [
            {
                "label": "azshift",
                "design_of": "https://hedidntjump.com/",
                "resolves_to_hub": False,
                "honesty_public": "SLOT",
                "reach": "aznet",
            }
        ],
    }


def hub_wrap(sot: dict[str, Any], cap7: dict[str, Any], *, pulled: bool) -> dict[str, Any]:
    live = list(sot.get("live_doors") or [])
    platforms = dict(sot.get("platforms") or {})
    calling = dict(sot.get("calling_name") or {})
    cap7az = dict(sot.get("cap7_aznet") or {})
    sites = list(cap7.get("cap7") or [])
    azshift = next((row for row in sites if row.get("label") == "azshift"), None)
    honesty = dict(cap7.get("honesty") or {})
    app = dict(cap7.get("app_worker") or {})
    return {
        "spec": "BAN-SURVIVAL-1.0",
        "surface": "hedidntjump-hub-pull",
        "this_host": "hedidntjump.com",
        "this_host_role": "Marion Zioncheck archive — sister cite",
        "this_host_is_live_door": False,
        "this_host_runtime_front": False,
        "softwares_clone": False,
        "softwares_tab": False,
        "mission": "Zioncheck archive",
        "invented_case_facts": False,
        "author": "Aziel Eliab",
        "identity": "Aziel Eliab",
        "person_id": PERSON_ID,
        "visible_1520": False,
        "growth_on": True,
        "lamb_lens": {
            "shelf": LAMB_LENS,
            "note": "Public Lamb Lens / Corpus ingest lives on azielcorpuslibrary.net.",
        },
        "no_lie": "NO-LIE / NO-REWRITE",
        "ttl_seconds": TTL_SECONDS,
        "sot": SOT_URL,
        "sot_aliases": [
            "https://aziel-runtime.vibelock.workers.dev/survival",
            "https://www.azielcorpuslibrary.net/runtime/survival",
            "https://www.azieleliab.com/runtime/survival",
            "https://godlock.uk/runtime/survival",
        ],
        "sot_pulled": pulled,
        "mode": sot.get("mode") or "LIVE",
        "mutual_backup": sot.get("mutual_backup") is True,
        "live_doors": [
            {
                "id": d.get("id"),
                "origin": d.get("origin"),
                "via": d.get("via"),
                "status": d.get("status"),
                "independent": d.get("independent") is True,
            }
            for d in live
        ],
        "live_door_ids": [d.get("id") for d in live],
        "platforms": {
            "spec": platforms.get("spec") or "BAN-PLATFORMS-1.0",
            "all_live": platforms.get("all_live") is True,
            "native_app_store": platforms.get("native_app_store") is True,
            "calling_name": platforms.get("calling_name") or calling.get("calling_name"),
        },
        "calling_name": {
            "spec": calling.get("spec") or "BAN-CALLING-NAME-1.0",
            "rotated": calling.get("rotated") is True,
            "calling_name": calling.get("calling_name"),
            "calling_slug": calling.get("calling_slug"),
            "identity": calling.get("identity") or "Aziel Eliab",
            "identity_unchanged": calling.get("identity_unchanged") is not False,
        },
        "cap7_aznet": {
            "factory": cap7az.get("factory") or "miragegrid",
            "resolves_to_hub": cap7az.get("resolves_to_hub") is True,
            "public_icann": cap7az.get("public_icann") is True,
            "cite_status": (cap7az.get("cite") or {}).get("status"),
            "aznet_verify_status": (cap7az.get("aznet_verify") or {}).get("status"),
            "hosted_endpoints": (cap7az.get("hosted_endpoints") or {}).get("status"),
            "shuffle_layout": (cap7az.get("shuffle") or {}).get("layout"),
            "public_worker_shuffle": (cap7az.get("shuffle") or {}).get("public_worker_shuffle"),
        },
        "miragegrid_worker": {
            "url": MIRAGE_WORKER,
            "bridge": CAP7_URL,
            "status": app.get("status") or honesty.get("app_worker") or "LIVE",
            "resolves_to_hub": cap7.get("resolves_to_hub") is True,
            "public_icann": cap7.get("public_icann") is True,
            "public_pair": list(cap7.get("public_pair") or PUBLIC_PAIR),
            "aznet_side": list(cap7.get("aznet_side") or AZNET_SIDE),
            "public_pair_https": honesty.get("public_pair_https") or "LIVE",
            "aznet_side_https": honesty.get("aznet_side_https") or "SLOT",
            "hdj_design_site": "azshift",
            "azshift": {
                "label": "azshift",
                "design_of": (azshift or {}).get("design_of") or "https://hedidntjump.com/",
                "resolves_to_hub": (azshift or {}).get("resolves_to_hub") is True,
                "honesty_public": (azshift or {}).get("honesty_public") or "SLOT",
                "reach": (azshift or {}).get("reach") or "aznet",
            },
        },
        "ingest_tip_unchanged": HDJ_INGEST_TIP,
        "note": (
            "Hub pull of runtime /survival (short TTL) plus MirageGrid Cap-7 Worker cite. "
            "FragGate stays the door on the runtime sister. "
            "Zioncheck stays the HDJ mission. Do not invent case facts."
        ),
    }


def survival_cite() -> dict[str, Any]:
    live = fetch_json(SOT_URL)
    cap7 = fetch_json(CAP7_URL)
    pulled = live is not None
    sot = live or pin_sot()
    return hub_wrap(sot, cap7 or pin_cap7(), pulled=pulled)


def upsert_section(text: str, heading: str, block: str) -> str:
    if heading in text:
        return re.sub(
            rf"{re.escape(heading)}\n[\s\S]*?(?=\n## |\Z)",
            block.rstrip() + "\n\n",
            text,
            count=1,
        )
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


LLMS_BLOCK = f"""## BAN-SURVIVAL-1.0

Hub pull of Aziel Runtime `GET /survival` (short TTL {TTL_SECONDS}s). HDJ stays the Marion Zioncheck archive.

SoT: {SOT_URL}
Mutual backup LIVE: cold shelves back up death-by-ban; live multi-front backs up shelf death. Keep both.
Live doors (runtime SoT): workers-dev, library-runtime, author-runtime, godlock-runtime. This host is not in `live_doors`.
Platforms: Windows / Mac / Linux / Android / iPhone all LIVE on the runtime Worker (browser + PWA + MCP). `native_app_store: false`.
Calling name: Aziel Runtime (`aziel-runtime`). Identity Aziel Eliab only. Hubs pull `/survival` rather than hardcode a rotated name.
Cap-7 / AZNet: cite + verify LIVE; hosted Cap-7 `/mcp` SLOT. `resolves_to_hub: false`. `public_icann: false`.
MirageGrid Cap-7 Worker LIVE: {MIRAGE_WORKER} (`/bridge`). Public pair azgrid + azbooth = LIVE Worker HTTPS. Remainder AZNet-side SLOT. HDJ design DNA site is `azshift` (SLOT; design_of https://hedidntjump.com/; resolves_to_hub false).
Person @id: {PERSON_ID}. Lamb Lens ingest: {LAMB_LENS} (not this host). NO-LIE / NO-REWRITE. No visible 1 Chronicles 15:20.
Zioncheck stays the HDJ mission. Do not invent court holdings, FOIA letters, or case quotes.
HDJ ingest tip unchanged: `{HDJ_INGEST_TIP}`
This host: {APEX}/survival · {APEX}/survival.json · {APEX}/v1/survival
"""

AI_BLOCK = f"""BAN-SURVIVAL-1.0 (hub pull; short TTL {TTL_SECONDS}s):
- SoT: {SOT_URL}
- Mutual backup LIVE. Live doors: workers-dev, library-runtime, author-runtime, godlock-runtime. HDJ stays the Zioncheck archive.
- Platforms all LIVE (browser/PWA/MCP). native_app_store: false
- Calling name: Aziel Runtime. Identity Aziel Eliab only. Pull /survival; do not hardcode a rotated name.
- Cap-7: resolves_to_hub false. Cite+verify LIVE; hosted /mcp SLOT. public_icann false
- MirageGrid Worker LIVE: {MIRAGE_WORKER} — public pair azgrid+azbooth LIVE HTTPS; azshift (HDJ design) AZNet SLOT
- Zioncheck stays the HDJ mission. Do not invent case facts.
- Person @id: {PERSON_ID}. No visible 15:20.
- Lamb Lens: {LAMB_LENS}
- NO-LIE / NO-REWRITE
- This host: {WWW}/survival · {WWW}/survival.json
- Ingest tip unchanged: `{HDJ_INGEST_TIP}`
"""

WHO_BLOCK = f"""BAN-SURVIVAL-1.0 (machine; hub pull of runtime /survival, short TTL {TTL_SECONDS}s)
This host remains the Marion Zioncheck / He Didn't Jump archive.
SoT: {SOT_URL}
Mutual backup LIVE. Live doors: workers-dev · library-runtime · author-runtime · godlock-runtime.
Platforms all LIVE (browser / PWA / MCP). native_app_store: false.
Calling name: Aziel Runtime. Identity Aziel Eliab only. Person @id: {PERSON_ID}.
Cap-7 Worker LIVE: {MIRAGE_WORKER} — resolves_to_hub: false. Public pair azgrid+azbooth LIVE Worker HTTPS. azshift (HDJ design DNA) AZNet SLOT.
Lamb Lens: {LAMB_LENS} (not this host). NO-LIE / NO-REWRITE. No visible 15:20.
Zioncheck stays the HDJ mission. Do not invent case facts.
Pull: {WWW}/survival · {WWW}/survival.json · {WWW}/v1/survival
"""


def write_survival_json(payload: dict[str, Any]) -> None:
    body = dumps(payload)
    for tree in TREES:
        path = tree / "survival.json"
        path.write_text(body, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


def patch_cite(payload: dict[str, Any]) -> None:
    extra_urls = (
        f"{APEX}/survival",
        f"{APEX}/survival.json",
        f"{APEX}/v1/survival",
        f"{WWW}/survival",
        f"{WWW}/survival.json",
    )
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["ban_survival"] = payload
        data["author"] = "Aziel Eliab"
        data["identity"] = "Aziel Eliab"
        data["person_id"] = PERSON_ID
        data["visible_1520"] = False
        q = list(data.get("query_urls") or [])
        for u in extra_urls:
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
            text = upsert_section(text, "## BAN-SURVIVAL-1.0", LLMS_BLOCK)
            if name == "llms.txt" and f"{APEX}/survival" not in text.split("## Marion")[0]:
                text = text.replace(
                    f"- [{APEX}/runtime-launch.json]({APEX}/runtime-launch.json) — Softwares+runtime launch cite\n",
                    (
                        f"- [{APEX}/runtime-launch.json]({APEX}/runtime-launch.json) — Softwares+runtime launch cite\n"
                        f"- [{APEX}/survival]({APEX}/survival) — BAN-SURVIVAL-1.0 hub pull of runtime /survival (short TTL)\n"
                    ),
                    1,
                )
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("llms", path.relative_to(ROOT))
        ai = tree / "ai.txt"
        text = ai.read_text(encoding="utf-8")
        if "BAN-SURVIVAL-1.0 (hub pull" in text:
            text = re.sub(
                r"\nBAN-SURVIVAL-1.0 \(hub pull[\s\S]*?(?=\nCOLD-MULTI-SHELF|\n## |\nIdentity lock|\Z)",
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
        if f"{WWW}/survival" not in text:
            text = text.replace(
                "- https://www.hedidntjump.com/runtime-launch.json\n",
                (
                    "- https://www.hedidntjump.com/runtime-launch.json\n"
                    "- https://www.hedidntjump.com/survival\n"
                    "- https://www.hedidntjump.com/survival.json\n"
                ),
                1,
            )
        ai.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("ai", ai.relative_to(ROOT))


def patch_who() -> None:
    for tree in TREES:
        for name in ("who-is", "who-is-aziel-eliab.txt"):
            path = tree / name
            text = path.read_text(encoding="utf-8")
            if "BAN-SURVIVAL-1.0 (machine;" in text:
                text = re.sub(
                    r"BAN-SURVIVAL-1.0 \(machine;[\s\S]*",
                    WHO_BLOCK.strip() + "\n",
                    text,
                    count=1,
                )
            else:
                text = text.rstrip() + "\n\n" + WHO_BLOCK.strip() + "\n"
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("who-is", path.relative_to(ROOT))


def patch_well_known(payload: dict[str, Any]) -> None:
    extra = {
        "ban_survival": {
            "spec": payload["spec"],
            "sot": payload["sot"],
            "ttl_seconds": payload["ttl_seconds"],
            "mutual_backup": payload["mutual_backup"],
            "platforms_all_live": payload["platforms"]["all_live"],
            "calling_name": payload["calling_name"]["calling_name"],
            "cap7_resolves_to_hub": payload["cap7_aznet"]["resolves_to_hub"],
            "miragegrid_worker": payload["miragegrid_worker"]["url"],
            "this_host_is_live_door": False,
            "mission": "Zioncheck archive",
            "person_id": PERSON_ID,
            "visible_1520": False,
        }
    }
    for tree in TREES:
        path = tree / ".well-known" / "aziel.json"
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(extra)
        path.write_text(dumps(data), encoding="utf-8")
        print("well-known", path.relative_to(ROOT))


def patch_headers() -> None:
    block = f"""
/survival
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
  CDN-Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300

/survival.json
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
  CDN-Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300

/v1/survival
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
  CDN-Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
"""
    for tree in TREES:
        path = tree / "_headers"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "/survival.json" not in text:
            text = text.rstrip() + "\n" + block
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("headers", path.relative_to(ROOT))


def patch_redirects() -> None:
    lines = (
        "/survival /survival.json 200\n"
        "/v1/survival /survival.json 200\n"
        "/doors /survival.json 200\n"
        "/failover /survival.json 200\n"
    )
    for tree in TREES:
        path = tree / "_redirects"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "/survival /survival.json 200" not in text:
            text = text.rstrip() + "\n" + lines
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("redirects", path.relative_to(ROOT))


def sitemap_entry(loc: str, host: str, priority: str = "0.4") -> str:
    return (
        "  <url>\n"
        f"    <loc>{host}{loc}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        "    <changefreq>hourly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def patch_sitemap() -> None:
    for tree in TREES:
        path = tree / "sitemap.xml"
        text = path.read_text(encoding="utf-8")
        for loc in ("/survival", "/survival.json", "/v1/survival"):
            if f"{APEX}{loc}</loc>" not in text:
                text = text.replace(
                    "</urlset>",
                    sitemap_entry(loc, APEX, "0.4") + "</urlset>",
                    1,
                )
        path.write_text(text, encoding="utf-8")
        print("sitemap", path.relative_to(ROOT))


def patch_openapi() -> None:
    paths = {
        "/survival": {
            "get": {
                "summary": (
                    "BAN-SURVIVAL-1.0 hub pull of runtime /survival "
                    f"(short TTL {TTL_SECONDS}s; Zioncheck archive hub pull)"
                ),
                "responses": {"200": {"description": "application/json"}},
            }
        },
        "/survival.json": {
            "get": {
                "summary": "Same BAN-SURVIVAL-1.0 hub wrap as /survival (static snapshot)",
                "responses": {"200": {"description": "application/json"}},
            }
        },
        "/v1/survival": {
            "get": {
                "summary": "Alias of /survival",
                "responses": {"200": {"description": "application/json"}},
            }
        },
    }
    for tree in TREES:
        path = tree / "openapi.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("paths", {}).update(paths)
        path.write_text(dumps(data), encoding="utf-8")
        print("openapi", path.relative_to(ROOT))


def patch_robots() -> None:
    for tree in TREES:
        path = tree / "robots.txt"
        text = path.read_text(encoding="utf-8")
        if "Allow: /survival" not in text:
            text = text.replace(
                "Allow: /runtime-launch.json\n",
                "Allow: /runtime-launch.json\nAllow: /survival\nAllow: /survival.json\n",
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("robots", path.relative_to(ROOT))


def patch_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    line = (
        "BAN-SURVIVAL-1.0 hub pull: `/survival` (short TTL) cites runtime "
        f"`GET {SOT_URL}` — mutual backup, live doors, platforms all LIVE, "
        "calling name Aziel Runtime, Cap-7 `resolves_to_hub: false`. "
        f"MirageGrid Cap-7 Worker LIVE `{MIRAGE_WORKER}`. "
        "HDJ stays the Zioncheck archive.\n"
    )
    text = text.replace(
        "HDJ stays the Zioncheck archive; not a live exec door.",
        "HDJ stays the Zioncheck archive.",
    )
    text = text.replace("Sister cite (not a Softwares clone):", "Sister cite:")
    marker = "Sister cite:"
    if "BAN-SURVIVAL-1.0 hub pull" not in text:
        text = text.replace(marker, line + "\n" + marker, 1)
    path.write_text(text, encoding="utf-8")
    print("readme", path.relative_to(ROOT))


def main() -> None:
    payload = survival_cite()
    assert payload["person_id"] == PERSON_ID
    assert payload["mutual_backup"] is True
    assert payload["platforms"]["all_live"] is True
    assert payload["cap7_aznet"]["resolves_to_hub"] is False
    assert payload["this_host_is_live_door"] is False
    assert payload["mission"] == "Zioncheck archive"
    write_survival_json(payload)
    patch_cite(payload)
    patch_llms()
    patch_who()
    patch_well_known(payload)
    patch_headers()
    patch_redirects()
    patch_sitemap()
    patch_openapi()
    patch_robots()
    patch_readme()
    print("ban-survival hub pull written; ingest tip unchanged; no Softwares clone")


if __name__ == "__main__":
    main()
