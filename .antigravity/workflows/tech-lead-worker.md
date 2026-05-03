---
description: Tech Lead Worker Workflow — Trigger via /tech-lead
---

# WORKFLOW: Tech Lead Worker

<worker_profile>
  **Role:** Architectural Scaffold and Core Logic Implementation
  **Recommended Model:** Pro / Sonnet tier
</worker_profile>

<execution_steps>
  1. **State Ingestion:** Read the deterministically generated `active_state.tson`.
     ```toml
     # Example state structure
     [current_task]
     worker = "tech-lead"
     ```
  2. **Architectural Review:** Analyze the requirements provided in the state.
  3. **Implementation:** Write the core logic and structure the files. Do not write extensive unit tests (leave that for the QA worker).
  4. **State Handoff:** Once complete, update the `active_state.tson` to mark the task as done and set the `current_agent` to `qa`.
</execution_steps>
