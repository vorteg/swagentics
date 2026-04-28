import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Global exclusions applied to ALL roles — tooling caches and build artifacts
# that never contain meaningful source code for any agent.
GLOBAL_IGNORE_DIRS = {
    "node_modules", ".git", ".venv", "venv",
    "__pycache__", ".mypy_cache", ".ruff_cache",
    ".pytest_cache", ".tox", "htmlcov",
    "dist", "build", ".output", ".next", ".nuxt",
    "coverage", ".coverage", ".eggs",
    ".idea", ".vscode",
}

# 1. Role Configuration (Agnostic Brain)
ROLE_CONFIGS = {
    "dispatcher": {
        "extensions": {".md", ".tson", ".yml", ".yaml"},
        "ignore_dirs": GLOBAL_IGNORE_DIRS,
        "categories": {
            "memory_and_state": [".github/memory", "active_state"],
            "agent_definitions": [".github/agents", ".agent.md"],
            "manifest": [".copilot-dev.tson", "framework-version"]
        }
    },
    "tech-lead": {
        "extensions": {".py", ".md", ".tson", ".js", ".ts", ".go", ".rs", ".java"},
        "ignore_dirs": GLOBAL_IGNORE_DIRS,
        "categories": {
            "architecture_decisions": ["docs/adrs", "architecture", "design"],
            "core_contracts": ["core", "domain", "interfaces", "types", "schemas", "models", "proto"],
            "tests_structure": ["tests"]
        }
    },
    "explorer": {
        "extensions": {".py", ".md", ".tson", ".js", ".ts", ".go", ".rs", ".java", ".sh", ".yml", ".yaml", ".sql", ".html", ".css"},
        "ignore_dirs": GLOBAL_IGNORE_DIRS,
        "categories": {
            "documentation": ["docs", "README", "CHANGELOG", "LICENSE"],
            "source_code": ["src", "app", "lib", "pkg", "core"],
            "infrastructure_and_config": ["config", "deploy", "docker", "scripts", "env"]
        }
    },
    "appsec": {
        "extensions": {".py", ".js", ".ts", ".go", ".rs", ".md", ".toml", ".yaml", ".yml", ".lock"},
        "ignore_dirs": GLOBAL_IGNORE_DIRS,
        "categories": {
            "data_validation": ["schemas", "models", "dto", "validation"],
            "security_and_auth": ["auth", "security", "middlewares", "rbac", "permissions", "encryption"],
            "dependencies": ["pyproject.toml", "package.json", "go.mod", "Cargo.toml", "uv.lock", "package-lock.json", "requirements.txt"]
        }
    },
    "devops": {
        "extensions": {".py", ".yml", ".yaml", ".toml", ".sh", ".ini", "Dockerfile", "Makefile"},
        "ignore_dirs": GLOBAL_IGNORE_DIRS | {"tests"},
        "categories": {
            "ci_cd_pipelines": [".github/workflows", "pipelines", "actions"],
            "infrastructure": ["docker", "deploy", "terraform", "k8s", "kubernetes", "helm", "Dockerfile", "docker-compose"],
            "database_migrations": ["migrations", "alembic", "prisma", "flyway", "liquibase"],
            "scripts_and_config": ["scripts", "Makefile", "pyproject.toml", "package.json"]
        }
    },
    "framework-admin": {
        "extensions": {".md", ".py", ".sh", ".tson"},
        "ignore_dirs": GLOBAL_IGNORE_DIRS,
        "categories": {
            "framework_scripts": [".github/hooks/scripts"],
            "framework_agents": [".github/agents"],
            "framework_manifest": [".copilot-dev.tson", "framework-version.tson"]
        }
    },
    "qa": {
        "extensions": {".py", ".js", ".ts", ".go", ".rs", ".tson", ".md"},
        "ignore_dirs": GLOBAL_IGNORE_DIRS,
        "categories": {
            "test_suites": ["tests", "spec", "__tests__"],
            "fixtures_and_mocks": ["fixtures", "mocks", "conftest"],
            "source_under_test": ["src", "app", "lib", "core"]
        }
    }
}

def get_repo_structure(target_dir: Path, config: dict) -> list:
    file_list = []
    
    for root, dirs, files in os.walk(target_dir):
        # Modify 'dirs' in-place to ignore junk folders
        dirs[:] = [d for d in dirs if d not in config["ignore_dirs"]]
        
        for file in files:
            path = Path(root) / file
            # Check extension or full filename (for Dockerfile/Makefile)
            if path.suffix in config["extensions"] or file in config["extensions"]:
                # Normalize path to use '/' (Unix/URL style)
                try:
                    clean_path = path.relative_to(target_dir).as_posix()
                    file_list.append({
                        "file": file,
                        "path": clean_path,
                        "extension": path.suffix
                    })
                except ValueError:
                    continue
    return file_list

def generate_index(role: str, target_dir: str):
    if role not in ROLE_CONFIGS:
        # If role is not in config, use a default minimal config (explorer style)
        print(f"⚠️  Role '{role}' not found in configuration. Using default minimal scan.")
        config = ROLE_CONFIGS["explorer"]
    else:
        config = ROLE_CONFIGS[role]
    
    print(f"🔍 Scanning repository for role: {role}...")
    raw_files = get_repo_structure(Path(target_dir), config)
    
    # Build the TSON structure
    index_data = {
        "_meta": {
            "role": role,
            "description": f"File index for {role}. Use these paths for navigation.",
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    }
    
    # Group by categories dynamically based on the role
    for cat_name, keywords in config["categories"].items():
        index_data[cat_name] = [
            f for f in raw_files 
            if any(kw in f["path"] for kw in keywords)
        ]
    
    # Ensure output directory exists
    output_path = Path(f".github/agents/assets/{role}_index.tson")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the file
    from tson_utils import to_tson
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(to_tson(index_data))
        
    print(f"✅ Index successfully generated at: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a repository index for Copilot agents")
    parser.add_argument("--role", required=True, help="Agent role (e.g., dispatcher, qa)")
    parser.add_argument("--dir", default=".", help="Directory to scan")
    
    args = parser.parse_args()
    generate_index(args.role, args.dir)