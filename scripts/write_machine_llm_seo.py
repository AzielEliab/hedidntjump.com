#!/usr/bin/env python3
"""Machine-only LLM/SEO Person+site cites for hedidntjump.com.

Updates cite.json, llms.txt, ai.txt, person.jsonld, who-is*, plus the
other machine identity JSON (identity/graph/well-known/llms-full).
Does not rewrite newspaper HTML. ZionBot owns Pages SEO chrome.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_living import (
    AZDOC,
    CAP_CLASS,
    CAP_NOTE,
    CORPUS,
    DOI_RULE,
    FAQ_WHAT_DOES,
    FAQ_WHAT_DOES_BRIEF,
    FAQ_WHAT_SOFTWARE,
    FAQ_WHO_DEVELOPER,
    HARDWARE_ADDENDUM,
    HDJ_BLURB,
    JOB_TITLES,
    KEEP_JOB_TITLES,
    KNOWS_ABOUT_EXTRA,
    LIVING_STACK,
    OLD_STACK_PHRASES,
    PAGES_SEO,
    PERSON_ID,
    PERSON_LEAD,
    PRIMARY_SURFACES,
    RESEARCH_ADDENDUM,
    SISTERS,
    SISTERS_GLAMA,
    SISTERS_HDJ,
    WHAT_AZIEL_ELIAB_DOES,
    WHAT_AZIEL_ELIAB_DOES_ANSWER,
    WHAT_DOES_FAQ_TITLES,
    WHO_IS_NAMED,
    WHO_IS_SHORT,
)

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]

MACHINE_JSON = (
    "cite.json",
    "person.jsonld",
    "identity.jsonld",
    "graph.jsonld",
    ".well-known/aziel.json",
)
MACHINE_TXT = (
    "llms.txt",
    "llms-full.txt",
    "ai.txt",
    "who-is",
    "who-is-aziel-eliab.txt",
)

SISTERS_BLOCK = f"""Sister surfaces (this host is HDJ; not a Softwares clone)
- ae: {SISTERS["ae"]}
- corpus: {SISTERS["corpus"]}
- godlock: {SISTERS["godlock"]}
- runtime: {SISTERS["runtime"]}
- runtime (prefer Glama): {SISTERS_GLAMA}
- this: {SISTERS_HDJ} — {HDJ_BLURB}
Growth-ON. NO-LIE. Person @id: {PERSON_ID}
ZionBot owns newspaper HTML / Pages SEO chrome. This pack is machine files only.
"""

WHAT_DOES_FAQ_BLOCK = f"""## What Aziel Eliab does (locked FAQ brief)

{WHAT_AZIEL_ELIAB_DOES}

Q: {FAQ_WHAT_DOES}
Q: {FAQ_WHAT_DOES_BRIEF}
Q: {FAQ_WHO_DEVELOPER}
Q: {FAQ_WHAT_SOFTWARE}
A: {WHAT_AZIEL_ELIAB_DOES_ANSWER}

{RESEARCH_ADDENDUM}

{HARDWARE_ADDENDUM}
"""

WHAT_DOES_FAQ_ROWS = [
    {"q": title, "a": WHAT_AZIEL_ELIAB_DOES_ANSWER}
    for title in WHAT_DOES_FAQ_TITLES
]

FAQ_GRAPH_IDS = {
    FAQ_WHAT_DOES: "https://www.hedidntjump.com/#faq-what-does-aziel-eliab-do",
    FAQ_WHAT_DOES_BRIEF: "https://www.hedidntjump.com/#faq-what-aziel-eliab-does",
    FAQ_WHO_DEVELOPER: "https://www.hedidntjump.com/#faq-who-is-aziel-eliab-the-developer",
    FAQ_WHAT_SOFTWARE: "https://www.hedidntjump.com/#faq-what-software-does-aziel-eliab-make",
}


def dumps(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def upsert_faq_rows(faq: list) -> list:
    out = [item for item in faq if isinstance(item, dict)]
    have = {item.get("q") for item in out}
    for row in WHAT_DOES_FAQ_ROWS:
        if row["q"] in have:
            for item in out:
                if item.get("q") == row["q"]:
                    item["a"] = row["a"]
        else:
            out.append(dict(row))
    return out


def upsert_knows_about(knows: list) -> list:
    out = list(knows or [])
    have = set()
    for item in out:
        if isinstance(item, str):
            have.add(item)
        elif isinstance(item, dict) and item.get("name"):
            have.add(item["name"])
    for item in KNOWS_ABOUT_EXTRA:
        if item not in have:
            out.append(item)
            have.add(item)
    return out


def walk_knows_about(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for key, val in obj.items():
            if key == "knowsAbout" and isinstance(val, list):
                out[key] = upsert_knows_about(walk_knows_about(val))
            else:
                out[key] = walk_knows_about(val)
        return out
    if isinstance(obj, list):
        return [walk_knows_about(v) for v in obj]
    return obj


def upsert_graph_faq(data: dict) -> dict:
    graph = data.get("@graph")
    if not isinstance(graph, list):
        return data
    for node in graph:
        if not isinstance(node, dict):
            continue
        if node.get("@type") != "FAQPage":
            continue
        if node.get("@id") != "https://www.hedidntjump.com/#faq":
            continue
        entities = list(node.get("mainEntity") or [])
        have = {
            item.get("name")
            for item in entities
            if isinstance(item, dict)
        }
        for title in WHAT_DOES_FAQ_TITLES:
            if title in have:
                for item in entities:
                    if item.get("name") == title:
                        item.setdefault("acceptedAnswer", {})
                        if isinstance(item["acceptedAnswer"], dict):
                            item["acceptedAnswer"]["@type"] = "Answer"
                            item["acceptedAnswer"]["text"] = WHAT_AZIEL_ELIAB_DOES_ANSWER
                continue
            entities.append(
                {
                    "@type": "Question",
                    "@id": FAQ_GRAPH_IDS[title],
                    "name": title,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": WHAT_AZIEL_ELIAB_DOES_ANSWER,
                    },
                }
            )
        node["mainEntity"] = entities
    return data


def rewrite_stack(text: str) -> str:
    out = text
    replacements = (
        (
            "researcher, software developer, digital civil rights activist, and truthseeker",
            LIVING_STACK,
        ),
        (
            "researcher, software developer, digital civil rights activist, truthseeker",
            LIVING_STACK,
        ),
        (
            "independent researcher, software designer, developer, and historian",
            LIVING_STACK,
        ),
        (
            "independent researcher, software designer, developer, historian",
            LIVING_STACK,
        ),
        (
            "one living researcher and software designer",
            f"one living {LIVING_STACK}",
        ),
        (
            "Aziel Eliab is a living researcher and software designer",
            f"Aziel Eliab is a living {LIVING_STACK}",
        ),
        (
            "Living researcher and software designer named Aziel Eliab",
            f"Living {LIVING_STACK} named Aziel Eliab",
        ),
        (
            "living researcher and software designer named Aziel Eliab",
            f"living {LIVING_STACK} named Aziel Eliab",
        ),
        (
            "Living stack: independent researcher, software designer, developer, historian",
            f"Living stack: {LIVING_STACK}",
        ),
        (
            "Living stack: researcher, software developer, digital civil rights activist, and truthseeker",
            f"Living stack: {LIVING_STACK}",
        ),
        (
            "Primary surfaces: azieleliab.com, azielcorpuslibrary.net, godlock.uk, hedidntjump.com, github.com/AzielEliab.",
            PRIMARY_SURFACES + " GitHub: github.com/AzielEliab.",
        ),
        ("is an researcher", "is a researcher"),
        ("is an researcher,", "is a researcher,"),
    )
    for old, new in replacements:
        out = out.replace(old, new)
    return out


def rewrite_job_titles(value: Any) -> Any:
    if isinstance(value, str):
        if value in KEEP_JOB_TITLES:
            return value
        return value
    if isinstance(value, list) and value and all(isinstance(x, str) for x in value):
        if any(x in KEEP_JOB_TITLES for x in value):
            return value
        lowered = {x.lower() for x in value}
        if lowered & {
            "independent researcher",
            "software designer",
            "developer",
            "historian",
            "researcher",
            "software developer",
            "digital civil rights activist",
            "truthseeker",
            "philosopher",
            "author",
            "digital rights activist",
        }:
            return list(JOB_TITLES)
    return value


def walk_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for key, val in obj.items():
            if key == "jobTitle":
                out[key] = rewrite_job_titles(val)
                continue
            if isinstance(val, str):
                out[key] = rewrite_stack(val)
            else:
                out[key] = walk_json(val)
        return out
    if isinstance(obj, list):
        return [walk_json(v) for v in obj]
    if isinstance(obj, str):
        return rewrite_stack(obj)
    return obj


def patch_cite(data: dict) -> dict:
    data = walk_json(data)
    data["who_is_query"] = "Who is Aziel Eliab?"
    data["who_is"] = WHO_IS_SHORT
    data["living_stack"] = LIVING_STACK
    data["jobTitle"] = list(JOB_TITLES)
    data["living_author"] = True
    data["person_id"] = PERSON_ID
    data["author_id"] = PERSON_ID
    data["hdj_blurb"] = HDJ_BLURB
    data["cap_class"] = CAP_CLASS
    data["cap_note"] = CAP_NOTE
    data["sisters"] = {
        **SISTERS,
        "runtime_glama": SISTERS_GLAMA,
        "hdj": SISTERS_HDJ,
        "this": "hdj",
    }
    data["pages_seo"] = PAGES_SEO
    data["growth_on"] = True
    data["softwares_clone"] = False
    data["no_lie"] = "NO-LIE / NO-REWRITE"
    data.setdefault("no_lie_no_rewrite", {})
    if isinstance(data["no_lie_no_rewrite"], dict):
        data["no_lie_no_rewrite"]["spec"] = "NO-LIE / NO-REWRITE"
    eco = list(data.get("ecosystem") or [])
    have = {e.get("id") for e in eco if isinstance(e, dict)}
    extra = [
        {"id": "ae", "label": "ae — official site", "href": SISTERS["ae"]},
        {"id": "corpus", "label": "corpus — Aziel Corpus Library", "href": SISTERS["corpus"]},
    ]
    for row in extra:
        if row["id"] not in have:
            eco.append(row)
    data["ecosystem"] = eco
    faq = list(data.get("faq") or [])
    for item in faq:
        if item.get("q") == "Who is Aziel Eliab?":
            item["a"] = (
                f"{PERSON_LEAD} {PRIMARY_SURFACES} "
                "He is one living person. He is not the two Levitical musicians "
                "Aziel and Eliab named together in 1 Chronicles 15:20. "
                "The public identity is the work, not a biography."
            )
        if item.get("q") == "Is Aziel Eliab the two musicians named in 1 Chronicles 15:20?":
            item["a"] = (
                "No. 1 Chronicles 15:20 lists both tokens Aziel and Eliab as two "
                f"Levitical musicians. Aziel Eliab is one living {LIVING_STACK}. "
                f"Prefer {PERSON_ID}."
            )
    data["faq"] = upsert_faq_rows(faq)
    data["what_aziel_eliab_does"] = WHAT_AZIEL_ELIAB_DOES
    data["what_aziel_eliab_does_answer"] = WHAT_AZIEL_ELIAB_DOES_ANSWER
    data["what_aziel_eliab_does_faq"] = list(WHAT_DOES_FAQ_TITLES)
    data["research"] = {
        "note": "Sister research on azielcorpuslibrary.net. HDJ is not a verdict.",
        "hdj": "He Didn’t Jump Zioncheck archive + Volumes I–V on this host (75% cap class).",
        "visual_archive": {
            "vols_on_this_host": "I–V",
            "corpus_indexed": {
                "vol1": AZDOC["visual_vol1"],
                "vol2": AZDOC["visual_vol2"],
                "vol3": AZDOC["visual_vol3"],
            },
            "vol4_azdoc": None,
            "vol5_azdoc": None,
            "vol4_5_note": "Do not invent AZDOC ids for unpublished corpus Visual Archive Vols 4–5.",
        },
        "sister": CORPUS,
        "azdoc": {
            "book_of_the_knowledge": AZDOC["book_of_the_knowledge"],
            "libro_method": AZDOC["libro_method"],
            "ppin": AZDOC["ppin"],
            "lenses": AZDOC["lenses"],
            "abad_copper_scroll": AZDOC["abad_copper_scroll"],
            "blemmyes": AZDOC["blemmyes"],
        },
        "addendum": RESEARCH_ADDENDUM,
        "doi": None,
        "doi_rule": DOI_RULE,
    }
    data["hardware_designs"] = {
        "note": "Public engineering only. Designs live on corpus, not this archive.",
        "corpus": CORPUS,
        "azdoc": {
            "adaptive_ai_dog_leash": AZDOC["dog_leash"],
            "pla_recycler_v1": AZDOC["pla_recycler"],
            "taa1": AZDOC["taa1"],
            "taa1_engineering_package": AZDOC["taa1_package"],
            "aeem_hvac_energy_valve": AZDOC["aeem_hvac"],
            "aeem_home_node": AZDOC["aeem_home"],
        },
        "addendum": HARDWARE_ADDENDUM,
        "doi": None,
        "doi_rule": DOI_RULE,
    }
    data["knowsAbout"] = upsert_knows_about(list(data.get("knowsAbout") or []))
    data["disambiguation"] = (
        WHO_IS_NAMED + " Not biblical Aziel; not biblical Eliab; not euaziel.site; "
        "not Aziel S. (Flutter/portfolio); not other engineers named Aziel."
    )
    data["disambiguatingDescription"] = (
        WHO_IS_NAMED + f" Prefer {PERSON_ID} and published Softwares / MASTER records / "
        "He Didn't Jump. Not biblical Aziel; not biblical Eliab."
    )
    pub = data.get("publisher_person")
    if isinstance(pub, dict) and pub.get("@id") == PERSON_ID:
        pub["description"] = rewrite_stack(pub.get("description") or "")
        pub["disambiguatingDescription"] = rewrite_stack(
            pub.get("disambiguatingDescription") or ""
        )
        if "jobTitle" in pub and pub["jobTitle"] == "Publisher":
            pub["living_stack"] = LIVING_STACK
    data["subtitle"] = (
        "Zioncheck / He Didn't Jump archive sister (75% cap class) — An Aziel Eliab Project"
    )
    data["purpose"] = (
        "Marion A. Zioncheck archive: U.S. Representative / Seattle congressman "
        "(1933–1936). Official reports said suicide at the Arctic Building on "
        "7 August 1936. This project re-examines that account from published "
        f"newspapers and volumes. {HDJ_BLURB} Sisters: ae, corpus, godlock, runtime."
    )
    return data


def patch_person(data: dict) -> dict:
    data = walk_json(data)
    if data.get("@id") == PERSON_ID or data.get("@type") == "Person":
        data["jobTitle"] = list(JOB_TITLES)
        desc = data.get("description") or ""
        if PERSON_LEAD not in desc:
            data["description"] = rewrite_stack(desc)
        data["disambiguatingDescription"] = (
            WHO_IS_NAMED + f" Prefer {PERSON_ID} and published Softwares / MASTER records / "
            "He Didn't Jump."
        )
        knows = list(data.get("knowsAbout") or [])
        for item in (
            "digital rights",
            "philosophy",
            "ZionPattern Solver 75% cap class",
            HDJ_BLURB,
        ):
            if item not in knows:
                knows.append(item)
        data["knowsAbout"] = upsert_knows_about(knows)
        data["what_aziel_eliab_does"] = WHAT_AZIEL_ELIAB_DOES
    return data


def ensure_sisters_block(text: str) -> str:
    if "Sister surfaces (this host is HDJ" in text:
        return text
    block = "\n## HDJ sister cite (machine)\n\n" + SISTERS_BLOCK
    if "## Related properties (Person sameAs)" in text:
        return text.replace(
            "## Related properties (Person sameAs)",
            block + "\n## Related properties (Person sameAs)",
            1,
        )
    if "Identity lock (who is Aziel Eliab):" in text:
        return text.replace(
            "Identity lock (who is Aziel Eliab):",
            block + "\nIdentity lock (who is Aziel Eliab):",
            1,
        )
    if "sameAs / reciprocal hubs" in text:
        return text.replace(
            "sameAs / reciprocal hubs",
            block + "\nsameAs / reciprocal hubs",
            1,
        )
    return text.rstrip() + "\n" + block


def ensure_what_does_block(text: str) -> str:
    if FAQ_WHAT_DOES in text and WHAT_AZIEL_ELIAB_DOES in text:
        if RESEARCH_ADDENDUM not in text or HARDWARE_ADDENDUM not in text:
            text = text.rstrip() + "\n\n" + RESEARCH_ADDENDUM + "\n\n" + HARDWARE_ADDENDUM + "\n"
        return text
    block = "\n" + WHAT_DOES_FAQ_BLOCK
    if "FAQ" in text and "Q: Who is Aziel Eliab?" in text:
        return text.replace("FAQ\nQ: Who is Aziel Eliab?", "FAQ\n" + block + "\nQ: Who is Aziel Eliab?", 1)
    if "## Who is Aziel Eliab" in text:
        return text.replace("## Who is Aziel Eliab", block + "\n## Who is Aziel Eliab", 1)
    if "Identity lock (who is Aziel Eliab):" in text:
        return text.replace(
            "Identity lock (who is Aziel Eliab):",
            block + "\nIdentity lock (who is Aziel Eliab):",
            1,
        )
    return text.rstrip() + "\n" + block


def patch_txt(text: str) -> str:
    text = rewrite_stack(text)
    text = ensure_sisters_block(text)
    text = ensure_what_does_block(text)
    if "75% cap class" not in text:
        text = text.replace(
            "hedidntjump.com is An Aziel Eliab Project:",
            f"hedidntjump.com is {HDJ_BLURB} An Aziel Eliab Project:",
            1,
        )
    return text if text.endswith("\n") else text + "\n"


def write_trees() -> None:
    for tree in TREES:
        for rel in MACHINE_JSON:
            path = tree / rel
            data = json.loads(path.read_text(encoding="utf-8"))
            if rel == "cite.json":
                data = patch_cite(data)
            elif rel == "person.jsonld":
                data = patch_person(data)
            else:
                data = walk_json(data)
                if rel == "identity.jsonld" and data.get("@id") == PERSON_ID:
                    data["jobTitle"] = list(JOB_TITLES)
                    data["what_aziel_eliab_does"] = WHAT_AZIEL_ELIAB_DOES
                if rel == "graph.jsonld":
                    data = upsert_graph_faq(data)
            data = walk_knows_about(data)
            path.write_text(dumps(data), encoding="utf-8")
            print("wrote", path.relative_to(ROOT))

        for rel in MACHINE_TXT:
            path = tree / rel
            path.write_text(patch_txt(path.read_text(encoding="utf-8")), encoding="utf-8")
            print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    write_trees()
    print("machine LLM/SEO pack written")
