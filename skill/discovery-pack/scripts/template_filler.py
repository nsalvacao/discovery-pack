#!/usr/bin/env python3
"""
Discovery Pack Template Filler
Forces correct structure by not allowing manual markdown creation.

Usage:
    python template_filler.py 00_problem-frame.md output.md --interactive
    python template_filler.py 06_decision-log.md output.md --batch
"""

import sys
import yaml
import json
from pathlib import Path
from datetime import datetime
import argparse

SKILL_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = SKILL_DIR / "templates"
SCHEMA_DIR = SKILL_DIR / "schemas"

TEMPLATE_SCHEMAS = {
    "00_problem-frame.md": "problem-frame.schema.json",
    "01_constraints-nfr.md": "constraints-nfr.schema.json",
    "02_domain-model.md": "domain-model.schema.json",
    "03_option-space.md": "option-space.schema.json",
    "04_assumptions-unknowns.md": "assumptions-unknowns.schema.json",
    "05_validation-plan.md": "validation-plan.schema.json",
    "06_decision-log.md": "decision-log.schema.json",
    "07_speckit-handoff.md": "speckit-handoff.schema.json",
}


def load_template(template_name: str) -> tuple[dict, str]:
    """Load template and extract frontmatter structure."""
    template_path = TEMPLATE_DIR / template_name
    
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        sys.exit(1)
    
    content = template_path.read_text(encoding="utf-8")
    
    # Split frontmatter and body
    parts = content.split("---\n", 2)
    if len(parts) < 3:
        print(f"❌ Invalid template format (no frontmatter): {template_name}")
        sys.exit(1)
    
    frontmatter_text = parts[1]
    body_template = parts[2]
    
    frontmatter = yaml.safe_load(frontmatter_text)
    
    return frontmatter, body_template


def fill_frontmatter(template_fm: dict, project_name: str) -> dict:
    """Fill frontmatter with actual values."""
    filled = template_fm.copy()
    
    # Replace placeholders
    if "project" in filled:
        filled["project"] = project_name
    
    if "date" in filled:
        filled["date"] = datetime.now().strftime("%Y-%m-%d")
    
    if "metadata" in filled:
        filled["metadata"]["generated_at"] = datetime.now().isoformat()
        filled["metadata"]["generated_by"] = "Claude (via template_filler.py)"
    
    return filled


def validate_schema(frontmatter: dict, template_name: str) -> bool:
    """Validate frontmatter against JSON schema."""
    try:
        import jsonschema
    except ImportError:
        print("⚠️  jsonschema not installed, skipping validation")
        return True
    
    schema_name = TEMPLATE_SCHEMAS.get(template_name)
    if not schema_name:
        print(f"⚠️  No schema defined for {template_name}")
        return True
    
    schema_path = SCHEMA_DIR / schema_name
    if not schema_path.exists():
        print(f"⚠️  Schema not found: {schema_path}")
        return True
    
    schema = json.loads(schema_path.read_text())
    
    try:
        jsonschema.validate(frontmatter, schema)
        print(f"✅ Schema validation passed")
        return True
    except jsonschema.ValidationError as e:
        print(f"❌ Schema validation failed:")
        print(f"   {e.message}")
        return False


def write_artifact(output_path: Path, frontmatter: dict, body: str):
    """Write artifact with frontmatter and body."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n{body}"
    
    output_path.write_text(content, encoding="utf-8")
    print(f"✅ Written: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Discovery Pack Template Filler")
    parser.add_argument("template", help="Template name (e.g., 00_problem-frame.md)")
    parser.add_argument("output", help="Output file path")
    parser.add_argument("--project", default="Project Name", help="Project name")
    parser.add_argument("--body", help="Body content (if not provided, uses template placeholder)")
    parser.add_argument("--validate", action="store_true", help="Validate schema before writing")
    
    args = parser.parse_args()
    
    print(f"📝 Filling template: {args.template}")
    print(f"   Output: {args.output}")
    print()
    
    # Load template
    frontmatter_template, body_template = load_template(args.template)
    
    # Fill frontmatter
    frontmatter = fill_frontmatter(frontmatter_template, args.project)
    
    # Use provided body or template
    body = args.body if args.body else body_template
    
    # Validate if requested
    if args.validate:
        if not validate_schema(frontmatter, args.template):
            print("❌ Validation failed. Fix errors and try again.")
            sys.exit(1)
    
    # Write artifact
    output_path = Path(args.output)
    write_artifact(output_path, frontmatter, body)
    
    print()
    print("✅ Artifact generated successfully!")
    print()
    print("Next steps:")
    print("  1. Edit content in generated file")
    print("  2. Apply epistemic tags [FACT|ASSUMPTION|HYPOTHESIS|CONSTRAINT]")
    print(f"  3. Validate: python3 {SKILL_DIR}/scripts/validate.py {output_path.parent}")


if __name__ == "__main__":
    main()
