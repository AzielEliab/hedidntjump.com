#!/bin/sh
# Build /volumes/hedidntjump-all-volumes.zip from the five PDFs.
# The volume pages' "Download all volumes" button uses this zip when present
# (HEAD check in stats.js); otherwise it downloads each PDF.
# Reproducible: fixed member mtimes, no extra attributes, fixed member order,
# so rebuilding from the same PDFs yields byte-identical output.
set -eu
root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
src="$root/docs/volumes"
name="hedidntjump-all-volumes.zip"
limit=$((25 * 1024 * 1024))   # Cloudflare Pages per-file limit (25 MiB)
for i in 1 2 3 4 5; do
  cmp -s "$src/volume-$i.pdf" "$root/dist/volumes/volume-$i.pdf" || {
    echo "docs/ and dist/ volume-$i.pdf differ; sync them first" >&2; exit 1; }
done
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
for i in 1 2 3 4 5; do
  cp "$src/volume-$i.pdf" "$tmp/volume-$i.pdf"
  TZ=UTC touch -t 202610180000 "$tmp/volume-$i.pdf"
done
(cd "$tmp" && TZ=UTC zip -q -X -9 -D "$name" volume-1.pdf volume-2.pdf volume-3.pdf volume-4.pdf volume-5.pdf)
size=$(wc -c < "$tmp/$name")
if [ "$size" -ge "$limit" ]; then
  echo "zip is $size bytes, over the 25 MiB Pages limit; not written" >&2; exit 1
fi
cp -f "$tmp/$name" "$root/docs/volumes/$name"
cp -f "$tmp/$name" "$root/dist/volumes/$name"
echo "Wrote docs/volumes/$name and dist/volumes/$name ($size bytes)"
