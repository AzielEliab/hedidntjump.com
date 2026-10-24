#!/usr/bin/env python3
"""Build the EPUB 3 edition of the five He Didn't Jump research volumes.

Source: docs/volumes/volume-1.pdf … volume-5.pdf (the files served at
https://hedidntjump.com/volumes). Output: one EPUB 3 file.

- Vols IV–V have native text: converted to reflowable XHTML (headings,
  paragraphs, lists, the one summary table). Running headers/footers, the
  duplicate inner title page and the printed table of contents are dropped;
  the EPUB navigation replaces the printed contents.
- Vols I–III are image scans: each page is reproduced as a JPEG (max 1200 px)
  labelled "facsimile page N" (N = PDF page). The typed captions/cover text
  are kept as real text. Machine OCR is only shown for passages that pass a
  strict dictionary check, labelled as unverified; nothing is invented.

Reproducible: fixed identifier, dates, file order and zip timestamps.
Needs: PyMuPDF (pymupdf), Pillow, /usr/share/dict/words (optional).

Usage: python3 scripts/make-epub.py [output.epub]
"""
from __future__ import annotations

import html
import io
import re
import sys
import uuid
import zipfile
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VOLDIR = ROOT / "docs" / "volumes"
ASSETS = ROOT / "docs" / "assets"
DEFAULT_OUT = Path("/workspace/hdj/epub/hedidntjump-volumes-1-5.epub")

TITLE = "He Didn't Jump: The Marion Zioncheck Archive, Volumes I–V"
AUTHOR = "Aziel Eliab"
PUBLISHER = "hedidntjump.com"
DATE = "2026-10-19"
MODIFIED = "2026-10-19T00:00:00Z"
SOURCE = "https://hedidntjump.com/volumes"
BOOK_ID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "https://hedidntjump.com/volumes#epub-volumes-1-5"))
ZIP_TIME = (2026, 10, 19, 0, 0, 0)

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
VOLUME_TITLES = {
    1: "Primary Documents & Forensic Analysis",
    2: "News Coverage & Family Battles",
    3: "Personal Photographs & Research Materials",
    4: "The Physics Case",
    5: "The Human & Institutional Evidence",
}
OCR_FONT = "GlyphLessFont"  # ocrmypdf's invisible text layer
OCR_PAGE_MIN = 0.80  # share of clean OCR lines a page needs before any is shown
IMG_MAX = 1200
JPEG_Q = 80

DICT_PATH = Path("/usr/share/dict/words")
WORDS = (
    {w.strip().lower() for w in DICT_PATH.read_text(errors="ignore").splitlines()}
    if DICT_PATH.exists()
    else set()
)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def xhtml(title: str, body: str, *, epub_type: str = "") -> str:
    et = f' epub:type="{epub_type}"' if epub_type else ""
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
        'xml:lang="en" lang="en">\n'
        f"<head>\n<meta charset=\"utf-8\"/>\n<title>{esc(title)}</title>\n"
        '<link rel="stylesheet" type="text/css" href="css/style.css"/>\n</head>\n'
        f"<body{et}>\n{body}\n</body>\n</html>\n"
    )


CSS = """
body { font-family: serif; line-height: 1.45; margin: 0 4%; }
h1, h2, h3 { font-family: serif; line-height: 1.2; }
h1 { font-size: 1.6em; text-align: center; margin: 1.5em 0 0.4em; }
h2 { font-size: 1.3em; margin: 1.4em 0 0.6em; }
h3 { font-size: 1.05em; margin: 1.1em 0 0.4em; }
p { margin: 0 0 0.7em; }
.center { text-align: center; }
.small { font-size: 0.85em; }
.label { font-size: 0.8em; letter-spacing: 0.05em; text-transform: uppercase; text-align: center; margin: 0.6em 0; }
.subtitle { text-align: center; font-style: italic; }
figure.facsimile { margin: 0.5em 0; text-align: center; page-break-inside: avoid; }
figure.facsimile img { max-width: 100%; max-height: 80vh; }
figcaption { font-size: 0.85em; margin-top: 0.3em; }
.ocr { font-size: 0.9em; border-left: 2px solid #999; padding-left: 0.8em; margin-top: 1em; }
.ocr-note { font-size: 0.8em; font-style: italic; }
.gap { color: #666; }
h2.facs { margin: 0.2em 0; font-size: 0.75em; }
ul.numbered { list-style: none; padding-left: 0.5em; }
table { border-collapse: collapse; width: 100%; font-size: 0.85em; margin: 0.8em 0; }
th, td { border: 1px solid #888; padding: 0.25em 0.4em; text-align: left; vertical-align: top; }
.cover { margin: 0; padding: 0; text-align: center; }
.cover img { max-width: 100%; max-height: 100vh; }
nav ol { list-style: none; padding-left: 1em; }
"""


# ---------------------------------------------------------------- cover image
def _font(name: str, size: int):
    for path in (
        f"/usr/share/fonts/truetype/sand-box/google/IBM Plex Serif/IBMPlexSerif-{name}.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if name == "Bold" else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_cover() -> bytes:
    """Portrait cover from existing site art: the 1917 Arctic Building plate
    (docs/assets/arctic-building-1917.webp) on the site's newsprint palette."""
    W, H = 1600, 2400
    paper, ink, red = (244, 236, 213), (20, 17, 12), (139, 30, 30)
    im = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 28], fill=ink)
    d.rectangle([0, H - 28, W, H], fill=ink)

    def centered(y, text, font, fill=ink):
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, y), text, font=font, fill=fill)

    centered(120, "THE MARION ZIONCHECK ARCHIVE", _font("SemiBold", 54), red)
    d.rectangle([140, 215, W - 140, 223], fill=ink)
    centered(250, "He Didn\u2019t Jump", _font("Bold", 190))
    d.rectangle([140, 490, W - 140, 498], fill=ink)
    centered(530, "Volumes I\u2013V \u00b7 Seattle, 7 August 1936", _font("Regular", 60))

    photo = Image.open(ASSETS / "arctic-building-1917.webp").convert("RGB")
    pw = 960
    ph = round(photo.height * pw / photo.width)
    photo = photo.resize((pw, ph), Image.LANCZOS)
    px, py = (W - pw) // 2, 680
    d.rectangle([px - 10, py - 10, px + pw + 10, py + ph + 10], fill=ink)
    im.paste(photo, (px, py))
    cap_y = py + ph + 40
    centered(cap_y, "The Arctic Building, Seattle (1917)", _font("Italic", 44))
    centered(H - 230, "Aziel Eliab", _font("SemiBold", 84))
    centered(H - 120, "The record, not the verdict.", _font("Italic", 46))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85, optimize=True)
    return buf.getvalue()


# --------------------------------------------------------- vols I–III (scans)
def jpeg_from_xref(doc, xref: int) -> bytes:
    info = doc.extract_image(xref)
    img = Image.open(io.BytesIO(info["image"]))
    img.load()
    img = img.convert("RGB")
    img.thumbnail((IMG_MAX, IMG_MAX), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=JPEG_Q, optimize=True)
    return buf.getvalue()


def _clean_fragment(text: str) -> bool:
    """A strict check that an OCR fragment is clean prose."""
    if not WORDS:
        return False
    if re.search(r"[|\\{}<>~_¢©®°\[\]€£§¶•!]|,,|\.\.(?!\.)|\s[.,;:]", text):
        return False
    if not re.match(r"[A-Za-z“\"(0-9]", text):
        return False
    tokens = re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?|\S", text)
    words = [t for t in tokens if re.match(r"[A-Za-z]", t)]
    if len(words) < 4:
        return False
    junk = [t for t in tokens if not re.match(r"[A-Za-z0-9]", t) and t not in ".,;:'’\"“”()-–—?!&%$/"]
    if junk:
        return False
    ok = 0
    for w in words:
        lw = w.lower().replace("’", "'")
        if lw in WORDS or lw.rstrip("s") in WORDS or re.sub(r"'s$", "", lw) in WORDS:
            ok += 1
        elif w[0].isupper() and len(w) > 2 and w[1:].islower():
            ok += 0.75  # proper nouns get partial credit
    short_junk = sum(1 for w in words if len(w) == 1 and w.lower() not in ("a", "i"))
    return ok / len(words) >= 0.95 and short_junk == 0


def ocr_passages(page) -> list[str]:
    """Clean OCR passages from the invisible text layer, in reading order.
    Rejected stretches become a single gap marker."""
    lines = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = [s for s in line["spans"] if s["font"] == OCR_FONT]
            text = " ".join(s["text"].strip() for s in spans if s["text"].strip())
            if text:
                lines.append(text)
    # Only pages whose OCR is clean overall get a transcription at all.
    substantive = [t for t in lines if len(t.split()) >= 3]
    clean = [t for t in substantive if _clean_fragment(t)]
    if len(substantive) < 6 or len(clean) / len(substantive) < OCR_PAGE_MIN:
        return []
    out: list[str] = []
    current: list[str] = []
    gap = False
    for text in lines:
        if _clean_fragment(text):
            if gap and (out or current):
                if current:
                    out.append(" ".join(current))
                    current = []
                out.append("[…]")
            gap = False
            current.append(text)
        else:
            gap = True
    if current:
        out.append(" ".join(current))
    # Join hyphenated line breaks; keep only passages with some substance.
    passages = []
    for p in out:
        if p != "[…]":
            p = re.sub(r"(\w)- ([a-z])", r"\1\2", p)
            p = re.sub(r"(\w)- ([A-Z])", r"\1-\2", p)
            p = re.sub(r"\s*\S+-$", "", p)  # drop a word broken at the passage end
        if p == "[…]" or len(p.split()) >= 8:
            passages.append(p)
    while passages and passages[0] == "[…]":
        passages.pop(0)
    while passages and passages[-1] == "[…]":
        passages.pop()
    collapsed = []
    for p in passages:
        if p == "[…]" and collapsed and collapsed[-1] == "[…]":
            continue
        collapsed.append(p)
    return collapsed


def typed_spans(page) -> list[tuple[str, float, str]]:
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for s in line["spans"]:
                if s["font"] != OCR_FONT and s["text"].strip():
                    out.append((s["text"].strip(), s["size"], s["font"]))
    return out


def scan_volume(n: int, files: dict, nav: list, spine: list) -> None:
    doc = pymupdf.open(VOLDIR / f"volume-{n}.pdf")
    roman = ROMAN[n]
    vol_entry = {"title": f"Volume {roman}: {VOLUME_TITLES[n]}", "href": f"v{n}-title.xhtml", "children": []}

    # Volume title page: the typed cover text from PDF page 1.
    cover_lines = [t for t, _s, _f in typed_spans(doc[0])]
    body = [f'<section epub:type="part" id="vol{n}">',
            f'<p class="label">Volume {roman}</p>',
            f"<h1>{esc(VOLUME_TITLES[n])}</h1>"]
    if cover_lines:
        body.append('<p class="label">From the PDF cover</p>')
        for t in cover_lines:
            body.append(f'<p class="center">{esc(t)}</p>')
    body.append(
        f'<p class="small center">Image facsimile edition. Original PDF: '
        f'<a href="https://hedidntjump.com/volumes/volume-{n}.pdf">hedidntjump.com/volumes/volume-{n}.pdf</a></p>'
    )
    body.append("</section>")
    files[f"v{n}-title.xhtml"] = ("application/xhtml+xml", xhtml(f"Volume {roman}", "\n".join(body)))
    spine.append(f"v{n}-title.xhtml")

    for pno in range(len(doc)):
        page = doc[pno]
        images = page.get_images(full=True)
        if not images:
            continue  # cover (handled above) or blank page
        label_n = pno + 1
        caption = ""
        for t, _s, _f in typed_spans(page):
            m = re.search(r"IMAGE\s+(\d+)\s+OF\s+(\d+)", t)
            if m:
                caption = f"Image {m.group(1)} of {m.group(2)}"
        img_name = f"images/v{n}-p{label_n:02d}.jpg"
        files[img_name] = ("image/jpeg", jpeg_from_xref(doc, images[0][0]))
        fname = f"v{n}-p{label_n:02d}.xhtml"
        title = f"Volume {roman}, facsimile page {label_n}"
        alt = f"Facsimile page {label_n} of Volume {roman}" + (f" ({caption.lower()})" if caption else "")
        body = [
            f'<section id="v{n}p{label_n}">',
            f'<h2 class="label facs">Volume {roman} · facsimile page {label_n}</h2>',
            '<figure class="facsimile">',
            f'<img src="{img_name}" alt="{esc(alt)}"/>',
            f"<figcaption>Facsimile page {label_n}" + (f" · {esc(caption)}" if caption else "") + "</figcaption>",
            "</figure>",
        ]
        passages = ocr_passages(page)
        if passages:
            body.append('<div class="ocr">')
            body.append(
                '<p class="ocr-note">Machine transcription (OCR) of the clearly legible passages only. '
                "Unverified and may contain recognition errors; […] marks text that could not be read "
                "reliably. The page image above is the authoritative copy.</p>"
            )
            for p in passages:
                cls = ' class="gap"' if p == "[…]" else ""
                body.append(f"<p{cls}>{esc(p)}</p>")
            body.append("</div>")
        body.append("</section>")
        files[fname] = ("application/xhtml+xml", xhtml(title, "\n".join(body)))
        spine.append(fname)
        vol_entry["children"].append({"title": f"Facsimile page {label_n}" + (f" — {caption}" if caption else ""), "href": fname})
    nav.append(vol_entry)


# ----------------------------------------------------------- vols IV–V (text)
def _span_html(spans) -> str:
    parts = []
    for s in spans:
        t = esc(s["text"])
        if "Bold" in s["font"] and t.strip():
            parts.append(f"<strong>{t}</strong>")
        else:
            parts.append(t)
    return "".join(parts)


def _join_lines(lines) -> str:
    out = ""
    for line in lines:
        seg = _span_html(line["spans"]).strip()
        if not seg:
            continue
        if not out:
            out = seg
        elif out.endswith("-") and not out.endswith(" -"):
            out += seg
        else:
            out += " " + seg
    out = out.replace("</strong> <strong>", " ").replace("</strong><strong>", "")
    return re.sub(r"\s{2,}", " ", out)


def _plain(block) -> str:
    return " ".join(s["text"] for l in block["lines"] for s in l["spans"]).strip()


def _all_bold(block) -> bool:
    spans = [s for l in block["lines"] for s in l["spans"] if s["text"].strip()]
    return bool(spans) and all("Bold" in s["font"] for s in spans)


def _max_size(block) -> float:
    return max(s["size"] for l in block["lines"] for s in l["spans"])


def text_volume(n: int, files: dict, nav: list, spine: list) -> None:
    doc = pymupdf.open(VOLDIR / f"volume-{n}.pdf")
    roman = ROMAN[n]
    vol_entry = {"title": f"Volume {roman}: {VOLUME_TITLES[n]}", "href": f"v{n}-title.xhtml", "children": []}

    # Title page from PDF page 1 (page 2 repeats it).
    tblocks = [b for b in doc[0].get_text("dict")["blocks"] if b["type"] == 0]
    body = [f'<section epub:type="part" id="vol{n}">', f'<p class="label">Volume {roman}</p>',
            f"<h1>{esc(VOLUME_TITLES[n])}</h1>", '<p class="label">From the PDF title page</p>']
    for b in tblocks:
        body.append(f'<p class="center">{esc(_plain(b))}</p>')
    body.append(
        f'<p class="small center">Original PDF: <a href="https://hedidntjump.com/volumes/volume-{n}.pdf">'
        f"hedidntjump.com/volumes/volume-{n}.pdf</a></p></section>"
    )
    files[f"v{n}-title.xhtml"] = ("application/xhtml+xml", xhtml(f"Volume {roman}", "\n".join(body)))
    spine.append(f"v{n}-title.xhtml")

    # The printed contents page gives the same headings in mixed case; use it
    # for display when the words match exactly (headings are printed in caps).
    printed_toc = {}
    for pno in range(2, min(5, len(doc))):
        blocks = [b for b in doc[pno].get_text("dict")["blocks"] if b["type"] == 0]
        if any(_plain(b).upper() == "TABLE OF CONTENTS" for b in blocks):
            for b in blocks:
                t = _plain(b)
                if re.match(r"^\d+\.\s", t):
                    printed_toc[t.upper()] = t

    chapters: list[dict] = []
    cur: dict | None = None
    list_kind = None  # "ul" | "num"
    table: list[list[str]] | None = None
    last_para_open = False

    def close_list():
        nonlocal list_kind
        if list_kind and cur is not None:
            cur["html"].append("</ul>")
        list_kind = None

    def close_table():
        nonlocal table
        if table and cur is not None:
            rows = ["<table>"]
            head, *rest = table
            rows.append("<thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead><tbody>")
            for r in rest:
                rows.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
            rows.append("</tbody></table>")
            cur["html"].extend(rows)
        table = None

    for pno in range(2, len(doc)):
        page = doc[pno]
        blocks = [b for b in page.get_text("dict")["blocks"] if b["type"] == 0]
        body_blocks = [b for b in blocks if 30 <= b["bbox"][1] <= 760]
        if any(_plain(b).upper() == "TABLE OF CONTENTS" for b in body_blocks):
            continue  # printed contents; the EPUB nav replaces it
        first_on_page = True
        for b in body_blocks:
            text = _plain(b)
            if not text:
                continue
            size = _max_size(b)
            if _all_bold(b) and size >= 12:
                close_list(); close_table()
                shown = printed_toc.get(text.upper(), text)
                cur = {"title": shown, "html": [f"<h2>{esc(shown)}</h2>"]}
                chapters.append(cur)
                last_para_open = False
                first_on_page = False
                continue
            if cur is None:
                cur = {"title": f"Volume {roman}", "html": []}
                chapters.append(cur)
            xs = {round(l["bbox"][0]) for l in b["lines"]}
            ys = {round(l["bbox"][1]) for l in b["lines"]}
            if size <= 7.5 and len(b["lines"]) >= 3 and len(ys) == 1 and len(xs) == len(b["lines"]):
                close_list()
                row = [esc(" ".join(s["text"] for s in l["spans"]).strip()) for l in b["lines"]]
                table = (table or []) + [row]
                last_para_open = False
                first_on_page = False
                continue
            close_table()
            m_bullet = re.match(r"^[•●▪]\s*", text)
            m_num = re.match(r"^\d+\.\s", text) and b["bbox"][0] > 60
            if m_bullet or m_num:
                kind = "ul" if m_bullet else "num"
                if list_kind != kind:
                    close_list()
                    cur["html"].append("<ul>" if kind == "ul" else '<ul class="numbered">')
                    list_kind = kind
                item = _join_lines(b["lines"])
                if m_bullet:
                    item = re.sub(r"^(<strong>)?[•●▪]\s*", r"\1", item)
                cur["html"].append(f"<li>{item}</li>")
                last_para_open = False
                first_on_page = False
                continue
            close_list()
            inner = _join_lines(b["lines"])
            if text.startswith("—") and text.endswith("—"):
                cur["html"].append(f'<p class="center">{inner}</p>')
            elif _all_bold(b) and len(text) < 90 and text.endswith(":"):
                cur["html"].append(f"<h3>{esc(text)}</h3>")
                last_para_open = False
                first_on_page = False
                continue
            elif first_on_page and last_para_open and cur["html"] and cur["html"][-1].startswith("<p>"):
                prev = cur["html"].pop()
                cur["html"].append(prev[:-4] + " " + inner + "</p>")
            else:
                cur["html"].append(f"<p>{inner}</p>")
            last_para_open = not re.search(r"[.!?:”\"')]\s*(</strong>)?$", inner)
            first_on_page = False
    close_list(); close_table()

    for i, ch in enumerate(chapters, 1):
        fname = f"v{n}-c{i:02d}.xhtml"
        files[fname] = ("application/xhtml+xml",
                        xhtml(f"Volume {roman}: {ch['title']}", f'<section epub:type="chapter">\n' + "\n".join(ch["html"]) + "\n</section>"))
        spine.append(fname)
        vol_entry["children"].append({"title": ch["title"], "href": fname})
    nav.append(vol_entry)


# -------------------------------------------------------------- front matter
def front_matter(files: dict, nav: list, spine: list) -> None:
    files["images/cover.jpg"] = ("image/jpeg", make_cover())
    files["cover.xhtml"] = ("application/xhtml+xml", xhtml(
        "Cover", '<section epub:type="cover" class="cover"><img src="images/cover.jpg" '
        f'alt="Cover: {esc(TITLE)}, by {esc(AUTHOR)}"/></section>', epub_type="frontmatter"))
    files["title.xhtml"] = ("application/xhtml+xml", xhtml("Title page", "\n".join([
        '<section epub:type="titlepage">',
        "<h1>He Didn’t Jump</h1>",
        '<p class="subtitle">The Marion Zioncheck Archive</p>',
        '<p class="center">Volumes I–V</p>',
        f'<p class="center"><strong>{esc(AUTHOR)}</strong></p>',
        f'<p class="center small">{esc(PUBLISHER)} · 19 October 2026</p>',
        "</section>"]), epub_type="frontmatter"))
    about = [
        '<section epub:type="preface">',
        "<h2>About this edition</h2>",
        "<p>This is a free edition of the five research volumes of <em>He Didn’t Jump</em>, a document archive "
        "that re-examines the official account of the death of U.S. Representative Marion A. Zioncheck at the "
        "Arctic Building, Seattle, on 7 August 1936. It is a document archive, not a game or an ARG.</p>",
        f'<p>Source: <a href="{SOURCE}">{SOURCE}</a>, where the original PDFs can be downloaded.</p>',
        "<p><strong>Volumes I–III</strong> are image facsimiles of clippings, photographs and documents. Each page is "
        "reproduced as an image labelled “facsimile page N”, where N is the page number in the original PDF. "
        "Where the machine OCR of a page was clearly legible, those passages are given as text beneath the image. "
        "OCR may contain recognition errors; passages that could not be read reliably are omitted and marked […]. "
        "The page image is always the authoritative copy.</p>",
        "<p><strong>Volumes IV–V</strong> are converted from the text of the original PDFs into reflowable chapters. "
        "Running page headers and footers, the repeated inner title page and the printed table of contents were "
        "removed; the wording is unchanged.</p>",
        "<p>Original rights in reproduced clippings and photographs remain with their respective holders.</p>",
        "</section>",
    ]
    files["about.xhtml"] = ("application/xhtml+xml", xhtml("About this edition", "\n".join(about), epub_type="frontmatter"))
    spine.extend(["cover.xhtml", "title.xhtml", "about.xhtml"])
    nav.extend([{"title": "Title page", "href": "title.xhtml", "children": []},
                {"title": "About this edition", "href": "about.xhtml", "children": []}])


# ------------------------------------------------------------------ packaging
def nav_doc(nav: list) -> str:
    def render(items, depth=0):
        out = ["<ol>"]
        for it in items:
            out.append(f'<li><a href="{it["href"]}">{esc(it["title"])}</a>')
            if it.get("children"):
                out.extend(render(it["children"], depth + 1))
            out.append("</li>")
        out.append("</ol>")
        return out
    body = ['<nav epub:type="toc" id="toc"><h2>Contents</h2>', *render(nav), "</nav>",
            '<nav epub:type="landmarks" id="landmarks" hidden="hidden"><ol>',
            '<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>',
            '<li><a epub:type="titlepage" href="title.xhtml">Title page</a></li>',
            '<li><a epub:type="bodymatter" href="v1-title.xhtml">Volume I</a></li>',
            "</ol></nav>"]
    return xhtml("Contents", "\n".join(body))


def ncx_doc(nav: list) -> str:
    counter = [0]
    def render(items):
        out = []
        for it in items:
            counter[0] += 1
            out.append(f'<navPoint id="np{counter[0]}" playOrder="{counter[0]}"><navLabel><text>{esc(it["title"])}</text></navLabel><content src="{it["href"]}"/>')
            out.extend(render(it.get("children") or []))
            out.append("</navPoint>")
        return out
    points = "\n".join(render(nav))
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head>'
            f'<meta name="dtb:uid" content="{BOOK_ID}"/><meta name="dtb:depth" content="2"/>'
            '<meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>'
            f"<docTitle><text>{esc(TITLE)}</text></docTitle><navMap>\n{points}\n</navMap></ncx>\n")


def opf_doc(files: dict, spine: list) -> str:
    items = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
             '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>']
    ids = {}
    for i, (name, (mtype, _)) in enumerate(sorted(files.items()), 1):
        iid = "i" + re.sub(r"[^A-Za-z0-9]", "_", name)
        ids[name] = iid
        props = ' properties="cover-image"' if name == "images/cover.jpg" else ""
        items.append(f'<item id="{iid}" href="{name}" media-type="{mtype}"{props}/>')
    spine_xml = "\n".join(
        f'<itemref idref="{ids[s]}"' + (' linear="yes"' if True else "") + "/>" for s in spine)
    return f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
<dc:title>{esc(TITLE)}</dc:title>
<dc:creator id="creator">{esc(AUTHOR)}</dc:creator>
<meta refines="#creator" property="role" scheme="marc:relators">aut</meta>
<dc:language>en</dc:language>
<dc:publisher>{esc(PUBLISHER)}</dc:publisher>
<dc:date>{DATE}</dc:date>
<dc:source>{SOURCE}</dc:source>
<dc:subject>Marion Zioncheck</dc:subject>
<dc:subject>Arctic Building (Seattle)</dc:subject>
<dc:subject>Seattle (Wash.) — History — 20th century</dc:subject>
<dc:subject>United States. Congress — History — 1936</dc:subject>
<dc:description>{esc("A free document archive edition of the five research volumes of He Didn't Jump, re-examining the official account of the death of U.S. Representative Marion A. Zioncheck at the Arctic Building, Seattle, on 7 August 1936. Volumes I–III are image facsimiles; Volumes IV–V are reflowable text.")}</dc:description>
<dc:rights>Original rights in reproduced clippings and photographs remain with their respective holders.</dc:rights>
<meta property="dcterms:modified">{MODIFIED}</meta>
<meta name="cover" content="{ids["images/cover.jpg"]}"/>
</metadata>
<manifest>
{chr(10).join(items)}
</manifest>
<spine toc="ncx">
{spine_xml}
</spine>
</package>
'''


def build(out: Path) -> None:
    files: dict[str, tuple[str, str | bytes]] = {}
    nav: list = []
    spine: list = []
    front_matter(files, nav, spine)
    for n in (1, 2, 3):
        scan_volume(n, files, nav, spine)
    for n in (4, 5):
        text_volume(n, files, nav, spine)
    files["css/style.css"] = ("text/css", CSS.lstrip())
    entries = {
        "OEBPS/nav.xhtml": nav_doc(nav),
        "OEBPS/toc.ncx": ncx_doc(nav),
        "OEBPS/content.opf": opf_doc(files, spine),
        **{f"OEBPS/{k}": v for k, (_m, v) in sorted(files.items())},
    }
    container = ('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                 "</rootfiles></container>\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w") as zf:
        def add(name, data, compress=True):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data.encode("utf-8") if isinstance(data, str) else data)
        add("mimetype", "application/epub+zip", compress=False)
        add("META-INF/container.xml", container)
        for name, data in entries.items():
            add(name, data, compress=not name.endswith(".jpg"))
    size = out.stat().st_size
    print(f"wrote {out} ({size} bytes, {size / 1048576:.1f} MiB); {len(spine)} spine items")
    if size > 25 * 1024 * 1024:
        print("WARNING: over 25 MiB; split into per-volume EPUBs", file=sys.stderr)


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT)
