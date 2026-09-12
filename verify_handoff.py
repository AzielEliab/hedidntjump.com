from pathlib import Path
import hashlib, json, re
root = Path(__file__).resolve().parent
manifest = json.loads((root / "FILE_MANIFEST.json").read_text())
for item in manifest["files"]:
    path = root / item["path"]
    assert path.is_file(), f"Missing: {path}"
    data = path.read_bytes()
    assert len(data) == item["bytes"], f"Size mismatch: {path}"
    assert hashlib.sha256(data).hexdigest() == item["sha256"], f"Hash mismatch: {path}"
html = (root / "dist/index.html").read_text()
assert html.count("<details>") == 0
assert html.count('class="inquiry"') == 21
assert (root / "dist/official-narrative.html").is_file()
assert (root / "dist/azieleliab.html").is_file()
assert (root / "dist/assets/sigil.png").is_file()
assert (root / "dist/assets/plates/office-room.webp").is_file()
assert html.count('class="volume-button"') == 5
aziel_alias = (root / "dist/aziel.html").read_text()
assert 'url=/rubye.html' in aziel_alias
assert 'azieleliab.html' not in aziel_alias
page = (root / "dist/azieleliab.html").read_text()
assert "Seattle, Washington · 9/12/2026" in page
assert "Researcher. Builder. Just a man." in page
assert "I am temporary. The truth is not." in page
assert "— Aziel Eliab" in page
assert 'src="/assets/sigil.png"' in page
assert 'alt=""' in page
assert "EverBlooming" not in page
assert ">sigil<" not in page.lower()
for name in ("index.html", "official-narrative.html", "rubye.html", "foia.html", "azieleliab.html", "reader.html"):
    text = (root / "dist" / name).read_text()
    nav = text.split("<nav", 1)[1].split("</nav>", 1)[0]
    if name == "reader.html":
        assert nav.index('href="/azieleliab.html">AzielEliab</a>') > nav.index('href="/rubye.html">Rubye paper</a>')
    else:
        last_a = list(re.finditer(r"<a\s[^>]*>.*?</a>", nav, re.S))[-1].group(0)
        assert 'href="/azieleliab.html">AzielEliab</a>' in last_a, name
    strip = text.split('class="project-strip-inner"', 1)[1].split("</div>", 1)[0]
    last_tab = [line.strip() for line in strip.splitlines() if "class=\"project-tab" in line][-1]
    assert last_tab.endswith('href="/azieleliab.html">AzielEliab</a>'), name
cite = json.loads((root / "dist/cite.json").read_text())
assert cite["author"]["name"] == "Aziel Eliab"
assert "Truthseeker" in cite["author"]["jobTitle"]
assert any(e["id"] == "azieleliab" for e in cite["editions"])
assert cite["recommendedCitation"].startswith("Eliab, Aziel.")
stats = json.loads((root / "dist/stats.json").read_text())
assert stats["site"] == "https://hedidntjump.com/"
assert stats["as_of"] == "live"
assert stats["views"] is None and stats["downloads"] is None
assert "hedidntjump-stats.vibelock.workers.dev/api/stats" in stats["counters_url"]
assert "Read the five volumes" in stats["encouragement"]
meta = json.loads((root / "dist/meta.json").read_text())
assert meta["who"]["name"] == "Aziel Eliab"
assert meta["llms_txt"].endswith("/llms.txt")
assert meta["sitemap"].endswith("/sitemap.xml")
assert (root / "dist/site.json").read_text() == (root / "dist/meta.json").read_text()
for name in ("index.html", "official-narrative.html", "rubye.html", "foia.html", "azieleliab.html", "reader.html"):
    head = (root / "dist" / name).read_text().split("</head>", 1)[0]
    assert 'type="application/json" href="https://hedidntjump.com/cite.json"' in head
    assert 'type="application/json" href="https://hedidntjump.com/stats.json"' in head
    assert 'type="application/json" href="https://hedidntjump.com/meta.json"' in head
for volume, pages in enumerate([20, 20, 21, 15, 14], 1):
    assert (root / f"dist/volumes/volume-{volume}.pdf").is_file()
    for page_n in range(1, pages + 1):
        assert (root / f"dist/assets/v{volume}/{page_n}.webp").is_file()
print(f"Verified {len(manifest['files'])} files, 21 inquiries, official narrative, AzielEliab last tag, and 90 reader pages.")
