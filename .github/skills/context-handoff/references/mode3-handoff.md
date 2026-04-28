# Mode 3 — Cross-Session / Worktree Handoff

When agents work in separate sessions (e.g., parallel worktrees), they CANNOT use subagents across sessions. Use the state-file approach.

## Decision Tree

```
Does the next agent run in the SAME session?
│
├── YES → Use subagent invocation (Mode 1). Each subagent has isolated context.
│
└── NO  → Use active_state.tson as carrier.
          Write all decisions and context the next agent needs.
          Commit the state file to the worktree branch.
          The user opens a new session and invokes the next agent.
```

## State File Persistence

In Mode 3, `active_state.tson` **MUST be committed** to the worktree branch. This is the only mechanism for cross-session communication — agents in different chat sessions cannot share memory.

```
git add .github/memory/active_state.tson
git commit -m "chore: update active_state for @[next-agent]"
```

## Mandatory Handoff Block (Mode 3 only)

Every agent MUST end its final response with this block when operating in Mode 3:

```
---
## HANDOFF

**Next Agent:** @[role]
**State file updated:** `.github/memory/active_state.tson`
  - current_agent: "[role]"
  - status: "[pending|in_progress]"
  - next task: "[brief description]"

**Action for user:** Commit the state file, open a new chat session, and invoke @[role].
---
```

## Regenerating Runtime Commands

If slash commands change after a VS Code / Copilot Chat update, regenerate:

```bash
uv run .github/hooks/scripts/generate_copilot_runtime.py
```
