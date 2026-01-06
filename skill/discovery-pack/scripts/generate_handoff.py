#!/usr/bin/env python3
"""Generate 07_speckit-handoff.md from discovery artifacts"""
import sys, yaml, re
from pathlib import Path
from datetime import datetime

def extract_frontmatter(file_path):
    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}

def generate_handoff(discovery_dir):
    artifacts = {}
    for i in range(8):
        pattern = f"{i:02d}_*.md"
        files = list(discovery_dir.glob(pattern))
        if files:
            artifacts[i] = extract_frontmatter(files[0])
    
    project = artifacts.get(0, {}).get('project', discovery_dir.name)
    
    # Generate frontmatter
    frontmatter = {
        '$schema': '../schemas/speckit-handoff.schema.json',
        'project': project,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'discovery_status': 'complete',
        'metadata': {
            'generated_at': datetime.now().isoformat() + 'Z',
            'generated_by': 'generate_handoff.py',
            'discovery_pack_version': '1.0.0'
        },
        'constitution_input': {
            'principles': [],
            'constraints': {},
            'glossary': []
        },
        'specify_input': {
            'users': artifacts.get(0, {}).get('users', {}).get('primary', []),
            'journeys': [],
            'requirements': [],
            'success_metrics': artifacts.get(0, {}).get('success_metrics', {})
        },
        'ready_for_speckit': True
    }
    
    # Extract from 02_domain-model
    if 2 in artifacts:
        frontmatter['constitution_input']['glossary'] = artifacts[2].get('glossary', [])
    
    # Extract from 06_decision-log
    if 6 in artifacts:
        frontmatter['constitution_input']['architectural_decisions'] = [
            d.get('decision', '') for d in artifacts[6].get('decisions', [])
        ]
    
    body = f"""
# Spec-Kit Handoff

**Project:** {project}
**Discovery Status:** ✅ Complete

Ready-to-copy inputs for spec-kit commands.

## 📋 Constitution Input

Copy this to `/speckit.constitution`:

### Principles
{yaml.dump(frontmatter['constitution_input'].get('principles', []))}

### Glossary
{yaml.dump(frontmatter['constitution_input'].get('glossary', []))}

## 📝 Specify Input

Copy this to `/speckit.specify`:

### Users
{yaml.dump(frontmatter['specify_input'].get('users', []))}

### Success Metrics
{yaml.dump(frontmatter['specify_input'].get('success_metrics', {}))}

---

**Next:** Run `/speckit.constitution` and `/speckit.specify`
"""
    
    output = discovery_dir / "07_speckit-handoff.md"
    with output.open('w') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
        f.write('---\n')
        f.write(body)
    
    print(f"✅ Generated: {output}")

if __name__ == "__main__":
    generate_handoff(Path(sys.argv[1]))
