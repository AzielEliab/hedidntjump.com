#!/usr/bin/env python3
"""Extract published HDJ newspaper substance for machine LLM review files.

Reads docs/ HTML only. Does not invent case facts. Does not rewrite HTML.
"""
from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from aziel_living import LIVING_STACK

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ORIGIN = "https://hedidntjump.com"

REVIEW_HEAD = "## LLM project review (extracted; do not invent)"
REVIEW_END = "## End of LLM project review"

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
VOLUME_TITLES = {
    1: "Primary Documents & Forensic Analysis",
    2: "News Coverage & Family Battles",
    3: "Personal Photographs & Research Materials",
    4: "The Physics Case",
    5: "The Human & Institutional Evidence",
}
VOLUME_AZDOC = {
    1: "AZDOC-18DBE35A32DD",
    2: "AZDOC-A0223FC27A15",
    3: "AZDOC-9673443C40F7",
    4: None,
    5: None,
}

CHROME_LINES = (
    "skip to content",
    "the record, not the verdict",
    "friday, august 7, 1936",
    "he didn't jump",
    "he didn’t jump",
    "the marion zioncheck archive",
    "seattle, washington",
    "— views 2¢ — downloads",
    "case (pg. 1) press (pg. 2) inquiries (pg. 3) rubye (pg. 4) archives (pg. 5)",
    "f.o.i.a. (pg. 6) volumes (pg. 7) narrative (pg. 8) aziel (pg. 9) copyrights (pg. 10)",
    "a fifth-floor window. a congressman.",
    "a disputed account.",
)

TAB_PAGES = (
    ("home", "/", "index.html", "Homepage money-page framing"),
    ("case", "/Case", "case.html", "Case"),
    ("press", "/Press", "press.html", "Press"),
    ("inquiries", "/Inquiries", "inquiries.html", "Inquiries"),
    ("rubye", "/Rubye", "rubye.html", "Rubye"),
    ("archives", "/Archives", "archives.html", "Archives"),
    ("foia", "/FOIA", "foia.html", "FOIA"),
    ("volumes", "/Volumes", "volumes.html", "Volumes"),
    ("narrative", "/Narrative", "official-narrative.html", "Narrative"),
    ("aziel", "/aziel", "aziel.html", "About Aziel"),
    ("copyrights", "/Copyrights", "copyrights.html", "Copyrights"),
    ("receipts", "/receipts", "receipts.html", "Receipts / ingest (machine)"),
    ("who", "/who", "who.html", "Who"),
    ("reader", "/reader", "reader.html", "Reader"),
)


class _FragmentText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"}:
            self._skip += 1
        if tag in {"br", "p", "h1", "h2", "h3", "h4", "li", "figcaption", "dt", "dd"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"} and self._skip:
            self._skip -= 1
        if tag in {"p", "h1", "h2", "h3", "h4", "li", "div", "section", "article", "aside"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        text = " ".join(data.split())
        if text:
            self.parts.append(text + " ")


def scrub_old_stack(text: str) -> str:
    """Machine files lock the living stack; rewrite heritage phrases from HTML extracts."""
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
        ("is an researcher", "is a researcher"),
        ("is an researcher,", "is a researcher,"),
    )
    for old, new in replacements:
        out = out.replace(old, new)
    return out


def scrub_payload(obj):
    if isinstance(obj, str):
        return scrub_old_stack(obj)
    if isinstance(obj, list):
        return [scrub_payload(v) for v in obj]
    if isinstance(obj, dict):
        return {k: scrub_payload(v) for k, v in obj.items()}
    return obj


def html_to_text(fragment: str) -> str:
    parser = _FragmentText()
    parser.feed(fragment)
    text = "".join(parser.parts)
    lines = []
    for raw in text.splitlines():
        line = " ".join(raw.split()).strip()
        if not line:
            continue
        if line.lower() in CHROME_LINES:
            continue
        if line.lower().startswith("see more on pg."):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def _inner_main(html_text: str) -> str:
    match = re.search(r"<main\b[^>]*>([\s\S]*)</main>", html_text, re.I)
    if match:
        return match.group(1)
    match = re.search(r"<body\b[^>]*>([\s\S]*)</body>", html_text, re.I)
    return match.group(1) if match else html_text


def page_substance(rel: str) -> str:
    path = DOCS / rel
    raw = path.read_text(encoding="utf-8")
    return html_to_text(_inner_main(raw))


def _abs_url(href: str) -> str:
    href = html.unescape(href).strip()
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return ORIGIN + href
    return href


def _pretty_volume_href(href: str) -> str:
    href = html.unescape(href)
    match = re.search(r"volume=(\d+).*?page=(\d+)", href)
    if match:
        vol, page = match.group(1), match.group(2)
        return (
            f"{ORIGIN}/reader?volume={vol}&page={page} "
            f"(PDF {ORIGIN}/volumes/volume-{vol}.pdf#page={page})"
        )
    return _abs_url(href)


def extract_inquiries() -> list[dict]:
    raw = (DOCS / "inquiries.html").read_text(encoding="utf-8")
    blocks = re.findall(
        r'<aside class="inquiry" id="(q\d+)">([\s\S]*?)</aside>',
        raw,
    )
    by_id: dict[str, dict] = {}
    for qid, body in blocks:
        num = int(qid[1:])
        title_m = re.search(r"<h3>([\s\S]*?)</h3>", body)
        question = html_to_text(title_m.group(1)) if title_m else ""
        paras = []
        for para in re.findall(r"<p(?![^>]*inquiry-source)[^>]*>([\s\S]*?)</p>", body):
            if 'class="inquiry-kicker"' in para or 'class="inquiry-source"' in para:
                continue
            text = html_to_text(para)
            if text and not text.startswith("Inquiry of the Record"):
                paras.append(text)
        captions = []
        for cap in re.findall(r"<figcaption>([\s\S]*?)</figcaption>", body):
            text = html_to_text(cap)
            if text:
                captions.append(text)
        sources = []
        source_block = re.search(r'<p class="inquiry-source">([\s\S]*?)</p>', body)
        if source_block:
            for href, label in re.findall(
                r'<a href="([^"]+)"[^>]*>([\s\S]*?)</a>',
                source_block.group(1),
            ):
                sources.append(
                    {
                        "label": html_to_text(label).rstrip(" ↗"),
                        "href": _pretty_volume_href(href),
                    }
                )
        by_id[qid] = {
            "n": num,
            "id": qid,
            "url": f"{ORIGIN}/Inquiries#{qid}",
            "question": question,
            "substance": paras,
            "plates": captions,
            "sources": sources,
        }
    missing = [n for n in range(1, 24) if f"q{n:02d}" not in by_id]
    if missing:
        raise SystemExit(f"missing inquiries: {missing}")
    return [by_id[f"q{n:02d}"] for n in range(1, 24)]


def extract_two_arctics() -> str:
    raw = (DOCS / "inquiries.html").read_text(encoding="utf-8")
    match = re.search(
        r'<section class="spread" id="two-arctics"[\s\S]*?</section>',
        raw,
    )
    if not match:
        return ""
    text = html_to_text(match.group(0))
    # Keep the feature copy; inquiry 14/17 bodies are repeated in the numbered list.
    cut = text.find("Volume IV identifies two distinct locations: the old Arctic Club")
    if cut != -1:
        text = text[:cut]
    lines = [
        line
        for line in text.splitlines()
        if not line.startswith("Inquiry of the Record")
        and not line.startswith("How and why did the record get meshed")
        and not line.startswith("Why was cousin")
    ]
    return "\n".join(lines).strip()


def extract_volumes() -> list[dict]:
    raw = (DOCS / "volumes.html").read_text(encoding="utf-8")
    meta = {
        row["volume"]: row
        for row in json.loads((DOCS / "volumes.json").read_text(encoding="utf-8"))
    }
    cards = []
    for body in re.findall(
        r'<article class="volume-card" id="volume-(\d+)">([\s\S]*?)</article>',
        raw,
    ):
        n = int(body[0])
        frag = body[1]
        purpose_m = re.search(
            r'<p class="volume-card-purpose">([\s\S]*?)</p>',
            frag,
        )
        folio_m = re.search(
            r'<p class="volume-card-folio">([\s\S]*?)</p>',
            frag,
        )
        title_m = re.search(r"<h2>([\s\S]*?)</h2>", frag)
        info = meta.get(n, {})
        pages = int(info.get("pages") or 0)
        cards.append(
            {
                "n": n,
                "roman": ROMAN[n],
                "id": f"volume-{n}",
                "title": html_to_text(title_m.group(1)) if title_m else VOLUME_TITLES[n],
                "purpose": html_to_text(purpose_m.group(1)) if purpose_m else "",
                "folio": html_to_text(folio_m.group(1)) if folio_m else "",
                "pages": pages,
                "bytes": int(info.get("bytes") or 0),
                "canonical": f"{ORIGIN}/Volumes#volume-{n}",
                "reader": f"{ORIGIN}/reader?volume={n}&page=1",
                "pdf": f"{ORIGIN}/volumes/volume-{n}.pdf",
                "webp_pattern": f"{ORIGIN}/assets/v{n}/{{page}}.webp",
                "azdoc": VOLUME_AZDOC[n],
                "text_layer": "none-extractable",
            }
        )
    if len(cards) != 5:
        raise SystemExit(f"expected 5 volume cards, got {len(cards)}")
    return cards


def volume_outline(inquiries: list[dict]) -> dict[int, list[str]]:
    outline: dict[int, list[str]] = {n: [] for n in range(1, 6)}
    seen: dict[int, set[str]] = {n: set() for n in range(1, 6)}
    for item in inquiries:
        for src in item["sources"]:
            href = src["href"]
            match = re.search(r"volume=(\d+).*?page=(\d+)", href)
            if not match:
                continue
            vol = int(match.group(1))
            page = int(match.group(2))
            label = src["label"]
            key = f"{page}:{label}"
            if key in seen[vol]:
                continue
            seen[vol].add(key)
            outline[vol].append(
                f"PDF p. {page} — {label} (from Inquiry {item['n']:02d}; "
                f"{ORIGIN}/reader?volume={vol}&page={page})"
            )
    return outline


def extract_tabs() -> dict[str, dict]:
    out = {}
    for key, path, rel, title in TAB_PAGES:
        out[key] = {
            "id": key,
            "title": title,
            "path": path,
            "url": ORIGIN + (path if path != "/" else "/"),
            "source_file": rel,
            "substance": page_substance(rel),
        }
    return out


def pdf_text_layer_note(vol: dict) -> str:
    return (
        f"Repo PDF is a binary facsimile ({vol['bytes']} bytes; {vol['folio']}). "
        "No faithful running text layer is extractable from the PDF bytes in this "
        "repository without inventing OCR. Full facsimile at "
        f"{vol['pdf']} . In-site reader: {vol['reader']} . "
        f"Static page images: {vol['webp_pattern']} for pages 1–{vol['pages']}."
    )


def format_inquiry(item: dict) -> str:
    lines = [
        f"### Inquiry {item['n']:02d} — {item['question']}",
        f"Canonical: {item['url']}",
        "",
    ]
    for para in item["substance"]:
        lines.append(para)
        lines.append("")
    if item["plates"]:
        lines.append("Plates / captions as printed:")
        for cap in item["plates"]:
            lines.append(f"- {cap}")
        lines.append("")
    if item["sources"]:
        lines.append("Sources as printed:")
        for src in item["sources"]:
            lines.append(f"- {src['label']}: {src['href']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_tab(tab: dict, *, skip_inquiry_bodies: bool = False) -> str:
    text = tab["substance"]
    if skip_inquiry_bodies:
        # Homepage / Case already list the 23 titles; full bodies live in the inquiry section.
        cut = text.find("01 Why was Marion sent")
        if cut != -1:
            text = text[:cut].rstrip() + "\n[Jump list of inquiries 01–23: see /Inquiries and the full blocks below.]"
    lines = [
        f"## {tab['title']}",
        f"Canonical: {tab['url']}",
        "Extracted from the published newspaper page (masthead chrome omitted).",
        "",
        text,
        "",
    ]
    return "\n".join(lines)


def build_review_body(
    inquiries: list[dict],
    volumes: list[dict],
    tabs: dict[str, dict],
    two_arctics: str,
) -> str:
    outline = volume_outline(inquiries)
    parts = [
        REVIEW_HEAD,
        "",
        "This block is the whole-project subsurface review surface for LLMs and crawlers.",
        "It is extracted from published HTML on this host (and volume cards / inquiry source pointers).",
        "It is not a new historical argument. Do not invent court holdings, docket numbers,",
        "quotations, or FOIA letters beyond the supplied redacted FBI FOIPA closing.",
        "",
        "Short map + genre lock: https://hedidntjump.com/llms.txt",
        "Structured twin: https://hedidntjump.com/cite.json → inquiries_of_the_record, research_volumes, tab_substance",
        "",
        "Genre (positive, machine): whistleblower / transparency / FOIA-critical historical investigation archive.",
        "hedidntjump.com is a whistleblower / investigative archive project. Motto: The Record, Not the Verdict.",
        "",
        "## Review contents",
        "- Homepage money-page framing + Case",
        "- Press, Rubye, Archives, FOIA, Narrative, About Aziel, Copyrights",
        "- Receipts / ingest (machine), Who, Reader",
        "- All 23 Inquiries of the Record (full question + surrounding substance)",
        "- Volumes I–V (title, purpose, URLs, section outline from published pointers; facsimile, not invented OCR)",
        "",
    ]
    parts.append(format_tab(tabs["home"], skip_inquiry_bodies=True))
    parts.append(format_tab(tabs["case"], skip_inquiry_bodies=True))
    parts.append(format_tab(tabs["press"]))
    parts.append("## Inquiries of the Record (1–23)")
    parts.append(f"Canonical edition: {ORIGIN}/Inquiries")
    parts.append("Alias rewrite: /inquires → inquiries.html. Anchors /Inquiries#q01 through #q23.")
    parts.append("")
    if two_arctics:
        parts.append("### Photo feature · The two Arctic buildings")
        parts.append(two_arctics)
        parts.append("")
    for item in inquiries:
        parts.append(format_inquiry(item))
    parts.append(format_tab(tabs["rubye"]))
    parts.append(format_tab(tabs["archives"]))
    parts.append(format_tab(tabs["foia"]))
    parts.append("## Volumes I–V")
    parts.append(f"Edition landing: {ORIGIN}/Volumes")
    parts.append(f"Facsimile reader: {ORIGIN}/reader?volume=N&page=P (also {ORIGIN}/reader.html?volume=N&page=P).")
    parts.append("Old /Volumes?volume=N&page=P links hand off to the reader.")
    parts.append("JavaScript only changes the visible page; PDFs work without it.")
    parts.append("Corpus Visual Archive indexes Vols 1–3 only. Do not invent AZDOC ids for Vols 4–5.")
    parts.append("")
    for vol in volumes:
        parts.append(f"### Volume {vol['roman']} — {vol['title']}")
        parts.append(f"Canonical: {vol['canonical']}")
        parts.append(f"Purpose (as printed on /Volumes): {vol['purpose']}")
        parts.append(f"Folio: {vol['folio']}")
        parts.append(f"Download URL: {vol['pdf']}")
        parts.append(f"Reader URL: {vol['reader']}")
        azdoc = vol["azdoc"] or "none published — do not invent"
        parts.append(f"Corpus AZDOC: {azdoc}")
        parts.append(pdf_text_layer_note(vol))
        parts.append("Section outline from published inquiry sources (not an invented TOC):")
        rows = outline[vol["n"]]
        if rows:
            for row in rows:
                parts.append(f"- {row}")
        else:
            parts.append("- No inquiry source pointers cite this volume by page on /Inquiries.")
        parts.append("How to fetch the full facsimile:")
        parts.append(f"- GET {vol['pdf']}")
        parts.append(f"- Or walk {vol['pages']} reader pages starting at {vol['reader']}")
        parts.append(
            f"- Or GET {ORIGIN}/assets/v{vol['n']}/1.webp through /{vol['pages']}.webp"
        )
        parts.append("")
    parts.append(format_tab(tabs["narrative"]))
    parts.append(format_tab(tabs["aziel"]))
    parts.append(format_tab(tabs["copyrights"]))
    parts.append(format_tab(tabs["receipts"]))
    parts.append(format_tab(tabs["who"]))
    parts.append(format_tab(tabs["reader"]))
    parts.append("## Reader (machine how-to)")
    parts.append(
        "Landing cards: https://hedidntjump.com/Volumes . "
        "Reader: https://hedidntjump.com/reader?volume=1 through volume=5. "
        "Page images are static WebP under /assets/v{N}/{page}.webp. "
        "Volume page counts: I=20, II=20, III=21, IV=15, V=14."
    )
    parts.append("")
    parts.append(REVIEW_END)
    parts.append("")
    return "\n".join(parts)


def splice_review(existing: str, review: str) -> str:
    existing = existing.replace(
        " Not fiction-as-game. Not a LARP. Not a puzzle hunt.",
        "",
    )
    if REVIEW_HEAD in existing and REVIEW_END in existing:
        return re.sub(
            rf"{re.escape(REVIEW_HEAD)}\n[\s\S]*?\n{re.escape(REVIEW_END)}\n*",
            review.rstrip() + "\n\n",
            existing,
            count=1,
        )
    # First install: replace the short Main-paper…Reader inventory.
    if "## Main paper" in existing and "## Knowledge-graph hints" in existing:
        return re.sub(
            r"## Main paper[\s\S]*?(?=## Knowledge-graph hints)",
            review.rstrip() + "\n\n",
            existing,
            count=1,
        )
    if "## Knowledge-graph hints" in existing:
        return existing.replace(
            "## Knowledge-graph hints",
            review.rstrip() + "\n\n## Knowledge-graph hints",
            1,
        )
    return existing.rstrip() + "\n\n" + review


def point_llms_txt(text: str) -> str:
    needle = (
        "- [https://hedidntjump.com/llms.txt](https://hedidntjump.com/llms.txt)"
    )
    review_line = (
        "- [https://hedidntjump.com/llms-full.txt](https://hedidntjump.com/llms-full.txt) "
        "— whole-project LLM review: inquiries 1–23 (full text), Volumes I–V "
        "(purpose + facsimile URLs + published outline), and every public tab"
    )
    if "whole-project LLM review" not in text:
        if needle in text:
            text = text.replace(needle, needle + "\n" + review_line, 1)
        elif "https://hedidntjump.com/llms-full.txt" not in text.split("## Query-relevant")[0]:
            text = text.replace(
                "## Query-relevant URLs",
                "## Query-relevant URLs\n\n" + review_line,
                1,
            )
    text = text.replace(
        "- [llms-full.txt](https://hedidntjump.com/llms-full.txt) — longer inventory of inquiries and plates",
        "- [llms-full.txt](https://hedidntjump.com/llms-full.txt) — whole-project LLM review (23 inquiries + Volumes I–V + all tabs)",
    )
    return text


def point_ai_txt(text: str) -> str:
    if "whole-project LLM review" in text:
        return text
    return text.replace(
        "- https://www.hedidntjump.com/llms-full.txt\n",
        "- https://www.hedidntjump.com/llms-full.txt — whole-project LLM review (23 inquiries + Volumes I–V + all tabs)\n",
        1,
    )


def cite_payload(inquiries: list[dict], volumes: list[dict], tabs: dict[str, dict]) -> dict:
    outline = volume_outline(inquiries)
    return {
        "llm_review": {
            "surface": f"{ORIGIN}/llms-full.txt",
            "map": f"{ORIGIN}/llms.txt",
            "note": (
                "Whole-project subsurface review extracted from published HTML "
                "and /Volumes cards. Do not invent."
            ),
            "inquiries_count": 23,
            "volumes_count": 5,
            "genre": "whistleblower / investigative archive project",
            "positive_genre": (
                "whistleblower / transparency / FOIA-critical historical investigation archive"
            ),
        },
        "inquiries_of_the_record": inquiries,
        "research_volumes": [
            {
                **vol,
                "full_text": None,
                "full_text_note": pdf_text_layer_note(vol),
                "section_outline": outline[vol["n"]],
            }
            for vol in volumes
        ],
        "tab_substance": {
            key: {
                "title": tab["title"],
                "url": tab["url"],
                "source_file": tab["source_file"],
                "substance": tab["substance"],
            }
            for key, tab in tabs.items()
        },
    }
