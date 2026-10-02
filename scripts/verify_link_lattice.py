#!/usr/bin/env python3
"""Assert the soft link lattice and plain-text sitemap stay honest."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from write_ingest_as_receipt import FILENAME, PAYLOAD, dumps as ingest_dumps
from write_link_lattice import (
    HDJ_INGEST_TIP,
    MARKER_END,
    MARKER_START,
    PERSON_ID,
    SUBJECT_ID,
    TABS,
    lattice_nodes,
)

ROOT = Path(__file__).resolve().parents[1]
APEX = "https://hedidntjump.com"
HTML = (
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


def main() -> None:
    nodes = lattice_nodes()
    ids = [str(node["id"]) for node in nodes]
    major = [row["id"] for row in TABS]
    expected_ingest = ingest_dumps(PAYLOAD)
    assert hashlib.sha256(expected_ingest.encode("utf-8")).hexdigest() == HDJ_INGEST_TIP

    docs_html = {
        name: hashlib.sha256((ROOT / "docs" / name).read_bytes()).hexdigest() for name in HTML
    }
    dist_html = {
        name: hashlib.sha256((ROOT / "dist" / name).read_bytes()).hexdigest() for name in HTML
    }

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        shelves_txt = (tree / "shelves.txt").read_text(encoding="utf-8")
        assert "whistleblower" in shelves_txt.lower()
        assert "NO-LIE" in shelves_txt
        assert "Do not invent holdings" in shelves_txt
        assert PERSON_ID in shelves_txt
        assert SUBJECT_ID in shelves_txt
        assert HDJ_INGEST_TIP in shelves_txt
        assert "NOT an ARG" not in shelves_txt
        for node in nodes:
            assert str(node["href"]) in shelves_txt, node["id"]
            assert str(node["label"]) in shelves_txt, node["id"]

        for rel in ("llms.txt", "llms-full.txt", "ai.txt", "help.txt"):
            text = (tree / rel).read_text(encoding="utf-8")
            assert MARKER_START in text, rel
            assert MARKER_END in text, rel
            assert f"{APEX}/shelves.txt" in text, rel
            assert PERSON_ID in text, rel
            assert SUBJECT_ID in text, rel
            assert "whistleblower" in text.lower(), rel
            assert "NOT an ARG" not in text, rel
            for row in TABS:
                assert row["href"] in text, (rel, row["id"])
            for number in range(1, 6):
                assert f"{APEX}/reader?volume={number}&page=1" in text, rel
                assert f"{APEX}/volumes/volume-{number}.pdf" in text, rel

        cite = json.loads((tree / "cite.json").read_text(encoding="utf-8"))
        lattice = cite["link_lattice"]
        assert lattice["spec"] == "HDJ-LINK-LATTICE-1.0"
        assert lattice["invented_holdings"] is False
        assert lattice["publisher_id"] == PERSON_ID
        assert lattice["subject_id"] == SUBJECT_ID
        assert lattice["ingest_tip"] == HDJ_INGEST_TIP
        assert lattice["map"] == f"{APEX}/shelves.txt"
        cite_ids = [node["id"] for node in lattice["nodes"]]
        assert cite_ids == ids
        for node in lattice["nodes"]:
            assert set(node["see_also"]) == set(ids) - {node["id"]}
            if node["id"] in major:
                for other in major:
                    if other != node["id"]:
                        assert other in node["see_also"], node["id"]
        assert f"{APEX}/shelves.txt" in cite["query_urls"]
        assert cite["ingest_as_receipt"]["tip"] == HDJ_INGEST_TIP

        shelves = json.loads((tree / "shelves.json").read_text(encoding="utf-8"))
        assert shelves["public_url_lattice"] == lattice
        assert shelves["shelves_txt"] == f"{APEX}/shelves.txt"
        assert shelves["verify"]["hdj_ingest_tip"] == HDJ_INGEST_TIP
        assert (tree / "shelves").read_text(encoding="utf-8") == (tree / "shelves.json").read_text(
            encoding="utf-8"
        )

        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Allow: /shelves.txt" in robots
        assert "Allow: /sitemap.txt" in robots
        assert "User-agent: GPTBot\nAllow: /" in robots
        assert "User-agent: GPTBot\nDisallow:" not in robots

        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/shelves.txt /shelves.txt 200" in redirects
        assert "/sitemap.txt /shelves.txt 200" in redirects
        assert "/shelves /shelves.json 200" in redirects
        assert (
            "/4241818f-5799-488c-9457-da724a30831c.txt /4241818f-5799-488c-9457-da724a30831c.txt 200"
            in redirects
        )
        assert "/.well-known/indexnow-key.txt /.well-known/indexnow-key.txt 200" in redirects

        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"<loc>{APEX}/shelves.txt</loc>" in sitemap
        assert f"<loc>{APEX}/sitemap.txt</loc>" in sitemap

        headers = (tree / "_headers").read_text(encoding="utf-8")
        assert "/shelves.txt" in headers
        assert "/sitemap.txt" in headers

        openapi = json.loads((tree / "openapi.json").read_text(encoding="utf-8"))
        assert "/shelves.txt" in openapi["paths"]
        assert "/sitemap.txt" in openapi["paths"]

        ingest = (tree / FILENAME).read_text(encoding="utf-8")
        assert ingest == expected_ingest
        assert hashlib.sha256(ingest.encode("utf-8")).hexdigest() == HDJ_INGEST_TIP

        for name in HTML:
            raw = (tree / name).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            assert digest == docs_html[name] == dist_html[name], name
            assert b"shelves.txt" not in raw, name

    docs_map = (ROOT / "docs" / "shelves.txt").read_text(encoding="utf-8")
    dist_map = (ROOT / "dist" / "shelves.txt").read_text(encoding="utf-8")
    assert docs_map == dist_map
    for rel in (
        "llms.txt",
        "llms-full.txt",
        "ai.txt",
        "help.txt",
        "cite.json",
        "shelves.json",
        "robots.txt",
        "_redirects",
        "sitemap.xml",
    ):
        assert (ROOT / "docs" / rel).read_bytes() == (ROOT / "dist" / rel).read_bytes(), rel

    print("soft link lattice OK")


if __name__ == "__main__":
    main()
