#!/bin/bash
# upgrade.sh — Selectively upgrades the Swagentics framework
#
# Only touches files listed in .github/.copilot-dev.tson (manifest).
# Your workflows, ISSUE_TEMPLATE, CODEOWNERS, etc. are NEVER modified.
# Custom agents, skills, and instructions you created are also preserved.
# Deprecated framework files are detected and flagged (with backup).
#
# Usage:
#   bash .github/hooks/scripts/upgrade.sh              # Upgrade to latest (main)
#   bash .github/hooks/scripts/upgrade.sh v2.0.0       # Upgrade to a specific tag
#
# Compatible with: Linux, macOS

set -e

VERSION="${1:-main}"
REPO="vorteg/swagentics"
GITHUB_DIR=".github"
MANIFEST_FILE="${GITHUB_DIR}/.copilot-dev.tson"

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

echo -e "${CYAN}🔄 Swagentics framework upgrade${NC}"
echo -e "   Target version: ${YELLOW}${VERSION}${NC}"
echo ""

# ── Checks ────────────────────────────────────────────────────────────────────
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo -e "${RED}❌ Not inside a git repository.${NC}"
  exit 1
fi

if ! command -v curl &>/dev/null; then
  echo -e "${RED}❌ curl is required. Install it and try again.${NC}"
  exit 1
fi

# ── Currently installed version ───────────────────────────────────────────────
CURRENT_VERSION="(not installed)"
VERSION_FILE="${GITHUB_DIR}/framework-version.tson"
if [ -f "$VERSION_FILE" ]; then
  CURRENT_VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('$VERSION_FILE', 'rb')).get('version', '(not installed)'))" 2>/dev/null || echo "(not installed)")
fi
echo -e "   Current version: ${DIM}${CURRENT_VERSION}${NC}"
echo ""

# ── Preserve user's project_profile (if exists) ──────────────────────────────
USER_PROJECT_PROFILE=""
if [ -f "$MANIFEST_FILE" ]; then
  USER_PROJECT_PROFILE=$(python3 -c "import tomllib; print(tomllib.load(open('$MANIFEST_FILE', 'rb')).get('project_profile', ''))" 2>/dev/null || echo "")
fi

# ── Download target version ──────────────────────────────────────────────────
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

DOWNLOAD_OK=false

# Strategy 1: gh CLI (works with private repos, auto-authenticated)
if command -v gh &>/dev/null; then
  echo -e "${CYAN}📥 Downloading ${VERSION} via gh CLI...${NC}"
  if gh api "repos/${REPO}/tarball/${VERSION}" > "${TMPDIR}/archive.tar.gz" 2>/dev/null; then
    DOWNLOAD_OK=true
  else
    echo -e "${DIM}   gh CLI failed, trying alternatives...${NC}"
  fi
fi

# Strategy 2: curl with GITHUB_TOKEN (private repos without gh CLI)
if [ "$DOWNLOAD_OK" = false ] && [ -n "${GITHUB_TOKEN:-}" ]; then
  echo -e "${CYAN}📥 Downloading ${VERSION} with GITHUB_TOKEN...${NC}"
  HTTP_CODE=$(curl -sL -w "%{http_code}" \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    -o "${TMPDIR}/archive.tar.gz" \
    "https://api.github.com/repos/${REPO}/tarball/${VERSION}")

  if [ "$HTTP_CODE" = "200" ]; then
    DOWNLOAD_OK=true
  else
    echo -e "${DIM}   GITHUB_TOKEN failed (HTTP ${HTTP_CODE}), trying without auth...${NC}"
  fi
fi

# Strategy 3: curl without auth (public repos only)
if [ "$DOWNLOAD_OK" = false ]; then
  TARBALL_URL="https://github.com/${REPO}/archive/refs/tags/${VERSION}.tar.gz"

  # If not a tag (e.g., "main"), use the branch URL
  if [[ "$VERSION" == "main" || "$VERSION" == "dev" || ! "$VERSION" =~ ^v ]]; then
    TARBALL_URL="https://github.com/${REPO}/archive/refs/heads/${VERSION}.tar.gz"
  fi

  echo -e "${CYAN}📥 Downloading ${VERSION} (public)...${NC}"
  HTTP_CODE=$(curl -sL -w "%{http_code}" -o "${TMPDIR}/archive.tar.gz" "$TARBALL_URL")

  if [ "$HTTP_CODE" = "200" ]; then
    DOWNLOAD_OK=true
  fi
fi

if [ "$DOWNLOAD_OK" = false ]; then
  echo -e "${RED}❌ Could not download version '${VERSION}'.${NC}"
  echo ""
  echo "   If the repo is private, you need one of these options:"
  echo "     1. Install gh CLI:  https://cli.github.com  (then: gh auth login)"
  echo "     2. Export token:    export GITHUB_TOKEN=ghp_xxxxx"
  echo ""
  echo "   Verify the tag/branch exists at: https://github.com/${REPO}"
  exit 1
fi

# Extract — GitHub tarball has a variable root directory
tar -xzf "${TMPDIR}/archive.tar.gz" -C "$TMPDIR"
EXTRACTED_DIR=$(find "${TMPDIR}" -mindepth 1 -maxdepth 1 -type d | head -1)

if [ -z "$EXTRACTED_DIR" ] || [ ! -d "${EXTRACTED_DIR}/.github" ]; then
  echo -e "${RED}❌ Downloaded archive does not have the expected structure.${NC}"
  exit 1
fi

SOURCE_GITHUB="${EXTRACTED_DIR}/.github"

# ── Read manifest from downloaded version ─────────────────────────────────────
NEW_MANIFEST="${SOURCE_GITHUB}/.copilot-dev.tson"
if [ ! -f "$NEW_MANIFEST" ]; then
  echo -e "${RED}❌ Version ${VERSION} does not include a manifest (.copilot-dev.tson).${NC}"
  echo "   Only versions >= 2.0.0 support automatic upgrades."
  exit 1
fi

NEW_VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('$NEW_MANIFEST', 'rb')).get('version', 'unknown'))" 2>/dev/null || echo "unknown")

echo -e "   Downloaded version: ${GREEN}${NEW_VERSION}${NC}"
echo ""

# ── Extract lists from manifest ──────────────────────────────────────────────
mapfile -t MANAGED_FILES < <(python3 -c "import tomllib; print('\n'.join(tomllib.load(open('$NEW_MANIFEST', 'rb')).get('managed_files', [])))" 2>/dev/null)
mapfile -t DEPRECATED_FILES < <(python3 -c "import tomllib; print('\n'.join(tomllib.load(open('$NEW_MANIFEST', 'rb')).get('deprecated_files', [])))" 2>/dev/null)

# ── Project Profile Filtering ────────────────────────────────────────────────
PROJECT_PROFILE=""
if [ -n "$USER_PROJECT_PROFILE" ]; then
  PROJECT_PROFILE="$USER_PROJECT_PROFILE"
elif [ -f "$MANIFEST_FILE" ]; then
  PROJECT_PROFILE=$(python3 -c "import tomllib; print(tomllib.load(open('$MANIFEST_FILE', 'rb')).get('project_profile', ''))" 2>/dev/null)
fi

if [ -n "$PROJECT_PROFILE" ]; then
  echo -e "   Detected profile: ${CYAN}${PROJECT_PROFILE}${NC}"
else
  echo -e "   Profile: ${DIM}(not set — run /copilot-init to configure)${NC}"
fi

# If profile is set, filter optional agents
if [ -n "$PROJECT_PROFILE" ] && [ "$PROJECT_PROFILE" != "fullstack" ]; then
  echo -e "   ${DIM}Filtering optional agents for profile: ${PROJECT_PROFILE}...${NC}"
  
  # Extract allowed agents for this profile
  mapfile -t PROFILE_AGENTS < <(python3 -c "import tomllib; data=tomllib.load(open('$NEW_MANIFEST', 'rb')); print('\n'.join(data.get('optional_agents', {}).get('$PROJECT_PROFILE', [])))" 2>/dev/null)
  
  if [ ${#PROFILE_AGENTS[@]} -gt 0 ] && [ "${PROFILE_AGENTS[0]}" != "" ]; then
    MANAGED_FILES+=("${PROFILE_AGENTS[@]}")
  fi

  # Extract all optional agents NOT for this profile to mark as deprecated
  mapfile -t ALL_OPTIONAL < <(python3 -c "import tomllib; data=tomllib.load(open('$NEW_MANIFEST', 'rb')); print('\n'.join([a for agents in data.get('optional_agents', {}).values() for a in agents]))" 2>/dev/null)
  for opt_agent in "${ALL_OPTIONAL[@]}"; do
    if [ -n "$opt_agent" ]; then
      if [[ ! " ${PROFILE_AGENTS[@]} " =~ " ${opt_agent} " ]]; then
        DEPRECATED_FILES+=("$opt_agent")
      fi
    fi
  done
else
  # If fullstack or empty, include ALL optional agents from all categories
  mapfile -t ALL_OPTIONAL < <(python3 -c "import tomllib; data=tomllib.load(open('$NEW_MANIFEST', 'rb')); print('\n'.join([a for agents in data.get('optional_agents', {}).values() for a in agents]))" 2>/dev/null)
  if [ ${#ALL_OPTIONAL[@]} -gt 0 ] && [ "${ALL_OPTIONAL[0]}" != "" ]; then
    MANAGED_FILES+=("${ALL_OPTIONAL[@]}")
  fi
fi

if [ ${#MANAGED_FILES[@]} -eq 0 ]; then
  echo -e "${RED}❌ No files found in the manifest.${NC}"
  exit 1
fi

echo -e "${CYAN}📋 ${#MANAGED_FILES[@]} files in manifest${NC}"
if [ ${#DEPRECATED_FILES[@]} -gt 0 ]; then
  echo -e "${DIM}   ${#DEPRECATED_FILES[@]} files marked as deprecated${NC}"
fi
echo ""

# ── Phase 1: Detect deprecated files (warn only, no delete) ──────────────────
LEGACY_FOUND=0
LEGACY_LIST=()

if [ ${#DEPRECATED_FILES[@]} -gt 0 ]; then
  for dep_file in "${DEPRECATED_FILES[@]}"; do
    if [ -z "$dep_file" ]; then continue; fi
    TARGET_DEP="${GITHUB_DIR}/${dep_file}"

    if [ -f "$TARGET_DEP" ]; then
      echo -e "  ${YELLOW}⚠${NC} ${dep_file} ${DIM}(legacy format detected)${NC}"
      LEGACY_FOUND=$((LEGACY_FOUND + 1))
      LEGACY_LIST+=("$dep_file")
    fi
  done

  if [ $LEGACY_FOUND -gt 0 ]; then
    echo ""
  fi
fi

# ── Phase 2: Apply updates ───────────────────────────────────────────────────
ADDED=0
UPDATED=0
CONFLICT=0
SKIPPED=0

for file in "${MANAGED_FILES[@]}"; do
  if [ -z "$file" ]; then continue; fi
  SOURCE_FILE="${SOURCE_GITHUB}/${file}"
  TARGET_FILE="${GITHUB_DIR}/${file}"

  # Don't self-update during execution — done at the end
  if [ "$file" = "hooks/scripts/upgrade.sh" ]; then
    continue
  fi

  if [ ! -f "$SOURCE_FILE" ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  TARGET_DIR=$(dirname "$TARGET_FILE")
  mkdir -p "$TARGET_DIR"

  if [ ! -f "$TARGET_FILE" ]; then
    cp "$SOURCE_FILE" "$TARGET_FILE"
    echo -e "  ${GREEN}+${NC} ${file} ${DIM}(new)${NC}"
    ADDED=$((ADDED + 1))
  else
    if diff -q "$SOURCE_FILE" "$TARGET_FILE" &>/dev/null; then
      SKIPPED=$((SKIPPED + 1))
    else
      BACKUP="${TARGET_FILE}.pre-upgrade"
      cp "$TARGET_FILE" "$BACKUP"
      cp "$SOURCE_FILE" "$TARGET_FILE"
      echo -e "  ${YELLOW}~${NC} ${file} ${DIM}(updated — backup at ${file}.pre-upgrade)${NC}"
      UPDATED=$((UPDATED + 1))
      CONFLICT=$((CONFLICT + 1))
    fi
  fi
done

# ── Phase 3: Restore user's project_profile in manifest ──────────────────────
if [ -n "$USER_PROJECT_PROFILE" ] && [ -f "${GITHUB_DIR}/.copilot-dev.tson" ]; then
  python3 -c "
import re
file_path = '${GITHUB_DIR}/.copilot-dev.tson'
try:
    with open(file_path, 'r') as f: content = f.read()
    if 'project_profile' in content:
        content = re.sub(r'project_profile\s*=\s*\".*?\"', f'project_profile = \"${USER_PROJECT_PROFILE}\"', content)
    else:
        content += f'\nproject_profile = \"${USER_PROJECT_PROFILE}\"\n'
    with open(file_path, 'w') as f: f.write(content)
except Exception as e:
    pass
" 2>/dev/null || true
fi

echo ""

# ── Summary ───────────────────────────────────────────────────────────────────
echo -e "${CYAN}────────────────────────────────────────${NC}"
echo -e "  ${GREEN}+ ${ADDED} new${NC}"
echo -e "  ${YELLOW}~ ${UPDATED} updated${NC}"
if [ $LEGACY_FOUND -gt 0 ]; then
  echo -e "  ${YELLOW}⚠ ${LEGACY_FOUND} legacy files detected${NC}"
fi
echo -e "  ${DIM}  ${SKIPPED} unchanged${NC}"
echo -e "${CYAN}────────────────────────────────────────${NC}"

if [ $CONFLICT -gt 0 ]; then
  echo ""
  echo -e "${YELLOW}⚠️  ${CONFLICT} file(s) had differences.${NC}"
  echo -e "   Backups created as ${DIM}.pre-upgrade${NC} for each."
  echo -e "   Review changes: ${DIM}diff file file.pre-upgrade${NC}"
  echo -e "   If all good:    ${DIM}rm .github/**/*.pre-upgrade${NC}"
fi

if [ $LEGACY_FOUND -gt 0 ]; then
  echo ""
  echo -e "${YELLOW}📋 ${LEGACY_FOUND} file(s) in legacy format need migration.${NC}"
  echo -e "   These files may contain custom project content."
  echo -e "   To migrate them safely, open Copilot Chat and run:"
  echo ""
  echo -e "   ${CYAN}@copilot /copilot-upgrade${NC}"
fi

# ── Post-upgrade: regenerate indexes ─────────────────────────────────────────
if [ -f "${GITHUB_DIR}/hooks/scripts/sync_agents.sh" ]; then
  echo ""
  echo -e "${CYAN}🔧 Regenerating framework indexes...${NC}"
  rm -f "${GITHUB_DIR}/agents/assets"/*.tson
  bash "${GITHUB_DIR}/hooks/scripts/sync_agents.sh"
fi

# ── Update version file ──────────────────────────────────────────────────────
NEW_VERSION_FILE="${EXTRACTED_DIR}/.github/framework-version.tson"
TARGET_VERSION_FILE="${GITHUB_DIR}/framework-version.tson"
if [ -f "$NEW_VERSION_FILE" ]; then
    cp "$NEW_VERSION_FILE" "$TARGET_VERSION_FILE"
fi

echo ""
echo -e "${GREEN}✅ Framework upgraded: v${CURRENT_VERSION} → v${NEW_VERSION}${NC}"
echo ""

SELF_SOURCE="${SOURCE_GITHUB}/hooks/scripts/upgrade.sh"
SELF_TARGET="${GITHUB_DIR}/hooks/scripts/upgrade.sh"
if [ -f "$SELF_SOURCE" ] && ! diff -q "$SELF_SOURCE" "$SELF_TARGET" &>/dev/null; then
  cp "$SELF_TARGET" "${SELF_TARGET}.pre-upgrade" 2>/dev/null || true
  cp "$SELF_SOURCE" "$SELF_TARGET"
fi
