import json

def to_tson(data, prefix=""):
    """
    Serializes a dictionary to TOML format (TSON).
    This creates token-efficient text representation.
    """
    lines = []
    # Write primitives
    for k, v in data.items():
        if not isinstance(v, (dict, list)):
            if isinstance(v, bool):
                v_str = "true" if v else "false"
            elif isinstance(v, str):
                v_str = json.dumps(v)
            elif v is None:
                v_str = '""'
            else:
                v_str = str(v)
            lines.append(f'{k} = {v_str}')
    
    # Write lists of primitives
    for k, v in data.items():
        if isinstance(v, list) and (not v or not isinstance(v[0], dict)):
            lines.append(f"{k} = {json.dumps(v)}")
            
    # Write dictionaries
    for k, v in data.items():
        if isinstance(v, dict):
            new_prefix = f"{prefix}.{k}" if prefix else k
            lines.append(f"\n[{new_prefix}]")
            child_lines = to_tson(v, new_prefix)
            if child_lines.strip():
                lines.extend(child_lines.split('\n'))
            
    # Write lists of dicts
    for k, v in data.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            for item in v:
                new_prefix = f"{prefix}.{k}" if prefix else k
                lines.append(f"\n[[{new_prefix}]]")
                child_lines = to_tson(item, new_prefix)
                if child_lines.strip():
                    lines.extend(child_lines.split('\n'))
                
    return "\n".join(lines).strip() + "\n"
