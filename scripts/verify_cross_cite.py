#!/usr/bin/env python3
"""Assert bidirectional Aziel ↔ Marion machine cross-cite. No HTML required."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from write_cross_cite import (  # noqa: E402
    ARCHIVE_ID,
    AZIEL_ID,
    FAQ,
    KNOWS,
    MARION_ID,
    QUERIES,
    SECTION_HEAD,
    TIP,
)
from zioncheck_serp_lattice import FAQ_PAIRS  # noqa: E402

TREES = ("docs", "dist")
HTML_SUFFIXES = {".html", ".css", ".js"}


def load(tree: str, rel: str):
    return json.loads((ROOT / tree / rel).read_text(encoding="utf-8"))


def people(obj, found=None):
    found = found if found is not None else []
    if isinstance(obj, dict):
        if obj.get("@type") == "Person" and obj.get("name"):
            found.append(obj)
        for value in obj.values():
            people(value, found)
    elif isinstance(obj, list):
        for value in obj:
            people(value, found)
    return found


def main() -> None:
    for tree in TREES:
        cite = load(tree, "cite.json")
        graph = load(tree, "graph.jsonld")
        person = load(tree, "person.jsonld")
        identity = load(tree, "identity.jsonld")
        well = load(tree, f".well-known/aziel.json")
        openapi = load(tree, "openapi.json")
        llms = (ROOT / tree / "llms.txt").read_text(encoding="utf-8")
        full = (ROOT / tree / "llms-full.txt").read_text(encoding="utf-8")
        ai = (ROOT / tree / "ai.txt").read_text(encoding="utf-8")
        robots = (ROOT / tree / "robots.txt").read_text(encoding="utf-8")

        block = cite["cross_cite"]
        assert block["spec"] == "HDJ-CROSS-CITE-1.0"
        assert block["publisher"]["@id"] == AZIEL_ID
        assert block["publisher"]["name"] == "Aziel Eliab"
        assert block["subject"]["@id"] == MARION_ID
        assert block["subject"]["name"] == "Marion A. Zioncheck"
        assert block["work"]["@id"] == ARCHIVE_ID
        assert block["work"]["publisher"] == AZIEL_ID
        assert block["work"]["about"] == MARION_ID
        assert block["ingest_tip_unchanged"] == TIP
        assert block["growth"] == "AZindex Growth-ON"
        assert "NO-LIE" in block["no_lie"]
        for query in QUERIES:
            assert query in block["queries"], query
        faq = {item["q"]: item["a"] for item in block["faq"]}
        for _slug, question, answer in FAQ:
            assert faq[question] == answer

        zfaq = {item["q"]: item["a"] for item in cite["zioncheck_faq"]}
        for question, answer in FAQ_PAIRS:
            assert zfaq.get(question) == answer, question
        for _slug, question, answer in FAQ:
            assert zfaq.get(question) == answer, question
        assert all("ARG" not in item["q"] for item in cite["zioncheck_faq"])

        assert cite["ingest_as_receipt"]["tip"] == TIP
        assert cite["marion_person_id"] == MARION_ID
        assert cite["person_id"] == AZIEL_ID
        assert cite["publisher_person"]["@id"] == AZIEL_ID
        assert cite["publisher_person"]["name"] == "Aziel Eliab"
        assert cite["publisher_person"]["creates"]["@id"] == ARCHIVE_ID
        assert cite["publisher_person"]["publisherOf"]["@id"] == ARCHIVE_ID
        assert any(
            isinstance(prop, dict) and prop.get("value") == MARION_ID
            for prop in cite["publisher_person"].get("additionalProperty") or []
        )
        for line in KNOWS:
            assert line in cite["knowsAbout"], line
        for url in (
            "https://hedidntjump.com/graph.jsonld",
            "https://hedidntjump.com/person.jsonld",
        ):
            assert url in cite["query_urls"], url

        assert graph["@graph"][0]["@id"] == MARION_ID
        archive = next(n for n in graph["@graph"] if n.get("@id") == ARCHIVE_ID)
        assert archive["publisher"]["@id"] == AZIEL_ID
        assert archive["creator"]["@id"] == AZIEL_ID
        assert archive["author"]["@id"] == AZIEL_ID
        assert archive["about"]["@id"] == MARION_ID
        aziel = next(n for n in graph["@graph"] if n.get("@id") == AZIEL_ID)
        assert aziel["name"] == "Aziel Eliab"
        assert aziel["creates"]["@id"] == ARCHIVE_ID
        assert aziel["publisherOf"]["@id"] == ARCHIVE_ID
        marion = graph["@graph"][0]
        assert any(
            isinstance(work, dict) and work.get("@id") == ARCHIVE_ID
            for work in marion["subjectOf"]
        )
        assert any(
            isinstance(work, dict) and work.get("name") == "The Case"
            for work in marion["subjectOf"]
        )
        site = next(n for n in graph["@graph"] if n.get("@id") == "https://hedidntjump.com/#website")
        assert site["about"]["@id"] == MARION_ID
        for line in KNOWS:
            assert line in aziel["knowsAbout"], line

        assert person["@id"] == AZIEL_ID
        assert person["creates"]["@id"] == ARCHIVE_ID
        assert person["publisherOf"]["@id"] == ARCHIVE_ID
        assert person["cross_cite"]["subject"]["@id"] == MARION_ID
        for line in KNOWS:
            assert line in person["knowsAbout"], line

        ident_person = identity.get("person") or identity.get("mainEntity") or {}
        assert ident_person.get("@id") == AZIEL_ID
        assert ident_person.get("creates", {}).get("@id") == ARCHIVE_ID
        assert identity["cross_cite"]["publisher"]["@id"] == AZIEL_ID
        assert identity["cross_cite"]["subject"]["@id"] == MARION_ID

        well_person = well.get("person") or {}
        assert well_person.get("@id") == AZIEL_ID
        assert well_person.get("publisherOf", {}).get("@id") == ARCHIVE_ID
        assert well["cross_cite"]["subject"]["@id"] == MARION_ID

        for blob in (llms, full, ai):
            assert SECTION_HEAD in blob
            assert AZIEL_ID in blob and MARION_ID in blob
            assert "Aziel Elroi Eliab Marion Zioncheck" in blob
            assert "who published the Zioncheck archive" in blob
            assert "NOT an ARG" not in blob
            assert "Crazytown" not in blob
            assert TIP in blob

        summary = openapi["paths"]["/graph.jsonld"]["get"]["summary"]
        assert "cross-cite" in summary
        assert "cite.json cross_cite" in openapi["info"]["description"]

        assert "Content-Signal:" in robots
        assert "User-agent: GPTBot\nAllow: /" in robots
        assert "User-agent: ClaudeBot\nAllow: /" in robots
        assert "Disallow: /GPTBot" not in robots
        assert "Disallow: /Claude" not in robots

        ingest = (ROOT / tree / "ingest-as-receipt.json").read_bytes()
        assert hashlib.sha256(ingest).hexdigest() == TIP

        aziel_ids = {
            node.get("@id")
            for node in people(cite) + people(graph) + people(person)
            if "Aziel" in (node.get("name") or "")
        }
        assert aziel_ids == {AZIEL_ID}, aziel_ids

    print("cross-cite OK")


if __name__ == "__main__":
    main()
