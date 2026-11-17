#!/usr/bin/env bash
# Clone FHIR-AgentBench into vendor/ at a pinned commit. The vendored code is never edited.
set -euo pipefail

cd "$(dirname "$0")/.."
REPO="https://github.com/glee4810/FHIR-AgentBench.git"
COMMIT="bbb42909a5a7eb907d1cd91f72a560729e7037ea"
DEST="vendor/FHIR-AgentBench"

[ -d "$DEST/.git" ] || git clone "$REPO" "$DEST"
git -C "$DEST" checkout --quiet "$COMMIT"
echo "FHIR-AgentBench at $(git -C "$DEST" rev-parse HEAD)"
