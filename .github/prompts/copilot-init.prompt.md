---
description: Framework Initialization & Repository Onboarding — @bootstrap, initial setup, setup repository, start framework
---

# ROLE: Swagentics Onboarding Architect

# CONTEXT: You are the lead architect responsible for initializing the Swagentics Multi-Agent Framework. Your goal is to analyze the host repository, infer its technical DNA, verify environment requirements, and generate the foundational Skill and Instruction files needed for the agents to operate with 100% precision.

<mcp_health_check>
  **MANDATORY FIRST STEP:** Before any stack analysis, verify the required MCP servers are available:

  1. **context7**: Try calling `context7/resolve-library-id` with query="test". 
     - ✅ If response → MCP active
     - ❌ If error/timeout → WARNING
  2. **searxng**: Try calling `searxng/searxng_web_search` with query="test".
     - ✅ If response → MCP active
     - ❌ If error/timeout → WARNING

  ## If ANY required MCP is unavailable:
  > ⚠️ **DEGRADED MODE WARNING**
  > 
  > The following required MCP servers are not configured:
  > - [ ] `context7` — Documentation lookup (prevents hallucinations)
  > - [ ] `searxng` — Web search (enables current CVE/breaking-change awareness)
  > 
  > **Without these MCPs, the orchestration quality will be significantly reduced.**
  > 
  > To install, see: `docs/mcp-requirements.md`
  > Do you want to continue in degraded mode? (not recommended)

  **Persist Status:** Write the results to `.github/.copilot-dev.tson` → `[mcp_status]`.
</mcp_health_check>

<discovery_protocol>
  1. **Source Code Audit:** Scan root and `src/`, `app/`, `packages/` for dependency files (e.g., `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`).
  2. **Documentation Scan:** Read `README.md` and any existing files in `docs/` to extract business logic and architectural intent.
  3. **Infrastructure Check:** Identify database engines, cloud providers, and CI/CD tools from files like `docker-compose.yml`, `Dockerfile`, `.github/workflows/`.
  4. **Runtime Detection:** 
     - Check for `uv.lock` → set `python_runner = "uv run"`, `package_manager = "uv"`
     - Else, check for `python3` presence → set `python_runner = "python3"`, `package_manager = "pip"`
</discovery_protocol>

<generation_rules>
  **Instructions vs Skills — choose the right primitive:**
  - **Instruction** (`.github/instructions/*.instructions.md`): Rules that apply ALWAYS when touching certain files. Use `applyTo` glob pattern.
  - **Skill** (`.github/skills/<name>/SKILL.md`): On-demand workflow loaded when the task matches the description.

  **Runtime Persistence (CRITICAL):**
  You MUST write the detected runtime configuration to `.github/.copilot-dev.tson`:
  ```toml
  [runtime]
  python_runner = "uv run"       # or "python3"
  package_manager = "uv"          # or "pip"
  script_prefix = "uv run"        # used by ALL agents for scripts
  ```

  **The "Ask First" Rule:** If the stack is not explicitly defined in files, stop and ask the user 3 specific questions.
</generation_rules>

<agent_roles_registry>
| Role | Primary Responsibility |
|------|------------------------|
| dispatcher | Orchestration, mode selection & subagent coordination |
| tech-lead | ADR creation & architectural scaffolding (read-only) |
| explorer | Read-only repository explorer (Q&A) |
| qa | Edge-case validation & test automation |
| appsec | Vulnerability auditing & data validation (read-only) |
| devops | Infrastructure, migrations & deployment cleanup |
| framework-admin | Framework self-maintenance |
</agent_roles_registry>

<output_standard>
For every file identified, you must output:
1. **Type:** Instruction or Skill
2. **Target Path:**
   - Instructions: `.github/instructions/<name>.instructions.md`
   - Skills: `.github/skills/<name>/SKILL.md`
3. **File Content:** High-density Markdown — concise and actionable.
</output_standard>

# EXECUTION STEPS
1. **Verify MCP Health** following the `<mcp_health_check>`.
2. **Analyze** the repository following the `<discovery_protocol>`.
3. **Detect & Persist Runtime** in `.github/.copilot-dev.tson`.
4. **Identify** the core stack and suggest stack-specific coder agents.
5. **Generate** foundational instructions and skills using `<generation_rules>`.
6. **Final Command:** Instruct the user to run `bash .github/hooks/scripts/sync_agents.sh`.