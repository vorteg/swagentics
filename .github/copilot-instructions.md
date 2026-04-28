# SYSTEM CONTEXT: Swagentics — Multi-Agent Orchestration Framework (v2)
This repository uses a hybrid AI-assisted development framework that combines custom orchestration infrastructure with VS Code's native subagent system.

## 1. Universal Directives (Unbreakable)

### Runtime Configuration
Before executing ANY Python script, read `.github/.copilot-dev.tson` → `[runtime].python_runner`.
- If `python_runner = "uv run"` → use `uv run script.py`
- If `python_runner = "python3"` → use `python3 script.py`
- If the `[runtime]` section is empty or missing → run `which uv` to detect, then persist the result in `.copilot-dev.tson`.

**NEVER assume `python`, `python3`, or `uv run` without checking this config first.**

### Project Stack Awareness
Before ANY code generation, read `.github/.copilot-dev.tson` to identify:
- `project_profile` (e.g., "backend", "devops", "fullstack")
- `managed_files` list
- Active skills and instructions

**NEVER suggest code or tools outside the detected stack profile.**

### Core Protocols
- **Context Economy (Lazy Loading):** DO NOT assume the project structure. You MUST read **`.github/agents/assets/atlas.tson`** at the start of a session. It is your root map.
- **Discovery Tool:** NEVER read large `.tson` files fully. Use the discovery tool: read `[runtime].python_runner` from `.copilot-dev.tson`, then run `<python_runner> .github/hooks/scripts/discovery.py --query <keyword> --type [file|skill]`.
- **Resilience Protocol (Zero-Runtime):**
  - If the detected Python runtime is missing, perform all framework operations (indexing, blueprinting) **manually**.
  - If a requested stack/pattern is missing from the library, generate it using the **Veracity & Evidence** rule.
- **Veracity & Evidence (Zero-Hallucination):**
  - For ALL decisions regarding Architecture, Design Patterns, Methodology, and Testing, you MUST query official sources via `context7` or `searxng`.
  - **Cite your sources:** Explicitly state where the recommendation comes from (e.g., "Following the official Rust API Guidelines...").
  - **Transparency of Failure:** If no reliable/official information is found, you MUST inform the user: *"I could not find official documentation for [X] in [Y]. Proposing a general engineering approach instead, or we can look for a documented alternative."*
- **Strict Context Isolation:** Do NOT automatically include files open in the editor. Rely on the Discovery Tool.

### State Management
Cross-agent communication uses TWO mechanisms depending on the execution mode:
- **Within a session (Mode 1):** The `@dispatcher` invokes agents as **subagents** via the `agent` tool. The dispatcher MUST create and update `.github/memory/active_state.tson` after each subagent returns. Each subagent runs in its own isolated context window and returns only a summary. DO NOT roleplay the subagents; you must physically call the `agent` tool.
- **Across sessions (Mode 3):** State persists in `.github/memory/active_state.tson`. This file MUST be committed to the worktree branch — it is the only communication channel between chat sessions.
- **Historical Traceability (The "Why"):** If you need to understand *why* a decision was made or review the historical log of subagent handoffs, query `.github/memory/activity_log.md`. Do NOT use the `read` tool to load the entire file if it is large; instead, use the `search` tool (or `grep` if you have the `execute` tool) to find specific keywords related to the component in question.
- **Graceful Degradation:** If `active_state.tson` does not exist, operate in **standalone mode** — read the repo map and skills directly, skip state synchronization, and do NOT produce a handoff block.
  - When creating `active_state.tson`, always start from the template at `.github/memory/templates/active_state.template.tson` and validate against `.github/memory/schemas/active_state.schema.tson`. Never write freeform state.
- **Documentation Integrity:** When working with third-party libraries, frameworks, or APIs:
  - **ALWAYS** consult MCP servers (context7, web search) to verify current API syntax, configuration, and version-specific behavior before writing code. Do NOT rely on training data alone.
  - Tag your confidence: if you are unsure about an API, config option, or version detail, say so explicitly. Use phrases like "I need to verify this" and then look it up — never invent plausible-sounding answers.
  - If no MCP server is available and you cannot verify, **ask the user** rather than guessing.
- **Output Discipline:** Be concise. Do not duplicate file contents in the chat when the edit is already applied. Confirm changes briefly — the diff speaks for itself. Avoid verbose explanations unless the user asks for detail.
- **Pre-Commit Sync:** Before executing any `git commit` command, ALWAYS run the sync script first (using the detected `python_runner`): `bash .github/hooks/scripts/sync_agents.sh`. This regenerates agent indexes (`.tson` files). Stage the updated `.tson` files before committing.

## 2. Agent Ecosystem
Each agent has restricted tools defined in its frontmatter. The `@dispatcher` is the coordinator and can invoke any other agent as a subagent.
- `@dispatcher`: Orchestrator. Analyzes tasks, selects execution mode, and coordinates agents via subagents or handoffs.
- `@tech-lead`: Architecture & scaffolding. Read/search only — no file editing or terminal execution.
- `@explorer`: Read-only repository explorer. Answers questions about the codebase. User-invocable only — not part of any pipeline.
- `@appsec`: Security audit. **Read-only tools** — cannot modify code, only report findings.
- `@qa`: Test generation. Full tool access for writing and running tests.
- `@devops`: Infrastructure & cleanup. Full tool access for migrations, Docker, CI/CD.
- `@framework-admin`: Framework self-maintenance. Manages agent definitions, scripts, and manifest.

> **Note:** Users can add their own agents (e.g., `@backend-coder`, `@frontend-coder`) via `/copilot-init` based on their project's needs. See `docs/creating-agents.md` for guidance.

## 3. MCP Tool Integration
MCP server tools are controlled via the agent's `tools` frontmatter — **skills cannot add tools**.
- To grant an agent access to ALL tools from an MCP server: `tools: ['<server-name>/*']`
- To grant access to a specific tool: `tools: ['<server-name>/<tool-name>']`
- MCP servers must be configured in `.vscode/mcp.json` (workspace) or user settings. See `.vscode/mcp.json.example` for a template.
- If a tool listed in the frontmatter is not available in the environment, it is silently ignored.
- Example: `tools: ['github/*', 'context7/*', 'search', 'edit']` grants GitHub MCP + Context7 + built-in search/edit.

### Required MCPs
The following MCP servers are **required** for optimal orchestration quality:
- **`context7`** — Documentation lookup. Prevents hallucinations by ensuring agents use current, official docs.
- **`searxng`** — Web search. Enables awareness of current CVEs, breaking changes, and community solutions.

### Strongly Recommended MCPs
- **`filesystem`** — Precise file read/write with line-level control, directory trees, and metadata.
- **`github-mcp-server`** — GitHub API integration for PRs, issues, and code search.

If these MCPs are not available, run `/copilot-init` to get a degraded mode warning and configuration guidance.