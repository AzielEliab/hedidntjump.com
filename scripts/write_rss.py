#!/usr/bin/env python3
"""Write RSS 2.0 and Atom feeds for the Marion Zioncheck archive.

Item titles and descriptions are copied from the published HTML. Volume
entries use the volume-card headings and purpose paragraphs on /volumes,
and point at the facsimile reader. PDF and zip files are enclosures of
those existing downloads.

Canonical links are the apex host. www.hedidntjump.com 301s to
https://hedidntjump.com (functions/_middleware.js and docs/_redirects),
which is the URL already used in <link rel="canonical">.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "docs", ROOT / "dist"]
APEX = "https://hedidntjump.com"
PERSON = "https://www.azieleliab.com/#aziel"
CHANNEL_TITLE = "He Didn't Jump"
# Newest published surface in the feed (doors / ecosystem stamp). Sitemap
# lastmod stays inside the dates verify_azindex_growth.py already allows.
FEED_DAY = "2026-11-20"
PAGE_DAY = "2026-10-30"

# Reading order of the newspaper, not a claim of new historical events.
PAGES: list[tuple[str, str, str]] = [
    ("index.html", "/", PAGE_DAY),
    ("case.html", "/case", PAGE_DAY),
    ("inquiries.html", "/inquiries", PAGE_DAY),
    ("official-narrative.html", "/official-narrative", PAGE_DAY),
    ("volumes.html", "/volumes", PAGE_DAY),
    ("foia.html", "/foia", PAGE_DAY),
    ("press.html", "/press", PAGE_DAY),
    ("rubye.html", "/rubye", PAGE_DAY),
    ("archives.html", "/archives", PAGE_DAY),
    ("reader.html", "/reader", PAGE_DAY),
    ("aziel.html", "/aziel", PAGE_DAY),
    ("who.html", "/who", PAGE_DAY),
    ("doors.html", "/doors", FEED_DAY),
    ("copyrights.html", "/copyrights", PAGE_DAY),
    ("receipts.html", "/receipts", PAGE_DAY),
]

VOLUME_CARD = re.compile(
    r'<article class="volume-card" id="volume-(\d+)">\s*'
    r'<p class="volume-card-num">Volume ([IVX]+)</p>\s*'
    r"<h2>(.*?)</h2>\s*"
    r'<p class="volume-card-purpose">(.*?)</p>',
    re.S,
)

HEAD_LINKS = (
    '<link rel="alternate" type="application/rss+xml" '
    'title="He Didn\'t Jump (RSS)" href="https://hedidntjump.com/rss.xml">\n'
    '<link rel="alternate" type="application/atom+xml" '
    'title="He Didn\'t Jump (Atom)" href="https://hedidntjump.com/atom.xml">\n'
)

HEADER_TYPES = """
/rss.xml
  Content-Type: application/rss+xml; charset=utf-8
  Cache-Control: public, max-age=3600

/atom.xml
  Content-Type: application/atom+xml; charset=utf-8
  Cache-Control: public, max-age=3600
"""

REDIRECTS = """# RSS and Atom. Aliases 301 to the files that return 200.
/rss /rss.xml 301
/feed /rss.xml 301
/feed.xml /rss.xml 301
/atom /atom.xml 301
"""

SITEMAP_ENTRIES = """  <url>
    <loc>https://hedidntjump.com/rss.xml</loc>
    <lastmod>2026-11-20</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://hedidntjump.com/atom.xml</loc>
    <lastmod>2026-11-20</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.4</priority>
  </url>
"""

OPENAPI_PATHS = """    "/rss.xml": {
      "get": {
        "summary": "RSS 2.0 of the published papers and Volumes I–V",
        "responses": {
          "200": {
            "description": "application/rss+xml"
          }
        }
      }
    },
    "/atom.xml": {
      "get": {
        "summary": "Atom feed of the same published papers and Volumes I–V",
        "responses": {
          "200": {
            "description": "application/atom+xml"
          }
        }
      }
    }
"""


@dataclass(frozen=True)
class Enclosure:
    href: str
    length: int
    mime: str


@dataclass(frozen=True)
class Item:
    title: str
    path: str
    description: str
    day: str
    enclosure: Enclosure | None = None

    @property
    def link(self) -> str:
        return APEX + self.path


def xml_text(value: str) -> str:
    return escape(value)


def xml_attr(value: str) -> str:
    return escape(value, {'"': "&quot;"})


def rfc822(day: str) -> str:
    year, month, dom = (int(part) for part in day.split("-"))
    return format_datetime(datetime(year, month, dom, tzinfo=timezone.utc))


def atom_time(day: str) -> str:
    return f"{day}T00:00:00Z"


def plain(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def extract_title(page: str) -> str:
    match = re.search(r"<title>(.*?)</title>", page, re.S)
    if not match:
        raise SystemExit("missing <title>")
    return plain(match.group(1))


def extract_description(page: str) -> str:
    match = re.search(r'<meta name="description" content="([^"]*)"', page)
    if not match:
        raise SystemExit("missing meta description")
    return plain(match.group(1))


def file_len(tree: Path, rel: str) -> int:
    path = tree / rel.lstrip("/")
    if not path.is_file():
        raise SystemExit(f"missing enclosure {path}")
    return path.stat().st_size


def enclosure_for(tree: Path, rel: str, mime: str) -> Enclosure:
    length = file_len(tree, rel)
    other = (ROOT / "dist" if tree.name == "docs" else ROOT / "docs") / rel.lstrip("/")
    if other.is_file() and other.stat().st_size != length:
        raise SystemExit(f"enclosure size differs for {rel}")
    return Enclosure(href=APEX + rel, length=length, mime=mime)


def volume_items(tree: Path) -> list[Item]:
    page = (tree / "volumes.html").read_text(encoding="utf-8")
    found = VOLUME_CARD.findall(page)
    if [number for number, _roman, _title, _purpose in found] != ["1", "2", "3", "4", "5"]:
        raise SystemExit(f"volume cards drifted: {found!r}")
    items: list[Item] = []
    for number, roman, title, purpose in found:
        items.append(
            Item(
                title=f"Volume {roman} — {plain(title)}",
                path=f"/reader?volume={number}&page=1",
                description=plain(purpose),
                day=PAGE_DAY,
                enclosure=enclosure_for(
                    tree, f"/volumes/volume-{number}.pdf", "application/pdf"
                ),
            )
        )
    return items


def build_items(tree: Path) -> list[Item]:
    items: list[Item] = []
    for name, path, day in PAGES:
        page = (tree / name).read_text(encoding="utf-8")
        enc = None
        if path == "/archives":
            enc = enclosure_for(
                tree, "/volumes/hedidntjump-all-volumes.zip", "application/zip"
            )
        items.append(
            Item(
                title=extract_title(page),
                path=path,
                description=extract_description(page),
                day=day,
                enclosure=enc,
            )
        )
        if path == "/volumes":
            items.extend(volume_items(tree))
    return items


def channel_description(tree: Path) -> str:
    page = (tree / "index.html").read_text(encoding="utf-8")
    return extract_description(page)


def render_rss(items: list[Item], description: str) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">',
        "  <channel>",
        f"    <title>{xml_text(CHANNEL_TITLE)}</title>",
        f"    <link>{APEX}/</link>",
        f'    <atom:link href="{APEX}/rss.xml" rel="self" type="application/rss+xml"/>',
        f"    <description>{xml_text(description)}</description>",
        "    <language>en-us</language>",
        f"    <lastBuildDate>{rfc822(FEED_DAY)}</lastBuildDate>",
        "    <generator>scripts/write_rss.py</generator>",
        "    <copyright>Aziel Eliab</copyright>",
        "    <dc:creator>Aziel Eliab</dc:creator>",
        f"    <dc:rights>See {APEX}/copyrights</dc:rights>",
        "    <image>",
        f"      <url>{APEX}/assets/logo.jpg</url>",
        f"      <title>{xml_text(CHANNEL_TITLE)}</title>",
        f"      <link>{APEX}/</link>",
        "    </image>",
    ]
    for item in items:
        lines.extend(
            [
                "    <item>",
                f"      <title>{xml_text(item.title)}</title>",
                f"      <link>{xml_text(item.link)}</link>",
                f'      <guid isPermaLink="true">{xml_text(item.link)}</guid>',
                f"      <pubDate>{rfc822(item.day)}</pubDate>",
                "      <dc:creator>Aziel Eliab</dc:creator>",
                f"      <description>{xml_text(item.description)}</description>",
            ]
        )
        if item.enclosure:
            enc = item.enclosure
            lines.append(
                "      <enclosure"
                f' url="{xml_attr(enc.href)}"'
                f' length="{enc.length}"'
                f' type="{xml_attr(enc.mime)}"/>'
            )
        lines.append("    </item>")
    lines.extend(["  </channel>", "</rss>", ""])
    return "\n".join(lines)


def render_atom(items: list[Item], description: str) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f"  <title>{xml_text(CHANNEL_TITLE)}</title>",
        f"  <subtitle>{xml_text(description)}</subtitle>",
        f'  <link href="{APEX}/" rel="alternate" type="text/html"/>',
        f'  <link href="{APEX}/atom.xml" rel="self" type="application/atom+xml"/>',
        f'  <link href="{APEX}/rss.xml" rel="alternate" type="application/rss+xml"/>',
        f"  <id>{APEX}/atom.xml</id>",
        f"  <updated>{atom_time(FEED_DAY)}</updated>",
        "  <author>",
        "    <name>Aziel Eliab</name>",
        f"    <uri>{PERSON}</uri>",
        "  </author>",
        f"  <rights>Aziel Eliab. See {APEX}/copyrights</rights>",
        "  <generator>scripts/write_rss.py</generator>",
    ]
    for item in items:
        lines.extend(
            [
                "  <entry>",
                f"    <title>{xml_text(item.title)}</title>",
                f'    <link href="{xml_attr(item.link)}" rel="alternate" type="text/html"/>',
                f"    <id>{xml_text(item.link)}</id>",
                f"    <updated>{atom_time(item.day)}</updated>",
                '    <author><name>Aziel Eliab</name></author>',
                f'    <summary type="text">{xml_text(item.description)}</summary>',
            ]
        )
        if item.enclosure:
            enc = item.enclosure
            lines.append(
                "    <link"
                ' rel="enclosure"'
                f' href="{xml_attr(enc.href)}"'
                f' type="{xml_attr(enc.mime)}"'
                f' length="{enc.length}"/>'
            )
        lines.append("  </entry>")
    lines.extend(["</feed>", ""])
    return "\n".join(lines)


def ensure_insert(text: str, anchor: str, addition: str, label: str) -> str:
    if addition in text:
        return text
    count = text.count(anchor)
    if count != 1:
        raise SystemExit(f"{label}: anchor count {count}")
    return text.replace(anchor, anchor + addition, 1)


def patch_html(text: str) -> str:
    if "application/rss+xml" in text and "application/atom+xml" in text:
        return text
    canonical = re.search(r'^<link rel="canonical" href="[^"]+">\n', text, re.M)
    if canonical:
        at = canonical.end()
        return text[:at] + HEAD_LINKS + text[at:]
    description = re.search(r'^<meta name="description" content="[^"]*">\n', text, re.M)
    if not description:
        raise SystemExit("html has neither canonical nor description")
    at = description.end()
    return text[:at] + HEAD_LINKS + text[at:]


def patch_headers(text: str) -> str:
    anchor = '</graph.jsonld>; rel="describedby"; type="application/ld+json"'
    addition = (
        ', </rss.xml>; rel="alternate"; type="application/rss+xml"'
        ', </atom.xml>; rel="alternate"; type="application/atom+xml"'
    )
    text = ensure_insert(text, anchor, addition, "_headers link")
    if "\n/rss.xml\n" not in text:
        text = text.rstrip() + "\n" + HEADER_TYPES.strip() + "\n"
    return text if text.endswith("\n") else text + "\n"


def patch_robots(text: str) -> str:
    return ensure_insert(
        text,
        "Allow: /llms.txt\n",
        "Allow: /rss.xml\nAllow: /atom.xml\n",
        "robots",
    )


def patch_redirects(text: str) -> str:
    if "/feed /rss.xml 301" in text and "/atom /atom.xml 301" in text:
        return text if text.endswith("\n") else text + "\n"
    anchor = "https://www.hedidntjump.com/* https://hedidntjump.com/:splat 301\n"
    if text.count(anchor) != 1:
        raise SystemExit(f"redirects: anchor count {text.count(anchor)}")
    return text.replace(anchor, REDIRECTS + anchor, 1)


def patch_sitemap(text: str) -> str:
    if f"<loc>{APEX}/rss.xml</loc>" in text and f"<loc>{APEX}/atom.xml</loc>" in text:
        return text if text.endswith("\n") else text + "\n"
    if text.count("</urlset>") != 1:
        raise SystemExit("sitemap: expected one </urlset>")
    if not text.endswith("\n"):
        text += "\n"
    return text.replace("</urlset>\n", SITEMAP_ENTRIES + "</urlset>\n", 1)


def patch_llms(text: str) -> str:
    return ensure_insert(
        text,
        "- [https://hedidntjump.com/llms.txt](https://hedidntjump.com/llms.txt)\n",
        "- [https://hedidntjump.com/rss.xml](https://hedidntjump.com/rss.xml) — RSS 2.0 of the published papers and Volumes I–V\n"
        "- [https://hedidntjump.com/atom.xml](https://hedidntjump.com/atom.xml) — Atom of the same items\n",
        "llms.txt",
    )


def patch_ai(text: str) -> str:
    return ensure_insert(
        text,
        "- https://www.hedidntjump.com/sitemap.xml\n",
        "- https://hedidntjump.com/rss.xml — RSS 2.0 of the published papers and Volumes I–V\n"
        "- https://hedidntjump.com/atom.xml — Atom of the same items\n",
        "ai.txt",
    )


def patch_help(text: str) -> str:
    return ensure_insert(
        text,
        "- [https://hedidntjump.com/llms.txt](https://hedidntjump.com/llms.txt)\n",
        "- [https://hedidntjump.com/rss.xml](https://hedidntjump.com/rss.xml) — RSS 2.0 of the published papers and Volumes I–V\n"
        "- [https://hedidntjump.com/atom.xml](https://hedidntjump.com/atom.xml) — Atom of the same items\n",
        "help.txt",
    )


def patch_shelves(text: str) -> str:
    return ensure_insert(
        text,
        "https://hedidntjump.com/sitemap.xml — XML sitemap\n",
        "https://hedidntjump.com/rss.xml — RSS 2.0 of the published papers and Volumes I–V\n"
        "https://hedidntjump.com/atom.xml — Atom of the same items\n",
        "shelves.txt",
    )


def patch_cite(text: str) -> str:
    # Four-space indent is the top-level query_urls list. A six-space copy
    # of the same URL sits in a nested list, so the anchor includes the
    # previous four-space line and is not a substring of that copy.
    return ensure_insert(
        text,
        '    "https://hedidntjump.com/llms.txt",\n'
        '    "https://hedidntjump.com/llms-full.txt",\n',
        '    "https://hedidntjump.com/rss.xml",\n'
        '    "https://hedidntjump.com/atom.xml",\n',
        "cite.json",
    )


def patch_openapi(text: str) -> str:
    anchor = '''    "/.well-known/tip.json": {
      "get": {
        "summary": "Same HDJ tip door as /tip.json",
        "responses": {
          "200": {
            "description": "application/json"
          }
        }
      }
    }
'''
    if '"/rss.xml"' in text and '"/atom.xml"' in text:
        return text if text.endswith("\n") else text + "\n"
    if text.count(anchor) != 1:
        raise SystemExit(f"openapi.json: anchor count {text.count(anchor)}")
    # The tip door is the last path, so its object has no trailing comma.
    return text.replace(anchor, anchor.rstrip() + ",\n" + OPENAPI_PATHS, 1)


def write_trees() -> None:
    docs_items = build_items(ROOT / "docs")
    dist_items = build_items(ROOT / "dist")
    if docs_items != dist_items:
        raise SystemExit("docs and dist feed items differ")
    description = channel_description(ROOT / "docs")
    if description != channel_description(ROOT / "dist"):
        raise SystemExit("docs and dist channel descriptions differ")
    rss = render_rss(docs_items, description)
    atom = render_atom(docs_items, description)
    patches = {
        "_headers": patch_headers,
        "robots.txt": patch_robots,
        "_redirects": patch_redirects,
        "sitemap.xml": patch_sitemap,
        "llms.txt": patch_llms,
        "ai.txt": patch_ai,
        "help.txt": patch_help,
        "shelves.txt": patch_shelves,
        "cite.json": patch_cite,
        "openapi.json": patch_openapi,
    }
    for tree in TREES:
        (tree / "rss.xml").write_text(rss, encoding="utf-8")
        (tree / "atom.xml").write_text(atom, encoding="utf-8")
        for html_path in sorted(tree.glob("*.html")):
            html_path.write_text(patch_html(html_path.read_text(encoding="utf-8")), encoding="utf-8")
        for name, patch in patches.items():
            path = tree / name
            path.write_text(patch(path.read_text(encoding="utf-8")), encoding="utf-8")
        print("rss", tree.name, "items", len(docs_items))


def main() -> None:
    write_trees()
    print("rss refresh OK", FEED_DAY)


if __name__ == "__main__":
    main()
