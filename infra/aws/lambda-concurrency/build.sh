#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# System zip preserves the executable bit on run.sh, which the Web Adapter needs
# to exec it. terraform's archive_file does not preserve file modes reliably.
rm -rf dist
mkdir -p dist
chmod +x src/run.sh

( cd src && zip -q -X ../dist/plain.zip lambda.mjs shared.mjs )
( cd src && zip -q -X ../dist/lwa.zip server.mjs shared.mjs run.sh )

echo "built:"
echo "  dist/plain.zip -> $(unzip -Z1 dist/plain.zip | tr '\n' ' ')"
echo "  dist/lwa.zip   -> $(unzip -Z1 dist/lwa.zip | tr '\n' ' ')"
