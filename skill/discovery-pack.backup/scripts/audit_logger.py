#!/usr/bin/env python3
"""Add audit metadata to discovery artifacts"""
import sys, yaml, re
from pathlib import Path
from datetime import datetime

def add_metadata(file_path, model_name="claude-sonnet-4.5", duration=None):
    content = file_path.read_text()
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        print(f"⚠️  No frontmatter in {file_path.name}")
        return
    
    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2)
    
    # Add or update metadata
    if 'metadata' not in frontmatter:
        frontmatter['metadata'] = {}
    
    frontmatter['metadata'].update({
        'generated_at': datetime.now().isoformat() + 'Z',
        'generated_by': model_name,
        'discovery_pack_version': '1.0.0',
        'validated': False
    })
    
    if duration:
        frontmatter['metadata']['duration_seconds'] = duration
    
    # Write back
    with file_path.open('w') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
        f.write('---\n')
        f.write(body)
    
    print(f"✅ Added metadata to {file_path.name}")

if __name__ == "__main__":
    target = Path(sys.argv[1])
    model = sys.argv[2] if len(sys.argv) > 2 else "claude-sonnet-4.5"
    
    if target.is_dir():
        for md_file in target.glob("*.md"):
            add_metadata(md_file, model)
    else:
        add_metadata(target, model)
