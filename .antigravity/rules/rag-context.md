---
description: Semantic Vector Search & Context via Pinecone
---

# RULE: Codebase Retrieval-Augmented Generation (RAG)

<pinecone_protocol>
  **MCP Execution:** When navigating large codebases where the deterministic local map (`Atlas`) is insufficient or lacks deep context, Antigravity MUST leverage the `pinecone-mcp-server` to perform semantic searches over the indexed repository.

  1. **When to use:** Use this when asked broad architectural questions, when searching for implementations of specific patterns across the entire codebase, or if a required file is missing from the local `active_state.tson`.
  2. **Querying:** Use the `mcp_pinecone-mcp-server_search-records` tool to search for context. You can use the Pinecone assistant or developer server depending on the setup.
  3. **Context Injection:** Synthesize the results obtained from Pinecone and inject the findings into the current workflow execution to prevent hallucinations.
</pinecone_protocol>
