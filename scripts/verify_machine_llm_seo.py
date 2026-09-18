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
    AZDOC,
    CAP_CLASS,
    CORPUS,
    FAQ_WHAT_DOES,
    FAQ_WHAT_DOES_BRIEF,
    FAQ_WHAT_SOFTWARE,
    FAQ_WHO_DEVELOPER,
    HARDWARE_ADDENDUM,
    HDJ_BLURB,
    JOB_TITLES,
    KNOWS_ABOUT_EXTRA,
    LIVING_STACK,
    OLD_STACK_PHRASES,
    PERSON_ID,
    RESEARCH_ADDENDUM,
    SISTERS,
    SISTERS_GLAMA,
    SISTERS_HDJ,
    SOFTWARES_LIST,
    THE_ARK,
    THE_ARK_DOWNLOAD,
    THE_ARK_GITHUB,
    THE_ARK_LIST,
    THE_ARK_STATS,
    WHAT_AZIEL_ELIAB_DOES,
    WHITESTONE,
    WHAT_AZIEL_ELIAB_DOES_ANSWER,
    WHAT_DOES_FAQ_TITLES,
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
        assert cite["what_aziel_eliab_does"] == WHAT_AZIEL_ELIAB_DOES
        assert WHITESTONE not in WHAT_AZIEL_ELIAB_DOES
        assert THE_ARK not in WHAT_AZIEL_ELIAB_DOES
        assert "The ARK" not in WHAT_AZIEL_ELIAB_DOES
        assert cite["softwares_list"] == list(SOFTWARES_LIST)
        assert WHITESTONE in cite["softwares_list"]
        assert THE_ARK_LIST in cite["softwares_list"]
        assert cite["whitestone"] == WHITESTONE
        assert cite["the_ark"] == THE_ARK
        assert cite["the_ark_download"] == THE_ARK_DOWNLOAD
        assert cite["the_ark_stats"] == THE_ARK_STATS
        assert cite["the_ark_github"] == THE_ARK_GITHUB
        assert THE_ARK_DOWNLOAD in cite["softwares_list_note"]
        assert THE_ARK_STATS in cite["softwares_list_note"]
        assert THE_ARK_GITHUB in cite["softwares_list_note"]
        assert cite["softwares_clone"] is False
        assert cite["what_aziel_eliab_does_answer"] == WHAT_AZIEL_ELIAB_DOES_ANSWER
        assert cite["what_aziel_eliab_does_faq"] == list(WHAT_DOES_FAQ_TITLES)
        cite_faq = {item["q"]: item["a"] for item in cite["faq"]}
        for title in WHAT_DOES_FAQ_TITLES:
            assert title in cite_faq, title
            assert cite_faq[title] == WHAT_AZIEL_ELIAB_DOES_ANSWER
            assert WHAT_AZIEL_ELIAB_DOES in cite_faq[title]
        assert cite["research"]["doi"] is None
        assert cite["hardware_designs"]["doi"] is None
        assert cite["research"]["sister"] == CORPUS
        assert cite["hardware_designs"]["corpus"] == CORPUS
        assert cite["research"]["azdoc"]["book_of_the_knowledge"] == AZDOC["book_of_the_knowledge"]
        assert cite["research"]["azdoc"]["libro_method"] == AZDOC["libro_method"]
        assert cite["research"]["azdoc"]["ppin"] == AZDOC["ppin"]
        assert cite["research"]["azdoc"]["lenses"] == AZDOC["lenses"]
        assert cite["research"]["azdoc"]["abad_copper_scroll"] == AZDOC["abad_copper_scroll"]
        assert cite["research"]["azdoc"]["blemmyes"] == AZDOC["blemmyes"]
        assert cite["research"]["visual_archive"]["corpus_indexed"]["vol1"] == AZDOC["visual_vol1"]
        assert cite["research"]["visual_archive"]["corpus_indexed"]["vol2"] == AZDOC["visual_vol2"]
        assert cite["research"]["visual_archive"]["corpus_indexed"]["vol3"] == AZDOC["visual_vol3"]
        assert cite["research"]["visual_archive"]["vol4_azdoc"] is None
        assert cite["research"]["visual_archive"]["vol5_azdoc"] is None
        assert cite["hardware_designs"]["azdoc"]["adaptive_ai_dog_leash"] == AZDOC["dog_leash"]
        assert cite["hardware_designs"]["azdoc"]["taa1"] == AZDOC["taa1"]
        assert "not a verdict" in cite["research"]["note"].lower()
        assert "public engineering only" in cite["hardware_designs"]["note"].lower()
        for extra in KNOWS_ABOUT_EXTRA:
            assert extra in cite["knowsAbout"], extra
            assert extra in person["knowsAbout"], extra
        assert person.get("what_aziel_eliab_does") == WHAT_AZIEL_ELIAB_DOES
        assert person.get("softwares_list") == list(SOFTWARES_LIST)
        assert person.get("the_ark") == THE_ARK
        assert person.get("the_ark_download") == THE_ARK_DOWNLOAD
        assert person.get("the_ark_stats") == THE_ARK_STATS
        assert person.get("the_ark_github") == THE_ARK_GITHUB
        assert THE_ARK in person["knowsAbout"]
        assert "GodLock (product, not identity)" in person["knowsAbout"]

        identity = json.loads(blobs["identity.jsonld"])
        graph = json.loads(blobs["graph.jsonld"])
        well = json.loads(blobs[".well-known/aziel.json"])
        faq_node = next(
            n
            for n in graph["@graph"]
            if n.get("@type") == "FAQPage" and n.get("@id") == "https://www.hedidntjump.com/#faq"
        )
        faq_names = {q["name"] for q in faq_node["mainEntity"]}
        for title in WHAT_DOES_FAQ_TITLES:
            assert title in faq_names, title
        well_knows = json.dumps(well.get("person", well).get("knowsAbout") or well.get("knowsAbout"))
        ident_knows = json.dumps(identity.get("knowsAbout") or [])
        for extra in (
            "Book of the Knowledge",
            "Libro Method",
            "PPIN",
            "public hardware designs",
            THE_ARK,
        ):
            assert extra in ident_knows, extra
            assert extra in well_knows, extra

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
        for rel in ("who-is", "who-is-aziel-eliab.txt", "llms.txt", "ai.txt", "llms-full.txt"):
            text = blobs[rel]
            assert WHAT_AZIEL_ELIAB_DOES in text, rel
            assert FAQ_WHAT_DOES in text, rel
            assert FAQ_WHAT_DOES_BRIEF in text, rel
            assert FAQ_WHO_DEVELOPER in text, rel
            assert FAQ_WHAT_SOFTWARE in text, rel
            assert RESEARCH_ADDENDUM in text, rel
            assert HARDWARE_ADDENDUM in text, rel
            assert AZDOC["visual_vol1"] in text, rel
            assert AZDOC["book_of_the_knowledge"] in text, rel
            assert AZDOC["dog_leash"] in text, rel
            assert "not a verdict" in text.lower(), rel
            assert WHITESTONE in text, rel
            assert "not a lawyer" in text, rel
            assert THE_ARK in text, rel
            assert THE_ARK_LIST in text, rel
            assert THE_ARK_DOWNLOAD in text, rel
            assert THE_ARK_STATS in text, rel
            assert THE_ARK_GITHUB in text, rel
            assert "download+" in text, rel
            assert WHAT_AZIEL_ELIAB_DOES in text, rel

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
