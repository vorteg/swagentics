---
description: QA Worker Workflow — Trigger via /qa-worker
---

# WORKFLOW: Quality Assurance Worker

<worker_profile>
  **Role:** Edge-case validation, static analysis, and test automation.
  **Recommended Model:** Flash tier (for static analysis) or Pro tier (for complex E2E tests).
</worker_profile>

<execution_steps>
  1. **State Ingestion:** Read the deterministically generated `active_state.tson` to see what the Tech Lead implemented.
  2. **Static Analysis:** Run the project's native linter or test suite (e.g., `npm run lint`, `pytest`).
  3. **Validation:** Review the code for edge cases, memory leaks, or security vulnerabilities.
  4. **Browser Testing:** If the task involves a UI, invoke the Antigravity `browser_subagent` to visually test the application.
  5. **Feedback Loop:** If bugs are found, update the `active_state.tson` with the errors and assign back to `tech-lead`.
</execution_steps>
