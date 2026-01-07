# Implementation Plan: Anthropic Skills Specification Compliance Fixes

**Branch**: `001-spec-compliance-fixes` | **Date**: 2026-01-07 | **Spec**: [spec.md](./spec.md)
**Input**: Fix P0-P1 critical compliance violations: schema-template sync, hardcoded paths, sub-skills consolidation, SKILL.md size reduction

## Summary

Transform discovery-pack from 5.2/10 compliance score to 100% Anthropic Skills specification compliance by synchronizing 8 template/schema pairs, eliminating hardcoded agent paths, consolidating 9 SKILL.md files into 1 (<450 lines), and implementing progressive disclosure to reduce token consumption by 20-30%. This is a **structural refactoring** project without new features, targeting validation pass rate improvement from 12.5% to 100%.

## Technical Context

**Language/Version**: Python 3.11+ (existing scripts), Bash (POSIX-compatible for scripts), Markdown (templates/docs)
**Primary Dependencies**: 
- Python: `jsonschema>=4.17.0`, `PyYAML>=6.0` (existing)
- Bash: Standard POSIX utilities (grep, find, sed)
- Git: For version control and branch management

**Storage**: Filesystem-based (templates/, schemas/, skill/ directories) - No database
**Testing**: 
- Schema validation: `scripts/validate.py` (existing)
- Path validation: `grep -r` patterns for hardcoded paths
- Line count validation: `wc -l` for SKILL.md size
- Cross-agent testing: Manual verification in Claude Code + Copilot CLI

**Target Platform**: Multi-agent (Claude Code, Copilot CLI, Gemini, Cursor, VS Code agent mode)
**Project Type**: Skill package refactoring (no runtime application)
**Performance Goals**: 
- Validation execution <5 seconds for 8 artifacts (SC-008)
- Token consumption ≤25k for full mode (20-30% reduction via progressive disclosure)

**Constraints**: 
- SKILL.md MUST be <500 lines (target <450) per Anthropic spec
- 100% schema validation pass rate (non-negotiable)
- Zero hardcoded agent-specific paths (grep validation must pass)
- Preserve all functional logic during consolidation (no feature removal)

**Scale/Scope**: 
- 8 templates to sync with schemas (00-07)
- 9 SKILL.md files to consolidate into 1
- ~15-20 script path references to convert to relative
- 549 lines SKILL.md to reduce by 18%+ (to <450)
- 24 functional requirements across 4 issues

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 Check

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Skills Spec Compliance** | 🔴 **FAIL** | Currently violates flat architecture (9 SKILL.md), >500 lines (549), hardcoded paths |
| **II. Schema-Template Sync** | 🔴 **FAIL** | 7/8 artifacts fail validation (12.5% pass rate) |
| **III. Cross-Agent Portability** | 🔴 **FAIL** | Hardcoded `~/.copilot/` paths break Claude Code |
| **IV. Token Efficiency** | 🟡 **PARTIAL** | Automation exists but progressive disclosure not enforced |
| **V. Methodology Rigor** | ✅ **PASS** | JTBD, ADR, Lean applied correctly (not in scope of this fix) |
| **VI. Spec-Kit Integration** | ✅ **PASS** | Handoff format correct (not in scope) |
| **VII. Quality Gates** | 🔴 **FAIL** | Validation gates exist but fail due to schema issues |
| **VIII. Naming Conventions** | ✅ **PASS** | Kebab-case, snake_case followed (not in scope) |

**Gate Status**: ❌ **BLOCKED** - Critical violations in Principles I, II, III prevent release

**Justification for proceeding**: This implementation plan **FIXES** the violations. Post-Phase 1, all principles will pass.

### Post-Phase 1 Target

| Principle | Expected Status | Evidence |
|-----------|-----------------|----------|
| **I. Skills Spec Compliance** | ✅ **PASS** | 1 SKILL.md file, <450 lines, relative paths, flat architecture |
| **II. Schema-Template Sync** | ✅ **PASS** | 8/8 artifacts pass validation (100%) |
| **III. Cross-Agent Portability** | ✅ **PASS** | Zero hardcoded paths, tested in Claude Code + Copilot CLI |
| **IV. Token Efficiency** | ✅ **PASS** | Progressive disclosure enforced, 20-30% token reduction measured |

## Project Structure

### Documentation (this feature)

```text
specs/001-spec-compliance-fixes/
├── plan.md              # This file (Phase 0 complete)
├── research.md          # Phase 0: Schema sync patterns, consolidation strategies
├── data-model.md        # N/A (no data entities in refactoring project)
├── quickstart.md        # Phase 1: Developer onboarding for compliance workflow
├── contracts/           # N/A (no API contracts in skill package)
├── checklists/
│   └── requirements.md  # Already created (spec validation)
└── spec.md              # Feature specification (already created)
```

### Source Code (repository root)

```text
skill/discovery-pack/                        ← Target of refactoring
├── SKILL.md                                 ← CONSOLIDATE from 9 → 1 file (<450 lines)
│
├── templates/                               ← FIX schema sync (8 files)
│   ├── 00_problem-frame.md                 ← Add missing YAML fields, fix enums
│   ├── 01_constraints-nfr.md               ← Fix array vs object types
│   ├── 02_domain-model.md                  ← Add required 'name' field
│   ├── 03_option-space.md                  ← Fix vendor_lock_in enum
│   ├── 04_assumptions-unknowns.md          ← Validate structure
│   ├── 05_validation-plan.md               ← Add exit_criteria field
│   ├── 06_decision-log.md                  ← Fix nullable superseded_by
│   └── 07_speckit-handoff.md               ← Add glossary field
│
├── schemas/                                 ← Reference (source of truth)
│   ├── 00_problem-frame.schema.json
│   ├── 01_constraints-nfr.schema.json
│   ├── 02_domain-model.schema.json
│   ├── 03_option-space.schema.json
│   ├── 04_assumptions-unknowns.schema.json
│   ├── 05_validation-plan.schema.json
│   ├── 06_decision-log.schema.json
│   ├── 07_speckit-handoff.schema.json
│   └── shared-definitions.schema.json
│
├── scripts/                                 ← FIX relative paths
│   ├── validate.py                         ← Update to use relative schema paths
│   ├── extract_assumptions.py              ← Update to use relative paths
│   ├── gate_detector.py
│   ├── pre-flight-check.sh                 ← Create/update for FR-021
│   ├── template_filler.py
│   └── requirements.txt
│
├── shared-references/                       ← CREATE workflows/ subdirectory
│   ├── methodologies.md                    ← Existing (reference only)
│   ├── glossary.md                         ← Existing (reference only)
│   └── workflows/                          ← NEW: Move verbose workflow details
│       ├── lite-mode.md                    ← Phase 1-3 detailed steps
│       └── full-mode.md                    ← Phase 1-8 detailed steps
│
└── discovery-{frame,decide,domain,...}/     ← DELETE (8 sub-skill directories)
    └── SKILL.md                            ← Consolidate into main SKILL.md

README.md                                    ← UPDATE installation instructions (FR-010)
CONTRIBUTING.md                              ← UPDATE with validation checklist
.specify/memory/constitution.md              ← Reference (principles enforced)
```

**Structure Decision**: Single skill package refactoring (Option 1 adapted). No frontend/backend/mobile separation needed. Focus is on transforming existing `skill/discovery-pack/` structure to comply with Anthropic specification.

## Complexity Tracking

> Constitution violations justified as **temporary state during refactoring** - all will be resolved by Phase 1 completion.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 9 SKILL.md files (Principle I) | Legacy structure from v0.9.0 | Must consolidate (this project fixes it) |
| 7/8 validation failures (Principle II) | Template-schema desync from manual edits | Must audit field-by-field (this project fixes it) |
| Hardcoded `~/.copilot/` paths (Principle III) | Early Copilot-only development | Must use relative paths (this project fixes it) |

**Post-Phase 1**: All violations will be **RESOLVED** - no complexity justification needed.

---

## Phase 0: Research & Strategy

### Objectives

1. Determine optimal consolidation strategy for 9 → 1 SKILL.md without functional regression
2. Identify schema-template field mismatches for all 8 artifacts
3. Research progressive disclosure patterns in Anthropic skills (reference implementations)
4. Define path resolution strategy for cross-agent compatibility

### Research Tasks

#### R1: Schema-Template Field Audit

**Goal**: Create field-by-field comparison matrix for templates 00-07 vs schemas

**Method**:
1. For each template (00-07):
   - Extract YAML frontmatter fields
   - Load corresponding JSON schema
   - Compare required properties, types, enums
   - Document mismatches with examples

**Output**: Table in `research.md`:

| Template | Schema Field | Template Value | Schema Requirement | Fix Action |
|----------|--------------|----------------|--------------------|------------|
| 00_problem-frame.md | `what_pain` | (missing) | Required string | Add field with placeholder |
| 03_option-space.md | `vendor_lock_in` | "none" | Enum: low\|medium\|high | Change to "low" default |
| ... | ... | ... | ... | ... |

**Decision**: Fix templates to match schemas (schemas are source of truth per Principle II)

#### R2: Sub-Skills Consolidation Strategy

**Goal**: Determine how to merge 8 sub-skills into main SKILL.md without exceeding 500 lines

**Method**:
1. Read all 9 SKILL.md files (main + 8 sub-skills)
2. Identify unique vs duplicated content
3. Calculate line counts per phase
4. Design compression strategy (bullets, tables, move to bundled resources)

**Research Questions**:
- Can phase instructions be collapsed to 40-50 lines each (8 phases × 50 = 400 lines)?
- Which verbose content moves to `workflows/lite-mode.md` and `workflows/full-mode.md`?
- How to preserve workflow sequencing without sub-skill invocations?

**Output**: Consolidation blueprint in `research.md`:

```markdown
### Consolidation Strategy

**Target**: 1 SKILL.md file, <450 lines (buffer below 500 limit)

**Phase Allocation** (lines):
- Header/Metadata: 30 lines
- Mode Selection: 40 lines
- Phase 1-8 Consolidated: 300 lines (37.5 lines per phase average)
- Validation/Handoff: 40 lines
- Footer/References: 40 lines
**Total**: ~450 lines

**Content Migration**:
- Move to `workflows/lite-mode.md`: Step-by-step execution for artifacts 00, 03, 07 (detailed)
- Move to `workflows/full-mode.md`: Step-by-step execution for artifacts 00-07 (detailed)
- Keep in SKILL.md: High-level overview, decision points, template pointers
```

**Decision**: Hybrid approach - concise inline workflow + detailed bundled resources

#### R3: Progressive Disclosure Implementation Patterns

**Goal**: Research how other Anthropic skills implement progressive disclosure

**Method**:
1. Review Anthropic documentation on progressive disclosure
2. Analyze reference skills (if accessible) for template loading patterns
3. Define "on-demand" vs "upfront" loading semantics

**Research Questions**:
- At what point should SKILL.md reference a template vs quote it inline?
- How to instruct agent to load templates only when generating specific artifact?
- Token measurement: baseline (current) vs target (progressive disclosure)

**Output**: Pattern definition in `research.md`:

```markdown
### Progressive Disclosure Pattern

**Before** (current - loads all templates upfront):
```
Step 3: Generate Artifacts
[Read ALL templates from templates/ directory]
For each artifact: generate using preloaded template
```

**After** (progressive - loads on-demand):
```
Step 3: Generate Artifacts
For each artifact in [mode-specific list]:
  → Load template from templates/{NN}_artifact-name.md
  → Generate artifact following template structure
  → Validate immediately
  → Move to next artifact
```

**Token savings**: Estimated 3-5k tokens (20-30% reduction for full mode)
```

**Decision**: Implement "just-in-time" template loading with explicit agent instructions

#### R4: Path Resolution Strategy for Cross-Agent Compatibility

**Goal**: Define how scripts locate resources without hardcoded agent paths

**Method**:
1. Identify all script invocations in SKILL.md and sub-skills
2. Document current hardcoded patterns (`~/.copilot/skills/discovery-pack/`)
3. Research Python/Bash path resolution from script location
4. Test path resolution in 3 installation scenarios (Claude, Copilot, project-local)

**Research Questions**:
- How to make Python scripts find `schemas/` relative to script location?
- Can Bash scripts use `$( cd "$(dirname "$0")" && pwd)` for portability?
- What assumptions about skill root directory are safe across agents?

**Output**: Path resolution spec in `research.md`:

```markdown
### Path Resolution Strategy

**Python scripts** (validate.py, extract_assumptions.py):
```python
import os
from pathlib import Path

# Determine skill root (parent of scripts/ directory)
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_ROOT = SCRIPT_DIR.parent
SCHEMAS_DIR = SKILL_ROOT / "schemas"
TEMPLATES_DIR = SKILL_ROOT / "templates"

# Load schema relative to skill root
schema_path = SCHEMAS_DIR / f"{artifact_num:02d}_{artifact_name}.schema.json"
```

**Bash scripts** (pre-flight-check.sh):
```bash
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_ROOT/templates"
SCHEMAS_DIR="$SKILL_ROOT/schemas"
```

**SKILL.md references**:
- BEFORE: `bash ~/.copilot/skills/discovery-pack/scripts/validate.py`
- AFTER: `bash scripts/validate.py` (relative to skill root)

**Assumption**: Agent working directory is skill root when SKILL.md is invoked
```

**Decision**: Relative paths from script location (Python `__file__`, Bash `BASH_SOURCE`)

### Research Deliverables

**File**: `specs/001-spec-compliance-fixes/research.md`

**Sections**:
1. Schema-Template Field Audit (R1) - Comparison matrix for all 8 artifacts
2. Sub-Skills Consolidation Strategy (R2) - Line allocation blueprint
3. Progressive Disclosure Pattern (R3) - Before/after implementation
4. Path Resolution Strategy (R4) - Python + Bash code patterns

**Status**: Ready for Phase 1 (design artifacts)

---

## Phase 1: Design & Implementation Blueprint

### Prerequisites

- ✅ `research.md` complete with all 4 research tasks (R1-R4)
- ✅ Constitution Principle violations understood (temporary during refactoring)

### Artifacts to Generate

#### 1. quickstart.md - Developer Onboarding

**Purpose**: Guide contributors through compliance validation workflow

**Sections**:
- **Prerequisites**: Python 3.11+, Git, text editor
- **Validation Workflow**:
  1. Install dependencies: `pip install -r scripts/requirements.txt`
  2. Run schema validation: `python scripts/validate.py skill/discovery-pack/templates/`
  3. Check SKILL.md size: `wc -l skill/discovery-pack/SKILL.md` (expect <450)
  4. Check hardcoded paths: `grep -r '~/.copilot' skill/discovery-pack/` (expect 0 results)
  5. Cross-agent test: Install in Claude Code, run lite mode
- **Common Issues**:
  - Schema validation failures: Check template YAML against schema JSON
  - Path resolution failures: Verify relative paths in scripts
  - Line count exceeded: Move verbose content to `workflows/`

**Output**: `specs/001-spec-compliance-fixes/quickstart.md`

#### 2. data-model.md - N/A for This Project

**Rationale**: This is a structural refactoring project, not a feature with domain entities. No data model to design.

**Output**: (skip)

#### 3. contracts/ - N/A for This Project

**Rationale**: No API contracts in a skill package. Skill interface is SKILL.md format (defined by Anthropic spec).

**Output**: (skip)

#### 4. Implementation Checklist

**File**: `specs/001-spec-compliance-fixes/checklists/implementation.md`

**Purpose**: Task-level checklist for Phase 2 (tasks.md generation)

**Sections**:
- [ ] **Issue #1: Schema-Template Sync** (FR-001 to FR-005)
  - [ ] Audit all 8 templates vs schemas (research.md matrix)
  - [ ] Fix template 00: Add `what_pain` field
  - [ ] Fix template 01: Change throughput type to array
  - [ ] Fix template 02: Add `name` field to bounded_contexts
  - [ ] Fix template 03: Fix `vendor_lock_in` enum ("none" → "low")
  - [ ] Fix template 05: Add `exit_criteria` field
  - [ ] Fix template 06: Fix `superseded_by` nullable type
  - [ ] Fix template 07: Add `glossary` field
  - [ ] Validate all templates: `python scripts/validate.py` (expect 8/8 pass)

- [ ] **Issue #2: Hardcoded Paths** (FR-006 to FR-010)
  - [ ] Audit SKILL.md for `~/.copilot` references (grep search)
  - [ ] Convert SKILL.md script paths to relative (e.g., `scripts/validate.py`)
  - [ ] Update `validate.py`: Use `Path(__file__).parent.parent` for skill root
  - [ ] Update `extract_assumptions.py`: Use relative paths
  - [ ] Test in Claude Code installation
  - [ ] Test in Copilot CLI installation
  - [ ] Test in project-local installation
  - [ ] Update README: Document all installation locations

- [ ] **Issue #3: Sub-Skills Consolidation** (FR-011 to FR-015)
  - [ ] Read all 9 SKILL.md files (main + 8 sub-skills)
  - [ ] Create consolidation blueprint (from research.md)
  - [ ] Merge Phase 1-8 into main SKILL.md (inline sections)
  - [ ] Move verbose workflow to `workflows/lite-mode.md`
  - [ ] Move verbose workflow to `workflows/full-mode.md`
  - [ ] Remove sub-skill directories (discovery-frame/, discovery-decide/, etc.)
  - [ ] Replace sub-skill invocations with direct template reads
  - [ ] Verify line count: `wc -l skill/discovery-pack/SKILL.md` (<450)

- [ ] **Issue #4: SKILL.md Size Reduction** (FR-016 to FR-020)
  - [ ] Identify verbose sections in SKILL.md (>50 lines)
  - [ ] Convert prose to bullet points
  - [ ] Create tables for comparison content
  - [ ] Move methodology details to `shared-references/methodologies.md`
  - [ ] Implement progressive disclosure: "Load template when generating artifact"
  - [ ] Verify line count target: <450 lines (buffer below 500 limit)

- [ ] **Validation & Quality Gates** (FR-021 to FR-024)
  - [ ] Create `scripts/pre-flight-check.sh` (Python version, packages, permissions)
  - [ ] Update SKILL.md: Run pre-flight before workflow
  - [ ] Add inline validation after each artifact generation
  - [ ] Update validation error messages: Show file path, specific error, fix suggestion
  - [ ] Test end-to-end: Lite mode (3 artifacts) + Full mode (8 artifacts)

**Output**: `specs/001-spec-compliance-fixes/checklists/implementation.md`

### Agent Context Update

**Script**: `.specify/scripts/bash/update-agent-context.sh claude`

**Purpose**: Update `.claude/` agent-specific context with project technologies

**Technologies to Add**:
- Python 3.11+ (scripting for validation)
- JSON Schema Draft 7 (validation framework)
- YAML frontmatter (template structure)
- Bash scripting (automation)
- Markdown (documentation and templates)

**Output**: `.claude/context.md` or similar agent file (depends on agent type)

### Phase 1 Deliverables

- ✅ `quickstart.md` - Compliance validation workflow guide
- ✅ `checklists/implementation.md` - Granular task checklist
- ✅ Agent context updated with project technologies
- ⏭️ Ready for Phase 2: `/speckit.tasks` (task breakdown)

---

## Post-Phase 1 Constitution Re-Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. Skills Spec Compliance** | 🟢 **WILL PASS** | Design complete for 1 SKILL.md (<450 lines), flat architecture, relative paths |
| **II. Schema-Template Sync** | 🟢 **WILL PASS** | Field audit complete, fixes defined in checklist (8/8 artifacts will pass) |
| **III. Cross-Agent Portability** | 🟢 **WILL PASS** | Path resolution strategy defined, cross-agent testing in checklist |
| **IV. Token Efficiency** | 🟢 **WILL PASS** | Progressive disclosure pattern defined (20-30% savings target) |

**Gate Status**: ✅ **APPROVED** - Design satisfies all constitution principles. Proceed to Phase 2 (task breakdown).

---

## Next Steps

1. **Generate Tasks**: Run `/speckit.tasks` to break down implementation checklist into atomic, prioritized tasks
2. **Implementation**: Execute tasks sequentially (Issues #1 → #2 → #3 → #4)
3. **Validation**: Run full compliance check after each issue completion
4. **Release**: Tag v1.0.0 after all 4 issues resolved and gates pass

**Estimated Effort**: 20-25 hours (per tasks.md analysis)
- Issue #1: 6-8 hours (schema sync)
- Issue #2: 2-3 hours (path fixes)
- Issue #3: 8-10 hours (consolidation)
- Issue #4: 4-6 hours (size reduction + progressive disclosure)

**Success Criteria Reference**: See spec.md SC-001 to SC-010 for measurable outcomes
