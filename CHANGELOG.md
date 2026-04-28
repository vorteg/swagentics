# Changelog

All notable changes to the Swagentics framework will be documented in this file.

## [2.0.0-alpha.1] - 2026-04-28

### 🚀 Major Rebranding & Agnosticism (Genesis)
- **Brand Identity:** Officially rebranded to **Swagentics**.
- **Agnostic Core:** Removed all hardcoded technology stacks (React, TypeScript, etc.) to support any language.
- **English First:** Translated the entire framework (agents, scripts, prompts, documentation) to English for global use.
- **Pure Python Runtime:** Migrated all Node.js/MJS scripts to Python 3 for simplified dependency management.
- **MIT License:** Repository is now officially MIT Licensed.

### ✨ New Features
- **Explorer Agent:** Added `@explorer` — a read-only codebase analyst for safe Q&A.
- **Dynamic Runtime Detection:** Framework now detects and persists the user's environment (`uv` or `python3`) in `.copilot-dev.tson`.
- **MCP-First Protocol:** Standardized `context7` and `searxng` as required MCPs to mitigate hallucinations.
- **Veracity & Evidence Protocol:** Agents must now cite official documentation sources for technical decisions.
- **Mode-Agnostic State Management:** Corrected Mode 1 state-sync bug; all pipeline transitions now record state in `active_state.tson` and `activity_log.md`.
- **Discovery Engine (Atlas):** Optimized project mapping for low-overhead context loading.

### 🛡️ Security & IP
- **Purge:** Deleted all corporate-branded assets, design instructions, and private team presentation summaries.
- **Sanitization:** Audited all instructions to remove specific company internal library references.

### 🔧 Maintenance
- **v2 master manifest:** New `.copilot-dev.tson` structure with `[runtime]` and `[mcp_status]` sections.
- **Refactored `upgrade.sh`:** Selective framework updates that respect the user's `project_profile`.
