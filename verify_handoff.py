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
assert html.count('class="inquiry"') == 17
assert html.count('class="volume-button"') == 5
for volume, pages in enumerate([20, 20, 21, 15, 14], 1):
    assert (root / f"dist/volumes/volume-{volume}.pdf").is_file()
    for page in range(1, pages + 1):
        assert (root / f"dist/assets/v{volume}/{page}.webp").is_file()
print(f"Verified {len(manifest['files'])} files, 17 inquiries and 90 reader pages.")
