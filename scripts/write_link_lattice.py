#!/usr/bin/env python3
"""Soft internal link lattice + plain-text sitemap for hedidntjump.com.

Machine files only (docs/ and dist/). Does not open HTML/CSS/JS for writing.
Published newspaper tabs, reader volumes, and PDFs cross-reference each other.
NO-LIE. Whistleblower archive framing. Does not invent holdings.
Does not change the HDJ ingest tip.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "docs", ROOT / "dist"]
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
PERSON_ID = "https://www.azieleliab.com/#aziel"
SUBJECT_ID = f"{APEX}/#marion-zioncheck"
# Cite only. ingest-as-receipt.json bytes stay untouched.
HDJ_INGEST_TIP = "ef967e4acb47ba913ce3959b673767278da605b307de33210b2dc2f1cfd86f60"
LASTMOD = "2026-10-01"

MARKER_START = "## Soft link lattice (machine)"
MARKER_END = "## End soft link lattice"

FRAMING = (
    "whistleblower / transparency / FOIA-critical historical investigation archive"
)

# Short honest labels already used on this host. Not new holdings.
TABS: list[dict[str, str]] = [
    {
        "id": "home",
        "label": "Money page — Marion A. Zioncheck whistleblower archive",
        "href": f"{APEX}/",
    },
    {
        "id": "case",
        "label": "Case edition",
        "href": f"{APEX}/case",
    },
    {
        "id": "volumes",
        "label": "Volumes I–V desk",
        "href": f"{APEX}/volumes",
    },
    {
        "id": "inquiries",
        "label": "23 inquiries of the record",
        "href": f"{APEX}/inquiries",
    },
    {
        "id": "press",
        "label": "Press tip and investigative source directory",
        "href": f"{APEX}/press",
    },
    {
        "id": "rubye",
        "label": "Rubye paper",
        "href": f"{APEX}/rubye",
    },
    {
        "id": "foia",
        "label": "FOIA paper (supplied FBI FOIPA no-records only)",
        "href": f"{APEX}/foia",
    },
    {
        "id": "archives",
        "label": "Archive and volume downloads",
        "href": f"{APEX}/archives",
    },
    {
        "id": "narrative",
        "label": "Official-account contrast",
        "href": f"{APEX}/official-narrative",
    },
    {
        "id": "about-aziel",
        "label": "About Aziel (one body)",
        "href": f"{APEX}/aziel",
    },
    {
        "id": "copyrights",
        "label": "Copyrights and historical-research notice",
        "href": f"{APEX}/copyrights",
    },
    {
        "id": "reader",
        "label": "Facsimile volume reader",
        "href": f"{APEX}/reader",
    },
]

VOLUMES: list[tuple[int, str, str]] = [
    (1, "I", "Primary Documents & Forensic Analysis"),
    (2, "II", "News Coverage & Family Battles"),
    (3, "III", "Personal Photographs & Research Materials"),
    (4, "IV", "The Physics Case"),
    (5, "V", "The Human & Institutional Evidence"),
]

# Same body as an existing tab. Listed so crawlers do not treat them as extra holdings.
ALIASES: list[tuple[str, str]] = [
    (f"{APEX}/aziel", "/AboutAziel 301s here (same body as /aziel)"),
    (f"{APEX}/aziel", "/Aziel 301s here (same body as /aziel)"),
    (f"{APEX}/aziel", "/AzielEliab 301s here (same body as /aziel)"),
    (f"{APEX}/inquiries", "/inquires 301s here (same body as /inquiries)"),
    (f"{APEX}/rubye", "/Rubeye 301s here (same body as /rubye)"),
    (f"{APEX}/archives", "/Archive 301s here (same body as /archives)"),
]

MACHINE: list[tuple[str, str]] = [
    (f"{APEX}/llms.txt", "LLM brief"),
    (f"{APEX}/llms-full.txt", "Whole-project LLM review"),
    (f"{APEX}/ai.txt", "AI crawl aid"),
    (f"{APEX}/help.txt", "Human help"),
    (f"{APEX}/addendum.txt", "Human addendum"),
    (f"{APEX}/help/how-to-read.txt", "How to read the papers and volumes"),
    (f"{APEX}/cite.json", "Citation lattice"),
    (f"{APEX}/shelves", "COLD-MULTI-SHELF JSON (corpus sister cite)"),
    (f"{APEX}/shelves.json", "Same COLD-MULTI-SHELF JSON as /shelves"),
    (f"{APEX}/shelves.txt", "This plain-text sitemap"),
    (f"{APEX}/sitemap.txt", "Alias of /shelves.txt"),
    (f"{APEX}/sitemap.xml", "XML sitemap"),
    (f"{APEX}/robots.txt", "robots (Growth-ON)"),
    (f"{APEX}/openapi.json", "Read-only public surfaces"),
]


def volume_nodes() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for number, roman, title in VOLUMES:
        rows.append(
            {
                "id": f"reader-{number}",
                "label": f"Volume {roman} reader — {title}",
                "href": f"{APEX}/reader?volume={number}&page=1",
            }
        )
        rows.append(
            {
                "id": f"pdf-{number}",
                "label": f"Volume {roman} PDF — {title}",
                "href": f"{APEX}/volumes/volume-{number}.pdf",
            }
        )
    rows.append(
        {
            "id": "foia-transcript",
            "label": "FOIA Binary citation transcript (labeled transcript)",
            "href": f"{APEX}/assets/foia-binary-acknowledgement.pdf",
        }
    )
    return rows


def lattice_nodes() -> list[dict[str, object]]:
    base = [dict(row) for row in TABS] + volume_nodes()
    ids = [str(row["id"]) for row in base]
    out: list[dict[str, object]] = []
    for row in base:
        out.append(
            {
                "id": row["id"],
                "label": row["label"],
                "href": row["href"],
                "see_also": [i for i in ids if i != row["id"]],
            }
        )
    return out


def public_url_lattice() -> dict:
    return {
        "spec": "HDJ-LINK-LATTICE-1.0",
        "kind": "soft-internal",
        "framing": FRAMING,
        "no_lie": True,
        "growth_on": True,
        "invented_holdings": False,
        "map": f"{APEX}/shelves.txt",
        "map_alias": f"{APEX}/sitemap.txt",
        "publisher_id": PERSON_ID,
        "subject_id": SUBJECT_ID,
        "ingest_tip": HDJ_INGEST_TIP,
        "nodes": lattice_nodes(),
    }


def dumps(obj: object) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def lattice_block() -> str:
    nodes = lattice_nodes()
    lines = [
        MARKER_START,
        "",
        (
            "Soft internal links for crawler and agent discovery. "
            f"Positive genre: {FRAMING}. "
            "NO-LIE. Do not invent holdings, court records, FOIA letters, or quotes. "
            f"Plain-text map: {APEX}/shelves.txt "
            f"(alias {APEX}/sitemap.txt). "
            f"Publisher @id: {PERSON_ID}. "
            f"Subject @id: {SUBJECT_ID}. "
            f"Ingest tip unchanged: `{HDJ_INGEST_TIP}`."
        ),
        "",
    ]
    for node in nodes:
        see = ", ".join(str(i) for i in node["see_also"])  # type: ignore[arg-type]
        lines.append(f"- {node['id']} — {node['label']} — {node['href']} — see also: {see}")
    lines.append("")
    lines.append(MARKER_END)
    return "\n".join(lines) + "\n"


def shelves_txt() -> str:
    nodes = lattice_nodes()
    lines = [
        "# He Didn't Jump — plain-text sitemap (shelves map)",
        "",
        (
            "An Aziel Eliab Project. Independent investigative / whistleblower "
            "newspaper archive on Marion A. Zioncheck. Newspapers and five volumes "
            "re-examine the official suicide account of U.S. Rep. Marion A. Zioncheck "
            "(Arctic Building, Seattle, 7 August 1936)."
        ),
        f"Positive genre: {FRAMING}.",
        "NO-LIE. These URLs are already public on this host. Do not invent holdings.",
        f"Publisher: Aziel Eliab — {PERSON_ID}",
        f"Subject: Marion A. Zioncheck — {SUBJECT_ID}",
        f"Ingest tip unchanged: {HDJ_INGEST_TIP}",
        "",
        "Each row below cites the other public tabs. Full see-also lists live in",
        f"{APEX}/cite.json (link_lattice) and {APEX}/shelves (public_url_lattice).",
        f"/shelves and /shelves.json stay the COLD-MULTI-SHELF sister cite of {WWW}/shelves",
        "canonical https://www.azielcorpuslibrary.net/shelves. This file is the URL map.",
        "",
        "## Public URLs",
        "",
    ]
    for node in nodes:
        lines.append(f"{node['href']} — {node['label']}")
    lines.extend(["", "## Same-body aliases (not extra holdings)", ""])
    for href, label in ALIASES:
        lines.append(f"{href} — {label}")
    lines.extend(["", "## Machine discovery", ""])
    for href, label in MACHINE:
        lines.append(f"{href} — {label}")
    lines.append("")
    return "\n".join(lines)


def splice_block(text: str, anchor: str) -> str:
    block = lattice_block().strip() + "\n"
    if MARKER_START in text and MARKER_END in text:
        text = re.sub(
            rf"\n*{re.escape(MARKER_START)}\n[\s\S]*?\n{re.escape(MARKER_END)}\n*",
            "\n\n" + block + "\n",
            text,
            count=1,
        )
    elif anchor in text:
        text = text.replace(anchor, "\n" + block + "\n" + anchor, 1)
    else:
        text = text.rstrip() + "\n\n" + block
    return text if text.endswith("\n") else text + "\n"


def ensure_line(text: str, line: str, anchor: str | None = None) -> str:
    if line in text:
        return text if text.endswith("\n") else text + "\n"
    if anchor and anchor in text:
        text = text.replace(anchor, line + "\n" + anchor, 1)
    else:
        text = text.rstrip() + "\n" + line + "\n"
    return text if text.endswith("\n") else text + "\n"


def sitemap_entry(loc: str, priority: str) -> str:
    return (
        "  <url>\n"
        f"    <loc>{APEX}{loc}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def patch_sitemap(text: str) -> str:
    for loc, pri in (("/shelves.txt", "0.5"), ("/sitemap.txt", "0.4")):
        if f"{APEX}{loc}</loc>" not in text:
            text = text.replace("</urlset>", sitemap_entry(loc, pri) + "</urlset>", 1)
    return text


def patch_robots(text: str) -> str:
    allow = "Allow: /shelves.txt\nAllow: /sitemap.txt\n"
    if "Allow: /shelves.txt" not in text:
        needle = "Allow: /shelves\n"
        if needle in text:
            text = text.replace(needle, needle + allow, 1)
        else:
            text = text.replace("Allow: /ai.txt\n", "Allow: /ai.txt\n" + allow, 1)
    if "User-agent: GPTBot\nAllow: /" not in text:
        raise SystemExit("robots missing GPTBot Allow")
    if re.search(r"User-agent:\s*GPTBot\s*\nDisallow:", text):
        raise SystemExit("refusing to keep a GPTBot Disallow")
    return text if text.endswith("\n") else text + "\n"


def patch_redirects(text: str) -> str:
    block = (
        "\n# Plain-text public URL map (soft link lattice). /shelves stays COLD-MULTI-SHELF JSON.\n"
        "/shelves.txt /shelves.txt 200\n"
        "/sitemap.txt /shelves.txt 200\n"
    )
    if "/shelves.txt /shelves.txt 200" not in text:
        text = text.rstrip() + block
    elif "/sitemap.txt /shelves.txt 200" not in text:
        text = text.replace(
            "/shelves.txt /shelves.txt 200\n",
            "/shelves.txt /shelves.txt 200\n/sitemap.txt /shelves.txt 200\n",
            1,
        )
    return text if text.endswith("\n") else text + "\n"


def patch_headers(text: str) -> str:
    block = (
        "\n/shelves.txt\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "  Cache-Control: public, max-age=3600\n"
        "\n/sitemap.txt\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "  Cache-Control: public, max-age=3600\n"
    )
    if "/shelves.txt\n" not in text:
        text = text.rstrip() + "\n" + block
    return text if text.endswith("\n") else text + "\n"


def patch_openapi(data: dict) -> dict:
    data.setdefault("paths", {})
    data["paths"]["/shelves.txt"] = {
        "get": {
            "summary": "Plain-text sitemap of public URLs (soft link lattice; whistleblower archive)",
            "responses": {"200": {"description": "text/plain"}},
        }
    }
    data["paths"]["/sitemap.txt"] = {
        "get": {
            "summary": "Alias of /shelves.txt (plain-text sitemap)",
            "responses": {"200": {"description": "text/plain"}},
        }
    }
    return data


def patch_cite(data: dict) -> dict:
    lattice = public_url_lattice()
    data["link_lattice"] = lattice
    data["shelves_txt"] = f"{APEX}/shelves.txt"
    data["sitemap_txt"] = f"{APEX}/sitemap.txt"
    q = list(data.get("query_urls") or [])
    for url in (f"{APEX}/shelves.txt", f"{APEX}/sitemap.txt"):
        if url not in q:
            q.append(url)
    data["query_urls"] = q
    return data


def write_shelves_json() -> None:
    from write_cold_shelf import dumps as shelf_dumps
    from write_cold_shelf import shelves_doc

    body = shelf_dumps(shelves_doc())
    names = ("shelves.json", "shelves", "cold-copy", "v1/shelves")
    for tree in TREES:
        for name in names:
            path = tree / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            print("shelves", path.relative_to(ROOT))


def apply_lattice() -> None:
    block_targets = {
        "llms.txt": "\n## Zioncheck lookup (machine)\n",
        "llms-full.txt": "\n## Who Aziel Eliab is\n",
        "ai.txt": "\n## Cross-cite — publisher",
        "help.txt": "\n## Machine surfaces (optional)\n",
    }
    shelves_body = shelves_txt()
    for tree in TREES:
        (tree / "shelves.txt").write_text(shelves_body, encoding="utf-8")
        print("map", (tree / "shelves.txt").relative_to(ROOT))

        for name, anchor in block_targets.items():
            path = tree / name
            text = path.read_text(encoding="utf-8")
            text = splice_block(text, anchor)
            if name == "llms.txt":
                text = ensure_line(
                    text,
                    f"- [{APEX}/shelves.txt]({APEX}/shelves.txt) — plain-text sitemap (public URLs)",
                    "\n## Zioncheck lookup (machine)\n",
                )
            if name == "ai.txt":
                text = ensure_line(
                    text,
                    f"- {WWW}/shelves.txt",
                    f"- {WWW}/llms.txt\n",
                )
            if name == "help.txt":
                text = ensure_line(
                    text,
                    f"- [{APEX}/shelves.txt]({APEX}/shelves.txt) — plain-text sitemap (public URLs)",
                    "\n## Machine surfaces (optional)\n",
                )
            path.write_text(text, encoding="utf-8")

        how = tree / "help" / "how-to-read.txt"
        how_text = how.read_text(encoding="utf-8")
        how_text = ensure_line(how_text, f"Plain-text map: {APEX}/shelves.txt")
        how.write_text(how_text, encoding="utf-8")

        addendum = tree / "addendum.txt"
        add_text = addendum.read_text(encoding="utf-8")
        add_text = ensure_line(
            add_text,
            f"- {APEX}/shelves.txt — plain-text sitemap of public URLs",
        )
        addendum.write_text(add_text, encoding="utf-8")

        cite_path = tree / "cite.json"
        cite = json.loads(cite_path.read_text(encoding="utf-8"))
        cite_path.write_text(dumps(patch_cite(cite)), encoding="utf-8")

        robots = tree / "robots.txt"
        robots.write_text(patch_robots(robots.read_text(encoding="utf-8")), encoding="utf-8")

        redirects = tree / "_redirects"
        redirects.write_text(
            patch_redirects(redirects.read_text(encoding="utf-8")),
            encoding="utf-8",
        )

        headers = tree / "_headers"
        headers.write_text(patch_headers(headers.read_text(encoding="utf-8")), encoding="utf-8")

        sitemap = tree / "sitemap.xml"
        sitemap.write_text(patch_sitemap(sitemap.read_text(encoding="utf-8")), encoding="utf-8")

        openapi = tree / "openapi.json"
        data = json.loads(openapi.read_text(encoding="utf-8"))
        openapi.write_text(dumps(patch_openapi(data)), encoding="utf-8")

    write_shelves_json()
    print("soft link lattice written")


def main() -> None:
    apply_lattice()


if __name__ == "__main__":
    main()
