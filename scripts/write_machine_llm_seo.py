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
    CAP_CLASS,
    CAP_NOTE,
    HDJ_BLURB,
    JOB_TITLES,
    LIVING_STACK,
    OLD_STACK_PHRASES,
    PAGES_SEO,
    PERSON_ID,
    PERSON_LEAD,
    PRIMARY_SURFACES,
    SISTERS,
    SISTERS_GLAMA,
    SISTERS_HDJ,
    WHO_IS_NAMED,
    WHO_IS_SHORT,
    KEEP_JOB_TITLES,
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


def dumps(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


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
    data["faq"] = faq
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
        data["knowsAbout"] = knows
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


def patch_txt(text: str) -> str:
    text = rewrite_stack(text)
    text = ensure_sisters_block(text)
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
            path.write_text(dumps(data), encoding="utf-8")
            print("wrote", path.relative_to(ROOT))

        for rel in MACHINE_TXT:
            path = tree / rel
            path.write_text(patch_txt(path.read_text(encoding="utf-8")), encoding="utf-8")
            print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    write_trees()
    print("machine LLM/SEO pack written")
