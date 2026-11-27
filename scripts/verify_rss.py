#!/usr/bin/env python3
"""Assert the RSS 2.0 and Atom feeds match the published pages."""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from write_rss import (  # noqa: E402
    APEX,
    FEED_DAY,
    HEAD_LINKS,
    build_items,
    channel_description,
    patch_ai,
    patch_cite,
    patch_headers,
    patch_help,
    patch_html,
    patch_llms,
    patch_openapi,
    patch_redirects,
    patch_robots,
    patch_shelves,
    patch_sitemap,
    render_atom,
    render_rss,
)

ROOT = Path(__file__).resolve().parents[1]
ATOM_NS = "{http://www.w3.org/2005/Atom}"
PATCHES = {
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


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def main() -> None:
    items = build_items(ROOT / "docs")
    assert items == build_items(ROOT / "dist")
    description = channel_description(ROOT / "docs")
    rss = render_rss(items, description)
    atom = render_atom(items, description)
    assert "www.hedidntjump.com" not in rss
    assert "www.hedidntjump.com" not in atom
    assert rss.count("<item>") == len(items)
    assert atom.count("<entry>") == len(items)

    docs_rss = (ROOT / "docs" / "rss.xml").read_text(encoding="utf-8")
    dist_rss = (ROOT / "dist" / "rss.xml").read_text(encoding="utf-8")
    docs_atom = (ROOT / "docs" / "atom.xml").read_text(encoding="utf-8")
    dist_atom = (ROOT / "dist" / "atom.xml").read_text(encoding="utf-8")
    assert docs_rss == dist_rss == rss
    assert docs_atom == dist_atom == atom

    root = ET.fromstring(rss)
    assert root.tag == "rss" and root.attrib.get("version") == "2.0"
    channel = root.find("channel")
    assert channel is not None
    assert channel.findtext("title") == "He Didn't Jump"
    assert channel.findtext("link") == f"{APEX}/"
    self_link = channel.find(f"{ATOM_NS}link")
    assert self_link is not None
    assert self_link.attrib["href"] == f"{APEX}/rss.xml"
    assert self_link.attrib["rel"] == "self"
    parsed = channel.findall("item")
    assert len(parsed) == len(items)
    for node, item in zip(parsed, items):
        assert node.findtext("title") == item.title
        assert node.findtext("link") == item.link
        assert node.findtext("guid") == item.link
        assert node.find("guid").attrib.get("isPermaLink") == "true"
        assert node.findtext("description") == item.description
        assert item.link.startswith(f"{APEX}/")
        enc = node.find("enclosure")
        if item.enclosure is None:
            assert enc is None
        else:
            assert enc is not None
            assert enc.attrib["url"] == item.enclosure.href
            assert enc.attrib["length"] == str(item.enclosure.length)
            assert enc.attrib["type"] == item.enclosure.mime
            assert item.enclosure.length == (
                ROOT / "docs" / item.enclosure.href.removeprefix(APEX).lstrip("/")
            ).stat().st_size

    feed = ET.fromstring(atom)
    assert local(feed.tag) == "feed"
    assert feed.findtext(f"{ATOM_NS}title") == "He Didn't Jump"
    assert feed.findtext(f"{ATOM_NS}subtitle") == description
    entries = feed.findall(f"{ATOM_NS}entry")
    assert len(entries) == len(items)
    for node, item in zip(entries, items):
        assert node.findtext(f"{ATOM_NS}title") == item.title
        assert node.findtext(f"{ATOM_NS}id") == item.link
        assert node.findtext(f"{ATOM_NS}summary") == item.description
        links = node.findall(f"{ATOM_NS}link")
        alternate = [link for link in links if link.attrib.get("rel") == "alternate"]
        enclosed = [link for link in links if link.attrib.get("rel") == "enclosure"]
        assert len(alternate) == 1 and alternate[0].attrib["href"] == item.link
        if item.enclosure is None:
            assert enclosed == []
        else:
            assert len(enclosed) == 1
            assert enclosed[0].attrib["href"] == item.enclosure.href
            assert enclosed[0].attrib["length"] == str(item.enclosure.length)

    assert any(item.day == FEED_DAY for item in items)
    assert any(item.path.startswith("/reader?volume=") for item in items)

    for tree_name in ("docs", "dist"):
        tree = ROOT / tree_name
        html_files = list(tree.glob("*.html"))
        assert html_files, tree_name
        for path in html_files:
            text = path.read_text(encoding="utf-8")
            assert HEAD_LINKS in text, path.name
            assert patch_html(text) == text, path.name
        for name, patch in PATCHES.items():
            text = (tree / name).read_text(encoding="utf-8")
            assert patch(text) == text, f"{tree_name}/{name}"
        assert f"<loc>{APEX}/rss.xml</loc>" in (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert f"<loc>{APEX}/atom.xml</loc>" in (tree / "sitemap.xml").read_text(encoding="utf-8")
        assert "<lastmod>2026-11-20</lastmod>" in (tree / "sitemap.xml").read_text(encoding="utf-8")
        robots = (tree / "robots.txt").read_text(encoding="utf-8")
        assert "Allow: /rss.xml\n" in robots
        assert "Allow: /atom.xml\n" in robots
        redirects = (tree / "_redirects").read_text(encoding="utf-8")
        assert "/rss /rss.xml 301" in redirects
        assert "/feed /rss.xml 301" in redirects
        assert "/feed.xml /rss.xml 301" in redirects
        assert "/atom /atom.xml 301" in redirects
        headers = (tree / "_headers").read_text(encoding="utf-8")
        assert "Content-Type: application/rss+xml; charset=utf-8" in headers
        assert "Content-Type: application/atom+xml; charset=utf-8" in headers
        assert 'rel="alternate"; type="application/rss+xml"' in headers

    assert (ROOT / "docs" / "rss.xml").read_bytes() == (ROOT / "dist" / "rss.xml").read_bytes()
    assert (ROOT / "docs" / "atom.xml").read_bytes() == (ROOT / "dist" / "atom.xml").read_bytes()
    print(f"rss OK items={len(items)}")


if __name__ == "__main__":
    main()
