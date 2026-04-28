import os
from pathlib import Path
from datetime import datetime, timezone

def generate_atlas(root_dir: str = "."):
    """
    Generates a high-level directory map (Atlas) of the project.
    Only maps directories up to depth 3 to avoid context bloat.
    """
    print("🗺️  Generating project Atlas...")
    
    ignore_dirs = {
        "node_modules", ".git", ".venv", "venv",
        "__pycache__", ".mypy_cache", ".ruff_cache",
        ".pytest_cache", ".tox", "htmlcov",
        "dist", "build", ".output", ".next", ".nuxt",
        "coverage", ".coverage", ".eggs",
        ".idea", ".vscode"
    }

    atlas_data = {
        "_meta": {
            "description": "Project Atlas. Shows the high-level directory structure. For specific files, use your role's indexes or the discovery script.",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "max_depth": 3
        },
        "directories": []
    }

    root_path = Path(root_dir).resolve()
    
    for root, dirs, files in os.walk(root_path):
        # Exclude ignored directories in place
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        rel_path = Path(root).relative_to(root_path)
        
        if rel_path.as_posix() == ".":
            depth = 0
        else:
            depth = len(rel_path.parts)
            
        if depth > 3:
            # Stop walking deeper than depth 3
            dirs[:] = []
            continue
            
        if depth > 0:
            atlas_data["directories"].append(rel_path.as_posix())

    # Sort directories alphabetically
    atlas_data["directories"].sort()

    output_path = Path(".github/agents/assets/atlas.tson")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    from tson_utils import to_tson
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(to_tson(atlas_data))

    print(f"✅ Atlas generated successfully at: {output_path}")

if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).parent))
    generate_atlas()
