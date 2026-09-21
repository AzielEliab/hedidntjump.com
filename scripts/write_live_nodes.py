#!/usr/bin/env python3
"""Cite Live Nodes from Worker GET /v1/mesh onto HDJ machine surfaces.

Live Nodes = human mesh users + cited human uses. Softwares ≠ Live Nodes.
software_nodes is the {slug}-worker roster and never feeds the pill.
HDJ stays the Zioncheck archive. Short-TTL hub pull; do not invent users.
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
LASTMOD = "2026-09-21"
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"
TTL_SECONDS = 60
SOT_URL = "https://aziel-runtime.vibelock.workers.dev/v1/mesh"
RUNTIME_PR = "https://github.com/AzielEliab/aziel-runtime/pull/151"
RUNTIME_GIT_SHA = "31ccb56b6c01647f434a9981c9843602c5967899"
RUNTIME_GIT_SHORT = "31ccb56"
RUNTIME_VERSION_ID = "d7b63ac1"
LAMB_LENS = "https://www.azielcorpuslibrary.net/corpus"
UA = "Mozilla/5.0"

LIVE_NODES_PLANE = "human-mesh-users-uses"
SOFTWARE_NODES_PLANE = "software-worker-fanout"
LIVE_NODES_NOTE = (
    "Public Live Nodes (live_nodes / rollup.mesh) count human mesh users "
    "(join/heartbeat/presence with human bearers) plus the cited human uses "
    "signal (USES / human_uses). Isolated humans stay on isolated_nodes. "
    "Not Softwares catalog length. Not downloaded Softwares instances. "
    "Not software_nodes. software_nodes is the {slug}-worker roster and never "
    "feeds this pill. Uses are interaction counters, not unique people — "
    "incomplete or unbound telemetry is reported honestly (0 + complete=false). "
    "Live Nodes does not invent users. Zero is honest when no humans are "
    "present and uses are 0/unbound."
)
SOFTWARE_NODES_NOTE = (
    "software_nodes / rollup.software count Softwares product Workers "
    "({slug}-worker) from suite-presence fan-out. They may appear in the mesh "
    "roster. They must never feed public Live Nodes."
)
HUMAN_NODES_NOTE = (
    "human_nodes / rollup.human count humans who exist as mesh users "
    "(join/heartbeat/presence — human bearers or kind=human). Auto-minted "
    "mesh_* joins are human participants. Named downloaded Softwares instance "
    "ids stay instance_nodes."
)
HUMAN_USES_NOTE = (
    "human_uses is the USES interaction counter (no PII), not a unique-user "
    "count. Incomplete or unbound telemetry is reported as 0 with "
    "complete=false. Live Nodes does not invent users from missing uses."
)


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
    except Exception as exc:  # noqa: BLE001 — writer falls back to locked cite
        print("fetch miss", url, type(exc).__name__, exc)
        return None


def is_human_live_nodes_plane(sot: dict[str, Any] | None) -> bool:
    if not sot:
        return False
    if sot.get("live_nodes_plane") == LIVE_NODES_PLANE:
        return True
    components = sot.get("live_nodes_components") or {}
    if components.get("software_nodes_excluded") is True:
        return True
    return isinstance(sot.get("human_uses"), (int, float)) and isinstance(
        sot.get("human_mesh_users"), (int, float)
    )


def as_count(value: Any) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        return 0
    return n if n >= 0 else 0


def hub_wrap(sot: dict[str, Any] | None, *, pulled: bool) -> dict[str, Any]:
    human_plane = is_human_live_nodes_plane(sot)
    software_nodes = as_count((sot or {}).get("software_nodes"))
    worker_live = as_count((sot or {}).get("live_nodes")) if sot else 0
    live_nodes = worker_live if human_plane else 0
    human_mesh_users = as_count((sot or {}).get("human_mesh_users")) if human_plane else 0
    human_uses = as_count((sot or {}).get("human_uses")) if human_plane else 0
    human_uses_complete = human_plane and (sot or {}).get("human_uses_complete") is True
    return {
        "spec": "LIVE-NODES-HUB-CITE-1.0",
        "surface": "hedidntjump-hub-pull",
        "this_host": "hedidntjump.com",
        "this_host_role": "Marion Zioncheck archive — sister cite",
        "this_host_is_live_door": False,
        "this_host_runtime_front": False,
        "softwares_clone": False,
        "softwares_tab": False,
        "mission": "Zioncheck archive",
        "invented_users": False,
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
            "https://aziel-runtime.vibelock.workers.dev/mesh",
            "https://aziel-runtime.vibelock.workers.dev/v1/mesh",
        ],
        "sot_pulled": pulled,
        "runtime_pr": RUNTIME_PR,
        "runtime_git_sha": RUNTIME_GIT_SHA,
        "runtime_git_short": RUNTIME_GIT_SHORT,
        "runtime_version_id": RUNTIME_VERSION_ID,
        "live_nodes_plane": LIVE_NODES_PLANE,
        "software_nodes_plane": SOFTWARE_NODES_PLANE,
        "live_nodes": live_nodes,
        "live_nodes_complete": human_plane,
        "human_mesh_users": human_mesh_users,
        "human_uses": human_uses,
        "human_uses_complete": human_uses_complete,
        "human_uses_kv": human_plane and (sot or {}).get("human_uses_kv") is True,
        "human_uses_source": (
            (sot or {}).get("human_uses_source") or "uses.total"
            if human_plane
            else "worker-legacy-plane-refused"
        ),
        "software_nodes": software_nodes,
        "software_nodes_excluded": True,
        "instance_nodes_excluded": True,
        "invent_users": False,
        "worker_human_plane": human_plane,
        "worker_live_nodes_plane": (sot or {}).get("live_nodes_plane") or "legacy-mesh-size",
        "worker_live_nodes_legacy": 0 if human_plane else worker_live,
        "live_nodes_note": LIVE_NODES_NOTE,
        "software_nodes_note": SOFTWARE_NODES_NOTE,
        "human_nodes_note": HUMAN_NODES_NOTE,
        "human_uses_note": (sot or {}).get("human_uses_note") or HUMAN_USES_NOTE,
        "live_nodes_components": {
            "human_mesh_users": human_mesh_users,
            "human_uses": human_uses,
            "software_nodes_excluded": True,
            "instance_nodes_excluded": True,
            "invent_users": False,
        },
        "ingest_tip_unchanged": HDJ_INGEST_TIP,
        "note": (
            "Hub pull of runtime GET /v1/mesh (short TTL). Live Nodes = human mesh users + cited human uses. Softwares stay on software_nodes and do not feed this pill. Zioncheck stays the HDJ mission."
            if human_plane
            else (
                "Hub pull of runtime GET /v1/mesh (short TTL). Worker still reports the "
                "legacy mesh-size plane (Softwares roster). HDJ does not display that "
                "roster as Live Nodes. live_nodes stays 0 + complete=false until the "
                "Worker human-mesh-users-uses plane is live. Zioncheck stays the HDJ mission."
            )
        ),
    }


def mesh_cite() -> dict[str, Any]:
    live = fetch_json(SOT_URL)
    return hub_wrap(live, pulled=live is not None)


def upsert_section(text: str, heading: str, block: str) -> str:
    if heading in text:
        return re.sub(
            rf"{re.escape(heading)}\n[\s\S]*?(?=\n## |\Z)",
            block.rstrip() + "\n\n",
            text,
            count=1,
        )
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


LLMS_BLOCK = f"""## LIVE-NODES-HUB-CITE-1.0

Hub pull of Aziel Runtime `GET /v1/mesh` (short TTL {TTL_SECONDS}s). HDJ stays the Marion Zioncheck archive.

SoT: {SOT_URL}
Runtime lock: {RUNTIME_PR} (main `{RUNTIME_GIT_SHORT}` / Worker `{RUNTIME_VERSION_ID}`)
Public **Live Nodes** (`live_nodes` / `rollup.mesh`) = **human mesh users** (join/heartbeat/presence with human bearers) + cited **human uses** (`USES` / `human_uses`).
`software_nodes` is the Softwares `{{slug}}-worker` roster. Softwares ≠ Live Nodes. Downloaded instances stay `instance_nodes`. Isolated humans stay on `isolated_nodes`.
Uses are interaction counters, not unique people. Incomplete or unbound telemetry is `0` + `complete=false`. Live Nodes does not invent users.
Read `live_nodes` + `live_nodes_note`. Do not display `software_nodes` as Live Nodes.
Person @id: {PERSON_ID}. Lamb Lens ingest: {LAMB_LENS}. NO-LIE / NO-REWRITE. No visible 1 Chronicles 15:20.
Zioncheck stays the HDJ mission.
HDJ ingest tip unchanged: `{HDJ_INGEST_TIP}`
This host: {APEX}/mesh · {APEX}/mesh.json · {APEX}/v1/mesh
"""

AI_BLOCK = f"""LIVE-NODES-HUB-CITE-1.0 (hub pull; short TTL {TTL_SECONDS}s):
- SoT: {SOT_URL}
- Runtime lock: {RUNTIME_PR} (main {RUNTIME_GIT_SHORT} / Worker {RUNTIME_VERSION_ID})
- Live Nodes = human mesh users + cited human uses. Softwares ≠ Live Nodes.
- software_nodes is the {{slug}}-worker roster and never feeds Live Nodes.
- Uses are counters, not unique people. Incomplete uses stay 0 + complete=false. Do not invent users.
- Read live_nodes + live_nodes_note. Do not display software_nodes as Live Nodes.
- Zioncheck stays the HDJ mission.
- Person @id: {PERSON_ID}. No visible 15:20.
- Lamb Lens: {LAMB_LENS}
- NO-LIE / NO-REWRITE
- This host: {WWW}/mesh · {WWW}/mesh.json
- Ingest tip unchanged: `{HDJ_INGEST_TIP}`
"""

WHO_BLOCK = f"""LIVE-NODES-HUB-CITE-1.0 (machine; hub pull of runtime /v1/mesh, short TTL {TTL_SECONDS}s)
This host remains the Marion Zioncheck / He Didn't Jump archive.
SoT: {SOT_URL}
Runtime lock: {RUNTIME_PR} (main {RUNTIME_GIT_SHORT} / Worker {RUNTIME_VERSION_ID})
Live Nodes = human mesh users + cited human uses. Softwares ≠ Live Nodes.
software_nodes is the Softwares {{slug}}-worker roster and never feeds Live Nodes.
Uses are interaction counters, not unique people. Incomplete uses stay 0 + complete=false. Do not invent users.
Identity Aziel Eliab only. Person @id: {PERSON_ID}.
Lamb Lens: {LAMB_LENS}. NO-LIE / NO-REWRITE. No visible 15:20.
Zioncheck stays the HDJ mission.
Pull: {WWW}/mesh · {WWW}/mesh.json · {WWW}/v1/mesh
"""


def write_mesh_json(payload: dict[str, Any]) -> None:
    body = dumps(payload)
    for tree in TREES:
        path = tree / "mesh.json"
        path.write_text(body, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


def patch_cite(payload: dict[str, Any]) -> None:
    extra_urls = (
        f"{APEX}/mesh",
        f"{APEX}/mesh.json",
        f"{APEX}/v1/mesh",
        f"{WWW}/mesh",
        f"{WWW}/mesh.json",
    )
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["live_nodes"] = payload
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
            if "## LIVE-NODES-HUB-CITE-1.0" in text:
                text = upsert_section(text, "## LIVE-NODES-HUB-CITE-1.0", LLMS_BLOCK)
            elif "## BAN-SURVIVAL-1.0" in text:
                text = text.replace(
                    "## BAN-SURVIVAL-1.0",
                    LLMS_BLOCK.rstrip() + "\n\n## BAN-SURVIVAL-1.0",
                    1,
                )
            else:
                text = upsert_section(text, "## LIVE-NODES-HUB-CITE-1.0", LLMS_BLOCK)
            if name == "llms.txt" and f"{APEX}/mesh" not in text.split("## Marion")[0]:
                text = text.replace(
                    f"- [{APEX}/survival]({APEX}/survival) — BAN-SURVIVAL-1.0 hub pull of runtime /survival (short TTL)\n",
                    (
                        f"- [{APEX}/survival]({APEX}/survival) — BAN-SURVIVAL-1.0 hub pull of runtime /survival (short TTL)\n"
                        f"- [{APEX}/mesh]({APEX}/mesh) — LIVE-NODES-HUB-CITE-1.0 hub pull of runtime /v1/mesh (human users + uses)\n"
                    ),
                    1,
                )
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("llms", path.relative_to(ROOT))
        ai = tree / "ai.txt"
        text = ai.read_text(encoding="utf-8")
        if "LIVE-NODES-HUB-CITE-1.0 (hub pull" in text:
            text = re.sub(
                r"\n+LIVE-NODES-HUB-CITE-1.0 \(hub pull[\s\S]*?(?=\nBAN-SURVIVAL|\nCOLD-MULTI-SHELF|\n## |\nIdentity lock|\Z)",
                "\n",
                text,
                count=1,
            )
        if "BAN-SURVIVAL-1.0 (hub pull" in text:
            text = text.replace(
                "BAN-SURVIVAL-1.0 (hub pull",
                AI_BLOCK.strip() + "\n\nBAN-SURVIVAL-1.0 (hub pull",
                1,
            )
        else:
            text = text.rstrip() + "\n\n" + AI_BLOCK
        if f"{WWW}/mesh" not in text:
            text = text.replace(
                "- https://www.hedidntjump.com/survival\n",
                (
                    "- https://www.hedidntjump.com/survival\n"
                    "- https://www.hedidntjump.com/mesh\n"
                    "- https://www.hedidntjump.com/mesh.json\n"
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
            if "LIVE-NODES-HUB-CITE-1.0 (machine;" in text:
                text = re.sub(
                    r"LIVE-NODES-HUB-CITE-1.0 \(machine;[\s\S]*?(?=\nBAN-SURVIVAL|\Z)",
                    WHO_BLOCK.strip() + "\n\n",
                    text,
                    count=1,
                )
            elif "BAN-SURVIVAL-1.0 (machine;" in text:
                text = text.replace(
                    "BAN-SURVIVAL-1.0 (machine;",
                    WHO_BLOCK.strip() + "\n\nBAN-SURVIVAL-1.0 (machine;",
                    1,
                )
            else:
                text = text.rstrip() + "\n\n" + WHO_BLOCK.strip() + "\n"
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
            print("who-is", path.relative_to(ROOT))


def patch_well_known(payload: dict[str, Any]) -> None:
    extra = {
        "live_nodes": {
            "spec": payload["spec"],
            "sot": payload["sot"],
            "ttl_seconds": payload["ttl_seconds"],
            "plane": payload["live_nodes_plane"],
            "runtime_version_id": payload["runtime_version_id"],
            "software_nodes_excluded": True,
            "invent_users": False,
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
/mesh
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
  CDN-Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300

/mesh.json
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
  CDN-Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300

/v1/mesh
  Content-Type: application/json; charset=utf-8
  Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
  CDN-Cache-Control: public, max-age={TTL_SECONDS}, stale-while-revalidate=300
"""
    for tree in TREES:
        path = tree / "_headers"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "/mesh.json" not in text:
            text = text.rstrip() + "\n" + block
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("headers", path.relative_to(ROOT))


def patch_redirects() -> None:
    lines = (
        "/mesh /mesh.json 200\n"
        "/v1/mesh /mesh.json 200\n"
        "/live-nodes /mesh.json 200\n"
    )
    for tree in TREES:
        path = tree / "_redirects"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "/mesh /mesh.json 200" not in text:
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
        for loc in ("/mesh", "/mesh.json", "/v1/mesh"):
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
        "/mesh": {
            "get": {
                "summary": (
                    "LIVE-NODES-HUB-CITE-1.0 hub pull of runtime /v1/mesh "
                    f"(short TTL {TTL_SECONDS}s; human mesh users + uses)"
                ),
                "responses": {"200": {"description": "application/json"}},
            }
        },
        "/mesh.json": {
            "get": {
                "summary": "Same LIVE-NODES-HUB-CITE-1.0 hub wrap as /mesh (static snapshot)",
                "responses": {"200": {"description": "application/json"}},
            }
        },
        "/v1/mesh": {
            "get": {
                "summary": "Alias of /mesh",
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
        if "Allow: /mesh" not in text:
            text = text.replace(
                "Allow: /survival.json\n",
                "Allow: /survival.json\nAllow: /mesh\nAllow: /mesh.json\n",
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        print("robots", path.relative_to(ROOT))


def patch_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    line = (
        "LIVE-NODES-HUB-CITE-1.0 hub pull: `/mesh` (short TTL) cites runtime "
        f"`GET {SOT_URL}` — Live Nodes = human mesh users + cited human uses. "
        "Softwares (`software_nodes`) never feed that pill. "
        f"Runtime lock {RUNTIME_PR} (main `{RUNTIME_GIT_SHORT}` / Worker `{RUNTIME_VERSION_ID}`). "
        "HDJ stays the Zioncheck archive.\n"
    )
    marker = "Sister cite:"
    if "LIVE-NODES-HUB-CITE-1.0 hub pull" in text:
        text = re.sub(
            r"LIVE-NODES-HUB-CITE-1.0 hub pull:[\s\S]*?(?=\nSister cite:)",
            line + "\n",
            text,
            count=1,
        )
    else:
        text = text.replace(marker, line + "\n" + marker, 1)
    path.write_text(text, encoding="utf-8")
    print("readme", path.relative_to(ROOT))


def main() -> None:
    payload = mesh_cite()
    assert payload["person_id"] == PERSON_ID
    assert payload["live_nodes_plane"] == LIVE_NODES_PLANE
    assert payload["software_nodes_excluded"] is True
    assert payload["invent_users"] is False
    assert payload["this_host_is_live_door"] is False
    assert payload["mission"] == "Zioncheck archive"
    if not payload["live_nodes_complete"]:
        assert payload["live_nodes"] == 0
        assert payload["software_nodes"] != payload["live_nodes"] or payload["software_nodes"] == 0
    write_mesh_json(payload)
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
    print("live-nodes hub pull written; ingest tip unchanged; Softwares excluded")


if __name__ == "__main__":
    main()
