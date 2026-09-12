from pathlib import Path
import hashlib, json
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
assert html.count('class="inquiry"') == 23
assert (root / "dist/official-narrative.html").is_file()
assert (root / "dist/assets/plates/office-room.webp").is_file()
assert (root / "dist/assets/plates/marion-death-certificate.webp").is_file()
assert (root / "dist/assets/plates/frances-death-certificate.webp").is_file()
assert (root / "dist/assets/plates/bogeyman-disguise.webp").is_file()
assert (root / "dist/assets/plates/whos-crazy-topic.webp").is_file()
assert (root / "dist/assets/plates/playboy-subdued.webp").is_file()
assert (root / "dist/assets/plates/last-picture-bride.webp").is_file()
assert (root / "dist/assets/plates/hoover-arrested.webp").is_file()
assert (root / "dist/assets/plates/foia-request.webp").is_file()
assert (root / "dist/assets/plates/foia-fee-waiver.webp").is_file()
assert (root / "dist/assets/plates/foia-subject-deceased.webp").is_file()
assert (root / "dist/assets/plates/foia-fbi-response-p1.webp").is_file()
assert (root / "dist/assets/plates/foia-fbi-response-p2.webp").is_file()
assert (root / "dist/assets/plates/escort-dc-bishop.webp").is_file()
assert (root / "dist/copyrights.html").is_file()
assert "marion-death-certificate.webp" in html
assert "frances-death-certificate.webp" in html
assert "bogeyman-disguise.webp" in html
assert "whos-crazy-topic.webp" in html
assert "Involutional Melancholia" in html
assert "libraries.wsu.edu" not in html
assert "escort-dc-bishop.webp" in html
assert "foia-fbi-response-p1.webp" in html
assert "copyrights.html" in html
assert "rights-bar" in html
assert "An Independent Investigation" not in html
assert 'class="byline-line"' not in html
assert 'class="flag-city"' in html
assert "Seattle, Washington" in html
assert "Friday, August 7, 1936" in html
assert "The Record, Not the Verdict" in html
copyrights = (root / "dist/copyrights.html").read_text()
assert "17 U.S.C. § 107" in copyrights
assert "not legal advice" in copyrights.lower()
assert "not a shrine" in copyrights
assert "Apache-2.0" in copyrights
assert "public vital records as preserved for historical research" in copyrights
assert "Wikimedia Commons" in copyrights
assert "credited archives" in copyrights
assert "Aziel’s Research Volumes" in html
assert 'href="/aziel.html">About Aziel</a>' in html
assert 'id="publisher"' not in html
assert html.count('class="volume-nav-row"') == 0
assert "called his cousin there for protection" in html
aziel = (root / "dist/aziel.html").read_text()
assert "url=/rubye.html" not in aziel
assert "http-equiv" not in aziel.lower()
assert "Researcher. Builder. Just a man." in aziel
assert "I am temporary. The truth is not." in aziel
assert "— Aziel Eliab" in aziel
assert "everblooming-sigil.webp" in aziel
assert "index,follow" in aziel
assert "https://hedidntjump.com/aziel.html" in aziel
assert (root / "dist/assets/everblooming-sigil.webp").is_file()
foia = (root / "dist/foia.html").read_text()
assert "foia-request.webp" in foia
assert foia.count("foia-fee-waiver.webp") == 1
assert "foia-subject-deceased.webp" in foia
assert "no agency denial letter explaining a present-day refusal" not in html
assert "no agency denial letter explaining a present-day refusal" not in foia
site_html = html + foia + (root / "dist/copyrights.html").read_text()
for banned in ("Horton", "Diplomat Court", "Beech Grove", "foipa@", "fbi.foia@", "ogis@nara"):
    assert banned not in site_html, f"PII leaked: {banned}"
assert html.count('class="volume-button"') == 5
for volume, pages in enumerate([20, 20, 21, 15, 14], 1):
    assert (root / f"dist/volumes/volume-{volume}.pdf").is_file()
    for page in range(1, pages + 1):
        assert (root / f"dist/assets/v{volume}/{page}.webp").is_file()
print(f"Verified {len(manifest['files'])} files, 23 inquiries, official narrative, and 90 reader pages.")
