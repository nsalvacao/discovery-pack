#!/usr/bin/env python3
"""
Discovery Pack Validator
Validates discovery artifacts against JSON schemas.

Usage:
    python validate.py /docs/discovery/2026-01-06-topic/
    python validate.py /docs/discovery/2026-01-06-topic/00_problem-frame.md
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
import re

try:
    import jsonschema
    from jsonschema import validate, ValidationError, RefResolver
except ImportError:
    print("❌ Error: jsonschema not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)


SCHEMA_DIR = Path(__file__).parent.parent / "schemas"
ARTIFACT_SCHEMAS = {
    "00_problem-frame.md": "problem-frame.schema.json",
    "01_constraints-nfr.md": "constraints-nfr.schema.json",
    "02_domain-model.md": "domain-model.schema.json",
    "03_option-space.md": "option-space.schema.json",
    "04_assumptions-unknowns.md": "assumptions-unknowns.schema.json",
    "05_validation-plan.md": "validation-plan.schema.json",
    "06_decision-log.md": "decision-log.schema.json",
    "07_speckit-handoff.md": "speckit-handoff.schema.json",
}


def extract_frontmatter(file_path: Path) -> Tuple[Dict, str]:
    """Extract YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding="utf-8")

    # Match YAML frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)

    if not match:
        return None, content

    frontmatter_text = match.group(1)
    body = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, body
    except yaml.YAMLError as e:
        print(f"❌ YAML parse error in {file_path.name}: {e}")
        return None, body


def load_schema(schema_name: str) -> Dict:
    """Load JSON schema and set up resolver for $ref."""
    schema_path = SCHEMA_DIR / schema_name

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    schema = json.loads(schema_path.read_text())

    # Create resolver for $ref to common.schema.json
    resolver = RefResolver(
        base_uri=f"file://{SCHEMA_DIR}/",
        referrer=schema
    )

    return schema, resolver


def validate_artifact(file_path: Path, verbose: bool = False) -> bool:
    """Validate single artifact file."""
    filename = file_path.name

    if filename not in ARTIFACT_SCHEMAS:
        if verbose:
            print(f"⏭️  {filename}: No schema defined (skipping)")
        return True

    schema_name = ARTIFACT_SCHEMAS[filename]

    # Extract frontmatter
    frontmatter, body = extract_frontmatter(file_path)

    if frontmatter is None:
        print(f"⚠️  {filename}: No YAML frontmatter found")
        return False

    # Load schema
    try:
        schema, resolver = load_schema(schema_name)
    except Exception as e:
        print(f"❌ {filename}: Failed to load schema: {e}")
        return False

    # Validate
    try:
        jsonschema.validate(
            instance=frontmatter,
            schema=schema,
            resolver=resolver
        )
        print(f"✅ {filename}: Valid")
        return True

    except ValidationError as e:
        print(f"❌ {filename}: Validation failed")
        print(f"   Error: {e.message}")
        print(f"   Path: {' > '.join(str(p) for p in e.path)}")

        if verbose and e.context:
            print(f"   Context:")
            for suberror in e.context:
                print(f"     - {suberror.message}")

        return False


def validate_directory(dir_path: Path, verbose: bool = False) -> Tuple[int, int]:
    """Validate all artifacts in directory."""
    if not dir_path.is_dir():
        print(f"❌ Not a directory: {dir_path}")
        return 0, 0

    artifacts = sorted(dir_path.glob("*.md"))

    if not artifacts:
        print(f"⚠️  No markdown files found in {dir_path}")
        return 0, 0

    print(f"\n🔍 Validating {len(artifacts)} artifacts in {dir_path.name}/\n")

    passed = 0
    failed = 0

    for artifact in artifacts:
        if validate_artifact(artifact, verbose):
            passed += 1
        else:
            failed += 1

    print(f"\n📊 Results: {passed} passed, {failed} failed")

    return passed, failed


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <path>")
        print("  <path>: Discovery directory or specific artifact file")
        print("\nExample:")
        print("  python validate.py /docs/discovery/2026-01-06-topic/")
        print("  python validate.py /docs/discovery/2026-01-06-topic/00_problem-frame.md")
        sys.exit(1)

    target = Path(sys.argv[1])
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    if not target.exists():
        print(f"❌ Path does not exist: {target}")
        sys.exit(1)

    if target.is_file():
        # Validate single file
        success = validate_artifact(target, verbose)
        sys.exit(0 if success else 1)

    elif target.is_dir():
        # Validate directory
        passed, failed = validate_directory(target, verbose)
        sys.exit(0 if failed == 0 else 1)

    else:
        print(f"❌ Invalid path: {target}")
        sys.exit(1)


if __name__ == "__main__":
    main()
