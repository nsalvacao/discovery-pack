# Discovery Pack - Improvement Tasks

**Project:** Discovery Pack Skill for Claude Code
**Base Path:** `D:\GitHub\discovery-pack\skill\discovery-pack`
**Analysis Date:** 2026-01-07
**Current Status:** 5.2/10 - Functional but not production-ready

---

## Priority Legend

- **P0 - Critical (Blocker):** Prevents proper functionality
- **P1 - High:** Major compliance violations or architectural issues
- **P2 - Medium:** Significant improvements to usability/maintainability
- **P3 - Low:** Nice-to-have enhancements

---

## Critical Issues (P0)

### Issue #1: Template-Schema Synchronization Failures

**Priority:** P0 - Critical
**Effort:** 6-8 hours
**Status:** Open
**Dependencies:** None

**Description:**

7 out of 8 generated artifacts fail JSON schema validation due to mismatches between templates and schemas. This breaks the validation workflow and undermines the entire discovery process quality assurance.

**Validation Failures Identified:**
```
❌ 00_problem-frame.md: 'what_pain' is a required property (Path: problem_statement)
❌ 01_constraints-nfr.md: {...} is not of type 'array' (Path: performance > throughput)
❌ 02_domain-model.md: 'name' is a required property (Path: bounded_contexts > 0)
❌ 03_option-space.md: 'none' not in enum ['low','medium','high'] (Path: options > 0 > lock_in > vendor_lock_in)
❌ 05_validation-plan.md: 'exit_criteria' is a required property
❌ 06_decision-log.md: None is not of type 'string' (Path: decisions > 0 > superseded_by)
❌ 07_speckit-handoff.md: 'glossary' is a required property (Path: constitution_input)
```

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\00_problem-frame.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\01_constraints-nfr.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\02_domain-model.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\03_option-space.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\05_validation-plan.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\06_decision-log.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\07_speckit-handoff.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\schemas\*.json` (all corresponding schemas)

**Acceptance Criteria:**
- [ ] Audit each template YAML frontmatter against corresponding JSON schema
- [ ] Add missing required fields to templates with placeholder values
- [ ] Remove fields from templates that don't exist in schemas
- [ ] Ensure enum values in templates match schema enums exactly
- [ ] Fix array vs object type mismatches
- [ ] Update nullable fields to handle None/null properly
- [ ] Test validation with `python scripts/validate.py` on sample artifacts
- [ ] All 7 artifacts must pass validation (target: 8/8 pass rate)

**Implementation Steps:**
1. Create validation test suite with minimal valid examples for each template
2. For each template:
   - Load corresponding schema from `schemas/`
   - Map every schema required property to template frontmatter
   - Add missing fields with `TODO` placeholders
   - Fix type mismatches (array vs object, string vs null)
   - Validate enum values
3. Run automated validation against test artifacts
4. Document schema-template mapping in `docs/schema-guide.md`

**References:**
- JSON Schema specification: https://json-schema.org/understanding-json-schema/
- YAML frontmatter best practices: https://www.mkdocs.org/user-guide/writing-your-docs/#yaml-style-meta-data

---

### Issue #2: Hardcoded Paths Break Cross-Agent Portability

**Priority:** P0 - Critical
**Effort:** 2-3 hours
**Status:** Open
**Dependencies:** None

**Description:**

SKILL.md contains hardcoded paths to `~/.copilot/skills/discovery-pack/` which breaks portability across different AI agent implementations (Claude Code uses `~/.claude/skills/`, Gemini Code Assist uses different paths, etc.).

**Hardcoded Paths Found:**
```bash
# Line 97
bash ~/.copilot/skills/discovery-pack/pre-flight-check.sh

# Line 156
bash ~/.copilot/skills/discovery-pack/discovery-pack-run.sh

# Line 399
python3 ~/.copilot/skills/discovery-pack/scripts/validate.py
```

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md`
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-run\SKILL.md`
- Any other sub-skill SKILL.md files with absolute paths

**Acceptance Criteria:**
- [ ] Replace all `~/.copilot/skills/discovery-pack/` with relative paths
- [ ] Use `scripts/` prefix for script references
- [ ] Use `templates/` prefix for template references
- [ ] Verify skill works in Claude Code (`~/.claude/skills/`)
- [ ] Verify skill works when invoked via `Skill` tool (agent-agnostic)
- [ ] Document path assumptions in README

**Implementation Steps:**
1. Search all SKILL.md files for `~/.copilot/` or absolute paths
2. Replace with relative paths:
   ```bash
   # Before
   bash ~/.copilot/skills/discovery-pack/pre-flight-check.sh

   # After
   bash scripts/pre-flight-check.sh
   ```
3. Update references to use skill base directory variable if needed
4. Test skill invocation from different agent environments
5. Add path resolution logic if scripts need to locate bundled resources

**References:**
- Agent Skills Best Practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Skill portability guidelines: https://agentskills.io/specification#portability

---

## High Priority Issues (P1)

### Issue #3: Sub-Skills Architecture Violates Flat Standard

**Priority:** P1 - High
**Effort:** 8-10 hours
**Status:** Open
**Dependencies:** Issue #4 (should be done together)

**Description:**

Discovery-pack uses 8 separate sub-skill directories with individual SKILL.md files (896 total lines across sub-skills), violating Anthropic's flat architecture recommendation. This creates:
- Redundant loading overhead (9 SKILL.md files instead of 1)
- Increased context usage for agent
- Maintenance burden (changes must propagate across files)
- Violation of progressive disclosure (loads all sub-skills eagerly)

**Current Structure:**
```
skill/discovery-pack/
├── SKILL.md (549 lines)
├── discovery-frame/SKILL.md
├── discovery-constraints/SKILL.md
├── discovery-domain/SKILL.md
├── discovery-options/SKILL.md
├── discovery-validate/SKILL.md
├── discovery-decide/SKILL.md
├── discovery-handoff/SKILL.md
└── discovery-run/SKILL.md
```

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (consolidation target)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-frame\SKILL.md` (to be merged)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-constraints\SKILL.md` (to be merged)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-domain\SKILL.md` (to be merged)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-options\SKILL.md` (to be merged)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-validate\SKILL.md` (to be merged)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-decide\SKILL.md` (to be merged)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-handoff\SKILL.md` (to be merged)
- `D:\GitHub\discovery-pack\skill\discovery-pack\discovery-run\SKILL.md` (to be merged)

**Acceptance Criteria:**
- [ ] Consolidate all sub-skill instructions into main SKILL.md
- [ ] Remove sub-skill directories entirely
- [ ] Represent phases as sections within unified workflow, not separate skills
- [ ] Maintain functional equivalence (all features preserved)
- [ ] Reduce total SKILL.md to <500 lines (see Issue #4)
- [ ] Verify agent can still execute phased workflow correctly
- [ ] Update any external documentation referencing sub-skills

**Implementation Steps:**

**Phase 1: Content Analysis (2 hours)**
1. Read all 8 sub-skill SKILL.md files
2. Extract unique instructions from each (eliminate duplication)
3. Identify phase-specific logic vs shared logic
4. Map sub-skill invocations to inline workflow steps

**Phase 2: Consolidation (4 hours)**
1. Create new unified workflow section in main SKILL.md:
   ```markdown
   ## Workflow Phases

   ### Phase 1: Problem Framing (discovery-frame)
   [Consolidated instructions from discovery-frame/SKILL.md]

   ### Phase 2: Constraints & NFRs (discovery-constraints)
   [Consolidated instructions from discovery-constraints/SKILL.md]

   ... (repeat for all 8 phases)
   ```
2. Convert sub-skill invocations to direct template reads + generation
3. Remove skill orchestration overhead (no more `invoke sub-skill X`)
4. Preserve phase sequencing logic in "Execution Workflow" section

**Phase 3: Cleanup (2 hours)**
1. Delete all sub-skill directories
2. Update `README.md` if it documents sub-skills
3. Search main SKILL.md for references to "invoke discovery-frame" etc. and replace
4. Test full workflow end-to-end with consolidated version

**Target Structure:**
```
skill/discovery-pack/
├── SKILL.md (<500 lines, all phases included)
├── templates/ (unchanged)
├── schemas/ (unchanged)
├── scripts/ (unchanged)
└── shared-references/ (unchanged)
```

**References:**
- Anthropic best practices on flat architecture: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#keep-it-simple
- Skills reference documentation: https://agentskills.io/specification#architecture

---

### Issue #4: SKILL.md Exceeds 500-Line Recommendation

**Priority:** P1 - High
**Effort:** 4-6 hours (after Issue #3 consolidation)
**Status:** Open
**Dependencies:** Issue #3 (must consolidate first, then trim)

**Description:**

Main SKILL.md is 549 lines, exceeding Anthropic's <500 line recommendation for optimal agent performance. After consolidating sub-skills (Issue #3), total may balloon further. Need aggressive trimming while preserving clarity.

**Current State:**
- Main SKILL.md: 549 lines
- After sub-skill consolidation: estimated 1200+ lines (unacceptable)
- Target: <500 lines total

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md`

**Acceptance Criteria:**
- [ ] Main SKILL.md reduced to <500 lines (hard target: <450)
- [ ] All critical workflow information preserved
- [ ] Move verbose content to bundled resources
- [ ] Maintain clarity for agent execution
- [ ] Progressive disclosure actually implemented (load resources on-demand)

**Implementation Steps:**

**Phase 1: Content Audit (1 hour)**
1. Categorize current content:
   - Essential (workflow steps, decision gates, tool usage)
   - Important but externalizable (methodology details, examples)
   - Redundant (repeated explanations, verbose prose)
2. Measure line count per section

**Phase 2: Extraction (2-3 hours)**
1. Move methodology deep-dive to `shared-references/methodologies.md` (already exists)
2. Create new bundled resources:
   - `workflows/lite-mode.md` - Lite mode detailed workflow
   - `workflows/full-mode.md` - Full mode detailed workflow
   - `examples/sample-execution.md` - Example execution transcript
   - `troubleshooting/common-issues.md` - Error handling guide
3. Replace verbose sections with:
   ```markdown
   ## Methodology Overview

   Uses JTBD, Amazon PR/FAQ, ADR, Lean Startup, DDD.
   → See `shared-references/methodologies.md` for details.
   ```

**Phase 3: Compression (2 hours)**
1. Convert prose to bullet points
2. Remove redundant explanations (don't repeat same concept)
3. Use tables instead of paragraphs where possible
4. Collapse "Examples" sections into single representative example
5. Replace step-by-step instructions with high-level flow + reference

**Target Outline (≈450 lines):**
```markdown
# Discovery Pack Workflow (50 lines)
- Purpose, when to activate, core methodologies

## Execution Modes (40 lines)
- Lite vs Full comparison table
- → Detailed workflows in workflows/*.md

## Workflow Sequence (80 lines)
- Step 1-7 overview with decision points
- → Phase details in workflows/*.md

## Artifact Structure (40 lines)
- YAML frontmatter requirements
- Tagging system
- → Templates in templates/*.md

## Automation Scripts (30 lines)
- Table of scripts with commands
- → Script docs in scripts/README.md

## Integration (20 lines)
- Spec-kit handoff
- → See templates/07_speckit-handoff.md

## Best Practices (30 lines)
- DO/DON'T lists (concise)

## Troubleshooting (30 lines)
- Common errors + fixes
- → Full guide in troubleshooting/common-issues.md

## Sub-Skill Phases (130 lines total, ~16 per phase)
- 8 phases x 16 lines each (compressed instructions)
- Reference templates for detailed structure
```

**References:**
- Skill-creator best practices: `~/.claude/skills/skill-creator/SKILL.md` (line 45: "Keep SKILL.md body to the essentials and under 500 lines")
- Anthropic platform docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#be-concise

---

### Issue #5: Missing Automation Script (Mode A)

**Priority:** P1 - High
**Effort:** 6-8 hours
**Status:** Open
**Dependencies:** Issue #3 (consolidation simplifies script logic)

**Description:**

SKILL.md recommends "Mode A: Automated Executor" using `discovery-pack-run.sh`, but script doesn't exist. This creates confusion between documented capability and actual implementation.

**Current Documentation (SKILL.md line 156):**
```markdown
Mode A: Automated Executor
bash ~/.copilot/skills/discovery-pack/discovery-pack-run.sh [topic-slug] [mode]
```

**Reality:**
```bash
$ ls discovery-pack-run.sh
ls: cannot access: No such file or directory
```

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\scripts\discovery-pack-run.sh` (to be created)
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (update to reference correct path)

**Acceptance Criteria:**
- [ ] Create `scripts/discovery-pack-run.sh` that orchestrates full workflow
- [ ] Support arguments: `[project-name] [mode: lite|full]`
- [ ] Automatically determine output directory
- [ ] Execute phases in sequence (lite: 3 artifacts, full: 7+1 artifacts)
- [ ] Call `extract_assumptions.py` for artifact 04
- [ ] Run `validate.py` at the end
- [ ] Generate handoff summary
- [ ] Handle errors gracefully (fail-fast with clear messages)
- [ ] Update SKILL.md with correct path and usage examples

**Implementation Steps:**

**Phase 1: Script Design (1 hour)**
1. Define CLI interface:
   ```bash
   Usage: scripts/discovery-pack-run.sh <project-name> [lite|full]

   Example:
     scripts/discovery-pack-run.sh nexus-cli-fleet full
   ```
2. Design workflow orchestration logic
3. Plan error handling and validation gates

**Phase 2: Core Implementation (4 hours)**
1. Create `scripts/discovery-pack-run.sh`:
   ```bash
   #!/bin/bash
   set -euo pipefail

   PROJECT_NAME="$1"
   MODE="${2:-lite}"
   OUTPUT_DIR="docs/discovery/$(date +%Y-%m-%d)-${PROJECT_NAME}"

   # Phase sequence based on mode
   if [[ "$MODE" == "lite" ]]; then
       PHASES=(00_problem-frame 03_option-space 07_speckit-handoff)
   else
       PHASES=(00_problem-frame 01_constraints-nfr 02_domain-model 03_option-space 05_validation-plan 06_decision-log 07_speckit-handoff)
   fi

   # Execute each phase
   for phase in "${PHASES[@]}"; do
       echo "Generating $phase..."
       # Call Claude via CLI to generate artifact
       # (This requires agent CLI integration)
   done

   # Auto-generate assumptions
   if [[ "$MODE" == "full" ]]; then
       python3 scripts/extract_assumptions.py "$OUTPUT_DIR"
   fi

   # Validate
   python3 scripts/validate.py "$OUTPUT_DIR"
   ```

2. Implement agent CLI invocation (requires research into how to invoke Claude programmatically)
3. Add pre-flight checks (Python available, templates exist, etc.)
4. Add progress indicators and logging

**Phase 3: Testing & Documentation (2 hours)**
1. Test script with sample project
2. Verify lite mode generates 3 artifacts
3. Verify full mode generates 7+1 artifacts
4. Test error handling (missing dependencies, invalid mode, etc.)
5. Update SKILL.md with usage examples
6. Create `scripts/README.md` documenting all automation scripts

**Alternative Solution:**
If automated orchestration proves infeasible (agent CLI limitations), consider:
1. Remove Mode A documentation entirely
2. Keep Mode B (manual/inline) as the only supported mode
3. Update SKILL.md to reflect reality

**References:**
- Bash scripting best practices: https://google.github.io/styleguide/shellguide.html
- Error handling in shell scripts: https://www.shellcheck.net/wiki/

---

## Medium Priority Issues (P2)

### Issue #6: Generic Skill Description Hurts Discoverability

**Priority:** P2 - Medium
**Effort:** 1 hour
**Status:** Open
**Dependencies:** None

**Description:**

Current description is too generic and doesn't communicate value proposition clearly. Needs concrete "what + when to use" according to agentskills.io spec.

**Current Description (SKILL.md line 28):**
```yaml
description: Complete project discovery workflow using Jobs-to-be-Done,
Amazon PR/FAQ, ADR, and Lean Startup validation. Transforms ambiguous
ideas into structured specifications ready for implementation. Activate
when user mentions "discovery", "requirements discovery", "project framing",
"validate assumptions", "JTBD analysis", or before starting implementation
of unclear ideas.
```

**Issues:**
- Reads like marketing copy, not functional description
- "What" is vague ("transforms ambiguous ideas")
- "When" is buried at the end
- Doesn't highlight key differentiators (7 artifacts, spec-kit integration, automation)
- Missing quantifiable benefits (token savings, time investment)

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (frontmatter)

**Acceptance Criteria:**
- [ ] Lead with concrete outcome ("Generate 7 structured artifacts...")
- [ ] Specify time investment (15-30 min lite, 1-2 hours full)
- [ ] Highlight automation benefits (35% token savings)
- [ ] Make "when to use" prominent and specific
- [ ] Stay within 1024 character limit
- [ ] A/B test with users to verify clarity improvement

**Recommended Description (draft):**
```yaml
description: |
  Generates 3-8 structured discovery artifacts (JTBD, domain models, ADRs,
  validation plans) with automated assumption extraction (~35% token savings).
  Choose lite mode (3 artifacts, 15-30 min) for small projects or full mode
  (7 artifacts, 1-2 hours) for enterprise/compliance-critical work. Outputs
  are spec-kit compatible for handoff to implementation.

  **Use when:** Starting new projects with unclear requirements, comparing
  technical approaches, validating assumptions, or generating spec-driven
  blueprints. **Don't use for:** Well-defined implementation tasks or quick
  prototypes without rigorous discovery.
```

**Character count:** 587/1024 ✓

**Implementation Steps:**
1. Draft 3-5 alternative descriptions
2. Test each with `skills-ref validate` if available
3. Get feedback from 2-3 users on clarity
4. Select best performing description
5. Update SKILL.md frontmatter

**References:**
- agentskills.io specification: https://agentskills.io/specification#description-field
- Anthropic skill description guidelines: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#write-clear-descriptions

---

### Issue #7: Missing Concrete Output Examples

**Priority:** P2 - Medium
**Effort:** 3-4 hours
**Status:** Open
**Dependencies:** Issue #1 (need valid artifacts first)

**Description:**

SKILL.md lacks concrete examples of what generated artifacts look like. Agent and users can't visualize expected output quality/structure without seeing real examples.

**Current State:**
- No example artifacts in repository
- No screenshots or snippets in documentation
- Only template structure shown (which is input, not output)

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\examples\` (directory to be created)
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (add references to examples)

**Acceptance Criteria:**
- [ ] Create `examples/` directory with complete sample project
- [ ] Include all 8 artifacts from real execution (use NEXUS CLI FLEET as basis)
- [ ] Artifacts must pass schema validation (requires Issue #1 fix)
- [ ] Add README in examples/ explaining the sample project
- [ ] Reference examples in SKILL.md "Example Execution" section
- [ ] Include both lite and full mode examples

**Implementation Steps:**

**Phase 1: Sample Project Selection (30 min)**
1. Use existing NEXUS CLI FLEET execution as base
2. Fix validation issues in those artifacts (apply Issue #1 fixes)
3. Rename/sanitize if needed for public sharing

**Phase 2: Example Creation (2 hours)**
1. Create directory structure:
   ```
   examples/
   ├── README.md
   ├── lite-mode-sample/
   │   ├── 00_problem-frame.md
   │   ├── 03_option-space.md
   │   └── 07_speckit-handoff.md
   └── full-mode-sample/
       ├── 00_problem-frame.md
       ├── 01_constraints-nfr.md
       ├── 02_domain-model.md
       ├── 03_option-space.md
       ├── 04_assumptions-unknowns.md
       ├── 05_validation-plan.md
       ├── 06_decision-log.md
       └── 07_speckit-handoff.md
   ```

2. Validate all artifacts:
   ```bash
   python scripts/validate.py examples/lite-mode-sample/
   python scripts/validate.py examples/full-mode-sample/
   ```

3. Write `examples/README.md`:
   ```markdown
   # Discovery Pack Examples

   ## Lite Mode Sample

   **Project:** Simple CLI tool for developer workflow
   **Time invested:** 22 minutes
   **Artifacts:** 3

   See `lite-mode-sample/` for complete output.

   ## Full Mode Sample

   **Project:** Enterprise multi-CLI orchestration system
   **Time invested:** 1.5 hours
   **Artifacts:** 8 (including auto-generated assumptions)

   See `full-mode-sample/` for complete output.
   ```

**Phase 3: Integration with SKILL.md (1 hour)**
1. Add new section to SKILL.md:
   ```markdown
   ## Example Output

   Want to see what discovery-pack generates? Check:
   - **Lite mode (3 artifacts):** `examples/lite-mode-sample/`
   - **Full mode (8 artifacts):** `examples/full-mode-sample/`

   Both examples include passing schema validation.
   ```

2. Reference examples in "When to Use" section
3. Link to examples in error messages/troubleshooting

**Phase 4: Optional Enhancements (30 min)**
1. Add annotated version highlighting key sections
2. Create diff showing lite → full evolution
3. Include metrics (line counts, tag usage, assumption extraction results)

**References:**
- Documentation best practices: https://documentation.divio.com/tutorials/
- Example-driven learning: https://www.nngroup.com/articles/example-driven-design/

---

### Issue #8: Progressive Disclosure Not Implemented

**Priority:** P2 - Medium
**Effort:** 2-3 hours
**Status:** Open
**Dependencies:** Issue #3, Issue #4 (consolidation and trimming enable this)

**Description:**

SKILL.md claims to use progressive disclosure ("Load Level 3 resources only when needed") but actually loads all templates eagerly during execution. This wastes tokens and violates the skill architecture pattern.

**Current Behavior:**
```markdown
Phase 1/3: Problem framing with JTBD...
[Read template 00_problem-frame.md]  ← Always loaded
[Generate artifact]
...
```

**Expected Behavior:**
```markdown
Phase 1/3: Problem framing with JTBD...
→ Template: templates/00_problem-frame.md (load on-demand)
[Generate artifact without pre-reading entire template]
```

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (workflow instructions)

**Acceptance Criteria:**
- [ ] SKILL.md provides high-level instructions only
- [ ] Templates referenced but not quoted inline
- [ ] Agent loads templates only when generating that specific artifact
- [ ] Measure token reduction (expect 20-30% savings in discovery phase)
- [ ] Maintain output quality (no degradation from on-demand loading)

**Implementation Steps:**

**Phase 1: Instruction Refactoring (1 hour)**
1. Remove verbose template excerpts from SKILL.md workflow section
2. Replace with references:
   ```markdown
   # Before (verbose)
   Phase 1: Problem Framing
   Read the template from templates/00_problem-frame.md:
   [50 lines of template structure quoted here]

   Fill the following sections:
   - Problem Statement: [detailed instructions]
   - User Personas: [detailed instructions]
   ...

   # After (progressive)
   Phase 1: Problem Framing
   Generate `00_problem-frame.md` using template structure.
   → Reference: templates/00_problem-frame.md

   Focus on:
   - JTBD analysis (jobs, context, outcomes)
   - North star metric (quantifiable, time-bound)
   - Tag all assumptions
   ```

**Phase 2: Execution Model (1 hour)**
1. Update workflow instructions to say:
   ```markdown
   ## Execution Model

   For each phase:
   1. Read high-level goals from this SKILL.md
   2. Load template from templates/ only when ready to generate
   3. Generate artifact following template structure
   4. Mark phase complete, move to next

   Do NOT pre-read all templates at workflow start.
   ```

**Phase 3: Validation (30 min)**
1. Test with new execution and measure token usage:
   - Baseline (current): ~X tokens
   - After progressive disclosure: ~Y tokens
   - Expected savings: 20-30%
2. Verify output quality unchanged
3. Update documentation with token efficiency metrics

**Phase 4: Best Practices Documentation (30 min)**
1. Add to SKILL.md:
   ```markdown
   ## Token Efficiency

   This skill uses progressive disclosure:
   - Level 1: Core workflow (SKILL.md)
   - Level 2: Template structure (loaded per-phase)
   - Level 3: Methodology details (loaded on-demand when clarification needed)

   Expected token usage:
   - Lite mode: ~5-8k tokens
   - Full mode: ~15-25k tokens
   - Automation scripts save additional ~35%
   ```

**References:**
- Progressive disclosure pattern: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#progressive-disclosure
- Token optimization: https://www.anthropic.com/research/context-efficiency

---

## Low Priority / Optional Enhancements (P3)

### Issue #9: Create Evaluation Framework

**Priority:** P3 - Low (Optional)
**Effort:** 8-12 hours
**Status:** Open
**Dependencies:** Issue #1 (need valid artifacts to test against)

**Description:**

No systematic way to test skill quality, regression test after changes, or benchmark improvements. Need evaluation framework with test cases and metrics.

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\tests\` (new directory)
- `D:\GitHub\discovery-pack\skill\discovery-pack\scripts\run_evaluation.py` (new script)

**Acceptance Criteria:**
- [ ] Create test suite with 5+ sample projects (varying complexity)
- [ ] Define quality metrics (schema validation, tag coverage, assumption extraction rate)
- [ ] Implement automated evaluation script
- [ ] Establish baseline scores for current version
- [ ] Track improvements over time
- [ ] CI/CD integration (optional)

**Implementation Steps:**

**Phase 1: Test Projects (3 hours)**
1. Create `tests/projects/` with 5 diverse scenarios:
   - `simple-cli/` - Personal tool (lite mode baseline)
   - `web-dashboard/` - Greenfield web app (full mode)
   - `enterprise-integration/` - Compliance-heavy (full mode, max constraints)
   - `mobile-app/` - Cross-platform mobile (domain modeling emphasis)
   - `ml-pipeline/` - Data science workflow (validation emphasis)

2. For each, create:
   - `input.md` - Project description (what user would provide)
   - `expected-lite/` - Expected lite mode output (3 artifacts)
   - `expected-full/` - Expected full mode output (8 artifacts)

**Phase 2: Metrics Definition (2 hours)**
1. Define quality dimensions:
   ```python
   metrics = {
       'schema_validation': {
           'weight': 0.30,
           'measure': lambda: passing_artifacts / total_artifacts
       },
       'tag_coverage': {
           'weight': 0.20,
           'measure': lambda: tagged_statements / total_statements
       },
       'assumption_extraction': {
           'weight': 0.15,
           'measure': lambda: extracted_assumptions / manual_count
       },
       'completion_rate': {
           'weight': 0.20,
           'measure': lambda: generated_artifacts / expected_artifacts
       },
       'spec_kit_compatibility': {
           'weight': 0.15,
           'measure': lambda: validate_handoff_artifact()
       }
   }
   ```

2. Document acceptable thresholds:
   - Schema validation: 100% (hard requirement)
   - Tag coverage: ≥60%
   - Assumption extraction: ≥90%
   - Completion rate: 100%
   - Spec-kit compatibility: Pass/Fail

**Phase 3: Evaluation Script (4 hours)**
1. Create `scripts/run_evaluation.py`:
   ```python
   #!/usr/bin/env python3
   """
   Discovery Pack Evaluation Framework

   Usage:
       python scripts/run_evaluation.py [--mode lite|full|both]
   """

   import json
   from pathlib import Path
   from typing import Dict, List

   def evaluate_project(project_dir: Path, mode: str) -> Dict:
       """Run discovery and compare against expected output."""
       # Invoke skill with project input
       # Compare generated vs expected
       # Calculate metrics
       pass

   def run_all_tests() -> Dict:
       """Run evaluation on all test projects."""
       results = {}
       for project in Path('tests/projects').iterdir():
           results[project.name] = {
               'lite': evaluate_project(project, 'lite'),
               'full': evaluate_project(project, 'full')
           }
       return results

   def generate_report(results: Dict) -> str:
       """Generate markdown report with scores."""
       # Overall score (weighted average)
       # Per-project breakdown
       # Regression detection (compare to baseline)
       pass

   if __name__ == '__main__':
       results = run_all_tests()
       report = generate_report(results)
       print(report)
       Path('tests/evaluation-report.md').write_text(report)
   ```

2. Implement comparison logic:
   - Schema validation via existing `validate.py`
   - Tag coverage via regex counting
   - Assumption extraction diff
   - Content similarity scoring (optional: use embeddings)

**Phase 4: Baseline & Tracking (2 hours)**
1. Run evaluation on current version (pre-fixes)
2. Save baseline scores to `tests/baseline.json`
3. After each major fix (Issues #1-8), re-run and compare
4. Document improvements in `tests/changelog.md`

**Phase 5: Optional - CI Integration (1 hour)**
1. Create `.github/workflows/evaluate-skill.yml`
2. Run on every PR to skill files
3. Fail if schema validation drops below 100%
4. Post results as PR comment

**Expected Outcome:**
```
Discovery Pack Evaluation Report
Generated: 2026-01-07

Overall Score: 7.8/10 (+2.6 from baseline)

Project Breakdown:
  simple-cli (lite):     9.2/10  ✓ All metrics pass
  web-dashboard (full):  8.1/10  ⚠ Tag coverage 58% (target: 60%)
  enterprise (full):     7.5/10  ⚠ 1 schema validation failure
  mobile-app (full):     7.2/10  ⚠ Assumption extraction 85% (target: 90%)
  ml-pipeline (full):    8.0/10  ✓ All metrics pass

Regression Detected: None
Improvements Since Baseline:
  - Schema validation: 12.5% → 87.5% (+75pp)
  - Tag coverage: 65% → 68% (+3pp)
  - Assumption extraction: 89% → 94% (+5pp)
```

**References:**
- Software testing best practices: https://martinfowler.com/articles/practical-test-pyramid.html
- Skill evaluation patterns: (create internal doc)

---

### Issue #10: Add Interactive Mode for Lite/Full Selection

**Priority:** P3 - Low (Optional)
**Effort:** 2-3 hours
**Status:** Open
**Dependencies:** None

**Description:**

Current mode selection requires user to understand lite vs full tradeoffs upfront. Could improve UX with interactive questionnaire that recommends mode based on project characteristics.

**Current Experience:**
```
Discovery mode selection:
- lite (3 artifacts): Small projects, < 5 people, low risk [15-30 min]
- full (7 artifacts): Enterprise, compliance, security-critical [1-2 hours]

Your choice: lite | full | (auto-detect from project context)
```

**Proposed Experience:**
```
Let's determine the right discovery mode for your project.

Question 1/3: What's your team size?
  a) Solo or 2-3 people
  b) 4-10 people
  c) 10+ people

Question 2/3: What's the risk profile?
  a) Personal project or low-stakes
  b) Production system but non-critical
  c) Financial, healthcare, or compliance-critical

Question 3/3: How well-defined are your requirements?
  a) Very unclear, exploring possibilities
  b) Partially defined, some unknowns
  c) Mostly clear, need documentation

Based on your answers (a, c, a):
→ Recommended: lite mode (3 artifacts, ~20 minutes)
→ Reason: Small team + low risk, even with unclear requirements

Proceed with lite mode? [Y/n]
```

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (add questionnaire logic)
- `D:\GitHub\discovery-pack\skill\discovery-pack\scripts\mode-selector.py` (optional helper script)

**Acceptance Criteria:**
- [ ] Ask 3-5 questions covering: team size, risk, compliance, timeline, existing docs
- [ ] Use decision tree to recommend mode
- [ ] Explain recommendation reasoning
- [ ] Allow override (user can choose opposite mode)
- [ ] Track mode selection accuracy over time (collect feedback)

**Implementation Steps:**

**Phase 1: Decision Tree Design (1 hour)**
1. Map project characteristics to mode recommendation:
   ```
   Decision Factors:
   - Team size: 1-3 → lite, 4-9 → either, 10+ → full
   - Risk: low → lite, medium → either, high → full
   - Compliance: none → lite, some → either, strict → full
   - Timeline: <1 week → lite, 1-4 weeks → either, >1 month → full
   - Documentation: none → full, some → either, extensive → lite

   Scoring:
   - Each factor contributes points
   - Lite: 0-4 points
   - Full: 5-10 points
   ```

2. Create questionnaire:
   - Minimum 3 questions (team, risk, compliance)
   - Maximum 5 questions (add timeline, documentation if needed)

**Phase 2: Integration (1.5 hours)**
1. Add questionnaire to SKILL.md workflow:
   ```markdown
   ### Step 1: Determine Mode

   Instead of asking directly, guide the user:

   > **Let's find the right discovery mode.**
   >
   > **Q1:** Team size?
   > a) Solo/2-3  b) 4-10  c) 10+
   >
   > **Q2:** Risk profile?
   > a) Personal/low  b) Production non-critical  c) High-stakes/compliance
   >
   > **Q3:** Requirement clarity?
   > a) Very unclear  b) Partially defined  c) Mostly clear

   Calculate recommendation:
   - Mostly 'a' → lite
   - Mostly 'c' → full
   - Mixed → explain both, let user choose
   ```

**Phase 3: Optional Script (30 min)**
1. Create `scripts/mode-selector.py` for non-interactive environments:
   ```python
   #!/usr/bin/env python3
   import sys

   def recommend_mode(team_size: int, risk: str, clarity: str) -> str:
       score = 0
       if team_size >= 10: score += 2
       if risk in ['high', 'compliance']: score += 3
       if clarity == 'unclear': score += 1

       return 'full' if score >= 5 else 'lite'

   if __name__ == '__main__':
       # CLI usage: python mode-selector.py --team 3 --risk low --clarity unclear
       # Output: lite
       pass
   ```

**Phase 4: Feedback Loop (30 min)**
1. After discovery completion, ask:
   ```
   Was [lite/full] mode the right choice for this project?
   - Yes, perfect fit
   - Somewhat, but [lite/full] would have been better
   - No, should have used [lite/full]

   (Optional) Why? [free text]
   ```
2. Log responses to improve decision tree

**References:**
- Conversational UX patterns: https://www.nngroup.com/articles/conversational-ui/
- Decision tree algorithms: https://scikit-learn.org/stable/modules/tree.html

---

### Issue #11: Multi-Language Template Support

**Priority:** P3 - Low (Optional)
**Effort:** 6-8 hours
**Status:** Open
**Dependencies:** Issue #1 (sync schemas first)

**Description:**

All templates and artifacts are in English. For global teams, supporting Portuguese, Spanish, French, etc. would improve usability. Implement i18n for templates while keeping schemas language-agnostic.

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\templates\` (add `templates/pt/`, `templates/es/`, etc.)
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (add language selection)

**Acceptance Criteria:**
- [ ] Support at minimum: English (en), Portuguese (pt), Spanish (es)
- [ ] Translate all 8 artifact templates
- [ ] Keep schemas in English (YAML keys language-agnostic)
- [ ] Add language selection to mode selection step
- [ ] Maintain schema validation compatibility across languages
- [ ] Document translation contribution process

**Implementation Steps:**

**Phase 1: Template Translation (4 hours)**
1. Create language directories:
   ```
   templates/
   ├── en/ (existing templates moved here)
   │   ├── 00_problem-frame.md
   │   └── ...
   ├── pt/
   │   ├── 00_problem-frame.md (Portuguese translation)
   │   └── ...
   └── es/
       ├── 00_problem-frame.md (Spanish translation)
       └── ...
   ```

2. Translate template markdown content (not YAML keys):
   ```markdown
   # English (templates/en/00_problem-frame.md)
   ## Problem Statement
   Describe the core problem this project aims to solve.

   # Portuguese (templates/pt/00_problem-frame.md)
   ## Declaração do Problema
   Descreva o problema central que este projeto visa resolver.

   # Spanish (templates/es/00_problem-frame.md)
   ## Declaración del Problema
   Describe el problema central que este proyecto busca resolver.
   ```

3. Keep YAML frontmatter keys in English (schemas expect English keys)

**Phase 2: Language Selection (1 hour)**
1. Add to mode selection workflow:
   ```
   Discovery mode: lite
   Language / Idioma / Idioma: [en|pt|es]
   ```

2. Update SKILL.md to reference language-specific templates:
   ```markdown
   Phase 1: Problem Framing
   Template: templates/{language}/00_problem-frame.md
   ```

**Phase 3: Validation (1 hour)**
1. Test schema validation with all language templates
2. Ensure YAML frontmatter keys match across languages
3. Fix any language-specific issues

**Phase 4: Documentation (1 hour)**
1. Create `CONTRIBUTING.md` with translation guidelines
2. Document how to add new languages
3. Create translation template checklist

**Phase 5: Optional - Professional Translation (external)**
1. Use machine translation (DeepL, GPT) for initial versions
2. Recommend professional translation for production
3. Community contributions for additional languages

**Limitations:**
- Methodology references (JTBD, ADR) may remain in English (standard terminology)
- Skill documentation (SKILL.md) stays in English (agent interface)
- Only artifact templates translated (user-facing content)

**References:**
- i18n best practices: https://www.w3.org/International/questions/qa-i18n
- YAML localization: https://yaml.org/spec/1.2.2/#example-multi-language-document

---

### Issue #12: Add Pre-Flight Dependency Checker

**Priority:** P3 - Low (Optional)
**Effort:** 2-3 hours
**Status:** Open
**Dependencies:** None

**Description:**

Current workflow assumes Python + dependencies are available. Should check upfront and provide helpful setup instructions if missing.

**Current Experience:**
```
Phase 1/3: Problem framing...
[Attempt automation]
Error: python3: command not found
[Fallback to manual mode, confusing for user]
```

**Proposed Experience:**
```
Discovery Pack Pre-Flight Check
--------------------------------
✓ Output directory writable
✓ Python 3.11+ installed (3.12.1 found)
✗ Required packages missing
  → Run: pip install -r scripts/requirements.txt

✓ Git repository detected
✗ 'gh' CLI not found (optional, for GitHub integration)

2/4 critical checks passed. Install missing dependencies? [Y/n]
```

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\scripts\pre-flight-check.sh` (to be created)
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (reference in Step 1.5)

**Acceptance Criteria:**
- [ ] Check Python version (≥3.11)
- [ ] Check required packages (jsonschema, pyyaml)
- [ ] Check write permissions to output directory
- [ ] Check git repository (warn if missing, but not required)
- [ ] Check optional tools (gh CLI, uv, speckit)
- [ ] Provide install commands for missing dependencies
- [ ] Exit codes: 0=ready, 1=missing critical, 2=missing optional

**Implementation Steps:**

**Phase 1: Script Creation (1.5 hours)**
1. Create `scripts/pre-flight-check.sh`:
   ```bash
   #!/bin/bash

   echo "Discovery Pack Pre-Flight Check"
   echo "--------------------------------"

   CRITICAL_PASS=0
   CRITICAL_TOTAL=0

   # Check Python
   CRITICAL_TOTAL=$((CRITICAL_TOTAL + 1))
   if command -v python3 >/dev/null 2>&1; then
       VERSION=$(python3 --version | cut -d' ' -f2)
       MAJOR=$(echo $VERSION | cut -d'.' -f1)
       MINOR=$(echo $VERSION | cut -d'.' -f2)
       if [[ $MAJOR -ge 3 && $MINOR -ge 11 ]]; then
           echo "✓ Python 3.11+ installed ($VERSION)"
           CRITICAL_PASS=$((CRITICAL_PASS + 1))
       else
           echo "✗ Python $VERSION < 3.11"
           echo "  → Install Python 3.11+: https://python.org"
       fi
   else
       echo "✗ Python 3 not found"
       echo "  → Install: https://python.org"
   fi

   # Check packages
   CRITICAL_TOTAL=$((CRITICAL_TOTAL + 1))
   if python3 -c "import jsonschema, yaml" 2>/dev/null; then
       echo "✓ Required packages installed"
       CRITICAL_PASS=$((CRITICAL_PASS + 1))
   else
       echo "✗ Required packages missing"
       echo "  → Run: pip install -r scripts/requirements.txt"
   fi

   # Check output directory
   CRITICAL_TOTAL=$((CRITICAL_TOTAL + 1))
   OUTPUT_DIR="${1:-docs/discovery}"
   if mkdir -p "$OUTPUT_DIR" 2>/dev/null; then
       echo "✓ Output directory writable ($OUTPUT_DIR)"
       CRITICAL_PASS=$((CRITICAL_PASS + 1))
   else
       echo "✗ Cannot write to $OUTPUT_DIR"
       echo "  → Check permissions or specify different directory"
   fi

   # Optional checks
   if git rev-parse --git-dir >/dev/null 2>&1; then
       echo "✓ Git repository detected"
   else
       echo "⚠ Not a git repository (optional)"
   fi

   if command -v gh >/dev/null 2>&1; then
       echo "✓ GitHub CLI available"
   else
       echo "⚠ 'gh' CLI not found (optional, for GitHub integration)"
   fi

   echo "--------------------------------"
   echo "$CRITICAL_PASS/$CRITICAL_TOTAL critical checks passed"

   if [[ $CRITICAL_PASS -eq $CRITICAL_TOTAL ]]; then
       echo "✓ Ready to run discovery workflow"
       exit 0
   elif [[ $CRITICAL_PASS -gt 0 ]]; then
       echo "⚠ Some checks failed (see above)"
       exit 2
   else
       echo "✗ Critical dependencies missing"
       exit 1
   fi
   ```

2. Make executable: `chmod +x scripts/pre-flight-check.sh`

**Phase 2: Integration (30 min)**
1. Update SKILL.md Step 1.5:
   ```markdown
   ### Step 1.5: Check Dependencies

   Run pre-flight check:
   ```bash
   bash scripts/pre-flight-check.sh
   ```

   If checks fail, guide user to install missing dependencies.
   ```

**Phase 3: Requirements File (30 min)**
1. Create `scripts/requirements.txt`:
   ```
   jsonschema>=4.17.0
   PyYAML>=6.0
   ```

2. Document in `scripts/README.md`

**Phase 4: Optional - Auto-Install (30 min)**
1. Add option to pre-flight script:
   ```bash
   # At end of script
   if [[ $CRITICAL_PASS -lt $CRITICAL_TOTAL ]]; then
       read -p "Install missing dependencies? [Y/n] " -r
       if [[ $REPLY =~ ^[Yy]$ ]]; then
           pip install -r scripts/requirements.txt
           echo "Re-running checks..."
           exec "$0" "$@"
       fi
   fi
   ```

**References:**
- Shell script dependency checking: https://www.shellcheck.net/
- Python package management: https://packaging.python.org/

---

## Documentation & Maintenance Tasks

### Issue #13: Create Comprehensive README

**Priority:** P2 - Medium
**Effort:** 2-3 hours
**Status:** Open
**Dependencies:** None (can be done anytime)

**Description:**

Repository likely has minimal or outdated README. Need comprehensive documentation covering installation, quick start, examples, troubleshooting, and contribution guidelines.

**Files Affected:**
- `D:\GitHub\discovery-pack\README.md` (to be created/updated)
- `D:\GitHub\discovery-pack\docs\` (optional extended docs directory)

**Acceptance Criteria:**
- [ ] Clear value proposition (what + why)
- [ ] Quick start guide (5 minutes to first artifact)
- [ ] Installation instructions (all environments)
- [ ] Usage examples (lite and full mode)
- [ ] Troubleshooting section
- [ ] Links to methodology references
- [ ] Contribution guidelines
- [ ] License and credits

**Recommended Structure:**
```markdown
# Discovery Pack

> Transform ambiguous ideas into structured specifications using JTBD, ADR, and Lean Startup methodologies.

## Quick Start

```bash
# 1. Install (if not already in Claude Code skills)
git clone https://github.com/your-org/discovery-pack
cp -r discovery-pack/skill/discovery-pack ~/.claude/skills/

# 2. Run discovery
cd your-project
claude
> /discovery-pack "my-project-name"
```

## What You Get

- **Lite Mode (15-30 min):** 3 artifacts - Problem frame, Options, Handoff
- **Full Mode (1-2 hours):** 8 artifacts - + Constraints, Domain model, Validation, Decisions, Assumptions

All outputs are [spec-kit](https://github.com/github/spec-kit) compatible.

## Features

- ✅ Automated assumption extraction (~35% token savings)
- ✅ Schema validation for artifact quality
- ✅ Epistemic tagging (FACT/ASSUMPTION/HYPOTHESIS)
- ✅ Integration with spec-kit for implementation handoff

## Installation

[Detailed instructions for Claude Code, Copilot, Gemini, etc.]

## Usage

[Examples with screenshots or output samples]

## Troubleshooting

[Common errors and solutions]

## Methodology

Based on:
- Jobs-to-be-Done (Clayton Christensen)
- Amazon PR/FAQ (Working Backwards)
- Architecture Decision Records (Michael Nygard)
- Lean Startup (Eric Ries)
- Domain-Driven Design (Eric Evans)

## Contributing

[Guidelines for contributing]

## License

[License info]
```

**Implementation Steps:**
1. Draft README following structure above
2. Add badges (if applicable): build status, version, license
3. Include screenshots/GIFs of execution
4. Link to example outputs
5. Review and polish

**References:**
- README best practices: https://www.makeareadme.com/
- Documentation guide: https://documentation.divio.com/

---

### Issue #14: Version Tracking and Changelog

**Priority:** P3 - Low (Optional)
**Effort:** 1 hour
**Status:** Open
**Dependencies:** None

**Description:**

No version tracking for skill evolution. Should implement semantic versioning and maintain changelog for users to understand changes/improvements.

**Files Affected:**
- `D:\GitHub\discovery-pack\skill\discovery-pack\SKILL.md` (add version to frontmatter)
- `D:\GitHub\discovery-pack\CHANGELOG.md` (to be created)
- `D:\GitHub\discovery-pack\VERSION` (to be created)

**Acceptance Criteria:**
- [ ] Add version to skill frontmatter
- [ ] Create CHANGELOG.md following Keep a Changelog format
- [ ] Document all changes from Issues #1-13
- [ ] Use semantic versioning (MAJOR.MINOR.PATCH)
- [ ] Update version after each significant change

**Implementation Steps:**

**Phase 1: Version Setup (20 min)**
1. Create `VERSION` file:
   ```
   0.9.0
   ```

2. Update SKILL.md frontmatter:
   ```yaml
   ---
   name: discovery-pack
   description: [updated description from Issue #6]
   metadata:
     discovery_pack_version: "0.9.0"
     last_updated: "2026-01-07"
   ---
   ```

**Phase 2: Changelog Creation (40 min)**
1. Create `CHANGELOG.md`:
   ```markdown
   # Changelog

   All notable changes to Discovery Pack will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
   and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

   ## [Unreleased]

   ### Added
   - Interactive mode selection questionnaire (#10)
   - Multi-language template support (PT, ES) (#11)
   - Pre-flight dependency checker (#12)
   - Comprehensive evaluation framework (#9)

   ### Fixed
   - Template-schema synchronization (7/8 artifacts now pass validation) (#1)
   - Hardcoded paths replaced with relative paths (#2)
   - SKILL.md reduced to <500 lines (#4)

   ### Changed
   - Consolidated sub-skills into flat architecture (#3)
   - Improved skill description for discoverability (#6)
   - Progressive disclosure actually implemented (#8)

   ### Removed
   - 8 sub-skill directories (consolidated into main SKILL.md) (#3)

   ## [0.9.0] - 2026-01-07

   ### Added
   - Initial public release
   - Full and lite mode workflows
   - 8 artifact templates with YAML schemas
   - Automation scripts (extract_assumptions.py, validate.py)
   - Spec-kit integration

   ### Known Issues
   - 7/8 artifacts fail schema validation (to be fixed in 1.0.0)
   - Sub-skills architecture violates flat standard
   - Hardcoded paths break portability

   [Unreleased]: https://github.com/your-org/discovery-pack/compare/v0.9.0...HEAD
   [0.9.0]: https://github.com/your-org/discovery-pack/releases/tag/v0.9.0
   ```

**Phase 3: Version Bumping Strategy (10 min)**
1. Document versioning rules:
   - MAJOR: Breaking changes (workflow changes, schema changes)
   - MINOR: New features (new templates, automation scripts)
   - PATCH: Bug fixes (schema sync, typos, documentation)

2. Example:
   - Fix Issue #1 (schemas): 0.9.0 → 0.9.1 (PATCH)
   - Add Issue #9 (eval framework): 0.9.1 → 0.10.0 (MINOR)
   - Consolidate Issue #3 (breaking workflow change): 0.10.0 → 1.0.0 (MAJOR)

**References:**
- Semantic Versioning: https://semver.org/
- Keep a Changelog: https://keepachangelog.com/

---

## Implementation Roadmap

### Phase 1: Critical Fixes (Must Have) - 20-25 hours
Execute in order:
1. Issue #2 - Fix hardcoded paths (2-3h) ← Start here (unblocks testing)
2. Issue #1 - Sync templates & schemas (6-8h) ← Critical for validation
3. Issue #3 - Consolidate sub-skills (8-10h) ← Architectural foundation
4. Issue #4 - Reduce SKILL.md size (4-6h) ← Must follow #3

**Milestone:** v1.0.0-beta (all artifacts pass validation, flat architecture)

### Phase 2: High Priority (Should Have) - 12-18 hours
5. Issue #5 - Create automation script or remove Mode A (6-8h)
6. Issue #6 - Improve description (1h)
7. Issue #7 - Add examples (3-4h) ← Requires #1 fixed first
8. Issue #8 - Implement progressive disclosure (2-3h) ← Requires #3, #4

**Milestone:** v1.0.0 (production-ready, optimized)

### Phase 3: Enhancements (Nice to Have) - 20-30 hours
9. Issue #9 - Evaluation framework (8-12h)
10. Issue #10 - Interactive mode selector (2-3h)
11. Issue #11 - Multi-language support (6-8h)
12. Issue #12 - Pre-flight checker (2-3h)
13. Issue #13 - README (2-3h)
14. Issue #14 - Versioning (1h)

**Milestone:** v1.1.0 (full-featured, enterprise-ready)

---

## Acceptance Testing

After completing all critical fixes (Issues #1-4), run full acceptance test:

```bash
# 1. Clean install
rm -rf ~/.claude/skills/discovery-pack
cp -r skill/discovery-pack ~/.claude/skills/

# 2. Run pre-flight
bash ~/.claude/skills/discovery-pack/scripts/pre-flight-check.sh

# 3. Test lite mode
cd /tmp/test-project-lite
claude --eval "/discovery-pack test-lite lite"

# 4. Validate output
python ~/.claude/skills/discovery-pack/scripts/validate.py docs/discovery/*

# Expected: 3/3 artifacts pass ✓

# 5. Test full mode
cd /tmp/test-project-full
claude --eval "/discovery-pack test-full full"

# 6. Validate output
python ~/.claude/skills/discovery-pack/scripts/validate.py docs/discovery/*

# Expected: 8/8 artifacts pass ✓

# 7. Test automation
python ~/.claude/skills/discovery-pack/scripts/extract_assumptions.py docs/discovery/*

# Expected: 04_assumptions-unknowns.md generated with >0 assumptions ✓

# 8. Test spec-kit integration
# Copy handoff sections to spec-kit and verify format
```

**Success Criteria:**
- [ ] 100% schema validation pass rate (8/8 artifacts)
- [ ] No hardcoded paths in any SKILL.md
- [ ] Single SKILL.md <500 lines
- [ ] All automation scripts execute without errors
- [ ] Example artifacts available and validated
- [ ] Progressive disclosure reduces token usage by 20-30%

---

## Contributing

When implementing these tasks:

1. **Create feature branch:** `git checkout -b fix/issue-{number}-{slug}`
2. **Reference issue:** Commit messages should reference issue number
3. **Test thoroughly:** Run validation suite before PR
4. **Update changelog:** Add entry to CHANGELOG.md [Unreleased] section
5. **Bump version:** Update VERSION file according to semver rules
6. **Document:** Update README if user-facing changes

---

## External References

- **Anthropic Agent Skills:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- **agentskills.io Spec:** https://agentskills.io/specification
- **GitHub Spec-Kit:** https://github.com/github/spec-kit
- **JSON Schema:** https://json-schema.org/understanding-json-schema/
- **YAML Spec:** https://yaml.org/spec/1.2.2/
- **Semantic Versioning:** https://semver.org/
- **Keep a Changelog:** https://keepachangelog.com/

---

**Total Estimated Effort:** 52-73 hours
- Critical (P0): 20-25 hours
- High (P1): 12-18 hours
- Medium/Optional (P2-P3): 20-30 hours

**Prioritization Recommendation:**
Execute Phase 1 (Issues #1-4) immediately to achieve production-ready status. Phase 2 and 3 can be scheduled based on user feedback and team capacity.

---

*Generated: 2026-01-07*
*Analysis Base: NEXUS CLI FLEET discovery execution + skill standards investigation*
*Target Score: 5.2/10 → 9.0+/10 after Phase 1+2 completion*
