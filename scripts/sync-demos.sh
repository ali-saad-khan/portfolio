#!/usr/bin/env bash
# Rebuilds each showcase project and copies its static demo into demos/.
# The n8n viewer uses relative URLs, and Vercel serves /demos/n8n-workflows without a
# trailing slash, so a <base> tag is injected into the portfolio copy only.
set -euo pipefail
APPS="${APPS:-$HOME/apps}"; OUT="$(cd "$(dirname "$0")/.." && pwd)/demos"
(cd "$APPS/pulseboard" && npm run build >/dev/null) && rm -rf "$OUT/pulseboard" && cp -r "$APPS/pulseboard/dist" "$OUT/pulseboard"
(cd "$APPS/taskflow-fullstack/web" && npm run build:demo >/dev/null) && rm -rf "$OUT/taskflow" && cp -r "$APPS/taskflow-fullstack/web/dist-demo" "$OUT/taskflow"
(cd "$APPS/launchpad-saas" && npm run build:demo >/dev/null) && rm -rf "$OUT/launchpad" && cp -r "$APPS/launchpad-saas/out" "$OUT/launchpad"
(cd "$APPS/n8n-automation-showcase" && npm run build:demo >/dev/null) && rm -rf "$OUT/n8n-workflows" && cp -r "$APPS/n8n-automation-showcase/dist-demo" "$OUT/n8n-workflows"
sed -i 's|<head>|<head>\n  <base href="/demos/n8n-workflows/">|' "$OUT/n8n-workflows/index.html"
echo "demos synced"
