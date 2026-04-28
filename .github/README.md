# Swagentics: Internal Framework Assets

This directory contains the core orchestration logic, agent definitions, and persistent memory for the Swagentics framework.

## 📁 Directory Overview

- **`agents/`**: Specialized agent definitions (`.agent.md`) and their dynamic TSON indices.
- **`hooks/scripts/`**: The Python-based automation engine for syncing agents, generating the project Atlas, and handling upgrades.
- **`instructions/`**: Global coding standards and profile-specific rules.
- **`memory/`**: Cross-agent state persistence (`active_state.tson`) and historical activity logs.
- **`prompts/`**: Operational commands like `/copilot-init` and `/copilot-upgrade`.
- **`skills/`**: On-demand expert workflows for specific tasks (Architecture, Handoffs, Audits).

## 🛡️ Usage Policy

These files are managed by the `@framework-admin` agent. While you can customize them, it is recommended to use the `/copilot-upgrade` protocol to ensure compatibility with future Genesis releases.

---
*Swagentics v2.0.0-alpha.1*