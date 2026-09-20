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
    CROSS_TETHER_SAME_AS,
    CROSS_TETHER_STATS,
    FAQ_WHAT_DOES,
    FAQ_WHAT_DOES_BRIEF,
    FAQ_WHAT_SOFTWARE,
    FAQ_WHO,
    FAQ_WHO_DEVELOPER,
    FAQ_WHY,
    FAQ_WHY_HDJ,
    FAQ_WHY_PUBLISH,
    GITHUB_PRIMARY,
    HDJ_GENRE,
    HDJ_PROJECT_KIND,
    LLMS_LEAD,
    SEO_BAN_MARKERS,
    HARDWARE_ADDENDUM,
    HDJ_BLURB,
    JOB_TITLES,
    KNOWS_ABOUT_EXTRA,
    LIVING_STACK,
    OLD_STACK_PHRASES,
    PEACELOCK,
    PEACELOCK_ADDENDUM,
    PEACELOCK_GITHUB,
    PEACELOCK_LIST,
    PERSON_ID,
    RESEARCH_ADDENDUM,
    SISTERS,
    SISTERS_GLAMA,
    SISTERS_HDJ,
    AZIEL_RUNTIME_ONE_LINE,
    SOFTWARES_CATALOG,
    SOFTWARES_COUNT,
    SOFTWARES_LIST,
    SOFTWARES_SSOT_SOFTWARE,
    SOFTWARES_SSOT_VERSION,
    SPECTRALLOCK,
    SPECTRALLOCK_ADDENDUM,
    SPECTRALLOCK_DOWNLOAD,
    SPECTRALLOCK_GITHUB,
    SPECTRALLOCK_HANDWRITING,
    SPECTRALLOCK_LIST,
    SPECTRALLOCK_OLD,
    SPECTRALLOCK_RECOVER,
    SPECTRALLOCK_UNREDACT,
    SPECTRALLOCK_WORKER,
    THE_ARK,
    THE_ARK_ADDENDUM,
    THE_ARK_DOWNLOAD,
    THE_ARK_GITHUB,
    THE_ARK_LIST,
    THE_ARK_STATS,
    TRADES_RUNTIME,
    TRADES_RUNTIME_ADDENDUM,
    TRADES_RUNTIME_DOWNLOAD,
    TRADES_RUNTIME_GITHUB,
    TRADES_RUNTIME_LIST,
    TRADES_RUNTIME_MCP,
    TRADES_RUNTIME_OPENAPI,
    TRADES_RUNTIME_WORKER,
    WHAT_AZIEL_ELIAB_DOES,
    WHITESTONE,
    WHAT_AZIEL_ELIAB_DOES_ANSWER,
    WHAT_DOES_FAQ_TITLES,
    WHY_AZIEL_ELIAB,
    WHY_FAQ_TITLES,
    X_HANDLE,
    X_URL,
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
            if rel not in ("identity.jsonld",):
                assert (
                    HDJ_BLURB.split(".")[0] in text
                    or "75% cap class" in text
                    or "Marion Zioncheck" in text
                ), rel

        cite = json.loads(blobs["cite.json"])
        person = json.loads(blobs["person.jsonld"])
        assert cite["project_kind"] == HDJ_PROJECT_KIND
        assert cite["genre"] == HDJ_GENRE
        assert cite["whistleblower"] is True
        assert "not_arg" not in cite
        assert "genre_not" not in cite
        assert "NOT an ARG" not in cite["purpose"]
        assert "whistleblower" in cite["purpose"]
        assert "independent investigative" in cite["purpose"]
        cite_faq = {item["q"]: item["a"] for item in cite["faq"]}
        assert "Is hedidntjump.com an ARG or alternate reality game?" not in cite_faq
        assert "Who is Aziel Eliab not?" not in cite_faq
        zfaq = {item["q"]: item["a"] for item in cite["zioncheck_faq"]}
        assert "Is hedidntjump.com an ARG or alternate reality game?" not in zfaq
        assert blobs["llms.txt"].startswith("# He Didn't Jump — Marion A. Zioncheck archive")
        assert blobs["llms.txt"].split("## Query-relevant")[0].strip().endswith(LLMS_LEAD) or LLMS_LEAD in blobs["llms.txt"]
        assert "NOT an ARG" not in blobs["llms.txt"]
        assert "whistleblower" in blobs["llms.txt"].lower()
        assert "Marion A. Zioncheck" in blobs["llms.txt"]
        assert "NOT an ARG" not in blobs["ai.txt"]
        assert "whistleblower" in blobs["ai.txt"].lower()
        assert "NOT an ARG" not in blobs["llms-full.txt"]
        assert "whistleblower" in blobs["llms-full.txt"].lower()
        for rel, text in blobs.items():
            if rel in ("cite.json", "llms.txt", "ai.txt", "llms-full.txt", "who-is", "who-is-aziel-eliab.txt"):
                for marker in SEO_BAN_MARKERS:
                    assert marker not in text, f"{tree_name}/{rel} still has {marker}"
                assert "Not a Softwares clone" not in text, rel
                assert "not a Softwares card" not in text.lower(), rel
                assert "Who is Aziel Eliab not?" not in text, rel
                assert "HDJ is not a Lamb Lens ingest host" not in text, rel
                assert "HDJ is not a live exec door" not in text, rel
                assert "blocked from" not in text, rel
                assert "addendum; not a verdict" not in text, rel
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
        assert cite["sisters"]["github"] == GITHUB_PRIMARY
        assert cite["sisters"]["x"] == X_URL
        assert cite["sisters"]["x_handle"] == X_HANDLE
        assert cite["github"] == GITHUB_PRIMARY
        assert cite["x"] == X_URL
        assert cite["x_handle"] == X_HANDLE
        assert cite["try_on_glama"] == SISTERS_GLAMA
        assert cite["why_aziel_eliab"] == WHY_AZIEL_ELIAB
        assert cite["why_aziel_eliab_faq"] == list(WHY_FAQ_TITLES)
        assert cite["cross_tether"]["github"] == GITHUB_PRIMARY
        assert cite["cross_tether"]["x"] == X_URL
        assert cite["cross_tether"]["x_handle"] == X_HANDLE
        assert cite["cross_tether"]["try_on_glama"] == SISTERS_GLAMA
        assert cite["cross_tether"]["ae"] == SISTERS["ae"]
        assert cite["cross_tether"]["corpus"] == SISTERS["corpus"]
        assert cite["cross_tether"]["godlock"] == SISTERS["godlock"]
        assert cite["cross_tether"]["runtime"] == SISTERS["runtime"]
        assert cite["cross_tether"]["hdj"] == SISTERS_HDJ
        assert cite["cross_tether"]["growth_on"] is True
        assert "paper-tabs" in cite["cross_tether"]["receipts_chrome"].lower()
        for url in CROSS_TETHER_SAME_AS:
            assert url in cite["cross_tether"]["sameAs"], url
        for label, url in CROSS_TETHER_STATS.items():
            assert cite["cross_tether"]["stats"][label] == url, label
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
        assert TRADES_RUNTIME not in WHAT_AZIEL_ELIAB_DOES
        assert "Trades-Runtime" not in WHAT_AZIEL_ELIAB_DOES
        assert SPECTRALLOCK not in WHAT_AZIEL_ELIAB_DOES
        assert "SpectralLock" not in WHAT_AZIEL_ELIAB_DOES
        assert PEACELOCK not in WHAT_AZIEL_ELIAB_DOES
        assert "PeaceLock" not in WHAT_AZIEL_ELIAB_DOES
        assert SPECTRALLOCK_OLD not in WHAT_AZIEL_ELIAB_DOES
        assert cite["softwares_list"] == list(SOFTWARES_LIST)
        assert len(cite["softwares_list"]) == SOFTWARES_COUNT
        assert cite["softwares_count"] == SOFTWARES_COUNT
        assert cite["softwares_designed_purpose"] is True
        assert cite["aziel_runtime_one_line"] == AZIEL_RUNTIME_ONE_LINE
        assert WHITESTONE in cite["softwares_list"]
        assert THE_ARK in cite["softwares_list"]
        assert THE_ARK_LIST not in cite["softwares_list"]
        assert TRADES_RUNTIME_LIST not in cite["softwares_list"]
        assert SPECTRALLOCK in cite["softwares_list"]
        assert PEACELOCK in cite["softwares_list"]
        for name, one_line in SOFTWARES_CATALOG:
            assert f"{name} — {one_line}" in cite["softwares_list"], name
            assert "THIS IS NOT" not in one_line
            assert "never invent" not in one_line.lower()
            assert "fielded_100" not in one_line
        assert cite["softwares_ssot"]["version"] == SOFTWARES_SSOT_VERSION
        assert cite["softwares_ssot"]["designed_purpose"] is True
        assert cite["softwares_ssot"]["count"] == SOFTWARES_COUNT
        assert cite["softwares_ssot"]["software"] == SOFTWARES_SSOT_SOFTWARE
        assert cite["softwares_ssot_version"] == SOFTWARES_SSOT_VERSION
        assert "version" not in cite["trades_runtime"]
        assert "version" not in cite["spectrallock"]
        assert "version" not in cite["peacelock"]
        assert cite["trades_runtime"]["ssot_version"] == SOFTWARES_SSOT_VERSION
        assert cite["spectrallock"]["ssot_version"] == SOFTWARES_SSOT_VERSION
        assert cite["peacelock"]["ssot_version"] == SOFTWARES_SSOT_VERSION
        assert cite["whitestone"] == WHITESTONE
        assert cite["the_ark"] == THE_ARK
        assert cite["the_ark_download"] == THE_ARK_DOWNLOAD
        assert cite["the_ark_stats"] == THE_ARK_STATS
        assert cite["the_ark_github"] == THE_ARK_GITHUB
        assert THE_ARK_DOWNLOAD in cite["softwares_list_note"]
        assert THE_ARK_STATS in cite["softwares_list_note"]
        assert THE_ARK_GITHUB in cite["softwares_list_note"]
        assert cite["softwares_clone"] is False
        assert cite["sisters"]["trades_runtime"] == TRADES_RUNTIME_WORKER
        assert cite["trades_runtime_worker"] == TRADES_RUNTIME_WORKER
        assert cite["trades_runtime_github"] == TRADES_RUNTIME_GITHUB
        assert cite["trades_runtime_download"] == TRADES_RUNTIME_DOWNLOAD
        assert cite["trades_runtime_openapi"] == TRADES_RUNTIME_OPENAPI
        assert cite["trades_runtime_mcp"] == TRADES_RUNTIME_MCP
        assert cite["trades_runtime"]["live_backends"] is False
        assert cite["trades_runtime"]["fraggate_exec"] is False
        assert cite["trades_runtime"]["cite_only"] is True
        assert cite["trades_runtime"]["public_softwares_cite"] is True
        assert cite["trades_runtime"]["worker"] == TRADES_RUNTIME_WORKER
        assert cite["trades_runtime"]["github"] == TRADES_RUNTIME_GITHUB
        assert cite["trades_runtime"]["download"] == TRADES_RUNTIME_DOWNLOAD
        assert cite["trades_runtime"]["openapi"] == TRADES_RUNTIME_OPENAPI
        assert cite["trades_runtime"]["mcp"] == TRADES_RUNTIME_MCP
        assert any(
            e.get("id") == "trades-runtime" and e.get("href") == TRADES_RUNTIME_WORKER
            for e in cite["ecosystem"]
            if isinstance(e, dict)
        )
        assert TRADES_RUNTIME_WORKER in cite["softwares_list_note"]
        assert TRADES_RUNTIME_GITHUB in cite["softwares_list_note"]
        assert TRADES_RUNTIME_DOWNLOAD in cite["softwares_list_note"]
        assert TRADES_RUNTIME_OPENAPI in cite["softwares_list_note"]
        assert TRADES_RUNTIME_MCP in cite["softwares_list_note"]
        assert "trades-runtime" in cite["purpose"]
        assert "peacelock" in cite["purpose"]
        assert "designed-purpose" in cite["purpose"]
        assert "42/42" in cite["purpose"]
        assert SOFTWARES_SSOT_VERSION in cite["purpose"]
        assert cite["sisters"]["peacelock"] == PEACELOCK_GITHUB
        assert cite["peacelock_github"] == PEACELOCK_GITHUB
        assert cite["peacelock"]["public_git"] is True
        assert cite["peacelock"]["local_only_runtime"] is True
        assert cite["peacelock"]["cite_only"] is True
        assert cite["peacelock"]["fraggate_exec"] is False
        assert cite["peacelock"]["hosted_runtime"] is False
        assert cite["peacelock"]["github"] == PEACELOCK_GITHUB
        assert "worker" not in cite["peacelock"]
        assert "download" not in cite["peacelock"]
        assert any(
            e.get("id") == "peacelock" and e.get("href") == PEACELOCK_GITHUB
            for e in cite["ecosystem"]
            if isinstance(e, dict)
        )
        assert PEACELOCK_GITHUB in cite["softwares_list_note"]
        assert SOFTWARES_SSOT_VERSION in cite["softwares_list_note"]
        assert SOFTWARES_SSOT_SOFTWARE in cite["softwares_list_note"]
        assert "public Softwares/cite" in cite["softwares_list_note"]
        assert cite["sisters"]["spectrallock"] == SPECTRALLOCK_WORKER
        assert cite["spectrallock_worker"] == SPECTRALLOCK_WORKER
        assert cite["spectrallock_unredact"] == SPECTRALLOCK_UNREDACT
        assert cite["spectrallock_recover"] == SPECTRALLOCK_RECOVER
        assert cite["spectrallock_handwriting"] == SPECTRALLOCK_HANDWRITING
        assert cite["spectrallock_github"] == SPECTRALLOCK_GITHUB
        assert cite["spectrallock_download"] == SPECTRALLOCK_DOWNLOAD
        assert cite["spectrallock"]["leftover_bytes_recovery"] is True
        assert cite["spectrallock"]["pigment_recovery"] is False
        assert cite["spectrallock"]["guessed_letters"] is False
        assert cite["spectrallock"]["heatmap_is_transcript"] is False
        assert cite["spectrallock"]["fraggate_door"] is False
        assert cite["spectrallock"]["fraggate_door_op"] is False
        assert cite["spectrallock"]["catalog_door"] is False
        assert cite["spectrallock"]["lab"] is False
        assert cite["spectrallock"]["forensic_certification"] is False
        assert cite["spectrallock"]["esda"] is False
        assert cite["spectrallock"]["writer_identification_as_fact"] is False
        assert cite["spectrallock"]["no_lie"] is True
        assert cite["spectrallock"]["cite_only"] is True
        assert cite["spectrallock"]["refuse_code"] == "SL-UNREDACT-OPAQUE"
        assert cite["spectrallock"]["unredact"] == SPECTRALLOCK_UNREDACT
        assert cite["spectrallock"]["recover"] == SPECTRALLOCK_RECOVER
        assert cite["spectrallock"]["handwriting"] == SPECTRALLOCK_HANDWRITING
        assert cite["spectrallock"]["worker"] == SPECTRALLOCK_WORKER
        assert cite["spectrallock"]["github"] == SPECTRALLOCK_GITHUB
        assert cite["spectrallock"]["download"] == SPECTRALLOCK_DOWNLOAD
        assert any(
            e.get("id") == "spectrallock" and e.get("href") == SPECTRALLOCK_WORKER
            for e in cite["ecosystem"]
            if isinstance(e, dict)
        )
        assert SPECTRALLOCK_UNREDACT in cite["softwares_list_note"]
        assert SPECTRALLOCK_RECOVER in cite["softwares_list_note"]
        assert SPECTRALLOCK_HANDWRITING in cite["softwares_list_note"]
        assert SPECTRALLOCK_GITHUB in cite["softwares_list_note"]
        assert SPECTRALLOCK_DOWNLOAD in cite["softwares_list_note"]
        assert "leftover-bytes" in cite["softwares_list_note"].lower()
        assert "spectrallock" in cite["purpose"]
        assert "/v1/recover" in cite["purpose"]
        assert "/v1/handwriting" in cite["purpose"]
        assert cite["what_aziel_eliab_does_answer"] == WHAT_AZIEL_ELIAB_DOES_ANSWER
        assert cite["what_aziel_eliab_does_faq"] == list(WHAT_DOES_FAQ_TITLES)
        cite_faq = {item["q"]: item["a"] for item in cite["faq"]}
        for title in WHAT_DOES_FAQ_TITLES:
            assert title in cite_faq, title
            assert cite_faq[title] == WHAT_AZIEL_ELIAB_DOES_ANSWER
            assert WHAT_AZIEL_ELIAB_DOES in cite_faq[title]
        for title in WHY_FAQ_TITLES:
            assert title in cite_faq, title
            assert cite_faq[title] == WHY_AZIEL_ELIAB
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
        assert "newspaper and volume archive" in cite["research"]["note"].lower()
        assert "public engineering only" in cite["hardware_designs"]["note"].lower()
        for extra in KNOWS_ABOUT_EXTRA:
            assert extra in cite["knowsAbout"], extra
            assert extra in person["knowsAbout"], extra
        assert person.get("what_aziel_eliab_does") == WHAT_AZIEL_ELIAB_DOES
        assert person.get("why_aziel_eliab") == WHY_AZIEL_ELIAB
        assert person.get("softwares_list") == list(SOFTWARES_LIST)
        assert person.get("the_ark") == THE_ARK
        assert person.get("the_ark_download") == THE_ARK_DOWNLOAD
        assert person.get("the_ark_stats") == THE_ARK_STATS
        assert person.get("the_ark_github") == THE_ARK_GITHUB
        assert person.get("trades_runtime") == TRADES_RUNTIME
        assert person.get("trades_runtime_worker") == TRADES_RUNTIME_WORKER
        assert person.get("trades_runtime_github") == TRADES_RUNTIME_GITHUB
        assert person.get("trades_runtime_download") == TRADES_RUNTIME_DOWNLOAD
        assert person.get("trades_runtime_openapi") == TRADES_RUNTIME_OPENAPI
        assert person.get("trades_runtime_mcp") == TRADES_RUNTIME_MCP
        assert person.get("spectrallock") == SPECTRALLOCK
        assert person.get("spectrallock_worker") == SPECTRALLOCK_WORKER
        assert person.get("spectrallock_unredact") == SPECTRALLOCK_UNREDACT
        assert person.get("spectrallock_recover") == SPECTRALLOCK_RECOVER
        assert person.get("spectrallock_handwriting") == SPECTRALLOCK_HANDWRITING
        assert person.get("spectrallock_github") == SPECTRALLOCK_GITHUB
        assert person.get("spectrallock_download") == SPECTRALLOCK_DOWNLOAD
        assert person.get("peacelock") == PEACELOCK
        assert person.get("peacelock_github") == PEACELOCK_GITHUB
        assert person.get("softwares_ssot_version") == SOFTWARES_SSOT_VERSION
        assert THE_ARK in person["knowsAbout"]
        assert TRADES_RUNTIME in person["knowsAbout"]
        assert SPECTRALLOCK in person["knowsAbout"]
        assert PEACELOCK in person["knowsAbout"]
        assert any(
            isinstance(item, str) and item.startswith("GodLock — ")
            for item in person["knowsAbout"]
        )

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
        for title in WHY_FAQ_TITLES:
            assert title in faq_names, title
        well_knows = json.dumps(
            well.get("person", well).get("knowsAbout") or well.get("knowsAbout") or well,
            ensure_ascii=False,
        )
        ident_knows = json.dumps(
            identity.get("knowsAbout")
            or (identity.get("person") or {}).get("knowsAbout")
            or (identity.get("mainEntity") or {}).get("knowsAbout")
            or identity,
            ensure_ascii=False,
        )
        for extra in (
            "Book of the Knowledge",
            "Libro Method",
            "PPIN",
            "public hardware designs",
            THE_ARK,
            TRADES_RUNTIME,
            SPECTRALLOCK,
            PEACELOCK,
        ):
            assert extra in ident_knows, extra
            assert extra in well_knows, extra

        assert "## Trades-Runtime sister cite (machine)" in blobs["llms.txt"]
        assert "## Trades-Runtime sister cite (machine)" in blobs["llms-full.txt"]
        assert "TRADES-RUNTIME (sister Softwares/runtime cite-only" in blobs["ai.txt"]
        assert "Sister Softwares cite: [Trades-Runtime]" in blobs["llms.txt"]
        assert "## SpectralLock sister cite (machine)" in blobs["llms.txt"]
        assert "## SpectralLock sister cite (machine)" in blobs["llms-full.txt"]
        assert "SPECTRALLOCK (sister Softwares cite-only" in blobs["ai.txt"]
        assert "Sister Softwares cite: [SpectralLock]" in blobs["llms.txt"]
        assert "## PeaceLock designed-purpose (machine)" in blobs["llms.txt"]
        assert "## PeaceLock designed-purpose (machine)" in blobs["llms-full.txt"]
        assert "PEACELOCK (designed-purpose" in blobs["ai.txt"]
        assert "PeaceLock designed-purpose:" in blobs["llms.txt"]
        assert SPECTRALLOCK_UNREDACT in blobs["llms.txt"]
        assert SPECTRALLOCK_RECOVER in blobs["llms.txt"]
        assert SPECTRALLOCK_HANDWRITING in blobs["llms.txt"]
        assert "leftover-bytes" in blobs["llms.txt"]
        assert "/v1/recover" in blobs["llms.txt"]
        assert "/v1/handwriting" in blobs["llms.txt"]
        assert "leftover-bytes" in blobs["llms.txt"].lower()
        assert SPECTRALLOCK_UNREDACT in blobs["ai.txt"]
        assert SPECTRALLOCK_RECOVER in blobs["ai.txt"]
        assert SPECTRALLOCK_HANDWRITING in blobs["ai.txt"]
        assert "/v1/handwriting" in blobs["ai.txt"]
        assert "leftover-bytes" in blobs["ai.txt"].lower()

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
            assert FAQ_WHO in text, rel
            assert FAQ_WHY in text, rel
            assert FAQ_WHY_PUBLISH in text, rel
            assert FAQ_WHY_HDJ in text, rel
            assert WHY_AZIEL_ELIAB in text, rel
            assert GITHUB_PRIMARY in text, rel
            assert X_URL in text, rel
            assert X_HANDLE in text, rel
            assert SISTERS_GLAMA in text, rel
            assert "Try on Glama" in text or SISTERS_GLAMA in text, rel
            assert RESEARCH_ADDENDUM in text, rel
            assert HARDWARE_ADDENDUM in text, rel
            assert AZDOC["visual_vol1"] in text, rel
            assert AZDOC["book_of_the_knowledge"] in text, rel
            assert AZDOC["dog_leash"] in text, rel
            assert "RESEARCH (addendum)" in text, rel
            assert WHITESTONE in text, rel
            assert "Whitestone" in text, rel
            assert THE_ARK in text, rel
            assert THE_ARK_ADDENDUM in text, rel
            assert THE_ARK_LIST in text, rel
            assert THE_ARK_DOWNLOAD in text, rel
            assert THE_ARK_STATS in text, rel
            assert THE_ARK_GITHUB in text, rel
            assert "download+" in text, rel
            assert TRADES_RUNTIME in text, rel
            assert TRADES_RUNTIME_ADDENDUM in text, rel
            assert TRADES_RUNTIME_WORKER in text, rel
            assert TRADES_RUNTIME_GITHUB in text, rel
            assert TRADES_RUNTIME_DOWNLOAD in text, rel
            assert TRADES_RUNTIME_OPENAPI in text, rel
            assert TRADES_RUNTIME_MCP in text, rel
            assert SPECTRALLOCK in text, rel
            assert SPECTRALLOCK_ADDENDUM in text, rel
            assert SPECTRALLOCK_UNREDACT in text, rel
            assert SPECTRALLOCK_RECOVER in text, rel
            assert SPECTRALLOCK_HANDWRITING in text, rel
            assert SPECTRALLOCK_GITHUB in text, rel
            assert SPECTRALLOCK_DOWNLOAD in text, rel
            assert SPECTRALLOCK_WORKER in text, rel
            assert PEACELOCK in text, rel
            assert PEACELOCK_ADDENDUM in text, rel
            assert PEACELOCK_GITHUB in text, rel
            assert "Record chosen silence or chosen inaction as a hash-chained receipt." in text, rel
            assert SOFTWARES_SSOT_VERSION in text, rel
            assert SOFTWARES_SSOT_SOFTWARE in text, rel
            assert "peacelock-download-tracker" not in text, rel
            assert "fielded_100" not in text, rel
            assert "THIS IS NOT" not in text, rel
            assert "Never ." not in text, rel
            assert (
                text.count("Aziel Runtime (suite; HDJ cites, does not host):") == 1
            ), rel
            assert AZIEL_RUNTIME_ONE_LINE in text, rel
            assert "leftover-bytes" in text, rel
            assert "/v1/recover" in text, rel
            assert "/v1/handwriting" in text, rel
            assert "leftover-bytes" in text.lower(), rel
            assert SPECTRALLOCK_OLD not in text, rel
            assert "/mcp" not in SPECTRALLOCK_ADDENDUM
            assert "live_backends false" in text, rel
            assert "live_backends false" in text, rel
            assert "1 Chronicles 15:20" not in TRADES_RUNTIME_ADDENDUM
            assert "1 Chronicles 15:20" not in SPECTRALLOCK_ADDENDUM
            assert WHAT_AZIEL_ELIAB_DOES in text, rel

        # Newspaper HTML chrome stays ZionBot's. This pack must not rewrite it.
        import re

        for name in HTML:
            html = (tree / name).read_text(encoding="utf-8")
            assert PERSON_ID in html
            assert "Everblooming Flower" not in html
            nav = re.search(r'<nav class="paper-tabs"[\s\S]*?</nav>', html)
            if nav:
                assert "Receipts" not in nav.group(0), f"{tree_name}/{name} paper-tabs gained Receipts"
        aziel = (tree / "aziel.html").read_text(encoding="utf-8")
        assert 'href="/receipts"' in aziel
        assert "@AzielEliab" in aziel

        sitemap = (tree / "sitemap.xml").read_text(encoding="utf-8")
        for loc in ("/llms.txt", "/ai.txt", "/cite.json"):
            assert f"<loc>https://hedidntjump.com{loc}</loc>" in sitemap, loc
            chunk = sitemap.split(f"<loc>https://hedidntjump.com{loc}</loc>", 1)[1][:80]
            assert "<lastmod>2026-09-20</lastmod>" in chunk, loc
        for loc in ("/help.txt", "/addendum.txt", "/help/how-to-read.txt"):
            assert f"<loc>https://hedidntjump.com{loc}</loc>" in sitemap, loc
        assert TRADES_RUNTIME_WORKER not in sitemap
        assert SPECTRALLOCK_WORKER not in sitemap
        assert SPECTRALLOCK_UNREDACT not in sitemap
        assert SPECTRALLOCK_RECOVER not in sitemap
        assert SPECTRALLOCK_HANDWRITING not in sitemap
        assert PEACELOCK_GITHUB not in sitemap
        assert "peacelock-download-tracker" not in sitemap
        index = (tree / "sitemap-index.xml").read_text(encoding="utf-8")
        assert "<loc>https://hedidntjump.com/sitemap.xml</loc>" in index
        assert "trades-runtime.vibelock.workers.dev" not in index
        assert "spectrallock-download-tracker.vibelock.workers.dev" not in index
        assert "peacelock-download-tracker" not in index

        ingest = (tree / "ingest-as-receipt.json").read_bytes()
        import hashlib

        tip = hashlib.sha256(ingest).hexdigest()
        assert tip == "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"

    print("machine LLM/SEO pack OK")


if __name__ == "__main__":
    main()
