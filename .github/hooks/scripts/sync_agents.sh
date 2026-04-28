#!/bin/bash

# Halt on errors
set -e

echo "🚀 Starting Swagentics framework synchronization..."

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

# 3. Skill Registry
echo "🧠 Generating Skill indexes..."
$RUNNER .github/hooks/scripts/generate_skill_registry.py

# 4. Copilot Runtime
echo "🖥️ Updating Copilot runtime..."
$RUNNER .github/hooks/scripts/generate_copilot_runtime.py || echo "⚠️ Copilot Chat extension not found — skipping."

echo "✅ Synchronization complete! .tson files updated in .github/agents/assets/"

# ── VALIDATION PHASE ──────────────────────────────────────────────────────────
echo ""
echo "🔍 Validating framework integrity..."

# 1. Clean orphaned TSONs for agents that no longer exist
for tson in .github/agents/assets/*_index.tson .github/agents/assets/*_skills.tson; do
  if [ -f "$tson" ]; then
    agent_name=$(basename "$tson" | sed 's/_\(index\|skills\).tson//')
    if [ ! -f ".github/agents/${agent_name}.agent.md" ]; then
      echo "  🧹 Removing orphaned asset: $(basename "$tson")"
      rm -f "$tson"
    fi
  fi
done

ERRORS=0

# Check that all skill paths in *_skills.tson actually exist
for tson in .github/agents/assets/*_skills.tson; do
  if [ -f "$tson" ]; then
    paths=$(grep -oP '"path"\s*:\s*"\K[^"]+' "$tson" 2>/dev/null || true)
    for skill_path in $paths; do
      if [ ! -d "$skill_path" ]; then
        echo "❌ BROKEN PATH in $(basename "$tson"): $skill_path does not exist"
        ERRORS=$((ERRORS + 1))
      fi
    done
  fi
done

if [ $ERRORS -gt 0 ]; then
  echo ""
  echo "⚠️  $ERRORS validation error(s) found. Fix before committing."
  exit 1
else
  echo "✅ All clear. Framework validated."
fi