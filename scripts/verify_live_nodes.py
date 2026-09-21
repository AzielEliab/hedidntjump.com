#!/usr/bin/env python3
"""Assert HDJ Live Nodes hub cite stays human-only and archive-focused."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from write_live_nodes import (  # noqa: E402
    APEX,
    HDJ_INGEST_TIP,
    HUMAN_USES_NOTE,
    LAMB_LENS,
    LIVE_NODES_NOTE,
    LIVE_NODES_PLANE,
    PERSON_ID,
    RUNTIME_PR,
    SOFTWARE_NODES_NOTE,
    SOT_URL,
    TTL_SECONDS,
    WWW,
    hub_wrap,
    is_human_live_nodes_plane,
)

PAPER_HTML = (
    "index.html",
    "case.html",
    "press.html",
    "inquiries.html",
    "inquires.html",
    "rubye.html",
    "archives.html",
    "foia.html",
    "volumes.html",
    "reader.html",
    "official-narrative.html",
    "copyrights.html",
    "aziel.html",
    "receipts.html",
    "who.html",
)


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return html


def check_wrap(payload: dict, label: str) -> None:
    assert payload["spec"] == "LIVE-NODES-HUB-CITE-1.0", label
    assert payload["author"] == "Aziel Eliab", label
    assert payload["identity"] == "Aziel Eliab", label
    assert payload["person_id"] == PERSON_ID, label
    assert payload["visible_1520"] is False, label
    assert payload["softwares_clone"] is False, label
    assert payload["softwares_tab"] is False, label
    assert payload["this_host_is_live_door"] is False, label
    assert payload["this_host_runtime_front"] is False, label
    assert payload["mission"] == "Zioncheck archive", label
    assert payload["invented_users"] is False, label
    assert payload["invent_users"] is False, label
    assert payload["software_nodes_excluded"] is True, label
    assert payload["instance_nodes_excluded"] is True, label
    assert payload["ttl_seconds"] == TTL_SECONDS, label
    assert payload["sot"] == SOT_URL, label
    assert payload["runtime_pr"] == RUNTIME_PR, label
    assert payload["live_nodes_plane"] == LIVE_NODES_PLANE, label
    assert payload["no_lie"].startswith("NO-LIE"), label
    assert payload["lamb_lens"]["shelf"] == LAMB_LENS, label
    assert payload["live_nodes_note"] == LIVE_NODES_NOTE, label
    assert payload["software_nodes_note"] == SOFTWARE_NODES_NOTE, label
    assert "never feed" in payload["software_nodes_note"], label
    assert HUMAN_USES_NOTE.split(".")[0] in payload["human_uses_note"], label
    comps = payload["live_nodes_components"]
    assert comps["software_nodes_excluded"] is True, label
    assert comps["invent_users"] is False, label
    if payload["live_nodes_complete"] is False:
        assert payload["live_nodes"] == 0, label
        assert payload["worker_human_plane"] is False, label
        assert payload["software_nodes"] != payload["live_nodes"] or payload["software_nodes"] == 0, label
    else:
        assert payload["worker_human_plane"] is True, label
        expected = payload["human_mesh_users"] + payload["human_uses"]
        assert payload["live_nodes"] == expected, (
            f"{label} live_nodes {payload['live_nodes']} != users+uses {expected}"
        )
        assert payload["live_nodes"] != payload["software_nodes"] or payload["software_nodes"] == 0, (
            f"{label} must not treat software_nodes as live_nodes"
        )


def main() -> None:
    ingest_expected = (ROOT / "docs" / "ingest-as-receipt.json").read_bytes()
    assert hashlib.sha256(ingest_expected).hexdigest() == HDJ_INGEST_TIP

    stale = {
        "live_nodes": 41,
        "software_nodes": 41,
        "note": "legacy mesh size",
    }
    stale_wrap = hub_wrap(stale, pulled=True)
    assert is_human_live_nodes_plane(stale) is False
    assert stale_wrap["live_nodes"] == 0
    assert stale_wrap["live_nodes_complete"] is False
    assert stale_wrap["software_nodes"] == 41
    assert stale_wrap["worker_live_nodes_legacy"] == 41
    assert stale_wrap["human_uses_source"] == "worker-legacy-plane-refused"

    human = {
        "live_nodes_plane": LIVE_NODES_PLANE,
        "live_nodes": 7,
        "human_mesh_users": 2,
        "human_uses": 5,
        "human_uses_complete": True,
        "human_uses_kv": True,
        "human_uses_source": "uses.total",
        "software_nodes": 41,
        "live_nodes_components": {"software_nodes_excluded": True},
    }
    human_wrap = hub_wrap(human, pulled=True)
    assert human_wrap["live_nodes"] == 7
    assert human_wrap["live_nodes_complete"] is True
    assert human_wrap["software_nodes"] == 41
    assert human_wrap["software_nodes"] != human_wrap["live_nodes"]

    pull = (ROOT / "functions" / "_lib" / "mesh-pull.js").read_text(encoding="utf-8")
    assert SOT_URL in pull
    assert PERSON_ID in pull
    assert LIVE_NODES_PLANE in pull
    assert "software_nodes_excluded" in pull
    assert "worker-legacy-plane-refused" in pull
    assert "Mozilla/5.0" in pull
    assert (ROOT / "functions" / "mesh.js").is_file()
    assert (ROOT / "functions" / "v1" / "mesh.js").is_file()

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        raw = (tree / "mesh.json").read_text(encoding="utf-8")
        payload = json.loads(raw)
        check_wrap(payload, f"{tree_name}/mesh.json")
        assert payload["ingest_tip_unchanged"] == HDJ_INGEST_TIP

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        check_wrap(cite["live_nodes"], f"{tree_name}/cite.live_nodes")
        assert cite["identity"] == "Aziel Eliab"
        assert cite["author"] == "Aziel Eliab"
        assert cite["visible_1520"] is False
        assert cite["softwares_clone"] is False
        for u in (f"{APEX}/mesh", f"{APEX}/mesh.json", f"{WWW}/mesh"):
            assert u in cite["query_urls"], u
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        assert "never_" not in cite
        assert '"":' not in json.dumps(cite)

        launch = json.loads((tree / "runtime-launch.json").read_text(encoding="utf-8"))
        ln = launch["live_nodes"]
        assert ln["sot"] == SOT_URL
        assert ln["plane"] == LIVE_NODES_PLANE
        assert ln["software_nodes_excluded"] is True
        assert ln["invent_users"] is False
        assert ln["runtime_pr"] == RUNTIME_PR
        assert ln["hub"] == f"{APEX}/mesh"
        assert "human mesh users" in ln["counts"]

        llms = (tree / "llms.txt").read_text(encoding="utf-8")
        llms_full = (tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (tree / "ai.txt").read_text(encoding="utf-8")
        who = (tree / "who-is-aziel-eliab.txt").read_text(encoding="utf-8")
        who_alias = (tree / "who-is").read_text(encoding="utf-8")
        for blob, label in (
            (llms, "llms"),
            (llms_full, "llms-full"),
            (ai, "ai"),
            (who, "who-is"),
            (who_alias, "who-is-alias"),
        ):
            assert "LIVE-NODES-HUB-CITE-1.0" in blob, label
            assert SOT_URL in blob, label
            assert RUNTIME_PR in blob, label
            assert "human mesh users" in blob, label
            assert "Softwares ≠ Live Nodes" in blob or "Softwares stay on software_nodes" in blob or "never feeds Live Nodes" in blob, label
            assert "Do not invent users" in blob or "does not invent users" in blob, label
            assert PERSON_ID in blob, label
            assert "NO-LIE" in blob, label
            assert "Zioncheck" in blob, label
            assert "Not a Softwares clone" not in blob, label

        lead = llms.split("## Marion")[0]
        assert f"{APEX}/mesh" in lead

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "/mesh" in openapi["paths"]
        assert "/mesh.json" in openapi["paths"]
        assert "/v1/mesh" in openapi["paths"]
        assert "human mesh users + uses" in openapi["paths"]["/mesh"]["get"]["summary"]
        assert "not a live exec door" not in openapi["paths"]["/mesh"]["get"]["summary"]

        headers = (tree / "_headers").read_text(encoding="utf-8")
        assert "/mesh.json" in headers
        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/mesh /mesh.json 200" in redirects
        assert "/v1/mesh /mesh.json 200" in redirects
        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"{APEX}/mesh</loc>" in sitemap
        assert f"{APEX}/mesh.json</loc>" in sitemap
        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Allow: /mesh" in robots
        assert "Allow: /mesh.json" in robots

        wk = json.loads((tree / ".well-known" / "aziel.json").read_text(encoding="utf-8"))
        assert wk["live_nodes"]["spec"] == "LIVE-NODES-HUB-CITE-1.0"
        assert wk["live_nodes"]["sot"] == SOT_URL
        assert wk["live_nodes"]["plane"] == LIVE_NODES_PLANE
        assert wk["live_nodes"]["software_nodes_excluded"] is True
        assert wk["live_nodes"]["invent_users"] is False
        assert wk["live_nodes"]["this_host_is_live_door"] is False
        assert wk["live_nodes"]["mission"] == "Zioncheck archive"
        assert wk["live_nodes"]["person_id"] == PERSON_ID

        for name in PAPER_HTML:
            html = (tree / name).read_text(encoding="utf-8")
            nav = re.search(r'<nav class="paper-tabs"[\s\S]*?</nav>', html)
            if nav:
                assert "Softwares" not in nav.group(0), f"{tree_name}/{name} paper-tabs gained Softwares"
            if name != "who.html":
                visible = visible_text(html)
                assert "15:20" not in visible, f"{tree_name}/{name} gained visible 15:20"
            assert "fielded_100" not in html

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "LIVE-NODES-HUB-CITE-1.0" in readme
    assert SOT_URL in readme
    assert "human mesh users" in readme
    assert "software_nodes" in readme

    print("live-nodes hub cite OK")
    print("sot", SOT_URL)
    print("plane", LIVE_NODES_PLANE)
    print("pr", RUNTIME_PR)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print("FAIL", exc, file=sys.stderr)
        raise
