# MCP Requirements

Swagentics relies on the **Model Context Protocol (MCP)** to ensure high-fidelity orchestration and to mitigate LLM hallucinations.

## Required MCP Servers

### 1. Context7 (Documentation Lookup)
Provides up-to-date documentation for any programming library or framework. 
- **Why:** Prevents agents from using deprecated APIs or hallucinating syntax.
- **Setup:**
  ```json
  "context7": {
    "command": "npx",
    "args": ["-y", "@context7/mcp-server"],
    "env": { "CONTEXT7_API_KEY": "your_key" }
  }
  ```
  Get a key at [context7.com](https://context7.com).

### 2. SearXNG (Web Search)
General-purpose web search for news, security vulnerabilities (CVEs), and community discussions.
- **Why:** Allows agents to research real-world issues outside their training data.
- **Setup:**
  ```json
  "searxng": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-searxng"],
    "env": { "SEARXNG_URL": "https://your-searxng-instance" }
  }
  ```

## Recommended MCP Servers

### 3. Filesystem
Precise file manipulation tools.
- **Setup:** 
  ```json
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
  }
  ```

### 4. GitHub
Integration with PRs, issues, and repository metadata.
- **Setup:** 
  ```json
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token" }
  }
  ```
