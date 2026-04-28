# Swagentics: Multi-Agent Orchestration Framework (v2)

![version](https://img.shields.io/badge/version-2.0.0--alpha.1-orange)
![license](https://img.shields.io/badge/license-MIT-green)

**Swagentics** is a production-grade, technology-agnostic multi-agent orchestration framework for GitHub Copilot Chat. It transforms your repository into an intelligent assembly line, providing a team of specialized agents with distinct roles, zero-hallucination protocols, and deterministic state management.

---

## 🚀 Key Features

- **Agnostic Architecture:** Not tied to any specific stack. Works with Python, JavaScript, Go, Rust, and more.
- **MCP-First Protocol:** Mandatory integration with `context7` and `searxng` to ensure agents use current, official documentation and real-world data.
- **Zero-Hallucination Evidence Protocol:** Agents are required to cite official sources for all architectural and technical decisions.
- **Deterministic State Management:** Mode-agnostic pipeline persistence via `active_state.tson`, enabling seamless agent handoffs even across sessions.
- **Subagent Isolation:** Mode 1 orchestration ensures each agent runs in its own encapsulated context window, preventing context bloat and "hallucinated roleplay."
- **Explorer Agent:** A built-in, read-only analyst for low-overhead codebase exploration without side effects.

---

## 📦 Installation

1. **Clone/Copy:** Add the `.github/` folder to your repository.
2. **Initialize:** Open Copilot Chat and run:
   ```
   @dispatcher /copilot-init
   ```
   *This will detect your runtime (uv/python), check MCP health, and generate foundational skills.*
3. **Sync:** Run the initial index generation:
   ```bash
   bash .github/hooks/scripts/sync_agents.sh
   ```

---

## 🤖 Core Agent Roster

| Agent | Role | Capability |
|-------|------|------------|
| `@dispatcher` | **Orchestrator** | Coordinates the team, selects execution modes, and manages subagent pipelines. |
| `@tech-lead` | **Architect** | Defines ADRs, interfaces, and scaffolding. (Read-only) |
| `@explorer` | **Analyst** | Read-only codebase explorer. Answers Q&A without modifying state. |
| `@qa` | **Tester** | Generates edge-case tests and validates implementation. |
| `@appsec` | **Auditor** | Security auditing (OWASP, RBAC). (Read-only) |
| `@devops` | **Ops** | Infrastructure, migrations, and deployment cleanup. |
| `@framework-admin`| **Maintainer**| Manages Swagentics internal scripts, agents, and manifest. |

*Users can dynamically add stack-specific agents (e.g., `@backend-coder`) during initialization.*

---

## 🛠️ Execution Modes

### Mode 1: Subagent Pipeline (Default)
The `@dispatcher` invokes agents as **isolated subagents**. Each agent completes its task and returns a summary to the dispatcher. This is the most robust mode for complex features.

### Mode 2: Compact Session
A single agent owns the task in a direct chat. Best for iterative, short-lived tasks where context continuity within the session is key.

### Mode 3: Parallel Worktrees
For massive features running in parallel. Uses `git worktree` and persists state in `active_state.tson` inside the worktree branch, allowing for cross-session continuity.

---

## 🗺️ Project Structure

```
.github/
├── copilot-instructions.md      # Universal framework directives
├── .copilot-dev.tson            # Framework manifest & runtime config
├── agents/                      # Specialized agent definitions (.agent.md)
│   └── assets/                  # Dynamic indices (TSON)
├── skills/                      # On-demand knowledge workflows
├── instructions/                # Always-on coding standards
├── prompts/                     # One-shot operational prompts (/init, /upgrade)
├── hooks/scripts/               # Pure Python automation engine
└── memory/                      # Persistent state & activity logs
```

---

## 🛡️ License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

## ⚠️ Status: Alpha

Swagentics v2 is currently in **Alpha**. We are actively seeking community feedback to reach a stable 2.0.0 release.