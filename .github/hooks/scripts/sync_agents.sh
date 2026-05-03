#!/bin/bash

# Halt on errors
set -e

echo "🚀 Starting Swagentics framework synchronization..."

# ── Change detection ──────────────────────────────────────────────────────────
# We only sync if there are changes in the repo, ignoring framework memory/assets
if git diff --quiet HEAD -- . ':!.github/memory' ':!.github/agents/assets' ':!.github/memory/activity_log.md' ':!activity_log.md'; then
  echo "✅ No relevant changes detected in the repository. Skipping synchronization."
  exit 0
fi

# ── Runtime detection ─────────────────────────────────────────────────────────
if command -v uv &>/dev/null; then
  RUNNER="uv run"
elif command -v python3 &>/dev/null; then
  RUNNER="python3"
else
  echo "❌ Error: Python3 or 'uv' is required to synchronize the framework."
  exit 1
fi

echo "⚡ Runtime detected: $RUNNER"

# 1. Atlas Map
echo "🗺️ Generating project Atlas..."
$RUNNER .github/hooks/scripts/generate_atlas.py

# 2. Repo Maps
echo "🗺️ Generating local repository maps..."
for agent_file in .github/agents/*.agent.md; do
  role_name=$(basename "$agent_file" .agent.md)
  if [ "$role_name" = "*" ]; then continue; fi
  echo "  🔍 Scanning for: $role_name"
  $RUNNER .github/hooks/scripts/generate_repo_index.py --role "$role_name"
done

echo "✅ Deterministic synchronization complete! .tson index files updated."

# ── VALIDATION PHASE ──────────────────────────────────────────────────────────
echo ""
echo "🔍 Validating framework integrity..."

# 1. Clean orphaned TSONs
for tson in .github/agents/assets/*_index.tson; do
  if [ -f "$tson" ]; then
    agent_name=$(basename "$tson" | sed 's/_index.tson//')
    if [ ! -f ".antigravity/workflows/${agent_name}-worker.md" ]; then
      echo "  🧹 Removing orphaned index asset: $(basename "$tson")"
      rm -f "$tson"
    fi
  fi
done

ERRORS=0



if [ $ERRORS -gt 0 ]; then
  echo ""
  echo "⚠️  $ERRORS validation error(s) found. Fix before committing."
  exit 1
else
  echo "✅ All clear. Framework validated."
fi