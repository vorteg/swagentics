#!/usr/bin/env python3
import sys
import os
import shutil
from datetime import datetime

# Try to use the native TOML parser (Python 3.11+) to read TSON
try:
    import tomllib
except ImportError:
    tomllib = None

# Define paths relative to the project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))

STATE_FILE = os.path.join(ROOT_DIR, ".github", "memory", "active_state.tson")
TEMPLATE_FILE = os.path.join(ROOT_DIR, ".github", "memory", "templates", "active_state.template.tson")
LOG_FILE = os.path.join(ROOT_DIR, ".github", "memory", "activity_log.md")

def parse_fallback(content):
    """Fallback parser for Python versions without tomllib."""
    import re
    data = {"agent": "Unknown", "status": "Unknown", "files": []}
    agent_match = re.search(r'current_agent\s*=\s*"([^"]+)"', content)
    if agent_match: data["agent"] = agent_match.group(1)
    
    status_match = re.search(r'status\s*=\s*"([^"]+)"', content)
    if status_match: data["status"] = status_match.group(1)
    return data

def main():
    print("💾 Starting memory commit (Commit Memory)...")
    
    if not os.path.exists(STATE_FILE):
        print(f"⚠️  No active state found at {STATE_FILE}. Skipping.")
        return

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse values
        agent = "Unknown"
        status = "Unknown"
        files = []
        
        if tomllib:
            try:
                data = tomllib.loads(content)
                agent = data.get("execution", {}).get("current_agent", "Unknown")
                status = data.get("execution", {}).get("status", "Unknown")
                files = data.get("context", {}).get("recent_files_modified", [])
            except Exception as e:
                print(f"⚠️ Error parsing TSON/TOML: {e}. Using fallback.")
                fallback_data = parse_fallback(content)
                agent = fallback_data["agent"]
                status = fallback_data["status"]
        else:
            fallback_data = parse_fallback(content)
            agent = fallback_data["agent"]
            status = fallback_data["status"]
            
        # Format the timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create the log entry
        log_entry = f"\n### 📝 Trace: {timestamp}\n"
        log_entry += f"- **Agent:** `{agent}`\n"
        log_entry += f"- **Status:** `{status}`\n"
        if files and len(files) > 0:
            files_str = ", ".join([f"`{file}`" for file in files])
            log_entry += f"- **Files modified:** {files_str}\n"
        else:
            log_entry += f"- **Files modified:** None recorded.\n"
            
        # Write to the activity log
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
            print(f"✅ Memory committed successfully to {os.path.basename(LOG_FILE)}")
        else:
            print(f"⚠️ {LOG_FILE} not found, log was not saved.")
            
        # Reset the state from the template
        if os.path.exists(TEMPLATE_FILE):
            shutil.copy2(TEMPLATE_FILE, STATE_FILE)
            print("🔄 active_state.tson reset from template.")
        else:
            print(f"⚠️ Template not found at {TEMPLATE_FILE}. State was not reset.")
            
    except Exception as e:
        print(f"❌ Critical error in commit_memory.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
