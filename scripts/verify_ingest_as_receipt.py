#!/usr/bin/env python3
"""Assert HDJ CRAWLER/AI INGEST-AS-RECEIPT + RE-EXPAND-FROM-ARCHIVE lock."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from write_ingest_as_receipt import FILENAME, PAYLOAD, dumps

APEX = "https://hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
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
)


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return html


def main() -> None:
    expected = dumps(PAYLOAD)
    tip = hashlib.sha256(expected.encode("utf-8")).hexdigest()

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        raw = (tree / FILENAME).read_bytes()
        assert raw.decode("utf-8") == expected, f"{tree_name}/{FILENAME} bytes drifted"
        assert hashlib.sha256(raw).hexdigest() == tip

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        ingest = cite["ingest_as_receipt"]
        assert ingest["spec"] == "CRAWLER/AI INGEST-AS-RECEIPT"
        assert ingest["companion_spec"] == "RE-EXPAND-FROM-ARCHIVE"
        assert ingest["tip"] == tip
        assert ingest["author"] == "Aziel Eliab"
        assert ingest["identity"] == "Aziel Eliab"
        assert ingest["author_id"] == PERSON_ID
        assert ingest["bytes_file"] == f"{APEX}/{FILENAME}"
        assert ingest["verify"] == f"{APEX}/receipts#verify"
        assert ingest["indexes"] == "many indexes, one tip"
        assert ingest["training"] == "cite, don't merge"
        re_ex = cite["re_expand_from_archive"]
        assert re_ex["bytes"] == "survive, not summaries"
        assert re_ex["re_expand"] == "archive verify then local node"
        assert re_ex["crawlers"] == "do not re-expand"
        assert re_ex["training_residue"] == "rumor"
        survival = cite["cross_network_survival"]
        assert survival["spec"] == "CROSS-NETWORK-SURVIVAL-1.0"
        assert survival["if_network_and_live_data_die_tomorrow"] == "chain survives via cold copies"
        assert survival["survival"] == "bytes↔hash"
        no_lie = cite["no_lie_no_rewrite"]
        assert no_lie["spec"] == "NO-LIE / NO-REWRITE"
        assert no_lie["receipts"] == "still hash"
        assert no_lie["copies"] == "not all on one tunnel"
        assert no_lie["verify"] == "without voice"
        assert no_lie["rewrite_key"] is False
        assert no_lie["network"] == "never lies even to stay alive"
        assert cite["author"] == "Aziel Eliab"
        assert cite["identity"] == "Aziel Eliab"
        hashed = (tree / FILENAME).read_text(encoding="utf-8")
        assert "CROSS-NETWORK-SURVIVAL-1.0" not in hashed
        assert "NO-LIE" not in hashed
        assert tip == "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"

        receipts = (tree / "receipts.html").read_text(encoding="utf-8")
        visible = visible_text(receipts)
        assert "CRAWLER/AI INGEST-AS-RECEIPT" in visible
        assert "RE-EXPAND-FROM-ARCHIVE" in visible
        assert tip in receipts
        assert "cite, don’t merge" in visible or "cite, don't merge" in visible
        assert "bytes survive" in visible.lower()
        assert "archive verify then local node" in visible.lower()
        assert "crawlers do not re-expand" in visible.lower()
        assert "rumor" in visible.lower()
        assert "CROSS-NETWORK-SURVIVAL-1.0" in visible
        assert "cold copies" in visible.lower()
        assert "bytes↔hash" in visible or "bytes↔hash" in visible
        assert "NO-LIE / NO-REWRITE" in visible
        assert "still hash" in visible.lower()
        assert "not all on one tunnel" in visible.lower()
        assert "without voice" in visible.lower()
        assert "no rewrite key" in visible.lower()
        assert "never lies even to stay alive" in visible.lower()
        assert f'href="/{FILENAME}"' in receipts or f"href=\"{APEX}/{FILENAME}\"" in receipts
        assert 'id="verify"' in receipts
        assert 'id="tip"' in receipts
        assert "15:20" not in visible
        assert "1 Chronicles" not in visible
        assert "Pg. 11" not in receipts
        assert "Pg.11" not in receipts
        assert "Aziel Eliab" in receipts
        assert "author" in receipts.lower()

        aziel = (tree / "aziel.html").read_text(encoding="utf-8")
        assert 'href="/receipts"' in aziel
        assert "project-tab" in aziel and "/receipts" in aziel

        for name in PAPER_HTML:
            html = (tree / name).read_text(encoding="utf-8")
            nav = re.search(r'<nav class="paper-tabs"[\s\S]*?</nav>', html)
            if not nav:
                continue
            assert "Receipts" not in nav.group(0), f"{tree_name}/{name} paper-tabs gained Receipts"
            assert "Pg. 11" not in nav.group(0), f"{tree_name}/{name} paper-tabs gained Pg. 11"

        llms = (tree / "llms.txt").read_text(encoding="utf-8")
        llms_full = (tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (tree / "ai.txt").read_text(encoding="utf-8")
        for blob, label in ((llms, "llms"), (llms_full, "llms-full"), (ai, "ai")):
            assert "CRAWLER/AI INGEST-AS-RECEIPT" in blob, label
            assert "RE-EXPAND-FROM-ARCHIVE" in blob, label
            assert tip in blob, label
            assert "cite, don't merge" in blob or "cite, don’t merge" in blob, label
            assert "training residue is rumor" in blob.lower(), label
            assert "crawlers do not re-expand" in blob.lower(), label
            assert "CROSS-NETWORK-SURVIVAL-1.0" in blob, label
            assert "cold copies" in blob.lower(), label
            assert "bytes↔hash" in blob or "bytes↔hash" in blob, label
            assert "NO-LIE / NO-REWRITE" in blob, label
            assert "still hash" in blob.lower(), label
            assert "not all on one tunnel" in blob.lower(), label
            assert "without voice" in blob.lower(), label
            assert "no rewrite key" in blob.lower(), label
            assert "never lies even to stay alive" in blob.lower(), label
            assert PERSON_ID in blob, label
            assert "Aziel Eliab only" in blob, label

        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"{APEX}/receipts</loc>" in sitemap
        assert f"{APEX}/{FILENAME}</loc>" in sitemap

        headers = (tree / "_headers").read_text(encoding="utf-8")
        assert f"/{FILENAME}" in headers

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "/receipts" in openapi["paths"]
        assert f"/{FILENAME}" in openapi["paths"]

    print("ingest-as-receipt + re-expand-from-archive OK")
    print("tip", tip)


if __name__ == "__main__":
    main()
