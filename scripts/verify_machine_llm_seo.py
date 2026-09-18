#!/usr/bin/env python3
"""Assert machine-only LLM/SEO Person+site cites. No HTML chrome required."""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_living import (
    CAP_CLASS,
    HDJ_BLURB,
    JOB_TITLES,
    LIVING_STACK,
    OLD_STACK_PHRASES,
    PERSON_ID,
    SISTERS,
    SISTERS_GLAMA,
    SISTERS_HDJ,
)

ROOT = Path(__file__).resolve().parents[1]
MACHINE = (
    "cite.json",
    "llms.txt",
    "ai.txt",
    "person.jsonld",
    "who-is",
    "who-is-aziel-eliab.txt",
    "llms-full.txt",
    "identity.jsonld",
    "graph.jsonld",
    ".well-known/aziel.json",
)
HTML = (
    "index.html",
    "aziel.html",
    "who.html",
    "case.html",
)


def main() -> None:
    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        blobs = {}
        for rel in MACHINE:
            blobs[rel] = (tree / rel).read_text(encoding="utf-8")

        for rel, text in blobs.items():
            assert PERSON_ID in text, rel
            assert LIVING_STACK in text, rel
            for old in OLD_STACK_PHRASES:
                assert old not in text, f"{tree_name}/{rel} still has {old!r}"
            assert "euaziel.site" in text, rel
            assert "an researcher" not in text, rel
            assert HDJ_BLURB.split(".")[0] in text or "75% cap class" in text, rel

        cite = json.loads(blobs["cite.json"])
        person = json.loads(blobs["person.jsonld"])
        assert cite["person_id"] == PERSON_ID
        assert cite["author_id"] == PERSON_ID
        assert cite["growth_on"] is True
        assert cite["softwares_clone"] is False
        assert cite["living_stack"] == LIVING_STACK
        assert cite["jobTitle"] == JOB_TITLES
        assert cite["cap_class"] == CAP_CLASS
        assert cite["hdj_blurb"] == HDJ_BLURB
        assert cite["sisters"]["ae"] == SISTERS["ae"]
        assert cite["sisters"]["corpus"] == SISTERS["corpus"]
        assert cite["sisters"]["godlock"] == SISTERS["godlock"]
        assert cite["sisters"]["runtime"] == SISTERS["runtime"]
        assert cite["sisters"]["runtime_glama"] == SISTERS_GLAMA
        assert cite["sisters"]["hdj"] == SISTERS_HDJ
        assert cite["pages_seo"]["owner"] == "ZionBot"
        assert cite["pages_seo"]["this_pack"] == "machine files only"
        assert cite["no_lie"].startswith("NO-LIE")
        assert person["@id"] == PERSON_ID
        assert person["jobTitle"] == JOB_TITLES
        assert LIVING_STACK in person["description"]
        assert "75% cap class" in json.dumps(cite)

        who = blobs["who-is"]
        who_txt = blobs["who-is-aziel-eliab.txt"]
        assert who == who_txt
        assert "living author of He Didn’t Jump" in who or "living author of He Didn't Jump" in who
        assert "FOIA Binary Acknowledgement" in who
        assert "Marion Zioncheck" in who
        for label, url in SISTERS.items():
            assert url in who, label
            assert url in blobs["llms.txt"], label
            assert url in blobs["ai.txt"], label

        # Newspaper HTML chrome stays ZionBot's. This pack must not rewrite it.
        for name in HTML:
            html = (tree / name).read_text(encoding="utf-8")
            assert PERSON_ID in html
            assert "Everblooming Flower" not in html

        ingest = (tree / "ingest-as-receipt.json").read_bytes()
        import hashlib

        tip = hashlib.sha256(ingest).hexdigest()
        assert tip == "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"

    print("machine LLM/SEO pack OK")


if __name__ == "__main__":
    main()
