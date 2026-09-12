#!/bin/sh
set -eu
root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
# Keep docs/CNAME. Copy the static site over the Pages root.
cname=""
if [ -f "$root/docs/CNAME" ]; then
  cname="$(cat "$root/docs/CNAME")"
fi
# Refresh tracked site files from dist without deleting extra Pages files.
cp -a "$root/dist/." "$root/docs/"
if [ -n "$cname" ]; then
  printf '%s\n' "$cname" > "$root/docs/CNAME"
fi
echo "Synced dist/ → docs/ (kept docs/CNAME)"
