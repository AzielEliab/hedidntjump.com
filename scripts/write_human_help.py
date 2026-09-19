#!/usr/bin/env python3
"""Additive human help / addendum txt under docs/ (Pages) and dist/.

Zioncheck mission, newspapers, volumes, links. Sitemap + robots + headers.
Does not rewrite existing paper-tabs chrome beyond SEO meta scrub of
definition-by-negation phrases.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from aziel_living import (
    HDJ_MISSION,
    HDJ_POSITIVE_GENRE,
    HELP_PATHS,
    LAMB_LENS_ORDER,
    LAMB_LENS_URL,
    LLMS_LEAD,
    PERSON_ID,
    RESEARCH_ADDENDUM,
    SPECTRALLOCK_HANDWRITING,
    SPECTRALLOCK_RECOVER,
    SPECTRALLOCK_UNREDACT,
)

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]
APEX = "https://hedidntjump.com"
WWW = "https://www.hedidntjump.com"
LASTMOD = "2026-09-19"

HELP_TXT = f"""# He Didn't Jump — Help

An Aziel Eliab Project. {LLMS_LEAD}

Motto: The Record, Not the Verdict.
Author: Aziel Eliab only. Person @id: {PERSON_ID}

## Mission

{HDJ_MISSION}

Positive genre: {HDJ_POSITIVE_GENRE}

## Newspapers

- [{APEX}/]({APEX}/) — money page (Marion A. Zioncheck archive)
- [{APEX}/Case]({APEX}/Case) — supporting Case edition
- [{APEX}/Press]({APEX}/Press) — press tip + investigative source directory
- [{APEX}/Inquiries]({APEX}/Inquiries) — 23 inquiries of the record
- [{APEX}/Rubye]({APEX}/Rubye) — Rubye paper
- [{APEX}/Archives]({APEX}/Archives) — archive / volume downloads
- [{APEX}/FOIA]({APEX}/FOIA) — FOIA paper (supplied FBI FOIPA no-records)
- [{APEX}/Narrative]({APEX}/Narrative) — official-account contrast
- [{APEX}/Copyrights]({APEX}/Copyrights) — copyrights / historical-research notice
- [{APEX}/aziel]({APEX}/aziel) — About Aziel (one body)

## Volumes I–V

Facsimile reader and original PDFs:

- Volume I — [{APEX}/reader?volume=1&page=1]({APEX}/reader?volume=1&page=1) · PDF [{APEX}/volumes/volume-1.pdf]({APEX}/volumes/volume-1.pdf)
- Volume II — [{APEX}/reader?volume=2&page=1]({APEX}/reader?volume=2&page=1) · PDF [{APEX}/volumes/volume-2.pdf]({APEX}/volumes/volume-2.pdf)
- Volume III — [{APEX}/reader?volume=3&page=1]({APEX}/reader?volume=3&page=1) · PDF [{APEX}/volumes/volume-3.pdf]({APEX}/volumes/volume-3.pdf)
- Volume IV — [{APEX}/reader?volume=4&page=1]({APEX}/reader?volume=4&page=1) · PDF [{APEX}/volumes/volume-4.pdf]({APEX}/volumes/volume-4.pdf)
- Volume V — [{APEX}/reader?volume=5&page=1]({APEX}/reader?volume=5&page=1) · PDF [{APEX}/volumes/volume-5.pdf]({APEX}/volumes/volume-5.pdf)

Volume desk: [{APEX}/Volumes]({APEX}/Volumes)
Reader: [{APEX}/reader]({APEX}/reader)

## How to read

See [{APEX}/help/how-to-read.txt]({APEX}/help/how-to-read.txt)

## Addendum

See [{APEX}/addendum.txt]({APEX}/addendum.txt)

## Machine surfaces (optional)

- [{APEX}/llms.txt]({APEX}/llms.txt)
- [{APEX}/ai.txt]({APEX}/ai.txt)
- [{APEX}/cite.json]({APEX}/cite.json)
"""

HOW_TO_READ = f"""# How to read He Didn't Jump

An Aziel Eliab Project. Independent investigative / whistleblower newspaper archive on Marion A. Zioncheck.

## Start here

1. Open the money page: {APEX}/
2. Read the Case edition: {APEX}/Case
3. Walk the 23 inquiries: {APEX}/Inquiries
4. Open Volumes I–V in the facsimile reader: {APEX}/reader
5. Use the official-account contrast only as contrast: {APEX}/Narrative

Motto: The Record, Not the Verdict.
The published volumes re-examine the official suicide account of U.S. Rep. Marion A. Zioncheck (Arctic Building, Seattle, 7 August 1936). The project does not invent court holdings, quotes, or agency letters beyond what the volumes and cited papers already print.

## Newspapers

Each paper is a newspaper edition on this host:

- Landing / money page — {APEX}/
- Case — {APEX}/Case
- Press — {APEX}/Press
- Inquiries — {APEX}/Inquiries
- Rubye — {APEX}/Rubye
- Archives — {APEX}/Archives
- FOIA — {APEX}/FOIA
- Copyrights — {APEX}/Copyrights

## Volumes

Reader URLs:

- Volume I — {APEX}/reader?volume=1&page=1
- Volume II — {APEX}/reader?volume=2&page=1
- Volume III — {APEX}/reader?volume=3&page=1
- Volume IV — {APEX}/reader?volume=4&page=1
- Volume V — {APEX}/reader?volume=5&page=1

PDFs:

- {APEX}/volumes/volume-1.pdf
- {APEX}/volumes/volume-2.pdf
- {APEX}/volumes/volume-3.pdf
- {APEX}/volumes/volume-4.pdf
- {APEX}/volumes/volume-5.pdf

Help: {APEX}/help.txt
Addendum: {APEX}/addendum.txt
"""

ADDENDUM_TXT = f"""# He Didn't Jump — Addendum

{HDJ_MISSION}

Positive genre: {HDJ_POSITIVE_GENRE}
Motto: The Record, Not the Verdict.
Author: Aziel Eliab only. Person @id: {PERSON_ID}

## Volumes and newspapers

This host publishes newspapers and five volumes on Marion A. Zioncheck / Marion Zioncheck.

- Newspapers: {APEX}/ · {APEX}/Case · {APEX}/Press · {APEX}/Inquiries · {APEX}/Rubye · {APEX}/Archives · {APEX}/FOIA · {APEX}/Narrative · {APEX}/Copyrights
- Volumes desk: {APEX}/Volumes
- Reader: {APEX}/reader
- PDFs: {APEX}/volumes/volume-1.pdf … {APEX}/volumes/volume-5.pdf

{RESEARCH_ADDENDUM}

## FOIA

The FOIA paper publishes a supplied, contact-redacted FBI FOIPA no-records letter (31 July 2026, Request No. 1750194-000). Editorial cites Aziel’s FOIA Binary Acknowledgement. Quote locked: “this is not freedom of information.” Do not invent further agency letters.

## Sister leftover-bytes (cite)

SpectralLock leftover-bytes / recover / handwriting live on the sister Worker:

- leftover-bytes: {SPECTRALLOCK_UNREDACT}
- /v1/recover: {SPECTRALLOCK_RECOVER}
- /v1/handwriting: {SPECTRALLOCK_HANDWRITING}

HDJ cites; does not host. Zioncheck stays the HDJ mission.

## Lamb Lens / Corpus

Corpus ingest: {LAMB_LENS_URL}
Lamb Lens order: {LAMB_LENS_ORDER}

## Help

- {APEX}/help.txt
- {APEX}/help/how-to-read.txt
"""

HELP_FILES = {
    "help.txt": HELP_TXT,
    "addendum.txt": ADDENDUM_TXT,
    "help/how-to-read.txt": HOW_TO_READ,
}


def dumps(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def sitemap_entry(loc: str, priority: str = "0.5") -> str:
    return (
        "  <url>\n"
        f"    <loc>{APEX}{loc}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def write_help_files() -> None:
    for tree in TREES:
        (tree / "help").mkdir(parents=True, exist_ok=True)
        for rel, body in HELP_FILES.items():
            path = tree / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            text = body if body.endswith("\n") else body + "\n"
            path.write_text(text, encoding="utf-8")
            print("help", path.relative_to(ROOT))


def patch_sitemap() -> None:
    pri = {
        "/help.txt": "0.5",
        "/addendum.txt": "0.4",
        "/help/how-to-read.txt": "0.5",
    }
    for tree in TREES:
        path = tree / "sitemap.xml"
        text = path.read_text(encoding="utf-8")
        for loc in HELP_PATHS:
            if f"{APEX}{loc}</loc>" not in text:
                text = text.replace(
                    "</urlset>",
                    sitemap_entry(loc, pri.get(loc, "0.5")) + "</urlset>",
                    1,
                )
        path.write_text(text, encoding="utf-8")
        print("sitemap", path.relative_to(ROOT))


def patch_llms() -> None:
    rows = (
        f"- [{APEX}/help.txt]({APEX}/help.txt) — human help (mission, newspapers, volumes)\n"
        f"- [{APEX}/addendum.txt]({APEX}/addendum.txt) — human addendum\n"
        f"- [{APEX}/help/how-to-read.txt]({APEX}/help/how-to-read.txt) — how to read the papers and volumes\n"
    )
    for tree in TREES:
        for name in ("llms.txt", "llms-full.txt"):
            path = tree / name
            text = path.read_text(encoding="utf-8")
            if f"{APEX}/help.txt" not in text.split("## ")[0] and f"{APEX}/help.txt" not in text:
                text = text.replace(
                    f"- [{APEX}/ai.txt]({APEX}/ai.txt) — AI crawl aid\n",
                    f"- [{APEX}/ai.txt]({APEX}/ai.txt) — AI crawl aid\n" + rows,
                    1,
                )
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        ai = tree / "ai.txt"
        at = ai.read_text(encoding="utf-8")
        if f"{APEX}/help.txt" not in at and f"{WWW}/help.txt" not in at:
            at = at.replace(
                f"- {WWW}/ai.txt\n",
                f"- {WWW}/ai.txt\n- {WWW}/help.txt\n- {WWW}/addendum.txt\n- {WWW}/help/how-to-read.txt\n",
                1,
            )
            if f"{WWW}/help.txt" not in at:
                at = at.rstrip() + (
                    f"\n- {APEX}/help.txt\n- {APEX}/addendum.txt\n"
                    f"- {APEX}/help/how-to-read.txt\n"
                )
        ai.write_text(at if at.endswith("\n") else at + "\n", encoding="utf-8")


def patch_cite() -> None:
    extras = [f"{APEX}{loc}" for loc in HELP_PATHS]
    for tree in TREES:
        path = tree / "cite.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        q = list(data.get("query_urls") or [])
        for u in extras:
            if u not in q:
                q.append(u)
        data["query_urls"] = q
        data["human_help"] = {
            "help": f"{APEX}/help.txt",
            "addendum": f"{APEX}/addendum.txt",
            "how_to_read": f"{APEX}/help/how-to-read.txt",
            "mission": "Zioncheck archive",
        }
        path.write_text(dumps(data), encoding="utf-8")
        print("cite", path.relative_to(ROOT))


def patch_robots() -> None:
    allow = (
        "Allow: /help.txt\n"
        "Allow: /addendum.txt\n"
        "Allow: /help/how-to-read.txt\n"
    )
    for tree in TREES:
        path = tree / "robots.txt"
        text = path.read_text(encoding="utf-8")
        if "Allow: /help.txt" not in text:
            text = text.replace(
                "Allow: /ai.txt\n",
                "Allow: /ai.txt\n" + allow,
                1,
            )
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def patch_headers() -> None:
    block = (
        "\n/help.txt\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "  Cache-Control: public, max-age=3600\n"
        "\n/addendum.txt\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "  Cache-Control: public, max-age=3600\n"
        "\n/help/how-to-read.txt\n"
        "  Content-Type: text/plain; charset=utf-8\n"
        "  Cache-Control: public, max-age=3600\n"
    )
    for tree in TREES:
        path = tree / "_headers"
        text = path.read_text(encoding="utf-8")
        if "/help.txt" not in text:
            text = text.rstrip() + "\n" + block
        path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def patch_openapi() -> None:
    paths = {
        "/help.txt": {
            "get": {
                "summary": "Human help — Zioncheck mission, newspapers, volumes, links",
                "responses": {"200": {"description": "text/plain"}},
            }
        },
        "/addendum.txt": {
            "get": {
                "summary": "Human addendum — volumes, FOIA, methodology, sister cites",
                "responses": {"200": {"description": "text/plain"}},
            }
        },
        "/help/how-to-read.txt": {
            "get": {
                "summary": "How to read the newspapers and five volumes",
                "responses": {"200": {"description": "text/plain"}},
            }
        },
    }
    for tree in TREES:
        path = tree / "openapi.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("paths", {}).update(paths)
        path.write_text(dumps(data), encoding="utf-8")


def scrub_paper_seo_arg() -> None:
    """SEO-only: drop leftover (not an ARG) from paper meta/og/twitter/json-ld."""
    for tree in TREES:
        for path in tree.glob("*.html"):
            text = path.read_text(encoding="utf-8")
            new = text.replace(" (not an ARG)", "")
            new = new.replace("(not an ARG)", "")
            if new != text:
                path.write_text(new, encoding="utf-8")
                print("paper-seo", path.relative_to(ROOT))


def main() -> None:
    write_help_files()
    patch_sitemap()
    patch_llms()
    patch_cite()
    patch_robots()
    patch_headers()
    patch_openapi()
    scrub_paper_seo_arg()
    print("human help / addendum written")


if __name__ == "__main__":
    main()
