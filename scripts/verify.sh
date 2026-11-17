#!/usr/bin/env bash
# Verifierar att testmiljön fungerar.
# Användning: bash scripts/verify.sh [förväntad version]
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"
EXPECTED_VERSION="${1:-}"
CONTAINER="servicekoll-test"

fail() {
  echo "VERIFIERING MISSLYCKADES: $1"
  echo "--- Containerloggar ---"
  docker logs "$CONTAINER" 2>&1 | tail -n 30 || true
  exit 1
}

echo "=== Verifierar $BASE_URL ==="

echo "1/3 Health check..."
for i in {1..15}; do
  if curl --fail --silent "$BASE_URL/health" >/dev/null; then
    echo "    OK: /health svarar"
    break
  fi
  if [ "$i" -eq 15 ]; then
    fail "/health svarade inte inom 30 sekunder"
  fi
  sleep 2
done

echo "2/3 Version..."
VERSION=$(curl --fail --silent "$BASE_URL/version" | python3 -c 'import json,sys; print(json.load(sys.stdin)["version"])') \
  || fail "/version gick inte att läsa"
echo "    Kör version: $VERSION"
if [ -n "$EXPECTED_VERSION" ] && [ "$VERSION" != "$EXPECTED_VERSION" ]; then
  fail "fel version, förväntade $EXPECTED_VERSION"
fi

echo "3/3 Smoke test av kärnfunktionen..."
STATUS=$(curl --fail --silent "$BASE_URL/service-status?type=pulver&last_service=2020-01-01" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["status"])') \
  || fail "/service-status svarade inte"
if [ "$STATUS" != "forsenad" ]; then
  fail "/service-status gav '$STATUS', förväntade 'forsenad'"
fi
echo "    OK: /service-status svarar rätt"

echo "=== Verifiering godkänd ==="