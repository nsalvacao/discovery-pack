#!/usr/bin/env python3
"""
Extract Assumptions from Discovery Artifacts
Scans 00-03 for [FACT/ASSUMPTION/HYPOTHESIS/CONSTRAINT] tags and generates 04_assumptions-unknowns.md

Usage:
    python extract_assumptions.py /docs/discovery/2026-01-06-topic/
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import yaml


TAG_PATTERN = re.compile(r'\[(FACT|ASSUMPTION|HYPOTHESIS|CONSTRAINT)\]\s*(.+?)(?=\[(?:FACT|ASSUMPTION|HYPOTHESIS|CONSTRAINT)\]|$)', re.DOTALL)


def extract_tags_from_file(file_path: Path) -> List[Dict]:
    """Extract all tagged statements from a markdown file."""
    content = file_path.read_text(encoding='utf-8')

    # Skip frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    matches = TAG_PATTERN.findall(content)

    results = []
    for tag, statement in matches:
        statement = statement.strip()
        if statement:
            results.append({
                'tag': tag,
                'statement': statement,
                'source': file_path.name,
                'artifact': file_path.stem
            })

    return results


def prioritize_assumption(assumption: Dict) -> str:
    """Determine priority based on tag and context."""
    tag = assumption['tag']
    source = assumption['source']

    # CONSTRAINT is always critical
    if tag == 'CONSTRAINT':
        return 'critical'

    # Assumptions from option-space or decision-log are high priority
    if source.startswith('03_') or source.startswith('06_'):
        if tag == 'ASSUMPTION':
            return 'high'
        elif tag == 'HYPOTHESIS':
            return 'medium'

    # Default priorities
    if tag == 'ASSUMPTION':
        return 'medium'
    elif tag == 'HYPOTHESIS':
        return 'low'
    elif tag == 'FACT':
        return None  # Facts don't go into assumptions list

    return 'low'


def generate_frontmatter(assumptions: List[Dict], project_name: str) -> Dict:
    """Generate YAML frontmatter for 04_assumptions-unknowns.md"""
    filtered = [a for a in assumptions if a['tag'] in ['ASSUMPTION', 'HYPOTHESIS', 'CONSTRAINT']]

    frontmatter = {
        '$schema': '../schemas/assumptions-unknowns.schema.json',
        'project': project_name,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'metadata': {
            'generated_at': datetime.now().isoformat() + 'Z',
            'generated_by': 'extract_assumptions.py',
            'discovery_pack_version': '1.0.0',
            'validated': False
        },
        'assumptions': []
    }

    for idx, assumption in enumerate(filtered, 1):
        priority = prioritize_assumption(assumption)
        if priority is None:
            continue

        entry = {
            'id': f'A{idx:03d}',
            'assumption': assumption['statement'][:200] + ('...' if len(assumption['statement']) > 200 else ''),
            'tag': assumption['tag'],
            'priority': priority,
            'falsification_test': '[TODO: What would prove this wrong?]',
            'impact_if_wrong': '[TODO: Impact on decision if invalidated]',
            'source_artifact': assumption['source']
        }

        frontmatter['assumptions'].append(entry)

    return frontmatter


def generate_markdown_body(assumptions: List[Dict]) -> str:
    """Generate markdown body for 04_assumptions-unknowns.md"""
    body = """
# Assumptions & Unknowns

**Purpose:** Explicitly capture what we assume to be true but haven't verified, and what we don't know that could affect decisions.

---

## Critical Assumptions

**Auto-generated from discovery artifacts. Review and complete TODO fields.**

"""

    filtered = [a for a in assumptions if a['tag'] in ['ASSUMPTION', 'HYPOTHESIS', 'CONSTRAINT']]

    for idx, assumption in enumerate(filtered, 1):
        priority = prioritize_assumption(assumption)
        if priority is None:
            continue

        priority_icon = {'critical': '🔴', 'high': '🟡', 'medium': '🟠', 'low': '🟢'}.get(priority, '⚪')

        body += f"""
### Assumption {idx}: {priority_icon} {priority.upper()}

**Tag:** `[{assumption['tag']}]`
**Source:** {assumption['source']}

**Assumption:**
{assumption['statement'][:500]}

**What would prove this wrong:**
[TODO: Complete falsification test]

**Impact if wrong:**
[TODO: Complete impact analysis]

**Validation method:**
[TODO: Link to experiment in 05_validation-plan.md]

---
"""

    return body


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_assumptions.py <discovery-directory>")
        sys.exit(1)

    discovery_dir = Path(sys.argv[1])

    if not discovery_dir.is_dir():
        print(f"❌ Not a directory: {discovery_dir}")
        sys.exit(1)

    # Extract from artifacts 00-03
    all_assumptions = []
    for i in range(4):
        pattern = f"{i:02d}_*.md"
        files = list(discovery_dir.glob(pattern))

        for file in files:
            print(f"🔍 Scanning {file.name}...")
            tags = extract_tags_from_file(file)
            all_assumptions.extend(tags)

    if not all_assumptions:
        print("⚠️  No tagged statements found")
        sys.exit(0)

    print(f"\n📊 Found {len(all_assumptions)} tagged statements")

    # Extract project name from directory
    project_name = discovery_dir.name.split('-', 3)[-1] if '-' in discovery_dir.name else discovery_dir.name

    # Generate frontmatter
    frontmatter = generate_frontmatter(all_assumptions, project_name)

    # Generate markdown body
    body = generate_markdown_body(all_assumptions)

    # Write output
    output_file = discovery_dir / "04_assumptions-unknowns.md"

    with output_file.open('w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        f.write('---\n')
        f.write(body)

    print(f"\n✅ Generated: {output_file}")
    print(f"   {len(frontmatter['assumptions'])} assumptions extracted")


if __name__ == "__main__":
    main()
