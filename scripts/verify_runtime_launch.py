#!/usr/bin/env python3
"""Assert HDJ Softwares+runtime launch cite stays honest and archive-focused."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from write_runtime_launch import (
    APEX,
    GIT_SHA,
    GIT_SHORT,
    HDJ_INGEST_TIP,
    PAGES_PREVIEW,
    PAGES_PROJECT,
    PERSON_ID,
    RUNTIME_DOWNLOAD,
    RUNTIME_GLAMA,
    RUNTIME_GITHUB,
    RUNTIME_MESH,
    RUNTIME_SOFTWARE,
    RUNTIME_WORKER,
    VERSION,
    VERSION_ID,
    WWW,
    dumps,
    launch_cite,
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

FORGED = (
    "https://framagit.org/AzielEliab/aziel-lockset-tip",
    ": true",
    '"": true',
    "Pg. 11",
    "Pg.11",
)


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return html


def walk_bools(obj, path=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from walk_bools(value, f"{path}.{key}" if path else key)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            yield from walk_bools(value, f"{path}[{i}]")
    else:
        yield path, obj


def main() -> None:
    expected = dumps(launch_cite())
    ingest_expected = (ROOT / "docs" / "ingest-as-receipt.json").read_bytes()
    assert hashlib.sha256(ingest_expected).hexdigest() == HDJ_INGEST_TIP

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        raw = (tree / "runtime-launch.json").read_bytes()
        assert raw.decode("utf-8") == expected, f"{tree_name}/runtime-launch.json drifted"
        launch = json.loads(raw)
        assert launch["spec"] == "SOFTWARES-RUNTIME-LAUNCH-1.0"
        assert launch["author"] == "Aziel Eliab"
        assert launch["identity"] == "Aziel Eliab"
        assert launch["person_id"] == PERSON_ID
        assert launch["softwares_clone"] is False
        assert launch["softwares_tab"] is False
        assert launch["visible_1520"] is False
        assert launch["lamb_lens"]["shelf"] == "https://www.azielcorpuslibrary.net/corpus"
        assert "azielcorpuslibrary.net" in launch["lamb_lens"]["note"]
        assert "not a Lamb Lens ingest host" not in launch["lamb_lens"]["note"]
        assert launch["no_lie"] == "NO-LIE / NO-REWRITE"
        sot = launch["runtime_sot"]
        assert sot["status"] == "LIVE"
        assert sot["version"] == VERSION
        assert sot["git_sha"] == GIT_SHA
        assert sot["git_short"] == GIT_SHORT
        assert sot["version_id"] == VERSION_ID
        assert sot["github"] == RUNTIME_GITHUB
        assert sot["worker"] == RUNTIME_WORKER
        assert sot["glama"] == RUNTIME_GLAMA
        assert sot["software"] == RUNTIME_SOFTWARE
        assert sot["download"] == RUNTIME_DOWNLOAD
        assert sot["mesh"] == RUNTIME_MESH
        ready = launch["readiness"]
        assert ready["human_ui"] is True
        assert ready["mcp"] is True
        assert ready["mesh"] is True
        assert ready["vpn"] is True
        assert ready["radios"] == "on"
        assert ready["download"] is True
        assert "does not host" in ready["note"]
        hdj = launch["hdj"]
        assert hdj["live_origin"] == "cloudflare-pages"
        assert hdj["pages_project"] == PAGES_PROJECT
        assert hdj["pages_preview"] == PAGES_PREVIEW
        assert hdj["deploy_root"] == "docs/"
        assert hdj["github_pages"] == "secondary-not-alone"
        assert "Aziel-page-only" in hdj["receipts_chrome"]
        assert "Pg.11" in hdj["receipts_chrome"]
        shelves = launch["shelves_honesty"]
        assert shelves["plane_b_framagit"] == "SLOT"
        assert shelves["plane_b_framagit_refuse"] == "CNS-NO-FORGE-MIRROR"
        assert shelves["plane_b_framagit_url"] is None
        assert shelves["plane_b_codeberg"] == "pass"
        assert shelves["plane_b_archive_org"] == "pass"
        assert shelves["plane_b_live"] is False
        assert shelves["plane_c"] == "SLOT"
        assert shelves["no_live_invent"] is True
        assert launch["ingest_tip_unchanged"] == HDJ_INGEST_TIP

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        assert cite["runtime_launch"]["runtime_sot"]["version_id"] == VERSION_ID
        assert cite["runtime_launch"]["runtime_sot"]["git_short"] == GIT_SHORT
        assert cite["runtime_sot"]["version_id"] == VERSION_ID
        assert cite["softwares_clone"] is False
        assert cite["live_origin"]["kind"] == "cloudflare-pages"
        assert cite["live_origin"]["project"] == PAGES_PROJECT
        assert cite["live_origin"]["deploy_root"] == "docs/"
        assert cite["identity"] == "Aziel Eliab"
        assert cite["author"] == "Aziel Eliab"
        assert cite["runtime_glama"] == RUNTIME_GLAMA
        assert cite["mcp_local"] is False
        assert f"{APEX}/runtime-launch.json" in cite["query_urls"]
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP
        assert cite["ingest_as_receipt"]["chrome"].startswith("Aziel-page-only")
        assert cite["visible_1520"] is False
        assert cite["softwares_tab"] is False
        planes = cite["planes"]
        assert planes["B"]["live_ready"] is False
        assert planes["B"]["status"] == "slot"
        assert planes["B"]["framagit_tip_pack"]["url"] is None
        assert planes["B"]["framagit_tip_pack"]["refuse"] == "CNS-NO-FORGE-MIRROR"
        assert planes["B"]["codeberg_tip_pack"]["hash_verify"] == "pass"
        assert planes["B"]["archive_org_tip_pack"]["hash_verify"] == "pass"
        assert planes["C"]["status"] == "slot"

        for path, value in walk_bools(cite):
            if path == "" or path.endswith("."):
                assert value is False, f"{tree_name} cite {path or '\"\"'} must be false"

        ingest = (tree / "ingest-as-receipt.json").read_bytes()
        assert hashlib.sha256(ingest).hexdigest() == HDJ_INGEST_TIP, f"{tree_name} ingest tip drifted"

        llms = (tree / "llms.txt").read_text(encoding="utf-8")
        llms_full = (tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (tree / "ai.txt").read_text(encoding="utf-8")
        for blob, label in ((llms, "llms"), (llms_full, "llms-full"), (ai, "ai")):
            assert "SOFTWARES-RUNTIME-LAUNCH-1.0" in blob, label
            assert GIT_SHORT in blob, label
            assert VERSION_ID in blob, label
            assert VERSION in blob, label
            assert RUNTIME_GLAMA in blob, label
            assert RUNTIME_GITHUB in blob, label
            assert "Try on Glama" in blob or RUNTIME_GLAMA in blob, label
            assert "never " in blob.lower() or "Never " in blob, label
            assert "Cloudflare Pages" in blob, label
            assert PAGES_PROJECT in blob, label
            assert "Marion Zioncheck" in blob or "Zioncheck" in blob, label
            assert "Not a Softwares clone" not in blob, label
            assert "Aziel-page-only" in blob or "Aziel-page-only" in blob, label
            assert "CNS-NO-FORGE-MIRROR" in blob, label
            assert "Plane C SLOT" in blob or "plane C SLOT" in blob.lower() or "Plane C: USB" in blob, label
            assert PERSON_ID in blob, label
            assert "Aziel Eliab only" in blob, label
            assert "NO-LIE" in blob, label
            assert "Lamb Lens" in blob, label
            for forged in FORGED:
                if forged in ("Pg. 11", "Pg.11"):
                    continue
                assert forged not in blob, f"{label} invented {forged}"

        mcp = json.loads((tree / "mcp.json").read_text(encoding="utf-8"))
        wk_mcp = json.loads((tree / ".well-known" / "mcp.json").read_text(encoding="utf-8"))
        for payload, label in ((mcp, "mcp"), (wk_mcp, "well-known-mcp")):
            server = payload["mcpServers"]["aziel-runtime"]
            assert server["version"] == VERSION, label
            assert server["git_sha"] == GIT_SHA, label
            assert server["version_id"] == VERSION_ID, label
            assert server["glama"] == RUNTIME_GLAMA, label
            assert "no local MCP" in server["note"] or "Prefer Try on Glama" in server["description"]

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "/runtime-launch.json" in openapi["paths"]
        assert "Cloudflare Pages" in openapi["info"]["description"]
        assert RUNTIME_GLAMA in openapi["info"]["description"]

        headers = (tree / "_headers").read_text(encoding="utf-8")
        assert "/runtime-launch.json" in headers
        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/runtime-launch.json /runtime-launch.json 200" in redirects
        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"{APEX}/runtime-launch.json</loc>" in sitemap
        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Allow: /runtime-launch.json" in robots

        wk = json.loads((tree / ".well-known" / "aziel.json").read_text(encoding="utf-8"))
        assert wk["runtime_sot"]["version_id"] == VERSION_ID
        assert wk["live_origin"]["project"] == PAGES_PROJECT

        shelves = json.loads((tree / "shelves.json").read_text(encoding="utf-8"))
        assert shelves["planes"]["B"]["framagit_tip_pack"]["url"] is None
        assert shelves["planes"]["B"]["framagit_tip_pack"]["refuse"] == "CNS-NO-FORGE-MIRROR"
        assert shelves["planes"]["B"]["live_ready"] is False
        assert shelves["planes"]["C"]["status"] == "slot"
        assert shelves["planes"]["B"]["codeberg_tip_pack"]["hash_verify"] == "pass"
        assert shelves["planes"]["B"]["archive_org_tip_pack"]["hash_verify"] == "pass"

        for name in PAPER_HTML:
            html = (tree / name).read_text(encoding="utf-8")
            nav = re.search(r'<nav class="paper-tabs"[\s\S]*?</nav>', html)
            if nav:
                assert "Receipts" not in nav.group(0), f"{tree_name}/{name} paper-tabs gained Receipts"
                assert "Pg. 11" not in nav.group(0)
                assert "Softwares" not in nav.group(0)
            if name != "who.html":
                visible = visible_text(html)
                assert "15:20" not in visible, f"{tree_name}/{name} gained visible 15:20"
            assert "fielded_100" not in html
            # Empty values (Plane B gitflic/gitlab/zenodo SLOT) dump as `: ""`.
            # Empty keys dump as `"":`.
            assert '"":' not in json.dumps(cite)  # no empty cite keys
            assert "never_" not in cite

        aziel = (tree / "aziel.html").read_text(encoding="utf-8")
        assert 'href="/receipts"' in aziel
        assert RUNTIME_GLAMA in aziel or "glama.ai/mcp/servers/AzielEliab/aziel-runtime" in aziel

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Cloudflare Pages" in readme
    assert PAGES_PROJECT in readme
    assert "docs/" in readme
    assert "not GH Pages alone" in readme or "not GitHub Pages alone" in readme

    print("runtime launch cite OK")
    print("sot", GIT_SHORT, VERSION_ID, VERSION)
    print("pages", PAGES_PROJECT)
    print("ingest_tip", HDJ_INGEST_TIP)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print("FAIL", exc, file=sys.stderr)
        raise
