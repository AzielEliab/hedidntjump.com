#!/usr/bin/env python3
"""Canonical archive URLs that return HTTP 200 on https://hedidntjump.com.

Confirmed live 2026-10-06: /case is 200 and /Case is 308 to /case. Cloudflare
Pages serves case.html at /case, then strips a _redirects 200 target of
case.html into that same 308. Capitalised and alias paths are explicit
one-way 301s to the 200 URL. Pages path matching is case-sensitive, so
/Case → /case does not match /case and does not loop.

Head canonical, og:url, and JSON-LD url/@id are not visible surface.
Body HTML, nav hrefs, and visible text stay untouched.
"""
from __future__ import annotations

from pathlib import Path

APEX = "https://hedidntjump.com"
ROOT = Path(__file__).resolve().parents[1]
TREES = [ROOT / "dist", ROOT / "docs"]

# HTML file → path that returns 200. inquires.html is an alias body.
CANONICAL_BY_FILE = {
    "index.html": f"{APEX}/",
    "case.html": f"{APEX}/case",
    "press.html": f"{APEX}/press",
    "inquiries.html": f"{APEX}/inquiries",
    "inquires.html": f"{APEX}/inquiries",
    "rubye.html": f"{APEX}/rubye",
    "archives.html": f"{APEX}/archives",
    "foia.html": f"{APEX}/foia",
    "volumes.html": f"{APEX}/volumes",
    "reader.html": f"{APEX}/reader",
    "official-narrative.html": f"{APEX}/official-narrative",
    "aziel.html": f"{APEX}/aziel",
    "copyrights.html": f"{APEX}/copyrights",
    "receipts.html": f"{APEX}/receipts",
    "who.html": f"{APEX}/who",
}

# Longer paths first. Applied only as a full path segment after the host.
PATH_REWRITES: list[tuple[str, str]] = [
    ("/AzielEliab", "/aziel"),
    ("/AboutAziel", "/aziel"),
    ("/official-narrative.html", "/official-narrative"),
    ("/inquiries.html", "/inquiries"),
    ("/inquires.html", "/inquiries"),
    ("/copyrights.html", "/copyrights"),
    ("/archives.html", "/archives"),
    ("/volumes.html", "/volumes"),
    ("/rubye.html", "/rubye"),
    ("/press.html", "/press"),
    ("/foia.html", "/foia"),
    ("/case.html", "/case"),
    ("/reader.html", "/reader"),
    ("/Copyrights", "/copyrights"),
    ("/Inquiries", "/inquiries"),
    ("/Narrative", "/official-narrative"),
    ("/Archives", "/archives"),
    ("/Volumes", "/volumes"),
    ("/Rubeye", "/rubye"),
    ("/Archive", "/archives"),
    ("/inquires", "/inquiries"),
    ("/Aziel", "/aziel"),
    ("/Press", "/press"),
    ("/Rubye", "/rubye"),
    ("/FOIA", "/foia"),
    ("/Case", "/case"),
]

# Sitemap keeps one loc per page. Aliases are removed, not renamed into dupes.
SITEMAP_RENAME = {
    "/Case": "/case",
    "/Press": "/press",
    "/Inquiries": "/inquiries",
    "/Rubye": "/rubye",
    "/Archives": "/archives",
    "/FOIA": "/foia",
    "/Volumes": "/volumes",
    "/Narrative": "/official-narrative",
    "/Copyrights": "/copyrights",
}

SITEMAP_DROP = {
    "/AzielEliab",
    "/AboutAziel",
    "/Aziel",
    "/inquires",
    "/Rubeye",
    "/Archive",
}

# Source path, 301 target. Target is the URL that returns 200.
ALIAS_REDIRECTS: list[tuple[str, str]] = [
    ("/Case", "/case"),
    ("/Press", "/press"),
    ("/Inquiries", "/inquiries"),
    ("/inquires", "/inquiries"),
    ("/Rubye", "/rubye"),
    ("/Rubeye", "/rubye"),
    ("/Archives", "/archives"),
    ("/Archive", "/archives"),
    ("/FOIA", "/foia"),
    ("/Volumes", "/volumes"),
    ("/Narrative", "/official-narrative"),
    ("/Copyrights", "/copyrights"),
    ("/Aziel", "/aziel"),
    ("/AboutAziel", "/aziel"),
    ("/AzielEliab", "/aziel"),
]

ROBOTS_ALLOW_RENAME = {
    "Allow: /Case": "Allow: /case",
    "Allow: /Narrative": "Allow: /official-narrative",
    "Allow: /Inquiries": "Allow: /inquiries",
    "Allow: /Volumes": "Allow: /volumes",
    "Allow: /FOIA": "Allow: /foia",
    "Allow: /Press": "Allow: /press",
    "Allow: /Rubye": "Allow: /rubye",
    "Allow: /Archives": "Allow: /archives",
    "Allow: /Copyrights": "Allow: /copyrights",
}

OPENAPI_PATH_RENAME = {
    "/Case": "/case",
    "/Narrative": "/official-narrative",
    "/Inquiries": "/inquiries",
    "/Volumes": "/volumes",
    "/FOIA": "/foia",
    "/Press": "/press",
    "/Rubye": "/rubye",
    "/Archives": "/archives",
    "/Copyrights": "/copyrights",
}

_HOSTS = (
    "https://www.hedidntjump.com",
    "http://www.hedidntjump.com",
    "https://hedidntjump.com",
    "http://hedidntjump.com",
)

MACHINE_NAMES = {
    "llms.txt",
    "llms-full.txt",
    "ai.txt",
    "cite.json",
    "robots.txt",
    "help.txt",
    "addendum.txt",
    "shelves.txt",
    "shelves.json",
    "who-is-aziel-eliab.txt",
    "graph.jsonld",
    "person.jsonld",
    "identity.jsonld",
    "openapi.json",
    "ai.txt",
}


def _segment_boundary(rest: str) -> bool:
    """True when the matched path is the whole segment, not a longer path."""
    if not rest:
        return True
    ch = rest[0]
    if ch in "\"' \t\r\n#?)>,]}<.;:":
        return True
    # Trailing slash before a fragment or query, not /Volumes/1.
    if ch == "/" and (len(rest) == 1 or rest[1] in "#?\""):
        return True
    return False


def rewrite_archive_urls(text: str) -> str:
    """Point hedidntjump.com page URLs at the path that returns 200.

    www hosts are rewritten to the apex only when the path itself changes.
    Already-correct paths on www are left for the later host pass.
    """
    for old, new in PATH_REWRITES:
        for host in _HOSTS:
            needle = host + old
            out: list[str] = []
            i = 0
            while True:
                j = text.find(needle, i)
                if j < 0:
                    out.append(text[i:])
                    break
                rest = text[j + len(needle) :]
                if _segment_boundary(rest):
                    out.append(text[i:j])
                    out.append(APEX + new)
                    i = j + len(needle)
                else:
                    out.append(text[i : j + 1])
                    i = j + 1
            text = "".join(out)
    return text


def rewrite_robots(text: str) -> str:
    for old, new in ROBOTS_ALLOW_RENAME.items():
        text = text.replace(old, new)
    return text


def rewrite_html(text: str) -> str:
    """Rewrite archive URLs inside <head> only. Body bytes stay put."""
    head, sep, body = text.partition("</head>")
    if not sep:
        return text
    return rewrite_archive_urls(head) + sep + body


def patch_redirect_text(text: str) -> str:
    """One-way 301 from capitalised and alias paths to the 200 URL.

    Do not 200-rewrite those paths to *.html. Pages html-stripping turns
    that target into a 308. Do not add /case → /Case: matching is
    case-sensitive and /case is already 200.
    """
    text = text.replace(
        "# Pretty tab paths (200 = rewrite, no redirect loop)\n",
        "# Pretty tab paths. Capitalised and alias paths 301 to the URL that returns 200.\n"
        "# Do not 200-rewrite these to *.html (Pages html-stripping turns that into a 308).\n"
        "# Do not add /case → /Case. Matching is case-sensitive and /case is already 200.\n",
    )
    text = text.replace(
        "Do not 301 /case↔/Case (Cloudflare pretty-URL 308 can loop).",
        "One-way 301 /Case → /case (case-sensitive; lowercase is already 200).",
    )
    text = text.replace(
        "# About Aziel — one body (aziel.html). Aliases 200 rewrite. Canonical /aziel.\n",
        "# About Aziel — one body (aziel.html). Canonical /aziel via html-extension 200.\n"
        "# Aliases 301 to /aziel. Do not 200-rewrite them to aziel.html.\n",
    )
    for src, dest in ALIAS_REDIRECTS:
        for status in ("200", "301", "308"):
            for target in (f"{dest}.html", dest, f"{dest.lstrip('/')}.html"):
                # dest is already a path like /case. html form is /case.html
                pass
        html_target = dest + ".html" if not dest.endswith(".html") else dest
        # Narrative's file is not /narrative.html. The old lines name the file.
        candidates = [
            f"{src} {html_target} 200",
            f"{src} {dest}.html 200",
            f"{src} {dest} 200",
            f"{src} {dest} 308",
        ]
        # Historical file targets that are not dest+".html".
        file_targets = {
            "/Narrative": "/official-narrative.html",
            "/inquires": "/inquiries.html",
            "/Rubeye": "/rubye.html",
            "/Archive": "/archives.html",
            "/Aziel": "/aziel.html",
            "/AboutAziel": "/aziel.html",
            "/AzielEliab": "/aziel.html",
        }
        if src in file_targets:
            candidates.append(f"{src} {file_targets[src]} 200")
        new_line = f"{src} {dest} 301"
        for old_line in candidates:
            text = text.replace(old_line, new_line)
    # Never publish the reverse rule. It is not in the file today; keep it out.
    text = text.replace("/case /Case 301\n", "")
    text = text.replace("/case.html /Case 301\n", "")
    return text


def rewrite_openapi(data: dict) -> dict:
    info = data.get("info") or {}
    desc = info.get("description") or ""
    old_q = "Query pages: /Case, /Narrative, /Inquiries, /Volumes, /FOIA."
    new_q = "Query pages: /case, /official-narrative, /inquiries, /volumes, /foia."
    if old_q in desc:
        info["description"] = desc.replace(old_q, new_q)
        data["info"] = info
    paths = data.get("paths")
    if isinstance(paths, dict):
        for old, new in OPENAPI_PATH_RENAME.items():
            if old not in paths:
                continue
            if new not in paths:
                paths[new] = paths.pop(old)
            else:
                paths.pop(old)
    return data


def apply_heads_and_redirects() -> None:
    for tree in TREES:
        for path in sorted(tree.glob("*.html")):
            text = path.read_text(encoding="utf-8")
            new = rewrite_html(text)
            if new != text:
                path.write_text(new, encoding="utf-8")
                print("head", path.relative_to(ROOT))
        redirects = tree / "_redirects"
        original = redirects.read_text(encoding="utf-8")
        patched = patch_redirect_text(original)
        if patched != original:
            redirects.write_text(patched, encoding="utf-8")
            print("redirects", redirects.relative_to(ROOT))


def apply_machine_urls() -> None:
    """URL substitution only. Does not rewrite prose or JSON shape."""
    import json

    skip = {"ingest-as-receipt.json", "sitemap.xml", "sitemap-index.xml"}
    for tree in TREES:
        for path in tree.rglob("*"):
            if not path.is_file():
                continue
            if path.name in skip or path.suffix.lower() in {
                ".html",
                ".pdf",
                ".webp",
                ".css",
                ".js",
                ".woff2",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".svg",
                ".mp4",
                ".zip",
            }:
                continue
            if path.name.startswith("_"):
                continue
            if "assets" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            new = rewrite_archive_urls(text)
            if path.name == "robots.txt":
                new = rewrite_robots(new)
            if path.name == "openapi.json":
                data = json.loads(text)
                rewritten = rewrite_openapi(json.loads(new))
                if rewritten != data:
                    new = json.dumps(rewritten, indent=2, ensure_ascii=False) + "\n"
                else:
                    new = rewrite_archive_urls(text)
            if new != text:
                path.write_text(new, encoding="utf-8")
                print("machine", path.relative_to(ROOT))
