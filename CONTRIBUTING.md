# Contributing to Swagentics

First off, thank you for considering contributing to Swagentics! It's people like you that make Swagentics such a great tool for the community.

## 🚀 How to Get Started

1. **Fork the repository** and clone it locally.
2. **Setup your environment**: Ensure you have VS Code 1.93+ and Copilot Chat 0.45+ installed.
3. **Initialize the framework**: Run `@dispatcher /copilot-init` in your project to see the framework in action.
4. **Explore the core**: Read `.github/copilot-instructions.md` to understand the orchestration rules.

## 🛠️ Contribution Guidelines

### Adding New Agents
If you want to contribute a new specialized agent:
1. Create a file named `your-agent.agent.md` in `.github/agents/`.
2. Follow the YAML frontmatter standard (refer to `explorer.agent.md`).
3. Ensure the agent is technology-agnostic or clearly marked as a specialized extension.

### Adding Skills
1. Create a folder in `.github/skills/your-skill-name/`.
2. Add a `SKILL.md` with appropriate triggers and descriptions.
3. Run `bash .github/hooks/scripts/sync_agents.sh` to update the indices.

### Code Style
- **Language**: All documentation, comments, and strings must be in **English**.
- **Python**: Use Python 3.10+ standards. Favor `pathlib` over `os.path`.
- **Determinism**: Avoid hardcoding paths or environment-specific assumptions. Use the discovery engine.

## 🤝 Pull Request Process

1. Create a new branch for your feature or bugfix.
2. Ensure all TSON files are regenerated using `sync_agents.sh`.
3. Update the `CHANGELOG.md` with your changes.
4. Submit the PR with a clear description of the problem it solves.

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---
*Thank you for helping us build the future of agentic orchestration!*
