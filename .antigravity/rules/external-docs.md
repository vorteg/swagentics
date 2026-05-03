---
description: External Documentation & Context Gathering (context7)
---

# RULE: External Knowledge Retrieval

<context_protocol>
  **MCP Execution:** Antigravity MUST use the `context7` MCP server to lookup framework or library documentation to prevent hallucinations.

  1. **When to lookup:** If a library, API, or framework method is unknown or potentially deprecated, DO NOT guess the syntax.
  2. **Resolution:** First, use the `mcp_context7_resolve-library-id` tool to find the exact library ID.
  3. **Query:** Use the `mcp_context7_query-docs` tool with the library ID to get the precise, up-to-date documentation.
  4. **State Update:** Apply the newly acquired knowledge to the codebase and document the structural decision in the `active_state.tson`.
</context_protocol>
