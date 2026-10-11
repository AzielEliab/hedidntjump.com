#!/usr/bin/env python3
"""Stamp the canonical Aziel Person and verified works into docs/ and dist/.

Head JSON-LD and machine files only. Does not rewrite HTML bodies.
Rerunning this script reproduces the same files.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_living import JOB_TITLES
from aziel_person import (
    DISAMBIGUATING_DESCRIPTION,
    KNOWS_ABOUT_DOMAINS,
    MONIKERS,
    PERSON_ID,
    PERSON_NAME,
    alternate_names,
    hebrew_property,
    occupations,
)
from aziel_works import (
    TRIAD_ID,
    WORKS_URL,
    full_records,
    person_works,
    triad_markdown,
    triad_node,
    triad_side_note,
    works_document,
)

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "docs", ROOT / "dist"]
ARCHIVE_ID = "https://hedidntjump.com/#archive"
LD_RE = re.compile(
    r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)'
)
WORKS_HEAD = "## Body of work (verified catalog)"
WORKS_END = "## End body of work"
OLD_DD_SHORT = (
    "Living author of He Didn’t Jump / Zioncheck archive. "
    "Public identity is Aziel Eliab only. Prefer https://www.azieleliab.com/#aziel."
)
OLD_AKA_LINE = (
    "alternateName (SEO only): Aziel Elroi Eliab; The Revealer of The Sealed; "
    "Revealer of The Sealed; Elias Artista"
)
NEW_AKA_LINE = (
    "alternateName (SEO only): "
    + "; ".join([*MONIKERS, "The Revealer of The Sealed", "Revealer of The Sealed"])
)
OLD_ALSO = (
    "- Also: Aziel Elroi Eliab; Elias Artista; The Revealer of The Sealed"
)
NEW_ALSO = "- Also: " + "; ".join(
    [*MONIKERS, "The Revealer of The Sealed"]
)
ROLES_LINE = "jobTitle: " + "; ".join(JOB_TITLES)

WORKS_HTML = {"index.html", "aziel.html"}
PROFILE_HTML = {"aziel.html"}


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def _is_aziel_person(node: dict) -> bool:
    if node.get("@id") != PERSON_ID:
        return False
    kind = node.get("@type")
    if kind == "Person":
        return True
    if isinstance(kind, list) and "Person" in kind:
        return True
    return False


def _knows(node: dict) -> None:
    knows = node.get("knowsAbout")
    if isinstance(knows, str):
        knows = [knows]
    elif not isinstance(knows, list):
        knows = []
    for domain in KNOWS_ABOUT_DOMAINS:
        if domain not in knows:
            knows.append(domain)
    node["knowsAbout"] = knows


def _hebrew(node: dict) -> None:
    props = node.get("additionalProperty")
    if isinstance(props, dict):
        props = [props]
    elif not isinstance(props, list):
        props = []
    if not any(
        isinstance(prop, dict) and prop.get("propertyID") == "hebrewDefinition"
        for prop in props
    ):
        props.append(hebrew_property())
    node["additionalProperty"] = props
    node.pop("hebrewDefinition", None)


def _merge_subject(node: dict, works: list[dict]) -> None:
    existing = node.get("subjectOf")
    if isinstance(existing, dict):
        existing = [existing]
    elif not isinstance(existing, list):
        existing = []
    kept = []
    for work in existing:
        work_id = str(work.get("@id") or "") if isinstance(work, dict) else ""
        if work_id.endswith("#aziel-work") or work_id == TRIAD_ID:
            continue
        if isinstance(work, dict) and work.get("@id") == ARCHIVE_ID:
            kept.append(work)
            continue
        kept.append(work)
    have = {work.get("@id") for work in kept if isinstance(work, dict)}
    for work in works:
        if work.get("@id") not in have:
            kept.append(work)
    node["subjectOf"] = kept
    node["workExample"] = works


def stamp_person(node: dict, *, with_works: bool, works: list[dict]) -> None:
    aka = node.get("alternateName")
    if isinstance(aka, str):
        aka = [aka]
    node["@type"] = "Person"
    node["@id"] = PERSON_ID
    node["name"] = PERSON_NAME
    node["alternateName"] = alternate_names(aka if isinstance(aka, list) else None)
    node["jobTitle"] = list(JOB_TITLES)
    node["hasOccupation"] = occupations()
    node["disambiguatingDescription"] = DISAMBIGUATING_DESCRIPTION
    _hebrew(node)
    _knows(node)
    if with_works:
        _merge_subject(node, works)


def walk(obj, *, with_works: bool, works: list[dict]) -> None:
    if isinstance(obj, dict):
        if _is_aziel_person(obj):
            stamp_person(obj, with_works=with_works, works=works)
        for value in obj.values():
            walk(value, with_works=with_works, works=works)
    elif isinstance(obj, list):
        for value in obj:
            walk(value, with_works=with_works, works=works)


def _profile_page() -> dict:
    return {
        "@type": "ProfilePage",
        "@id": "https://hedidntjump.com/aziel#profile",
        "url": "https://hedidntjump.com/aziel",
        "name": "Who is Aziel Eliab — About Aziel — He Didn't Jump",
        "mainEntity": {"@id": PERSON_ID},
        "about": {"@id": PERSON_ID},
    }


def ensure_profile(data: dict) -> None:
    graph = data.get("@graph")
    if not isinstance(graph, list):
        return
    for node in graph:
        if isinstance(node, dict) and node.get("@type") == "ProfilePage":
            node["mainEntity"] = {"@id": PERSON_ID}
            node.setdefault("url", "https://hedidntjump.com/aziel")
            return
    graph.append(_profile_page())


def stamp_json_file(path: Path, *, with_works: bool, works: list[dict]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    walk(data, with_works=with_works, works=works)
    if path.name == "cite.json" and isinstance(data, dict):
        data["jobTitle"] = list(JOB_TITLES)
        data["hasOccupation"] = occupations()
        data["disambiguatingDescription"] = DISAMBIGUATING_DESCRIPTION
        data["works"] = full_records()
        data["works_url"] = WORKS_URL
        data["az_triad"] = triad_node()
    if path.name == "aziel.json" and isinstance(data, dict):
        aka = data.get("alternateName")
        if isinstance(aka, str):
            aka = [aka]
        if isinstance(aka, list):
            data["alternateName"] = alternate_names(aka)
        data["disambiguatingDescription"] = DISAMBIGUATING_DESCRIPTION
        data["jobTitle"] = list(JOB_TITLES)
        data["hasOccupation"] = occupations()
        data["works_url"] = WORKS_URL
    path.write_text(dumps(data), encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def stamp_html(path: Path, *, works: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    with_works = path.name in WORKS_HTML

    def repl(match: re.Match) -> str:
        raw = match.group(2).strip()
        data = json.loads(raw)
        walk(data, with_works=with_works, works=works)
        if path.name in PROFILE_HTML and isinstance(data, dict):
            ensure_profile(data)
        body = json.dumps(data, indent=2, ensure_ascii=False)
        return match.group(1) + "\n" + body + "\n" + match.group(3)

    if not LD_RE.search(text):
        raise SystemExit(f"{path}: JSON-LD present but not stamped")
    new = LD_RE.sub(repl, text)
    path.write_text(new, encoding="utf-8")
    print("html", path.relative_to(ROOT))


def works_markdown() -> str:
    lines = [
        WORKS_HEAD,
        "",
        "Verified works of Aziel Eliab (http 200). Caution items and Zenodo DOI links are omitted.",
        f"Machine file: {WORKS_URL}",
        f"Person @id: {PERSON_ID}",
        "",
        ROLES_LINE,
        "",
        DISAMBIGUATING_DESCRIPTION,
        "",
        triad_markdown(),
        "",
    ]
    current = None
    for record in full_records():
        category = record.get("category")
        if category != current:
            current = category
            lines.append(f"### {category}")
            lines.append("")
        line = f"- {record['name']} — {record['url']}"
        note = triad_side_note(record["url"])
        if note:
            line += f" — {note}"
        lines.append(line)
    lines.append("")
    lines.append(WORKS_END)
    return "\n".join(lines)


def _swap_works_section(text: str) -> str:
    block = works_markdown()
    pattern = re.compile(
        re.escape(WORKS_HEAD) + r"[\s\S]*?" + re.escape(WORKS_END) + r"\n?"
    )
    if pattern.search(text):
        return pattern.sub(block + "\n", text, count=1)
    marker = "## Aziel publisher name lattice (machine)"
    if marker in text:
        return text.replace(marker, block + "\n\n" + marker, 1)
    return text.rstrip() + "\n\n" + block + "\n"


def stamp_text(path: Path, *, full_works: bool) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(OLD_DD_SHORT, DISAMBIGUATING_DESCRIPTION)
    text = text.replace(OLD_AKA_LINE, NEW_AKA_LINE)
    text = text.replace(OLD_ALSO, NEW_ALSO)
    if "jobTitle: Digital rights activist" not in text and NEW_AKA_LINE in text:
        text = text.replace(NEW_AKA_LINE, NEW_AKA_LINE + "\n" + ROLES_LINE, 1)
    if full_works:
        text = _swap_works_section(text)
    elif WORKS_URL not in text:
        text = text.rstrip() + (
            f"\n\nBody of work (verified catalog): {WORKS_URL}\n"
            f"{ROLES_LINE}\n{DISAMBIGUATING_DESCRIPTION}\n"
        )
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")
    print("text", path.relative_to(ROOT))


def main() -> None:
    works = person_works()
    document = dumps(works_document())
    json_names = (
        "person.jsonld",
        "identity.jsonld",
        "graph.jsonld",
        "cite.json",
        ".well-known/aziel.json",
    )
    for tree in TREES:
        (tree / "works.json").write_text(document, encoding="utf-8")
        print("wrote", (tree / "works.json").relative_to(ROOT))
        for name in json_names:
            stamp_json_file(
                tree / name,
                with_works=name == "person.jsonld",
                works=works,
            )
        for html in sorted(tree.glob("*.html")):
            if "application/ld+json" not in html.read_text(encoding="utf-8"):
                continue
            stamp_html(html, works=works)
        for name in ("llms.txt", "llms-full.txt"):
            stamp_text(tree / name, full_works=True)
        for name in ("ai.txt", "who-is-aziel-eliab.txt", "who-is"):
            stamp_text(tree / name, full_works=False)
    print("aziel identity + works stamped")


if __name__ == "__main__":
    main()
