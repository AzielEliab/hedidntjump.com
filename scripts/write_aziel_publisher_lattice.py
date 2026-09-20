#!/usr/bin/env python3
"""Stamp full Aziel publisher lattice onto machine surfaces only.

Does not rewrite Marion Zioncheck money-page H1/title/visible chrome.
Adds name lattice + Hebrew definition + both GitHub sameAs to Person nodes.
Writes dist/ and docs/.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_person import (
    CANONICAL_URL,
    CROSS_TETHER_ROUTES,
    GITHUB_PRIMARY,
    GITHUB_REVEALER,
    HEBREW_AKA,
    HEBREW_ONELINER,
    HUB_SAME_AS,
    MISSPELLINGS,
    NEVER_SAME_AS,
    PERSON_ID,
    PERSON_NAME,
    REQUIRED_AKA,
    REQUIRED_SAME_AS,
    WWW,
    dumps,
    enrich_ld,
    enrich_person_node,
    publisher_person,
    same_as,
)

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]

HTML_PAGES = (
    "index.html",
    "case.html",
    "aziel.html",
    "who.html",
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
)

MONEY_PAGES = {"index.html", "case.html"}

LD_RE = re.compile(r'<script type="application/ld\+json">([\s\S]*?)</script>')

REL_ME_REVEALER = f'<link rel="me" href="{GITHUB_REVEALER}">'
REL_ME_PRIMARY = f'<link rel="me" href="{GITHUB_PRIMARY}">'


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict) -> None:
    path.write_text(dumps(data) + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def enrich_person_file(path: Path) -> None:
    data = _load_json(path)
    if data.get("@type") == "Person" or data.get("@id") == PERSON_ID:
        data = enrich_person_node(data)
    elif "person" in data and isinstance(data["person"], dict):
        data["person"] = enrich_person_node(data["person"])
        if data.get("@id") == PERSON_ID or data.get("mainEntity"):
            data = enrich_ld(data)
    else:
        data = enrich_ld(data)
    data["hebrewDefinition"] = HEBREW_ONELINER
    data["hebrewAka"] = {**data.get("hebrewAka", {}), **HEBREW_AKA}
    _write_json(path, data)


def enrich_graph(path: Path) -> None:
    data = enrich_ld(_load_json(path))
    for node in data.get("@graph", []):
        if node.get("@type") == "AboutPage":
            links = list(node.get("significantLink") or [])
            for url in CROSS_TETHER_ROUTES:
                if url not in links:
                    links.append(url)
            node["significantLink"] = links
    data["hebrewDefinition"] = HEBREW_ONELINER
    data["hebrewAka"] = {**data.get("hebrewAka", {}), **HEBREW_AKA}
    _write_json(path, data)


def enrich_well_known(path: Path) -> None:
    data = _load_json(path)
    data["name"] = PERSON_NAME
    data["person_id"] = PERSON_ID
    data["hebrewDefinition"] = HEBREW_ONELINER
    data["hebrewAka"] = {**data.get("hebrewAka", {}), **HEBREW_AKA}
    aka = data.get("alternateName") or []
    if isinstance(aka, str):
        aka = [aka]
    for name in REQUIRED_AKA:
        if name not in aka:
            aka.insert(0 if name == REQUIRED_AKA[0] else len(aka), name)
    # Keep required names first.
    ordered = []
    for name in REQUIRED_AKA:
        if name in aka and name not in ordered:
            ordered.append(name)
    ordered.extend(n for n in aka if n not in ordered)
    data["alternateName"] = ordered
    data["sameAs"] = same_as(data.get("sameAs"))
    data["github"] = GITHUB_PRIMARY
    data["github_revealer"] = GITHUB_REVEALER
    if isinstance(data.get("person"), dict):
        data["person"] = enrich_person_node(data["person"])
    _write_json(path, data)


def enrich_cite(path: Path) -> None:
    data = _load_json(path)
    data["author"] = PERSON_NAME
    data["author_id"] = PERSON_ID
    data["identity"] = PERSON_NAME
    data["person_id"] = PERSON_ID
    data["hebrewDefinition"] = HEBREW_ONELINER
    data["hebrewAka"] = HEBREW_AKA
    aka = data.get("alternateName")
    names = [aka] if isinstance(aka, str) else list(aka or [])
    for name in REQUIRED_AKA:
        if name not in names:
            names.append(name)
    data["alternateName"] = names
    data["github"] = GITHUB_PRIMARY
    data["github_person"] = GITHUB_PRIMARY
    data["github_revealer"] = GITHUB_REVEALER
    data["sameAs"] = same_as(data.get("sameAs"))
    data["hubs"] = HUB_SAME_AS
    data["publisher_person"] = publisher_person(job_title="Publisher")
    data["identity_note"] = (
        "Aziel Eliab only. Aziel Elroi Eliab, Elias Artista, and "
        "The Revealer of The Sealed are SEO alternateName tethers only. "
        f"Shared Person @id is {PERSON_ID}. "
        "Never sameAs euaziel.site."
    )
    positive = (
        "Living author of He Didn't Jump / Zioncheck archive. "
        "Public identity is Aziel Eliab only."
    )
    for key in ("disambiguation", "disambiguatingDescription"):
        val = data.get(key) or ""
        if "Public identity is Aziel Eliab only" not in val:
            data[key] = (val.rstrip().rstrip(".") + ". " + positive).strip()
    data.pop("not", None)
    _write_json(path, data)


LATTICE_TXT = f"""Name lattice (SEO / schema alternateName only — one Person)
- {PERSON_NAME}
- Aziel Elroi Eliab
- Elias Artista
- The Revealer of The Sealed
Never a flower pen name.

Hebrew definition
{HEBREW_ONELINER}

GitHub sameAs
- {GITHUB_PRIMARY}
- {GITHUB_REVEALER}

Hub sameAs
- {CANONICAL_URL}
- https://www.azielcorpuslibrary.net/
- https://godlock.uk/
- {WWW}/

X sameAs
- https://x.com/AzielEliab

Glama / Try on Glama
- https://glama.ai/mcp/servers/AzielEliab/aziel-runtime
"""


def archive_who_is() -> str:
    """HDJ archive who-is (Marion / FOIA / volumes) plus publisher name lattice.

    Never start from the short hub who-is. Identity-machine text is the body;
    lattice lines are required on top.
    """
    import write_identity_machine as identity

    text = identity.who_is_txt()
    if "Elias Artista" not in text:
        text = text.replace(
            "alternateName (SEO only):",
            "alternateName (SEO only): Elias Artista;",
            1,
        )
    if HEBREW_ONELINER not in text:
        text = text.replace(
            "additionalName: Elroi\n",
            f"additionalName: Elroi\nHebrew: {HEBREW_ONELINER}\n",
            1,
        )
    for url in (GITHUB_PRIMARY, GITHUB_REVEALER):
        if url not in text:
            text = text.replace(
                "sameAs / reciprocal hubs\n",
                f"sameAs / reciprocal hubs\n- {url}\n",
                1,
            )
    if LATTICE_TXT.splitlines()[0] not in text:
        text = text.rstrip() + "\n\n" + LATTICE_TXT
    required = (
        "Marion Zioncheck",
        "FOIA Binary Acknowledgement",
        "official-narrative",
        "five volumes",
        "An Aziel Eliab Project",
        "living author of He Didn’t Jump",
        "Elias Artista",
        HEBREW_ONELINER,
        GITHUB_PRIMARY,
        GITHUB_REVEALER,
        "https://www.hedidntjump.com/api/stats",
    )
    missing = [n for n in required if n not in text]
    if missing:
        raise SystemExit(f"who-is missing archive/lattice substance: {missing}")
    if re.search(r"(?i)(?<!never: )Everblooming Flower", text):
        raise SystemExit("banned aka leaked into who-is")
    return text if text.endswith("\n") else text + "\n"


def write_who_is_pair(tree: Path) -> None:
    body = archive_who_is()
    for name in ("who-is", "who-is-aziel-eliab.txt"):
        path = tree / name
        path.write_text(body, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


def enrich_llms(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    block = (
        "\n## Aziel publisher name lattice (machine)\n\n"
        f"{LATTICE_TXT}\n"
        f"Person @id: {PERSON_ID}\n"
        "Never sameAs euaziel.site. Public identity is Aziel Eliab only.\n"
    )
    if "## Aziel publisher name lattice (machine)" in text:
        text = re.sub(
            r"## Aziel publisher name lattice \(machine\)[\s\S]*?(?=\n## |\n# |\Z)",
            block.lstrip(),
            text,
            count=1,
        )
    elif "## Related properties (Person sameAs)" in text:
        text = text.replace(
            "## Related properties (Person sameAs)",
            block.lstrip() + "\n## Related properties (Person sameAs)",
            1,
        )
    else:
        text = text.rstrip() + "\n" + block
    for url in (GITHUB_PRIMARY, GITHUB_REVEALER):
        if url not in text:
            text = text.replace(
                "- [GitHub AzielEliab](https://github.com/AzielEliab)\n",
                "- [GitHub AzielEliab](https://github.com/AzielEliab)\n"
                f"- [GitHub azieltherevealerofthesealed-arch]({GITHUB_REVEALER})\n",
                1,
            )
            if url not in text:
                text = text.rstrip() + f"\n- {url}\n"
    if "Elias Artista" not in text:
        text = text.replace(
            "Aziel Eliab (also Aziel Elroi Eliab)",
            "Aziel Eliab (also Aziel Elroi Eliab; Elias Artista; The Revealer of The Sealed)",
        )
    if HEBREW_ONELINER not in text:
        text = text.replace(
            "Hebrew forms are SEO aka tethers for the living author’s given name and surname only.",
            "Hebrew forms are SEO aka tethers for the living author’s given name and surname only. "
            + HEBREW_ONELINER,
            1,
        )
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def enrich_ai(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    extra = (
        "\nPublisher name lattice:\n"
        f"- Name: {PERSON_NAME}\n"
        "- Also: Aziel Elroi Eliab; Elias Artista; The Revealer of The Sealed\n"
        "- Never a flower pen name\n"
        f"- Hebrew: {HEBREW_ONELINER}\n"
        f"- GitHub: {GITHUB_PRIMARY}\n"
        f"- GitHub: {GITHUB_REVEALER}\n"
        f"- X @AzielEliab: https://x.com/AzielEliab\n"
        f"- Try on Glama: https://glama.ai/mcp/servers/AzielEliab/aziel-runtime\n"
        f"- Person @id: {PERSON_ID}\n"
        f"- Hubs: {', '.join(HUB_SAME_AS)}\n"
    )
    if "Publisher name lattice:" in text:
        text = re.sub(
            r"\nPublisher name lattice:[\s\S]*$",
            extra,
            text,
        )
    else:
        text = text.rstrip() + extra
    if GITHUB_REVEALER not in text:
        text = text.replace(
            f"GitHub: {GITHUB_PRIMARY}/hedidntjump.com",
            f"GitHub: {GITHUB_PRIMARY}/hedidntjump.com\n"
            f"Person GitHub: {GITHUB_PRIMARY}\n"
            f"Person GitHub: {GITHUB_REVEALER}",
            1,
        )
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def _insert_jsonld(text: str, graph: dict) -> str:
    block = (
        '<script type="application/ld+json">\n'
        + dumps(graph)
        + "\n</script>\n"
    )
    return text.replace("</head>", block + "</head>", 1)


def enrich_html(path: Path, *, money: bool) -> None:
    text = path.read_text(encoding="utf-8")
    title_before = re.search(r"<title>([^<]*)</title>", text)
    h1_before = re.search(r"<h1\b[^>]*>[\s\S]*?</h1>", text)

    matches = list(LD_RE.finditer(text))
    if not matches:
        text = _insert_jsonld(
            text,
            {"@context": "https://schema.org", "@graph": [publisher_person()]},
        )
    else:
        # Walk last-to-first so offsets stay valid.
        for m in reversed(matches):
            raw = m.group(1)
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}: invalid JSON-LD: {exc}") from exc
            data = enrich_ld(data, money=money)
            new = (
                '<script type="application/ld+json">\n'
                + dumps(data)
                + "\n</script>"
            )
            text = text[: m.start()] + new + text[m.end() :]

    if REL_ME_PRIMARY in text and REL_ME_REVEALER not in text:
        text = text.replace(REL_ME_PRIMARY, REL_ME_PRIMARY + "\n" + REL_ME_REVEALER, 1)

    title_after = re.search(r"<title>([^<]*)</title>", text)
    h1_after = re.search(r"<h1\b[^>]*>[\s\S]*?</h1>", text)
    if title_before and title_after and title_before.group(1) != title_after.group(1):
        raise SystemExit(f"{path}: title changed")
    if h1_before and h1_after and h1_before.group(0) != h1_after.group(0):
        raise SystemExit(f"{path}: H1 changed")
    if "Everblooming Flower" in text:
        raise SystemExit(f"{path}: banned aka")
    path.write_text(text, encoding="utf-8")
    print("html", path.relative_to(ROOT))


def guard_same_as() -> None:
    blob = " ".join(REQUIRED_SAME_AS + HUB_SAME_AS).lower()
    for banned in NEVER_SAME_AS:
        if banned.lower() in blob:
            raise SystemExit(f"sameAs must not include {banned}")


def main() -> None:
    guard_same_as()
    for tree in TREES:
        enrich_person_file(tree / "person.jsonld")
        enrich_person_file(tree / "identity.jsonld")
        enrich_graph(tree / "graph.jsonld")
        enrich_well_known(tree / ".well-known" / "aziel.json")
        enrich_cite(tree / "cite.json")
        write_who_is_pair(tree)
        enrich_llms(tree / "llms.txt")
        enrich_llms(tree / "llms-full.txt")
        enrich_ai(tree / "ai.txt")
        for name in HTML_PAGES:
            path = tree / name
            if path.is_file():
                enrich_html(path, money=name in MONEY_PAGES)
    print("aziel publisher lattice written")


if __name__ == "__main__":
    main()
