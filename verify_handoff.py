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
assert "marion-death-certificate.webp" in html
assert "frances-death-certificate.webp" in html
assert "bogeyman-disguise.webp" in html
assert "whos-crazy-topic.webp" in html
assert "Involutional Melancholia" in html
assert "libraries.wsu.edu" not in html
assert html.count('class="volume-button"') == 5
for volume, pages in enumerate([20, 20, 21, 15, 14], 1):
    assert (root / f"dist/volumes/volume-{volume}.pdf").is_file()
    for page in range(1, pages + 1):
        assert (root / f"dist/assets/v{volume}/{page}.webp").is_file()
print(f"Verified {len(manifest['files'])} files, 23 inquiries, official narrative, and 90 reader pages.")
