#!/usr/bin/env bash
# Optional. Downloads the original full-size image files from the current lyndonpolan.com
# host into images/, replacing the copies in this repository with byte-identical originals.
# Run it BEFORE the domain is pointed at GitHub Pages - afterwards the old host is no longer
# reachable under that name. Thumbnails (images/mini/) are left as they are.
#
#   bash tools/fetch-originals.sh
set -euo pipefail
cd "$(dirname "$0")/.."
BASE="https://lyndonpolan.com"
for i in $(seq 1 17); do
  curl -fsS -o "images/$i.jpg.tmp" "$BASE/images/$i.jpg" && mv "images/$i.jpg.tmp" "images/$i.jpg"
  echo "images/$i.jpg"
done
curl -fsS -o images/LyndonGif.gif.tmp "$BASE/images/LyndonGif.gif" && mv images/LyndonGif.gif.tmp images/LyndonGif.gif && echo "images/LyndonGif.gif"
curl -fsS -o favicon.png.tmp "$BASE/favicon.png" && mv favicon.png.tmp favicon.png && echo "favicon.png"
echo "Done. Nothing else needs rebuilding - the pages already point at these file names."
