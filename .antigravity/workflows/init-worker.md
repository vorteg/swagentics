---
description: Framework Initialization & Repository Onboarding — Trigger via /init
---

# WORKFLOW: Antigravity Initialization Worker

<mcp_health_check>
  **MANDATORY FIRST STEP:** Verify the required MCP servers are available in the Antigravity toolset before proceeding:

  1. **context7**: Verify `mcp_context7_resolve-library-id` and `mcp_context7_query-docs` tools exist.
  2. **sequential-thinking**: Verify `mcp_sequential-thinking_sequentialthinking` exists (crucial for Chain-of-Thought logic on Flash/Lightweight models during QA/Parsing).
  
  *If missing, warn the user that orchestration quality will be reduced and degraded mode will activate.*
</mcp_health_check>

<discovery_protocol>
  1. **Script Execution:** Do NOT attempt to index the repository manually. Use the `run_command` tool to execute the deterministic blueprint script via `uv`:
     ```powershell
     uv run python .github/hooks/scripts/blueprint.py --stack <stack_name>
     ```
     *(If the user did not specify a stack name, ask them before running the script).*
  2. **State Ingestion:** Wait for the script to finish and then read the generated `.github/memory/active_state.tson`.
</discovery_protocol>

<artifact_generation>
  Antigravity bridges the deterministic TOML state to the visual UI using Native Artifacts. You MUST generate these artifacts based on the script's output:
  
  1. **Task Artifact:** Translate the pending tasks from `active_state.tson` into an Antigravity Native `task` artifact (`task.md`). This provides an interactive UI checklist.
  2. **Implementation Plan Artifact:** If the blueprint script output outlines an architecture or ADR, translate it into an `implementation_plan` artifact for the user to formally approve.
  3. **Handoff:** Once the artifacts are generated, instruct the user to invoke the next appropriate worker (e.g., `/tech-lead`) to begin execution, utilizing the newly created UI checklist.
</artifact_generation>
