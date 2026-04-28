import os
import json
from pathlib import Path

# Path configuration
SKILLS_DIR = Path(".github/skills")
AGENTS_DIR = Path(".github/agents")
OUTPUT_DIR = Path(".github/agents/assets")

def parse_skill_frontmatter(file_path: Path) -> dict:
    """Extract the YAML frontmatter block from a native SKILL.md.
    
    The native format uses 'name' and 'description' for progressive discovery.
    'roles' and 'trigger' are no longer required — VS Code loads skills by
    description matching, not by frontmatter tags.
    
    If a skill still has 'roles' (legacy), it is respected for selective
    routing in agent TSON files.
    """
    skill_dir = file_path.parent.name
    metadata = {
        "name": skill_dir,
        "description": "",
        "path": file_path.parent.as_posix(),  # Points to the folder, not the file
        "roles": []  # Empty = all agents; legacy = selective routing
    }
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_block = parts[1].strip().split("\n")
                    for line in yaml_block:
                        if ":" in line:
                            key, val = line.split(":", 1)
                            key = key.strip()
                            val = val.strip()
                            
                            if key == "roles":
                                clean_val = val.strip("[]")
                                metadata["roles"] = [r.strip() for r in clean_val.split(",") if r.strip()]
                            elif key == "name":
                                metadata["name"] = val.strip("'\"")
                            elif key == "description":
                                metadata["description"] = val.strip("'\"")
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
        
    return metadata

def generate_skill_registries():
    print("🧠 Generating dynamic Skill indexes (Tag-based Routing)...")
    
    # 1. Discover which agents actually exist by reading the agents/ folder
    # Only take .agent.md files (e.g., dispatcher.agent.md → 'dispatcher')
    active_roles = []
    for f in AGENTS_DIR.glob("*.agent.md"):
        if f.is_file():
            # Strip '.agent.md' to get role name
            role_name = f.name.replace(".agent.md", "")
            active_roles.append(role_name)
    print(f"🕵️ Detected roles: {active_roles}")
    
    # Initialize an empty registry for each detected role
    registries = {role: [] for role in active_roles}
    
    # 2. Scan skills: find SKILL.md files, ignoring hidden directories
    all_skills = []
    if SKILLS_DIR.exists():
        for root, dirs, files in os.walk(SKILLS_DIR):
            # Filter out directories starting with a dot so walk doesn't enter them
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if "SKILL.md" in files:
                skill_file = Path(root) / "SKILL.md"
                all_skills.append(parse_skill_frontmatter(skill_file))
            
    # 3. Distribute skills to the corresponding agents
    for skill in all_skills:
        target_roles = skill.get("roles", [])
        
        # Copy the skill without the 'roles' key to keep the agent JSON clean
        clean_skill = {k: v for k, v in skill.items() if k != "roles"}
        
        if not target_roles or "all" in target_roles:
            # No roles defined or "all" → universal skill, goes to all agents
            for role in active_roles:
                registries[role].append(clean_skill)
        else:
            # Specific skill, distributed only to the agents that request it
            for role in target_roles:
                if role in registries:
                    registries[role].append(clean_skill)
                else:
                    print(f"⚠️ Warning: Skill '{skill['name']}' requests role '{role}', but that agent does not exist.")

    # 4. Save the TSON files
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    for role, skills in registries.items():
        # Even if an agent has no skills (e.g., the dispatcher), create an empty file
        registry_data = {
            "_meta": {
                "role": role,
                "description": f"Available Skills registry for {role}.",
                "instructions": "Use the skill 'description' to decide if it's relevant. Then read the SKILL.md from 'path'."
            },
            "available_skills": skills
        }
        
        output_file = OUTPUT_DIR / f"{role}_skills.tson"
        from tson_utils import to_tson
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(to_tson(registry_data))
            
        print(f"✅ Index generated: {output_file} ({len(skills)} skills routed)")

if __name__ == "__main__":
    generate_skill_registries()