#!/bin/sh
# Build /volumes/hedidntjump-all-volumes.zip from the five PDFs.
# The landing page uses this zip when present; otherwise it downloads each PDF.
set -eu
root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
outdir="$root/dist/volumes"
zipfile="$outdir/hedidntjump-all-volumes.zip"
cd "$outdir"
rm -f "$zipfile"
zip -q -j "$zipfile" volume-1.pdf volume-2.pdf volume-3.pdf volume-4.pdf volume-5.pdf
if [ -d "$root/docs/volumes" ]; then
  cp -f "$zipfile" "$root/docs/volumes/hedidntjump-all-volumes.zip"
fi
echo "Wrote $zipfile ($(wc -c < "$zipfile") bytes)"
