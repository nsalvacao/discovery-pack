#!/usr/bin/env python3
"""
Discovery Pack Compliance Checker
Post-generation validation to ensure ALL workflow requirements were met.
Run after discovery completion to verify compliance.

Usage:
    python compliance_checker.py <output-dir> <mode>
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
except ImportError:
    print("❌ PyYAML not installed. Install: pip install PyYAML")
    sys.exit(1)

# Compliance checks
LITE_ARTIFACTS = [
    "00_problem-frame.md",
    "03_option-space.md",
    "07_speckit-handoff.md",
]

FULL_ARTIFACTS = [
    "00_problem-frame.md",
    "01_constraints-nfr.md",
    "02_domain-model.md",
    "03_option-space.md",
    "04_assumptions-unknowns.md",
    "05_validation-plan.md",
    "06_decision-log.md",
    "07_speckit-handoff.md",
]

REQUIRED_TAGS = ["FACT", "ASSUMPTION", "HYPOTHESIS", "CONSTRAINT"]


def check_file_exists(output_dir: Path, filename: str) -> Tuple[bool, str]:
    """Check if artifact file exists."""
    file_path = output_dir / filename
    if file_path.exists():
        return True, f"✅ Found: {filename}"
    else:
        return False, f"❌ Missing: {filename}"


def check_yaml_frontmatter(file_path: Path) -> Tuple[bool, str]:
    """Check if file has valid YAML frontmatter."""
    content = file_path.read_text(encoding="utf-8")
    
    if not content.startswith("---\n"):
        return False, f"❌ Missing YAML frontmatter delimiter in {file_path.name}"
    
    # Extract frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return False, f"❌ Invalid YAML frontmatter format in {file_path.name}"
    
    try:
        frontmatter = yaml.safe_load(match.group(1))
        
        # Check required fields
        required_fields = ["project", "date", "metadata"]
        missing = [f for f in required_fields if f not in frontmatter]
        
        if missing:
            return False, f"❌ Missing frontmatter fields in {file_path.name}: {missing}"
        
        return True, f"✅ Valid YAML frontmatter: {file_path.name}"
    
    except yaml.YAMLError as e:
        return False, f"❌ YAML parse error in {file_path.name}: {e}"


def check_epistemic_tags(file_path: Path) -> Tuple[bool, str, Dict]:
    """Check if file uses epistemic tags."""
    content = file_path.read_text(encoding="utf-8")
    
    tag_counts = {tag: len(re.findall(rf'\[{tag}\]', content)) for tag in REQUIRED_TAGS}
    total_tags = sum(tag_counts.values())
    
    if total_tags == 0:
        return False, f"❌ No epistemic tags found in {file_path.name}", tag_counts
    
    if total_tags < 3:
        return False, f"⚠️  Very few tags ({total_tags}) in {file_path.name} - may be insufficient", tag_counts
    
    return True, f"✅ Epistemic tags present ({total_tags} total): {file_path.name}", tag_counts


def check_template_structure(file_path: Path, template_name: str) -> Tuple[bool, str]:
    """Check if file follows template structure."""
    # This is a simplified check - looks for key section headers
    content = file_path.read_text(encoding="utf-8")
    
    # Key sections per template (simplified)
    required_sections = {
        "00_problem-frame.md": ["Problem Statement", "Users", "Jobs", "Success Metrics"],
        "01_constraints-nfr.md": ["Security", "Performance", "Compliance"],
        "02_domain-model.md": ["Glossary", "Entities", "Events"],
        "03_option-space.md": ["Options", "Trade-off", "Recommendation"],
        "04_assumptions-unknowns.md": ["Assumptions", "Unknowns"],
        "05_validation-plan.md": ["Experiments", "Success Criteria"],
        "06_decision-log.md": ["Decision", "Context", "Consequences"],
        "07_speckit-handoff.md": ["Constitution", "Specify"],
    }
    
    if template_name not in required_sections:
        return True, f"⚠️  No structure check defined for {template_name}"
    
    sections = required_sections[template_name]
    missing = [s for s in sections if s.lower() not in content.lower()]
    
    if missing:
        return False, f"❌ Missing sections in {file_path.name}: {missing}"
    
    return True, f"✅ Template structure followed: {file_path.name}"


def generate_compliance_report(output_dir: Path, mode: str):
    """Generate full compliance report."""
    print("=" * 60)
    print("🔍 Discovery Pack Compliance Report")
    print("=" * 60)
    print(f"Output Directory: {output_dir}")
    print(f"Mode: {mode}")
    print()
    
    artifacts = LITE_ARTIFACTS if mode == "lite" else FULL_ARTIFACTS
    
    all_checks_passed = True
    results = []
    
    # Check 1: File existence
    print("📁 Check 1: Artifact Files")
    print("-" * 60)
    for artifact in artifacts:
        passed, message = check_file_exists(output_dir, artifact)
        print(f"  {message}")
        if not passed:
            all_checks_passed = False
        results.append((artifact, "existence", passed))
    print()
    
    # Check 2: YAML frontmatter
    print("📄 Check 2: YAML Frontmatter")
    print("-" * 60)
    for artifact in artifacts:
        file_path = output_dir / artifact
        if file_path.exists():
            passed, message = check_yaml_frontmatter(file_path)
            print(f"  {message}")
            if not passed:
                all_checks_passed = False
            results.append((artifact, "yaml", passed))
    print()
    
    # Check 3: Epistemic tags
    print("🏷️  Check 3: Epistemic Tags")
    print("-" * 60)
    for artifact in artifacts:
        file_path = output_dir / artifact
        if file_path.exists():
            passed, message, tag_counts = check_epistemic_tags(file_path)
            print(f"  {message}")
            if tag_counts:
                print(f"     Tags: {json.dumps(tag_counts, indent=None)}")
            if not passed:
                all_checks_passed = False
            results.append((artifact, "tags", passed))
    print()
    
    # Check 4: Template structure
    print("📋 Check 4: Template Structure")
    print("-" * 60)
    for artifact in artifacts:
        file_path = output_dir / artifact
        if file_path.exists():
            passed, message = check_template_structure(file_path, artifact)
            print(f"  {message}")
            if not passed:
                all_checks_passed = False
            results.append((artifact, "structure", passed))
    print()
    
    # Summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ COMPLIANCE: PASS")
        print("All artifacts meet discovery-pack requirements.")
    else:
        print("❌ COMPLIANCE: FAIL")
        print("Some artifacts do not meet requirements.")
        print("Fix errors and re-run compliance check.")
    print("=" * 60)
    
    return 0 if all_checks_passed else 1


def main():
    if len(sys.argv) < 3:
        print("Usage: python compliance_checker.py <output-dir> <mode>")
        print()
        print("Example:")
        print("  python compliance_checker.py ./docs/discovery/2026-01-06-topic full")
        sys.exit(1)
    
    output_dir = Path(sys.argv[1])
    mode = sys.argv[2]
    
    if not output_dir.exists():
        print(f"❌ Output directory not found: {output_dir}")
        sys.exit(1)
    
    if mode not in ["lite", "full"]:
        print(f"❌ Mode must be 'lite' or 'full', got: {mode}")
        sys.exit(1)
    
    exit_code = generate_compliance_report(output_dir, mode)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
