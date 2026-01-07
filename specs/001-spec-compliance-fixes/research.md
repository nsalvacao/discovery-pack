# Research: Anthropic Skills Specification Compliance Fixes

**Phase**: 0 (Research & Strategy)
**Date**: 2026-01-07
**Status**: Complete

## R1: Schema-Template Field Audit

### Methodology

For each template (00-07):
1. Extract YAML frontmatter fields from `skill/discovery-pack/templates/`
2. Load corresponding JSON schema from `skill/discovery-pack/schemas/`
3. Compare required properties, types, enums
4. Document mismatches with fix actions

### Field Mismatch Matrix

| Template | Field Path | Template Value | Schema Requirement | Fix Action | Priority |
|----------|------------|----------------|--------------------|-----------|---------| |00_problem-frame.md | `problem_statement.what_pain` | (missing) | Required string | Add placeholder field | P0 |
| 01_constraints-nfr.md | `performance.throughput` | Object `{requests_per_second:...}` | Array of objects | Convert to array format | P0 |
| 02_domain-model.md | `bounded_contexts[0].name` | (missing) | Required string | Add name field | P0 |
| 03_option-space.md | `options[0].lock_in.vendor_lock_in` | "none" | Enum: ["low","medium","high"] | Change "none" → "low" | P0 |
| 05_validation-plan.md | `exit_criteria` | (missing) | Required string or object | Add exit criteria section | P0 |
| 06_decision-log.md | `decisions[0].superseded_by` | None (Python) | String or null | Fix type handling | P0 |
| 07_speckit-handoff.md | `constitution_input.glossary` | (missing) | Required object or array | Add glossary section | P0 |
| 04_assumptions-unknowns.md | (various) | - | - | (validate structure) | P1 |

### Detailed Findings

#### Template 00: problem-frame.md
**Missing Required Fields**:
- `problem_statement.what_pain` (string)
- Possibly other nested fields in `jobs_to_be_done` structure

**Fix**: Add YAML frontmatter placeholders matching schema structure exactly

#### Template 01: constraints-nfr.md
**Type Mismatch**:
- Template has: `throughput: {requests_per_second: 1000}`
- Schema expects: `throughput: [{metric: "requests_per_second", value: 1000}]`

**Fix**: Convert single object to array of metric objects

#### Template 03: option-space.md
**Enum Violation**:
- Template allows: `vendor_lock_in: "none"`
- Schema enum: `["low", "medium", "high"]` only

**Fix**: Replace all "none" with "low" (default minimal lock-in)

### Audit Summary

- **Total templates**: 8
- **Requiring fixes**: 7 (87.5%)
- **Fix complexity**: Low (field additions/renames, no logic changes)
- **Estimated effort**: 1-2 hours per template (6-8 hours total for Issue #1)

**Decision**: Templates MUST conform to schemas (schemas are source of truth per Principle II)

---

## R2: Sub-Skills Consolidation Strategy

### Current State Analysis

**File Count**:
- Main SKILL.md: 549 lines
- Sub-skill SKILL.md files: 8 (discovery-frame, decide, domain, options, validate, decide, handoff, run)
- Total: 9 SKILL.md files, ~896 lines across sub-skills

**Content Analysis**:
- **Unique content**: Phase-specific instructions (~300 lines across 8 phases)
- **Duplicated content**: Workflow preamble, validation steps, error handling (~200 lines repeated)
- **Verbose content**: Methodology explanations, example outputs (~250 lines movable)

### Consolidation Blueprint

**Target**: 1 SKILL.md file, <450 lines (10% buffer below 500 limit)

#### Line Allocation (Total: 440 lines)

| Section | Lines | Content |
|---------|-------|---------|
| Header/Metadata | 30 | Frontmatter, description, activation triggers |
| Mode Selection | 40 | Lite vs Full mode decision tree |
| Phase 1: Problem Framing | 45 | Consolidated from discovery-frame |
| Phase 2: Constraints | 40 | Consolidated from discovery-constraints |
| Phase 3: Domain Modeling | 40 | Consolidated from discovery-domain |
| Phase 4: Option Analysis | 45 | Consolidated from discovery-options |
| Phase 5: Validation Planning | 35 | Consolidated from discovery-validate |
| Phase 6: Decision Logging | 35 | Consolidated from discovery-decide |
| Phase 7: Handoff | 40 | Consolidated from discovery-handoff |
| Phase 8: Orchestration | 30 | Consolidated from discovery-run |
| Validation & Quality Gates | 40 | Schema validation, pre-flight checks |
| Footer/References | 20 | Pointers to bundled resources |
| **Total** | **440** | **(60 line buffer to 500 limit)** |

#### Content Migration Strategy

**Move to `shared-references/workflows/lite-mode.md`** (~150 lines):
- Step-by-step execution for artifacts 00, 03, 07
- Detailed field-filling instructions
- Example YAML structures
- Troubleshooting tips

**Move to `shared-references/workflows/full-mode.md`** (~200 lines):
- Step-by-step execution for artifacts 00-07 + auto-generated 04
- Phase dependencies and sequencing
- Validation gate details
- Token optimization tips

**Keep in SKILL.md** (compressed):
- High-level phase overview (1-2 sentences per phase)
- Decision points (mode selection, artifact selection)
- Template pointers (→ templates/{NN}_artifact.md)
- Validation commands (bash/python one-liners)

### Compression Techniques

1. **Prose → Bullets**: Convert paragraphs to concise bullet lists
2. **Inline → Tables**: Use markdown tables for comparison content (e.g., lite vs full mode)
3. **Examples → References**: Replace inline examples with "See workflows/lite-mode.md#section"
4. **Repeated Instructions → DRY**: Extract common validation steps to single section, reference from phases

### Consolidation Workflow

**Phase 1**: Merge content (preserve all logic)
1. Read all 9 SKILL.md files
2. Extract unique phase-specific instructions
3. Create unified workflow sections
4. Remove duplications

**Phase 2**: Compress (reduce lines)
1. Apply compression techniques
2. Measure line count after each change
3. Move verbose content to bundled resources
4. Target: <450 lines

**Phase 3**: Validate (no functional regression)
1. Compare old workflow → new workflow (feature parity)
2. Test lite mode execution
3. Test full mode execution
4. Verify all 8 phases still functional

**Estimated Effort**: 8-10 hours (Issue #3)

**Decision**: Hybrid approach - concise inline workflow + detailed bundled resources (progressive disclosure)

---

## R3: Progressive Disclosure Implementation Pattern

### Current State (Eager Loading)

```markdown
## Workflow Step 3: Generate Artifacts

**Before starting, read ALL templates:**
- templates/00_problem-frame.md
- templates/01_constraints-nfr.md
- templates/02_domain-model.md
- ... (all 8 templates)

[Agent loads ~15-20k tokens of template content upfront]

Then for each artifact: Generate using preloaded template
```

**Problem**: Wastes tokens loading templates that may not be needed (lite mode only uses 3)

### Target State (Lazy Loading)

```markdown
## Workflow Step 3: Generate Artifacts

For each artifact in [mode-specific list]:
  1. **Load template**: Read templates/{NN}_artifact-name.md
  2. **Generate artifact**: Follow template structure
  3. **Validate**: Run scripts/validate.py on generated file
  4. **Move to next**: Do NOT preload remaining templates
```

**Benefit**: Only loads templates when generating that specific artifact

### Implementation Pattern

#### Agent Instructions (SKILL.md)

**OLD** (verbose, preload):
```markdown
### Artifact Generation

Read the following templates from the templates/ directory:
- 00_problem-frame.md [50 lines of structure quoted]
- 03_option-space.md [60 lines of structure quoted]
- 07_speckit-handoff.md [40 lines of structure quoted]

Now generate each artifact using the corresponding template.
```

**NEW** (concise, on-demand):
```markdown
### Artifact Generation

For each artifact {00, 03, 07} in lite mode:
1. Load template: templates/{NN}_{name}.md
2. Generate artifact following template YAML + markdown structure
3. Validate: `python scripts/validate.py docs/discovery/project/{NN}_{name}.md`
4. Confirm pass before proceeding to next artifact

→ Detailed instructions: shared-references/workflows/lite-mode.md
```

#### Bundled Resource (workflows/lite-mode.md)

**Purpose**: Detailed step-by-step for users/agents needing verbose guidance

**Structure**:
```markdown
# Lite Mode Workflow

## Artifact 00: Problem Frame

### Step 1: Load Template
Read templates/00_problem-frame.md

### Step 2: Fill YAML Frontmatter
[Detailed field-by-field instructions - 50 lines]

### Step 3: Write Markdown Body
[Section-by-section guidance - 30 lines]

### Step 4: Validate
```bash
python scripts/validate.py docs/discovery/project/00_problem-frame.md
```
[Troubleshooting common errors - 20 lines]

## Artifact 03: Option Space
[Repeat structure - 100 lines]

## Artifact 07: Spec-Kit Handoff
[Repeat structure - 80 lines]
```

### Token Savings Calculation

**Baseline** (current eager loading):
- SKILL.md: 549 lines (~11k tokens)
- All templates preloaded: 8 × 50 lines avg = 400 lines (~8k tokens)
- **Total upfront**: ~19k tokens

**Target** (progressive disclosure):
- SKILL.md: <450 lines (~9k tokens)
- Lite mode templates on-demand: 3 × 50 lines = 150 lines (~3k tokens)
- **Total lite mode**: ~12k tokens
- **Savings**: 37% (19k → 12k)

**Full mode**:
- SKILL.md: <450 lines (~9k tokens)
- All templates on-demand: 8 × 50 lines = 400 lines (~8k tokens)
- **Total full mode**: ~17k tokens
- **Savings**: 10% (19k → 17k)

**Average savings**: 20-30% (matches spec target SC-005)

**Decision**: Implement "just-in-time" template loading with explicit phased instructions

---

## R4: Path Resolution Strategy for Cross-Agent Compatibility

### Problem Statement

**Current**: Hardcoded agent-specific paths break portability
```bash
# SKILL.md line 97
bash ~/.copilot/skills/discovery-pack/pre-flight-check.sh

# SKILL.md line 399
python3 ~/.copilot/skills/discovery-pack/scripts/validate.py
```

**Impact**: Fails in Claude Code (`~/.claude/skills/`), project-local installations, other agents

### Path Resolution Requirements

1. **Agent-agnostic**: Works in `~/.claude/`, `~/.copilot/`, `.claude/` (project-local)
2. **Relative**: Scripts locate resources relative to skill root, not hardcoded home directory
3. **Portable**: Python and Bash both resolve paths correctly
4. **Testable**: Can verify with grep patterns (`grep -r '~/.copilot' skill/` → 0 results)

### Python Path Resolution Pattern

**File**: `scripts/validate.py`, `scripts/extract_assumptions.py`

```python
#!/usr/bin/env python3
import os
from pathlib import Path

# Determine skill root (parent of scripts/ directory)
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_ROOT = SCRIPT_DIR.parent
SCHEMAS_DIR = SKILL_ROOT / "schemas"
TEMPLATES_DIR = SKILL_ROOT / "templates"

# Load schema relative to skill root
def load_schema(artifact_name: str):
    schema_path = SCHEMAS_DIR / f"{artifact_name}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    return json.loads(schema_path.read_text())

# Load template relative to skill root
def load_template(artifact_num: int, artifact_name: str):
    template_path = TEMPLATES_DIR / f"{artifact_num:02d}_{artifact_name}.md"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text()
```

**Rationale**: `Path(__file__)` resolves to script location regardless of where it's invoked from

### Bash Path Resolution Pattern

**File**: `scripts/pre-flight-check.sh`

```bash
#!/bin/bash
set -euo pipefail

# Determine skill root (parent of scripts/ directory)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_ROOT/templates"
SCHEMAS_DIR="$SKILL_ROOT/schemas"
SHARED_REF_DIR="$SKILL_ROOT/shared-references"

# Check templates exist
if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "ERROR: Templates directory not found: $TEMPLATES_DIR"
    exit 1
fi

# Count templates
TEMPLATE_COUNT=$(find "$TEMPLATES_DIR" -name "*.md" -type f | wc -l)
echo "Found $TEMPLATE_COUNT templates in $TEMPLATES_DIR"
```

**Rationale**: `BASH_SOURCE[0]` resolves to script path, `dirname` gets parent directory

### SKILL.md Reference Pattern

**BEFORE** (hardcoded):
```markdown
### Step 1.5: Pre-Flight Check

Run dependency validation:
```bash
bash ~/.copilot/skills/discovery-pack/scripts/pre-flight-check.sh
```

### Step 9: Validate All Artifacts

Run schema validation:
```bash
python3 ~/.copilot/skills/discovery-pack/scripts/validate.py docs/discovery/project/
```
```

**AFTER** (relative):
```markdown
### Step 1.5: Pre-Flight Check

Run dependency validation:
```bash
bash scripts/pre-flight-check.sh
```

### Step 9: Validate All Artifacts

Run schema validation:
```bash
python scripts/validate.py docs/discovery/project/
```
```

**Assumption**: Agent working directory is skill root when SKILL.md is invoked (standard for Anthropic agents)

### Cross-Agent Testing Matrix

| Agent | Installation Path | Test Command | Expected Result |
|-------|-------------------|--------------|-----------------|
| Claude Code | `~/.claude/skills/discovery-pack/` | `bash scripts/validate.py` | ✅ Pass (relative path resolves) |
| Copilot CLI | `~/.copilot/skills/discovery-pack/` | `bash scripts/validate.py` | ✅ Pass (relative path resolves) |
| Project-local | `.claude/skills/discovery-pack/` | `bash scripts/validate.py` | ✅ Pass (relative path resolves) |
| Gemini | `~/.gemini/skills/discovery-pack/` | `bash scripts/validate.py` | ✅ Pass (relative path resolves) |

**Validation Command**:
```bash
# Must return 0 results (no hardcoded paths)
grep -r '~/.copilot' skill/discovery-pack/ | wc -l
grep -r '~/.claude' skill/discovery-pack/ | wc -l
```

**Decision**: Use relative paths from script location (Python `__file__`, Bash `BASH_SOURCE[0]`)

---

## Research Summary

### Findings

| Research Task | Key Decision | Estimated Effort |
|---------------|--------------|------------------|
| **R1: Schema Audit** | Fix 7/8 templates to match schemas (schemas are source of truth) | 6-8 hours |
| **R2: Consolidation** | Hybrid: concise SKILL.md + detailed workflows/ resources | 8-10 hours |
| **R3: Progressive Disclosure** | Just-in-time template loading (20-30% token savings) | Included in R2 |
| **R4: Path Resolution** | Relative paths via Python `__file__`, Bash `BASH_SOURCE[0]` | 2-3 hours |

**Total Estimated Effort**: 16-21 hours (within 20-25 hour project estimate)

### Unresolved Questions

**None** - All research tasks complete, decisions made, ready for Phase 1 design artifacts.

### Recommendations for Phase 1

1. **Create quickstart.md**: Guide contributors through validation workflow (1 hour)
2. **Create implementation checklist**: Granular task breakdown for Phase 2 (2 hours)
3. **Update agent context**: Add project technologies to `.claude/` files (15 min)
4. **Proceed to `/speckit.tasks`**: Generate atomic tasks from checklist (automated)

**Status**: ✅ Phase 0 Complete - Proceed to Phase 1 Design
