#!/usr/bin/env bash
# Startar en image i testmiljön.
# Användning: bash scripts/deploy.sh <image>
set -euo pipefail

IMAGE="${1:?Ange vilken image som ska deployas}"
CONTAINER="servicekoll-test"
HOST_PORT="${HOST_PORT:-8080}"
APP_PORT="${APP_PORT:-8000}"

echo "=== Deploy till testmiljön ==="
echo "Image: $IMAGE"

echo "Tar bort tidigare container om den finns..."
docker rm -f "$CONTAINER" >/dev/null 2>&1 || true

echo "Startar ny container..."
docker run -d \
  --name "$CONTAINER" \
  -p "$HOST_PORT:$APP_PORT" \
  -e APP_ENV=test \
  "$IMAGE"

echo "=== Containern är startad ==="