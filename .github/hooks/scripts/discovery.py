import json
import argparse
import sys
import tomllib
from pathlib import Path

def search_in_tson(file_path, query, search_type):
    if not file_path.exists():
        return []
    
    try:
        with open(file_path, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        return []

    results = []
    
    if search_type in ["file", "skill"]:
        # Search across all arrays of objects (thematic categories)
        for key, items in data.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        target = item.get("path") or item.get("name") or item.get("description") or ""
                        if query.lower() in target.lower():
                            results.append(item)
                    elif isinstance(item, str):
                        if query.lower() in item.lower():
                            results.append(item)
    elif search_type == "command":
        for mode, config in data.get("execution_modes", {}).items():
            if query.lower() in mode.lower() or query.lower() in config.get("label", "").lower():
                results.append({mode: config})
        for mode, commands in data.get("slash_commands_by_mode", {}).items():
            for cmd in commands:
                if query.lower() in cmd.get("command", "").lower() or query.lower() in cmd.get("description", "").lower():
                    results.append(cmd)
                
    return results[:10]  # Cap results to keep context clean

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Discovery Service")
    parser.add_argument("--query", required=True, help="Search term")
    parser.add_argument("--type", choices=["file", "skill", "command"], default="file")
    parser.add_argument("--role", help="Specific agent role to search for")
    args = parser.parse_args()

    assets_dir = Path(".github/agents/assets")
    all_results = []

    if args.type == "file":
        pattern = f"{args.role}_index.tson" if args.role else "*_index.tson"
        for f in assets_dir.glob(pattern):
            all_results.extend(search_in_tson(f, args.query, "file"))
            
    elif args.type == "skill":
        pattern = f"{args.role}_skills.tson" if args.role else "*_skills.tson"
        for f in assets_dir.glob(pattern):
            all_results.extend(search_in_tson(f, args.query, "skill"))

    elif args.type == "command":
        f = assets_dir / "copilot_runtime.tson"
        all_results.extend(search_in_tson(f, args.query, "command"))

    # Remove duplicates
    unique_results = []
    seen = set()
    for r in all_results:
        r_str = json.dumps(r, sort_keys=True)
        if r_str not in seen:
            unique_results.append(r)
            seen.add(r_str)

    print(json.dumps(unique_results[:15], indent=2))

if __name__ == "__main__":
    main()
