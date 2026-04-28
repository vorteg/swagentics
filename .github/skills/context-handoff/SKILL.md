---
name: context-handoff
description: 'Context handoff protocol for inter-agent transitions. Use when: switching agents, pipeline handoff, subagent orchestration, cross-session state, worktree handoff, Mode 1/2/3 transitions.'
---

# Context Handoff Protocol (Hybrid v2)

This protocol supports TWO handoff mechanisms depending on the execution mode.

## Mode 1 — Subagent Pipeline (Preferred)

The `@dispatcher` invokes each agent as a **subagent** via `runSubagent`.

- Each subagent runs in its **own isolated context window** — fully encapsulated.
- No manual re-tagging. The dispatcher passes tasks automatically.
- State is optional. The coordinator carries the thread.

```
Dispatcher (coordinator context)
├─ invoke @tech-lead as subagent → receives summary
├─ invoke @backend-coder as subagent → receives summary
├─ invoke @appsec as subagent → receives summary
└─ invoke @devops as subagent → receives summary
```

**When invoked as a subagent:**
1. Skip the handoff block — the coordinator handles orchestration.
2. Execute the task and return a clear summary.
3. Do NOT update `active_state.tson` — the coordinator manages state.

## Mode 2 — Compact Session

Single agent, long task. Use `/compact` when context gets long.
No handoff needed — the agent owns the full session.

## Mode 3 — Cross-Session / Worktree Handoff

For details on cross-session handoffs with `active_state.tson`, see [Mode 3 reference](./references/mode3-handoff.md).
