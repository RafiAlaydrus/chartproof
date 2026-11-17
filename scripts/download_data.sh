#!/usr/bin/env bash
# Download the MIMIC-IV FHIR demo (open, ODbL v1.0) into data/raw/, verify it, and gunzip.
set -euo pipefail

cd "$(dirname "$0")/.."
URL="https://physionet.org/files/mimic-iv-fhir-demo/2.1.0/"
DEST="data/raw"

mkdir -p "$DEST"
# -N skips files that are already up to date, -c resumes partial files
wget -r -N -c -np -nH --cut-dirs=3 -R "index.html*" -P "$DEST" "$URL"

# Check every downloaded file against the published checksums
# (the published file has one space between hash and name; shasum wants two)
(cd "$DEST" && sed 's/^\([0-9a-f]\{64\}\) /\1  /' SHA256SUMS.txt | shasum -a 256 -c -)

# -k keeps the .gz so re-runs with -N don't download again
find "$DEST" -name '*.gz' -exec gunzip -kf {} +
echo "Done. NDJSON files are in $DEST"
