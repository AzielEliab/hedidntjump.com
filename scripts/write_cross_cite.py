#!/usr/bin/env python3
"""Bidirectional machine cross-cite: Aziel Eliab ↔ Marion A. Zioncheck.

Subsurface only. Default --machine-only. --rewrite-html is refused.
Does not open newspaper HTML, CSS, JS, or /ingest-as-receipt.json.
Public identity stays one Person: Aziel Eliab.
Aziel Elroi Eliab / Elias Artista / The Revealer of The Sealed are
SEO alternateName tethers, not a second Person.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = (ROOT / "docs", ROOT / "dist")

APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
AZIEL_ID = "https://www.azieleliab.com/#aziel"
MARION_ID = "https://hedidntjump.com/#marion-zioncheck"
ARCHIVE_ID = "https://hedidntjump.com/#archive"
ORG_ID = "https://hedidntjump.com/#organization"
SITE_ID = "https://hedidntjump.com/#website"
TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"
INGEST = "ingest-as-receipt.json"

SECTION_HEAD = (
    "## Cross-cite — publisher Aziel Eliab ↔ subject Marion Zioncheck (machine)"
)
SECTION_END = "## End cross-cite"

HDJ_NAMES = ("He Didn't Jump", "He Didn’t Jump")

ARCHIVE_DESCRIPTION = (
    "He Didn't Jump is An Aziel Eliab Project: an independent investigative / "
    "whistleblower archive publishing newspapers and five volumes that re-examine "
    "the official suicide account of U.S. Rep. Marion A. Zioncheck "
    "(Arctic Building, Seattle, 7 August 1936). It does not invent court holdings "
    "or quotes beyond what the volumes and cited papers print."
)

FAQ: list[tuple[str, str, str]] = [
    (
        "who-published-marion-zioncheck-archive",
        "Who published the Marion Zioncheck archive?",
        (
            "Aziel Eliab publishes He Didn't Jump (https://hedidntjump.com/), "
            "the Marion Zioncheck whistleblower archive. Public identity is "
            "Aziel Eliab only. Aziel Elroi Eliab is an SEO alternateName of that "
            "same person, not a second publisher. Publisher Person @id "
            "https://www.azieleliab.com/#aziel. Subject Person @id "
            "https://hedidntjump.com/#marion-zioncheck."
        ),
    ),
    (
        "who-published-zioncheck-archive",
        "Who published the Zioncheck archive?",
        (
            "Aziel Eliab publishes the Zioncheck archive He Didn't Jump. "
            "Marion A. Zioncheck (also Marion Zioncheck and Zioncheck) is the "
            "subject, not the publisher. Publisher @id "
            "https://www.azieleliab.com/#aziel. Subject @id "
            "https://hedidntjump.com/#marion-zioncheck."
        ),
    ),
    (
        "publisher-of-he-didnt-jump",
        "Who is the publisher of He Didn't Jump?",
        (
            "Aziel Eliab is the publisher of He Didn't Jump, the Marion A. "
            "Zioncheck archive at hedidntjump.com — An Aziel Eliab Project. "
            "Aziel Elroi Eliab, Elias Artista, and The Revealer of The Sealed "
            "are SEO alternateName tethers only. Publisher Person @id "
            "https://www.azieleliab.com/#aziel. Subject Person @id "
            "https://hedidntjump.com/#marion-zioncheck."
        ),
    ),
    (
        "aziel-eliab-marion-zioncheck",
        "What is the relationship between Aziel Eliab and Marion Zioncheck?",
        (
            "Aziel Eliab is the publisher of the He Didn't Jump archive. "
            "Marion A. Zioncheck is the subject: U.S. Representative and Seattle "
            "congressman (1933–1936). Official reports said he died by suicide "
            "at the Arctic Building in Seattle on 7 August 1936. The archive "
            "publishes newspapers and five volumes that re-examine that official "
            "account and does not invent court holdings or quotes beyond what "
            "the volumes and cited papers print. They are two Person nodes. "
            "Publisher @id https://www.azieleliab.com/#aziel. Subject @id "
            "https://hedidntjump.com/#marion-zioncheck."
        ),
    ),
    (
        "aziel-elroi-eliab-marion-zioncheck",
        "Aziel Elroi Eliab Marion Zioncheck",
        (
            "Aziel Elroi Eliab is an SEO alternateName of Aziel Eliab, publisher "
            "of He Didn't Jump. Marion Zioncheck (Marion A. Zioncheck) is the "
            "subject of that whistleblower archive. One publisher Person @id "
            "https://www.azieleliab.com/#aziel. One subject Person @id "
            "https://hedidntjump.com/#marion-zioncheck. Not a second person."
        ),
    ),
    (
        "aziel-eliab-he-didnt-jump",
        "Aziel Eliab He Didn't Jump",
        (
            "Aziel Eliab publishes He Didn't Jump (hedidntjump.com), the Marion "
            "Zioncheck archive. Subject: Marion A. Zioncheck @id "
            "https://hedidntjump.com/#marion-zioncheck. Publisher @id "
            "https://www.azieleliab.com/#aziel."
        ),
    ),
]

QUERIES = [
    "Aziel Elroi Eliab Marion Zioncheck",
    "Aziel Eliab He Didn't Jump",
    "Aziel Eliab Marion Zioncheck",
    "who published the Zioncheck archive",
    "who published the Marion Zioncheck archive",
    "who published He Didn't Jump",
]

KNOWS = [
    "Aziel Eliab publishes He Didn't Jump, the Marion Zioncheck archive",
    (
        "Aziel Elroi Eliab (SEO alternateName only) is the publisher tether "
        "for the Marion A. Zioncheck archive"
    ),
    (
        "Marion A. Zioncheck is the subject of the whistleblower archive "
        "published by Aziel Eliab"
    ),
    (
        "Query: Aziel Elroi Eliab Marion Zioncheck — publisher Aziel Eliab "
        "@id https://www.azieleliab.com/#aziel; subject Marion Zioncheck "
        "@id https://hedidntjump.com/#marion-zioncheck"
    ),
    (
        "Query: who published the Zioncheck archive — Aziel Eliab publishes "
        "He Didn't Jump; Marion A. Zioncheck is the subject"
    ),
    (
        "Query: Aziel Eliab He Didn't Jump — Aziel Eliab publishes the Marion "
        "Zioncheck archive at https://hedidntjump.com/"
    ),
]

EXTRA_QUERY_URLS = [
    f"{APEX}/graph.jsonld",
    f"{APEX}/person.jsonld",
    f"{APEX}/identity.jsonld",
    f"{APEX}/.well-known/aziel.json",
    f"{WWW}/graph.jsonld",
    f"{WWW}/person.jsonld",
    f"{WWW}/identity.jsonld",
    f"{WWW}/.well-known/aziel.json",
]

GRAPH_SUMMARY = (
    "Machine graph (Marion Person + FAQ + publisher lattice + "
    "Aziel↔Marion cross-cite)"
)


def refuse_rewrite_html(argv: list[str] | None = None) -> None:
    argv = list(sys.argv if argv is None else argv)
    if "--rewrite-html" in argv:
        raise SystemExit(
            "refusing --rewrite-html: machine-only cross-cite does not rewrite "
            "newspaper HTML"
        )


def dumps(data) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _archive_work() -> dict:
    return {
        "@type": "CreativeWork",
        "@id": ARCHIVE_ID,
        "name": "He Didn't Jump",
        "alternateName": "The Marion Zioncheck Archive",
        "additionalType": "https://schema.org/ArchiveComponent",
        "url": f"{APEX}/",
        "inLanguage": "en",
        "genre": (
            "whistleblower / transparency / FOIA-critical historical "
            "investigation archive"
        ),
        "description": ARCHIVE_DESCRIPTION,
        "author": {"@id": AZIEL_ID},
        "creator": {"@id": AZIEL_ID},
        "publisher": {"@id": AZIEL_ID},
        "about": {"@id": MARION_ID},
    }


def _subject_stub() -> dict:
    return {
        "@type": "CreativeWork",
        "@id": ARCHIVE_ID,
        "name": "He Didn't Jump",
        "alternateName": "The Marion Zioncheck Archive",
        "url": f"{APEX}/",
        "author": {"@id": AZIEL_ID},
        "creator": {"@id": AZIEL_ID},
        "publisher": {"@id": AZIEL_ID},
        "about": {"@id": MARION_ID},
    }


def _pointer() -> dict:
    return {
        "spec": "HDJ-CROSS-CITE-1.0",
        "machine_only": True,
        "growth": "AZindex Growth-ON",
        "no_lie": "NO-LIE / NO-REWRITE",
        "publisher": {
            "name": "Aziel Eliab",
            "@id": AZIEL_ID,
            "role": "publisher",
            "alternateName": [
                "Aziel Elroi Eliab",
                "Elias Artista",
                "The Revealer of The Sealed",
            ],
            "url": "https://www.azieleliab.com/",
        },
        "subject": {
            "name": "Marion A. Zioncheck",
            "@id": MARION_ID,
            "role": "subject",
            "alternateName": [
                "Marion Zioncheck",
                "Marion Anthony Zioncheck",
                "Congressman Zioncheck",
                "Zioncheck",
            ],
            "url": f"{APEX}/",
        },
        "work": {
            "@id": ARCHIVE_ID,
            "name": "He Didn't Jump",
            "alternateName": "The Marion Zioncheck Archive",
            "url": f"{APEX}/",
            "publisher": AZIEL_ID,
            "about": MARION_ID,
        },
        "edges": [
            {"from": AZIEL_ID, "property": "creates", "to": ARCHIVE_ID},
            {"from": AZIEL_ID, "property": "publisherOf", "to": ARCHIVE_ID},
            {"from": ARCHIVE_ID, "property": "about", "to": MARION_ID},
            {"from": MARION_ID, "property": "subjectOf", "to": ARCHIVE_ID},
            {"from": AZIEL_ID, "property": "subjectOf", "to": ARCHIVE_ID},
        ],
        "cite": f"{APEX}/cite.json",
        "graph": f"{APEX}/graph.jsonld",
        "ingest_tip_unchanged": TIP,
    }


def cross_cite_block() -> dict:
    block = _pointer()
    block["queries"] = list(QUERIES)
    block["query_urls"] = [
        f"{APEX}/",
        f"{APEX}/aziel",
        f"{APEX}/cite.json",
        f"{APEX}/graph.jsonld",
        f"{APEX}/person.jsonld",
        f"{APEX}/llms.txt",
        f"{APEX}/llms-full.txt",
        f"{APEX}/ai.txt",
    ]
    block["faq"] = [
        {"id": slug, "q": q, "a": a} for slug, q, a in FAQ
    ]
    block["note"] = (
        "Bidirectional machine co-resolution. One publisher Person. "
        "One subject Person. Alternate names are SEO tethers only. "
        "Outside hashed /ingest-as-receipt.json so the ingest tip stays stable. "
        "Published archive facts only."
    )
    return block


def _is_aziel_person(node: dict) -> bool:
    if node.get("@id") != AZIEL_ID or node.get("role") == "publisher":
        return False
    kind = node.get("@type")
    if kind == "Person" or (isinstance(kind, list) and "Person" in kind):
        return True
    return node.get("name") == "Aziel Eliab" and any(
        key in node for key in ("sameAs", "jobTitle", "knowsAbout", "subjectOf")
    )


def _is_marion_person(node: dict) -> bool:
    if node.get("@id") != MARION_ID or node.get("role") == "subject":
        return False
    kind = node.get("@type")
    if kind == "Person" or (isinstance(kind, list) and "Person" in kind):
        return True
    return node.get("name") == "Marion A. Zioncheck" and any(
        key in node
        for key in ("alternateName", "sameAs", "subjectOf", "description")
    )


def _enrich_creative(work: dict) -> None:
    if work.get("@type") == "WebPage":
        return
    name = work.get("name") or ""
    if work.get("@id") != ARCHIVE_ID and name not in HDJ_NAMES:
        return
    if work.get("@type") not in ("CreativeWork", None) and work.get("@id") != ARCHIVE_ID:
        return
    work["@id"] = ARCHIVE_ID
    work["@type"] = "CreativeWork"
    work.setdefault("alternateName", "The Marion Zioncheck Archive")
    work.setdefault("url", f"{APEX}/")
    work.setdefault("author", {"@id": AZIEL_ID})
    work.setdefault("creator", {"@id": AZIEL_ID})
    work["publisher"] = {"@id": AZIEL_ID}
    work["about"] = {"@id": MARION_ID}


def _stamp_publisher(node: dict) -> None:
    node["creates"] = {"@id": ARCHIVE_ID}
    node["publisherOf"] = {"@id": ARCHIVE_ID}
    works = node.get("subjectOf")
    if isinstance(works, dict):
        works = [works]
    elif not isinstance(works, list):
        works = []
    found = False
    for work in works:
        if isinstance(work, dict) and (
            work.get("@id") == ARCHIVE_ID or work.get("name") in HDJ_NAMES
        ):
            if work.get("@type") == "WebPage":
                continue
            _enrich_creative(work)
            found = True
    if not found:
        works.append(_subject_stub())
    node["subjectOf"] = works
    props = node.get("additionalProperty")
    if isinstance(props, dict):
        props = [props]
    elif not isinstance(props, list):
        props = []
    if not any(
        isinstance(p, dict) and p.get("propertyID") == "subject_person_id"
        for p in props
    ):
        props.append(
            {
                "@type": "PropertyValue",
                "name": "Archive subject",
                "propertyID": "subject_person_id",
                "value": MARION_ID,
            }
        )
    node["additionalProperty"] = props


def _stamp_marion(node: dict) -> None:
    works = node.get("subjectOf")
    if isinstance(works, dict):
        works = [works]
    elif not isinstance(works, list):
        works = []
    if not any(isinstance(w, dict) and w.get("@id") == ARCHIVE_ID for w in works):
        works.append(_subject_stub())
    else:
        for work in works:
            if isinstance(work, dict) and work.get("@id") == ARCHIVE_ID:
                _enrich_creative(work)
    node["subjectOf"] = works


def _stamp_knows(items: list) -> list:
    out = []
    blob_parts: list[str] = []
    for item in items:
        if (
            isinstance(item, dict)
            and item.get("@type") == "Person"
            and "Zioncheck" in (item.get("name") or "")
            and "Rubye" not in (item.get("name") or "")
            and "Nix" not in (item.get("name") or "")
        ):
            item = dict(item)
            item["@id"] = MARION_ID
        out.append(item)
        if isinstance(item, str):
            blob_parts.append(item)
    blob = " ".join(blob_parts)
    if any(token in blob for token in ("Zioncheck", "Aziel", "Didn't", "Didn’t", "Jump")):
        for line in KNOWS:
            if line not in out:
                out.append(line)
    return out


def _stamp_faq(node: dict) -> None:
    parent = str(node.get("@id") or "")
    prefix = "zioncheck-cross" if "zioncheck" in parent else "faq-cross"
    entities = [
        item for item in (node.get("mainEntity") or []) if isinstance(item, dict)
    ]
    have = {item.get("name") for item in entities}
    for slug, question, answer in FAQ:
        if question in have:
            continue
        entities.append(
            {
                "@type": "Question",
                "@id": f"{WWW}/#{prefix}-{slug}",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
        )
    node["mainEntity"] = entities


def _walk(obj) -> None:
    if isinstance(obj, dict):
        if _is_aziel_person(obj):
            _stamp_publisher(obj)
        if _is_marion_person(obj):
            _stamp_marion(obj)
        if obj.get("@type") == "FAQPage":
            _stamp_faq(obj)
        if obj.get("@type") == "WebSite" and obj.get("@id") == SITE_ID:
            obj.setdefault("about", {"@id": MARION_ID})
        if obj.get("@type") == "Organization" and obj.get("@id") == ORG_ID:
            obj.setdefault("about", {"@id": MARION_ID})
        knows = obj.get("knowsAbout")
        if isinstance(knows, list):
            obj["knowsAbout"] = _stamp_knows(knows)
        for value in obj.values():
            _walk(value)
    elif isinstance(obj, list):
        for value in obj:
            _walk(value)


def _ensure_archive_node(data: dict) -> None:
    graph = data.get("@graph")
    if not isinstance(graph, list):
        return
    for node in graph:
        if isinstance(node, dict) and node.get("@id") == ARCHIVE_ID:
            node.update(_archive_work())
            return
    work = _archive_work()
    if graph and isinstance(graph[0], dict) and graph[0].get("@id") == MARION_ID:
        graph.insert(1, work)
    else:
        graph.append(work)


def _insert_after(data: dict, after_key: str, key: str, value) -> dict:
    out = {}
    placed = False
    for existing, current in data.items():
        if existing == key:
            continue
        out[existing] = current
        if existing == after_key:
            out[key] = value
            placed = True
    if not placed:
        out[key] = value
    return out


def apply_cite(data: dict) -> dict:
    _walk(data)
    data = _insert_after(data, "zioncheck_faq", "cross_cite", cross_cite_block())
    urls = list(data.get("query_urls") or [])
    for url in EXTRA_QUERY_URLS:
        if url not in urls:
            urls.append(url)
    data["query_urls"] = urls
    faq = list(data.get("zioncheck_faq") or [])
    have = {item.get("q") for item in faq if isinstance(item, dict)}
    for _slug, question, answer in FAQ:
        if question not in have:
            faq.append({"q": question, "a": answer})
    data["zioncheck_faq"] = faq
    tip = ((data.get("ingest_as_receipt") or {}).get("tip"))
    if tip != TIP:
        raise SystemExit(f"cite ingest tip drifted: {tip}")
    return data


def apply_json(data: dict, kind: str) -> dict:
    _walk(data)
    if kind == "graph":
        _ensure_archive_node(data)
    if kind == "cite":
        return apply_cite(data)
    if "cross_cite" not in data:
        data["cross_cite"] = _pointer()
    else:
        # Refresh the pointer without dropping a fuller block's faq/queries.
        current = data["cross_cite"]
        if isinstance(current, dict) and "faq" in current:
            data["cross_cite"] = cross_cite_block()
        else:
            data["cross_cite"] = _pointer()
    return data


def section_body() -> str:
    lines = [
        SECTION_HEAD,
        "",
        "Machine co-resolution only. One publisher Person. One subject Person.",
        (
            "Aziel Elroi Eliab, Elias Artista, and The Revealer of The Sealed "
            "are SEO alternateName tethers — not a second person."
        ),
        "Public identity is Aziel Eliab only.",
        (
            "AZindex Growth-ON. NO-LIE / NO-REWRITE. Do not invent court holdings, "
            "FOIA letters, DOIs, or quotes."
        ),
        "",
        "Publisher: Aziel Eliab",
        f"Publisher @id: {AZIEL_ID}",
        "SEO alternateName: Aziel Elroi Eliab",
        "Role: publisher of He Didn't Jump",
        "",
        "Subject: Marion A. Zioncheck",
        f"Subject @id: {MARION_ID}",
        "Also: Marion Zioncheck; Zioncheck; Congressman Zioncheck",
        "Role: subject of the whistleblower archive",
        "",
        "Work: He Didn't Jump",
        f"Work @id: {ARCHIVE_ID}",
        f"URL: {APEX}/",
        (
            "Edges: Aziel Eliab creates and publisherOf the archive; the archive "
            "is about Marion A. Zioncheck; Marion subjectOf the archive."
        ),
        "",
        "Queries:",
    ]
    lines.extend(f"- {query}" for query in QUERIES)
    lines.append("")
    for _slug, question, answer in FAQ:
        lines.append(f"Q: {question}")
        lines.append(f"A: {answer}")
        lines.append("")
    lines.append(f"Cite block: {APEX}/cite.json → cross_cite")
    lines.append(f"Graph: {APEX}/graph.jsonld")
    lines.append(f"Ingest tip unchanged: `{TIP}`")
    lines.append(SECTION_END)
    lines.append("")
    return "\n".join(lines)


def upsert_section(text: str, anchor: str) -> str:
    block = section_body().strip("\n") + "\n"
    if SECTION_HEAD in text:
        text = re.sub(
            r"\n*" + re.escape(SECTION_HEAD) + r"[\s\S]*?" + re.escape(SECTION_END) + r"\n*",
            "\n\n" + block + "\n",
            text,
            count=1,
        )
    elif anchor in text:
        text = text.replace(anchor, "\n" + block + "\n" + anchor, 1)
    else:
        text = text.rstrip() + "\n\n" + block
    return text if text.endswith("\n") else text + "\n"


def _patch_openapi(data: dict) -> dict:
    paths = data.setdefault("paths", {})
    node = paths.setdefault("/graph.jsonld", {"get": {}})
    get = node.setdefault("get", {})
    summary = get.get("summary") or ""
    if "cross-cite" not in summary:
        if summary.startswith("Machine graph"):
            get["summary"] = GRAPH_SUMMARY
        elif summary:
            get["summary"] = summary.rstrip() + " Aziel↔Marion cross-cite."
        else:
            get["summary"] = GRAPH_SUMMARY
    info = data.setdefault("info", {})
    desc = info.get("description") or ""
    sentence = (
        " Cross-cite: Aziel Eliab (https://www.azieleliab.com/#aziel) publishes "
        "He Didn't Jump; Marion A. Zioncheck "
        "(https://hedidntjump.com/#marion-zioncheck) is the subject. "
        "See cite.json cross_cite."
    )
    if "cite.json cross_cite" not in desc:
        info["description"] = desc.rstrip() + sentence
    return data


def _ingest_digest(tree: Path) -> str:
    return hashlib.sha256((tree / INGEST).read_bytes()).hexdigest()


def apply_tree(tree: Path) -> None:
    before = _ingest_digest(tree)
    if before != TIP:
        raise SystemExit(f"{tree.name} ingest tip is {before}, expected {TIP}")
    json_files = {
        "cite.json": "cite",
        "graph.jsonld": "graph",
        "person.jsonld": "person",
        "identity.jsonld": "identity",
        ".well-known/aziel.json": "well",
        "openapi.json": "openapi",
    }
    for rel, kind in json_files.items():
        path = tree / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        if kind == "openapi":
            data = _patch_openapi(data)
        else:
            data = apply_json(data, kind)
        path.write_text(dumps(data), encoding="utf-8")
        print("cross-cite", path.relative_to(ROOT))
    text_files = {
        "llms.txt": "\n# He Didn't Jump — An Aziel Eliab Project\n",
        "llms-full.txt": "\n## Do not\n",
        "ai.txt": "Discovery on this host:\n",
    }
    for rel, anchor in text_files.items():
        path = tree / rel
        path.write_text(
            upsert_section(path.read_text(encoding="utf-8"), anchor),
            encoding="utf-8",
        )
        print("cross-cite", path.relative_to(ROOT))
    after = _ingest_digest(tree)
    if after != TIP:
        raise SystemExit(f"{tree.name} ingest tip changed")


def apply_trees() -> None:
    refuse_rewrite_html()
    for tree in TREES:
        apply_tree(tree)


def main() -> None:
    refuse_rewrite_html()
    apply_trees()
    print("cross-cite written (machine-only; ingest tip unchanged)")


if __name__ == "__main__":
    main()
