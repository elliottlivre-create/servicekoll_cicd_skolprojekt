#!/usr/bin/env bash
# Rullar tillbaka testmiljön till senast verifierade version (taggen :stable).
# Användning: bash scripts/rollback.sh <image-namn utan tagg>
set -euo pipefail

IMAGE_NAME="${1:?Ange image-namnet, t.ex. ghcr.io/namn/servicekoll}"
STABLE="$IMAGE_NAME:stable"

echo "=== Rollback till $STABLE ==="

echo "Hämtar senast verifierade version..."
if ! docker pull "$STABLE" 2>/dev/null; then
  if ! docker image inspect "$STABLE" >/dev/null 2>&1; then
    echo "Det finns ingen $STABLE att rulla tillbaka till (första deployen?)."
    exit 1
  fi
  echo "Använder lokal kopia av $STABLE"
fi

bash scripts/deploy.sh "$STABLE"
bash scripts/verify.sh

echo "=== Rollback klar: testmiljön kör $STABLE igen ==="