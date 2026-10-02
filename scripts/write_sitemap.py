#!/usr/bin/env python3
"""Refresh hedidntjump.com sitemap.xml and sitemap-index.xml.

Machine files only (docs/ and dist/). Does not open HTML/CSS/JS for writing.

Discovery is the docs/ tree plus docs/_redirects, plus the per-volume reader
URLs already published in volumes.html (JSON-LD and the View links).
/Volumes/1–5 and /Volumes/I are not files and are not redirects. Live 200
for those paths is the homepage shell (canonical /). They are not listed.

Lastmod is the operator discovery date (America/Indianapolis), not file mtime.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "docs", ROOT / "dist"]
APEX = "https://hedidntjump.com"
LASTMOD = "2026-10-01"
# Sister sitemaps in the index were not republished on this date.
SISTER_LASTMOD = "2026-09-13"

SKIP_NAMES = {"CNAME", "_headers", "_redirects", "sitemap.xml"}
SKIP_SUFFIXES = {
    ".js",
    ".css",
    ".woff2",
    ".webp",
    ".jpg",
    ".jpeg",
    ".png",
    ".svg",
    ".mp4",
    ".gif",
}
# Homepage shell. Confirmed live: title and canonical match /, not a volume hub.
DENY_PATHS = {
    "/Volumes/1",
    "/Volumes/2",
    "/Volumes/3",
    "/Volumes/4",
    "/Volumes/5",
    "/Volumes/I",
    "/Volumes/II",
    "/Volumes/III",
    "/Volumes/IV",
    "/Volumes/V",
    "/volumes/1",
    "/volumes/2",
    "/volumes/3",
    "/volumes/4",
    "/volumes/5",
    "/volumes/I",
    "/volumes/1.html",
    "/Volumes/1.html",
    "/reader/1",
}

# Priority and changefreq already shipped. Kept so a regen does not drop them.
BASELINE: list[tuple[str, str, str]] = [
    ("/", "1.0", "weekly"),
    ("/Case", "0.9", "weekly"),
    ("/Press", "0.8", "weekly"),
    ("/Inquiries", "0.9", "weekly"),
    ("/Rubye", "0.7", "weekly"),
    ("/Archives", "0.7", "weekly"),
    ("/FOIA", "0.8", "weekly"),
    ("/Volumes", "0.9", "weekly"),
    ("/reader", "0.7", "weekly"),
    ("/Narrative", "0.9", "weekly"),
    ("/aziel", "0.5", "weekly"),
    ("/AzielEliab", "0.4", "weekly"),
    ("/AboutAziel", "0.4", "weekly"),
    ("/Copyrights", "0.3", "weekly"),
    ("/receipts", "0.4", "weekly"),
    ("/who", "0.6", "weekly"),
    ("/llms.txt", "0.5", "weekly"),
    ("/llms-full.txt", "0.3", "weekly"),
    ("/ai.txt", "0.3", "weekly"),
    ("/cite.json", "0.5", "weekly"),
    ("/shelves", "0.5", "weekly"),
    ("/shelves.json", "0.4", "weekly"),
    ("/lockset.json", "0.4", "weekly"),
    ("/v1/shelves", "0.3", "weekly"),
    ("/cold-copy", "0.3", "weekly"),
    ("/ingest-as-receipt.json", "0.5", "weekly"),
    ("/openapi.json", "0.2", "weekly"),
    ("/mcp.json", "0.2", "weekly"),
    ("/.well-known/mcp.json", "0.2", "weekly"),
    ("/volumes.json", "0.3", "weekly"),
    ("/robots.txt", "0.2", "weekly"),
    ("/sitemap-index.xml", "0.2", "weekly"),
    ("/person.jsonld", "0.3", "weekly"),
    ("/identity.jsonld", "0.3", "weekly"),
    ("/graph.jsonld", "0.3", "weekly"),
    ("/who-is-aziel-eliab.txt", "0.4", "weekly"),
    ("/who-is", "0.4", "weekly"),
    ("/.well-known/aziel.json", "0.3", "weekly"),
    ("/.well-known/llms.txt", "0.4", "weekly"),
    ("/redline", "0.4", "weekly"),
    ("/redline.json", "0.4", "weekly"),
    ("/runtime-launch.json", "0.4", "weekly"),
    ("/volumes/volume-1.pdf", "0.6", "weekly"),
    ("/volumes/volume-2.pdf", "0.6", "weekly"),
    ("/volumes/volume-3.pdf", "0.6", "weekly"),
    ("/volumes/volume-4.pdf", "0.6", "weekly"),
    ("/volumes/volume-5.pdf", "0.6", "weekly"),
    ("/assets/foia-binary-acknowledgement.pdf", "0.4", "weekly"),
    ("/survival", "0.4", "hourly"),
    ("/survival.json", "0.4", "hourly"),
    ("/v1/survival", "0.4", "hourly"),
    ("/help.txt", "0.5", "weekly"),
    ("/addendum.txt", "0.4", "weekly"),
    ("/help/how-to-read.txt", "0.5", "weekly"),
    ("/mesh", "0.4", "hourly"),
    ("/mesh.json", "0.4", "hourly"),
    ("/v1/mesh", "0.4", "hourly"),
    ("/Aziel", "0.3", "weekly"),
    ("/inquires", "0.3", "weekly"),
    ("/Rubeye", "0.3", "weekly"),
    ("/Archive", "0.3", "weekly"),
]

HOURLY = {
    "/survival",
    "/survival.json",
    "/v1/survival",
    "/doors",
    "/failover",
    "/mesh",
    "/mesh.json",
    "/v1/mesh",
    "/live-nodes",
}

ENTRY_RE = re.compile(
    r"<loc>(?P<loc>[^<]+)</loc>\s*"
    r"<lastmod>[^<]*</lastmod>\s*"
    r"<changefreq>(?P<cf>[^<]+)</changefreq>\s*"
    r"<priority>(?P<pri>[^<]+)</priority>",
    re.MULTILINE,
)
READER_RE = re.compile(r"/reader\?volume=(\d+)&(?:amp;)?page=1")


def unescape_loc(loc: str) -> str:
    return loc.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


def escape_loc(path: str) -> str:
    return path.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def path_of(loc: str) -> str:
    loc = unescape_loc(loc.strip())
    if loc.startswith(APEX):
        loc = loc[len(APEX) :]
    return loc or "/"


def defaults_for(path: str) -> tuple[str, str]:
    for loc, pri, cf in BASELINE:
        if loc == path:
            return pri, cf
    if path.startswith("/reader?volume="):
        return "0.6", "weekly"
    if path in HOURLY:
        return "0.4", "hourly"
    return "0.4", "weekly"


def redirect_paths(tree: Path) -> list[str]:
    path = tree / "_redirects"
    if not path.is_file():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3 or parts[0].startswith("http"):
            continue
        if parts[2] != "200":
            continue
        if parts[0].startswith("/"):
            out.append(parts[0])
    return out


def html_pretty_paths(tree: Path, redirect_targets: dict[str, list[str]]) -> list[str]:
    """Pretty locs for real HTML files. Never the raw .html path (those 308)."""
    out = []
    for html in sorted(tree.glob("*.html")):
        sources = redirect_targets.get(html.name, [])
        if sources:
            out.extend(sources)
            continue
        if html.name == "index.html":
            out.append("/")
        else:
            out.append("/" + html.stem)
    return out


def redirect_target_index(tree: Path) -> dict[str, list[str]]:
    """html filename -> pretty redirect sources that rewrite to it."""
    index: dict[str, list[str]] = {}
    path = tree / "_redirects"
    if not path.is_file():
        return index
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3 or parts[0].startswith("http") or parts[2] != "200":
            continue
        target = parts[1].lstrip("/")
        if target.endswith(".html"):
            index.setdefault(target, []).append(parts[0])
    return index


def file_paths(tree: Path) -> list[str]:
    out = []
    for path in tree.rglob("*"):
        if not path.is_file():
            continue
        rel = "/" + path.relative_to(tree).as_posix()
        if rel.startswith("/api/") or rel.startswith("/functions/") or "/functions/" in rel:
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        if rel.startswith("/assets/") and path.suffix.lower() != ".pdf":
            continue
        if path.suffix.lower() == ".html":
            continue
        out.append(rel)
    return out


def reader_volume_paths(tree: Path) -> list[str]:
    """Per-volume reader URLs published on the Volumes page. Not /Volumes/N."""
    page = tree / "volumes.html"
    if not page.is_file():
        return []
    text = page.read_text(encoding="utf-8")
    nums = sorted({int(n) for n in READER_RE.findall(text)})
    return [f"/reader?volume={n}&page=1" for n in nums]


def discover(tree: Path) -> list[str]:
    targets = redirect_target_index(tree)
    paths: list[str] = []
    paths.extend(loc for loc, _pri, _cf in BASELINE)
    paths.extend(redirect_paths(tree))
    paths.extend(html_pretty_paths(tree, targets))
    paths.extend(file_paths(tree))
    paths.extend(reader_volume_paths(tree))
    seen = set()
    out = []
    for path in paths:
        if not path.startswith("/"):
            continue
        if path in DENY_PATHS or path in seen:
            continue
        seen.add(path)
        out.append(path)
    return out


def parse_entries(text: str) -> list[tuple[str, str, str]]:
    entries = []
    for match in ENTRY_RE.finditer(text):
        path = path_of(match.group("loc"))
        if path in DENY_PATHS:
            continue
        entries.append((path, match.group("pri"), match.group("cf")))
    return entries


def merge_sitemap(text: str, tree: Path | None = None) -> str:
    """Keep shipped order and priorities. Append real missing URLs. Stamp lastmod."""
    tree = tree or (ROOT / "docs")
    existing = parse_entries(text)
    have = {path for path, _pri, _cf in existing}
    extras: list[tuple[str, str, str]] = []
    for path in discover(tree):
        if path in have:
            continue
        pri, cf = defaults_for(path)
        extras.append((path, pri, cf))
        have.add(path)

    def volume_key(item: tuple[str, str, str]) -> tuple[int, str]:
        path = item[0]
        match = re.search(r"volume=(\d+)", path)
        if match and path.startswith("/reader?"):
            return (0, f"{int(match.group(1)):02d}")
        return (1, path)

    extras.sort(key=volume_key)
    return render(existing + extras)


def render(entries: list[tuple[str, str, str]]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, pri, cf in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{APEX}{escape_loc(path)}</loc>")
        lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
        lines.append(f"    <changefreq>{cf}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_index() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{APEX}/sitemap.xml</loc>
    <lastmod>{LASTMOD}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.azieleliab.com/sitemap.xml</loc>
    <lastmod>{SISTER_LASTMOD}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.azielcorpuslibrary.net/sitemap.xml</loc>
    <lastmod>{SISTER_LASTMOD}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://godlock.uk/sitemap.xml</loc>
    <lastmod>{SISTER_LASTMOD}</lastmod>
  </sitemap>
</sitemapindex>
"""


def write_trees() -> None:
    docs = ROOT / "docs"
    base_path = docs / "sitemap.xml"
    before = base_path.read_text(encoding="utf-8").count("<loc>") if base_path.is_file() else 0
    text = merge_sitemap(base_path.read_text(encoding="utf-8") if base_path.is_file() else "", docs)
    index = render_index()
    for tree in TREES:
        (tree / "sitemap.xml").write_text(text, encoding="utf-8")
        (tree / "sitemap-index.xml").write_text(index, encoding="utf-8")
        print("sitemap", tree.name, "urls", text.count("<loc>"), "was", before)
    check(text, index)


def check(text: str, index: str) -> None:
    locs = [path_of(m.group("loc")) for m in ENTRY_RE.finditer(text)]
    assert locs, "sitemap empty"
    assert len(locs) == len(set(locs))
    assert text.count("<priority>1.0</priority>") == 1
    assert text.count("<lastmod>") == len(locs)
    assert set(re.findall(r"<lastmod>([^<]+)</lastmod>", text)) == {LASTMOD}
    for path, _pri, _cf in BASELINE:
        assert path in locs, path
    for n in range(1, 6):
        assert f"/reader?volume={n}&page=1" in locs
        assert f"/volumes/volume-{n}.pdf" in locs
        assert f"/Volumes/{n}" not in locs
    for path in ("/doors", "/failover", "/live-nodes", "/Volumes", "/reader"):
        assert path in locs, path
    assert "/Volumes/I" not in text
    assert f"<lastmod>{LASTMOD}</lastmod>" in index
    assert f"<loc>{APEX}/sitemap.xml</loc>" in index
    docs = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
    dist = (ROOT / "dist" / "sitemap.xml").read_text(encoding="utf-8")
    assert docs == dist
    assert (ROOT / "docs" / "sitemap-index.xml").read_text(encoding="utf-8") == (
        ROOT / "dist" / "sitemap-index.xml"
    ).read_text(encoding="utf-8")


def main() -> None:
    write_trees()
    print("sitemap refresh OK", LASTMOD)


if __name__ == "__main__":
    main()
