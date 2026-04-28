"""
generate_copilot_runtime.py
Reads the locally installed GitHub Copilot Chat extension and generates
.github/agents/assets/copilot_runtime.tson with the actual slash commands.

Run: uv run .github/hooks/scripts/generate_copilot_runtime.py
     uv run .github/hooks/scripts/generate_copilot_runtime.py
"""

import json
import platform
from pathlib import Path
from datetime import datetime, timezone


# ── Locate the extension ─────────────────────────────────────────────────────
def find_extension_path() -> Path | None:
    """Find the copilot-chat extension dir across OS and VS Code variants."""
    system = platform.system()

    if system == "Linux":
        base_dirs = [
            Path.home() / ".vscode" / "extensions",
            Path.home() / ".vscode-insiders" / "extensions",
        ]
    elif system == "Darwin":
        base_dirs = [
            Path.home() / ".vscode" / "extensions",
            Path.home() / ".vscode-insiders" / "extensions",
        ]
    elif system == "Windows":
        appdata = Path.home() / "AppData" / "Roaming"
        base_dirs = [
            appdata / "Code" / "User" / "extensions",
            appdata / "Code - Insiders" / "User" / "extensions",
        ]
    else:
        base_dirs = [Path.home() / ".vscode" / "extensions"]

    for base in base_dirs:
        matches = sorted(base.glob("github.copilot-chat-*"), reverse=True)
        if matches:
            return matches[0]  # newest version first

    return None


# ── Parse package.tson ────────────────────────────────────────────────────────
def extract_slash_commands(package_json: dict) -> dict:
    """
    Extract slash commands grouped by chat mode/participant from the extension.
    """
    participants = package_json.get("contributes", {}).get("chatParticipants", [])

    MODE_LABEL = {
        "ask": "ask_mode",
        "agent": "agent_mode",
        "edit": "edit_mode",
    }

    LOCATION_LABEL = {
        "panel": "panel",
        "editor": "inline_editor",
        "notebook": "notebook",
        "terminal": "terminal",
    }

    commands_by_mode: dict = {}

    for participant in participants:
        modes = participant.get("modes", [])
        locations = participant.get("locations", [])
        raw_commands = participant.get("commands", [])

        if not raw_commands:
            continue

        if modes:
            bucket = MODE_LABEL.get(modes[0], modes[0])
        elif locations:
            bucket = LOCATION_LABEL.get(locations[0], locations[0])
        else:
            bucket = "other"

        for cmd in raw_commands:
            name = cmd.get("name", "")
            description_raw = cmd.get("description", "")
            when = cmd.get("when", "")

            # Skip debug/internal commands
            if "debug" in when.lower():
                continue

            entry = {
                "command": f"/{name}",
                "description_key": description_raw,
                "available_when": when if when else "always",
            }
            commands_by_mode.setdefault(bucket, []).append(entry)

    return commands_by_mode


def resolve_nls(package_json: dict, ext_path: Path) -> dict:
    """Resolve %placeholder% strings from package.nls.tson."""
    nls_path = ext_path / "package.nls.json"
    if not nls_path.exists():
        return {}
    try:
        return json.loads(nls_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def replace_placeholders(commands_by_mode: dict, nls: dict) -> dict:
    """Replace %key% placeholders with real descriptions from NLS file."""
    resolved = {}
    for mode, cmds in commands_by_mode.items():
        resolved[mode] = []
        for cmd in cmds:
            desc_key = cmd.get("description_key", "")
            if desc_key.startswith("%") and desc_key.endswith("%"):
                lookup = desc_key.strip("%")
                desc = nls.get(lookup, desc_key)
            else:
                desc = desc_key
            resolved[mode].append({
                "command": cmd["command"],
                "description": desc,
                "available_when": cmd["available_when"],
            })
    return resolved




# ── Manually maintained sections (NOT auto-generated) ────────────────────────
# These sections are preserved across regenerations because their source of
# truth is NOT the extension package.tson — they require manual updates.
#
# execution_modes  → Workflow strategy definitions for @dispatcher
# available_models → GitHub Copilot models (check VS Code model picker dropdown)
#
# To update models: open Copilot Chat in VS Code → click model selector → update list below.
MANUAL_SECTIONS = {
    "execution_modes": {
        "_note": "Used by @dispatcher to recommend the optimal workflow strategy before acting.",
        "mode_1_subagent_pipeline": {
            "label": "Subagent Pipeline (Sequential or Parallel)",
            "context_strategy": "subagent isolation — each agent runs in its own encapsulated context",
            "git_isolation": False,
            "use_when": [
                "Tasks can be broken down into sub-tasks for different roles",
                "Subagents can run in PARALLEL if independent, or SEQUENTIAL if dependent",
                "No risk of branch dependency collision",
                "Bounded scope (single feature, single concern)",
            ],
            "agents_flow": "Sequential: @tech-lead → @coder | Parallel: @backend-coder AND @frontend-coder simultaneously",
            "best_model_profile": "balanced",
        },
        "mode_2_compact_session": {
            "label": "Compact Session",
            "context_strategy": "/compact within same session",
            "git_isolation": False,
            "use_when": [
                "Single agent handles the full task",
                "Highly iterative work (many rounds expected)",
                "Context continuity matters throughout",
                "No agent handoff needed",
            ],
            "agents_flow": "@[single_agent] → /compact as needed → delivers",
            "best_model_profile": "fast_iterative",
        },
        "mode_3_parallel_worktrees": {
            "label": "Parallel Worktrees",
            "context_strategy": "separate session per worktree, state persisted in active_state.tson (committed to branch)",
            "git_isolation": True,
            "use_when": [
                "Multiple independent features run simultaneously",
                "Risk of branch dependency collision",
                "Team parallelism required",
                "Clean branch isolation needed before PR",
            ],
            "agents_flow": "Worktree A: @tech-lead → @coder → @appsec (parallel with Worktree B)",
            "best_model_profile": "powerful_reasoning",
        },
    },
    "available_models": {
        "_note": "Manually maintained. Update when GitHub Copilot adds/removes models.",
        "_update_hint": "Check available models in VS Code: open Copilot Chat → click model selector dropdown.",
        "models": [
            {
                "id": "gpt-4o",
                "label": "GPT-4o",
                "profile": "balanced",
                "best_for": ["general coding", "sequential pipeline", "code review", "refactors"],
                "context_window": "128k",
                "speed": "fast",
            },
            {
                "id": "claude-3.7-sonnet",
                "label": "Claude 3.7 Sonnet",
                "profile": "powerful_reasoning",
                "best_for": ["complex architecture", "multi-file refactors", "security audits", "parallel worktrees", "long reasoning chains"],
                "context_window": "200k",
                "speed": "moderate",
            },
            {
                "id": "o3-mini",
                "label": "o3-mini",
                "profile": "analytical",
                "best_for": ["algorithmic problems", "debugging complex logic", "performance analysis"],
                "context_window": "128k",
                "speed": "moderate",
            },
            {
                "id": "gemini-2.0-flash",
                "label": "Gemini 2.0 Flash",
                "profile": "fast_iterative",
                "best_for": ["quick iterations", "compact sessions", "short tasks", "scaffolding", "boilerplate"],
                "context_window": "1M",
                "speed": "very_fast",
            },
        ],
    },
}


# ── Build the final TSON ──────────────────────────────────────────────────────
def build_runtime_tson(ext_path: Path, package_json: dict) -> dict:
    ext_version = package_json.get("version", "unknown")

    raw_commands = extract_slash_commands(package_json)
    nls = resolve_nls(package_json, ext_path)
    commands_by_mode = replace_placeholders(raw_commands, nls)

    return {
        "_meta": {
            "description": (
                "Dynamic registry of GitHub Copilot Chat runtime capabilities. "
                "AUTO-GENERATED from extension package.tson — do not edit manually."
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_extension": ext_path.name,
            "extension_version": ext_version,
            "update_command": "uv run .github/hooks/scripts/generate_copilot_runtime.py",
        },
        # Auto-detected from extension package.tson — always up-to-date
        "slash_commands_by_mode": commands_by_mode,
        # Manually maintained sections — preserved across regenerations.
        # Update MANUAL_SECTIONS dict above when workflows or models change.
        **MANUAL_SECTIONS,
        "context_strategies": {
            "compact": {
                "command": "/compact",
                "how": "Type /compact in the current chat session.",
                "effect": "Compresses chat history into a summary. Context is PRESERVED but condensed.",
                "use_when": [
                    "Mode 2: continuing with the SAME agent role in a long session.",
                    "The session history is too long but the agent still needs it.",
                    "Token limit pressure within a single agent session.",
                ],
                "available_in_modes": ["agent_mode"],
                "source": "Extension-defined (auto-detected from package.tson)",
            },
        },
    }


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("🔍 Locating GitHub Copilot Chat extension...")
    ext_path = find_extension_path()

    if not ext_path:
        print("❌ Could not find github.copilot-chat extension.")
        print("   Make sure VS Code is installed and the extension is enabled.")
        raise SystemExit(1)

    print(f"✅ Found: {ext_path.name}")

    pkg_path = ext_path / "package.json"
    package_json = json.loads(pkg_path.read_text(encoding="utf-8"))

    print("⚙️  Extracting slash commands from extension...")
    tson_data = build_runtime_tson(ext_path, package_json)

    output_path = Path(".github/agents/assets/copilot_runtime.tson")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    from tson_utils import to_tson
    output_path.write_text(to_tson(tson_data), encoding="utf-8")

    auto_cmds = sum(len(v) for v in tson_data["slash_commands_by_mode"].values())
    print(f"✅ Generated: {output_path}")
    print(f"   Auto-detected commands: {auto_cmds} (from extension v{tson_data['_meta']['extension_version']})")


if __name__ == "__main__":
    main()
