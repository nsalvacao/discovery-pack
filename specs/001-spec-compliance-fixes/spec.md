# Feature Specification: Anthropic Skills Specification Compliance Fixes

**Feature Branch**: `001-spec-compliance-fixes`  
**Created**: 2026-01-07  
**Status**: Draft  
**Input**: Fix P0-P1 critical compliance violations: schema-template sync, hardcoded paths, sub-skills consolidation, SKILL.md size reduction to achieve 100% Anthropic Skills specification compliance

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Schema Validation Success (Priority: P0)

**As a** skill user running discovery workflow  
**I want** all generated artifacts to pass JSON schema validation  
**So that** I can confidently use discovery-pack output in downstream tools (spec-kit, automation scripts) without validation errors blocking my workflow.

**Why this priority**: Currently 7/8 artifacts fail validation, breaking automation and undermining trust. This is the most critical blocker preventing production use.

**Independent Test**: Run \`python scripts/validate.py\` on generated lite mode artifacts (00, 03, 07). All 3 MUST pass validation with zero errors.

**Acceptance Scenarios**:

1. **Given** lite mode execution completes, **When** user runs \`scripts/validate.py docs/discovery/project/\`, **Then** 3/3 artifacts pass validation with output "✓ All artifacts valid"
2. **Given** full mode execution completes, **When** user runs \`scripts/validate.py docs/discovery/project/\`, **Then** 8/8 artifacts pass validation with zero schema errors
3. **Given** template 00_problem-frame.md is used, **When** agent generates artifact with all required fields, **Then** YAML frontmatter matches schema exactly (no missing fields, correct types, valid enum values)
4. **Given** artifact 03_option-space.md contains vendor_lock_in field, **When** validation runs, **Then** enum values match schema exactly ("low", "medium", "high" only - not "none")

---

### User Story 2 - Cross-Agent Portability (Priority: P0)

**As a** user switching between Claude Code, Copilot CLI, or other agents  
**I want** discovery-pack to work identically regardless of agent  
**So that** I can choose my preferred tooling without skill lock-in or unexpected failures.

**Why this priority**: Hardcoded \`~/.copilot/\` paths break portability, violating Principle III and preventing 40%+ of potential users (non-Copilot agents) from using the skill.

**Independent Test**: Install skill in Claude Code (\`~/.claude/skills/\`) and run lite mode. All scripts MUST execute without "file not found" errors.

**Acceptance Scenarios**:

1. **Given** skill installed in \`~/.claude/skills/discovery-pack/\`, **When** user invokes discovery-run in Claude Code, **Then** all scripts execute using relative paths (no \`~/.copilot\` references)
2. **Given** skill installed in project-local \`.claude/skills/\`, **When** user runs pre-flight check, **Then** script locates templates/schemas via relative paths from skill root
3. **Given** SKILL.md contains script invocations, **When** agent parses instructions, **Then** zero absolute paths to \`~/.copilot/\` or \`~/.claude/\` exist (grep test passes)
4. **Given** user runs discovery in any agent, **When** automation scripts execute, **Then** \`scripts/validate.py\` and \`scripts/extract_assumptions.py\` locate schemas/templates without hardcoded home directory assumptions

---

### User Story 3 - Flat Architecture Compliance (Priority: P1)

**As a** skill developer reviewing discovery-pack structure  
**I want** a single consolidated SKILL.md under 500 lines with no nested sub-skills  
**So that** the skill adheres to Anthropic specification, reduces token load, and simplifies maintenance.

**Why this priority**: Current 8 nested sub-skills (896 lines) violate flat architecture standard, cause redundant loading overhead, and complicate updates. Blocks spec compliance certification.

**Independent Test**: Check \`wc -l skill/discovery-pack/SKILL.md\` outputs <500 lines AND \`find skill/discovery-pack -name SKILL.md | wc -l\` outputs 1 (not 9).

**Acceptance Scenarios**:

1. **Given** sub-skill consolidation completes, **When** user navigates to \`skill/discovery-pack/\`, **Then** only ONE SKILL.md file exists (sub-skill directories removed)
2. **Given** consolidated SKILL.md, **When** line count checked, **Then** file contains <500 lines (target: <450)
3. **Given** workflow Phase 1-8 instructions, **When** agent parses SKILL.md, **Then** all phase-specific logic exists as inline sections (no sub-skill invocations via Skill tool)
4. **Given** verbose methodology details, **When** progressive disclosure applied, **Then** content moved to \`shared-references/\` with pointers in SKILL.md (not full duplication)

---

### User Story 4 - Progressive Disclosure Token Efficiency (Priority: P1)

**As a** user running discovery workflow  
**I want** templates loaded only when generating each specific artifact  
**So that** token consumption stays minimal (<25k for full mode) and skill execution is cost-effective.

**Why this priority**: Current implementation loads all templates upfront, wasting 20-30% tokens. With flat architecture consolidation, risk of token bloat increases unless progressive disclosure enforced.

**Independent Test**: Monitor token usage during lite mode execution. Template for artifact 03 MUST NOT be loaded before Step 3.3 (when generating that artifact).

**Acceptance Scenarios**:

1. **Given** lite mode starts, **When** Step 2 (mode selection) completes, **Then** zero templates have been read (no preloading)
2. **Given** artifact 00_problem-frame generation begins, **When** agent reads template, **Then** ONLY \`templates/00_problem-frame.md\` loaded (not 01-07)
3. **Given** full mode execution, **When** token usage measured, **Then** total consumption ≤25k tokens (20-30% improvement vs baseline)
4. **Given** user asks clarification mid-workflow, **When** agent needs methodology details, **Then** \`shared-references/methodologies.md\` loaded on-demand (not preloaded in SKILL.md)

---

### Edge Cases

- **Empty repository**: User runs discovery in non-git directory → Pre-flight check warns but does not fail (git optional)
- **Partial schema sync**: Developer updates template but forgets schema → CI validation fails with clear error pointing to mismatched fields
- **Mixed agent environments**: User has both \`~/.claude/\` and \`~/.copilot/\` installations → Skill works in both without conflicts (relative paths resolve correctly)
- **Mid-workflow agent switch**: User starts in Copilot CLI, continues in Claude Code → State maintained in output directory (agent-agnostic)
- **SKILL.md over limit after consolidation**: Initial merge exceeds 500 lines → Automated check fails, developer iterates to move content to bundled resources
- **Template reference broken**: SKILL.md references \`templates/nonexistent.md\` → Agent reports error immediately (no silent failure)

## Requirements *(mandatory)*

### Functional Requirements

**Schema-Template Synchronization (Issue #1)**

- **FR-001**: Template YAML frontmatter fields MUST match corresponding JSON schema required properties exactly (no missing fields, no extra fields not in schema)
- **FR-002**: Template enum values MUST match schema enum definitions exactly (e.g., vendor_lock_in: "low" | "medium" | "high" only)
- **FR-003**: Template field types MUST match schema types (array fields documented as lists, object fields as nested structures, nullable fields handle null)
- **FR-004**: Validation script \`scripts/validate.py\` MUST pass 8/8 artifacts generated from templates without modification
- **FR-005**: Schema changes MUST trigger template review checklist (automated or documented procedure)

**Cross-Agent Portability (Issue #2)**

- **FR-006**: All script invocations in SKILL.md MUST use relative paths (\`scripts/\`, \`templates/\`, \`schemas/\`) without hardcoded home directories
- **FR-007**: Skill installation MUST work in \`~/.claude/skills/\`, \`~/.copilot/skills/\`, and project-local \`.claude/skills/\` without path modifications
- **FR-008**: Automation scripts (Python, Bash) MUST locate resources relative to skill root, not via absolute paths
- **FR-009**: SKILL.md MUST contain zero instances of \`~/.copilot\`, \`~/.claude\`, or other agent-specific home directory references (grep validation passes)
- **FR-010**: README installation instructions MUST document all supported installation locations with examples

**Sub-Skills Consolidation (Issue #3)**

- **FR-011**: Skill package MUST contain exactly ONE SKILL.md file (no sub-skill directories with additional SKILL.md files)
- **FR-012**: Sub-skill phase logic (discovery-frame, discovery-decide, etc.) MUST be consolidated into main SKILL.md as inline workflow sections
- **FR-013**: Workflow sequencing MUST preserve all 8 phases without functional regressions (lite mode: 3 phases, full mode: 8 phases)
- **FR-014**: Sub-skill directories (discovery-frame/, discovery-decide/, etc.) MUST be removed entirely from repository
- **FR-015**: Skill invocations via Skill tool (e.g., "invoke discovery-frame") MUST be replaced with direct template reads and artifact generation instructions

**SKILL.md Size Reduction (Issue #4)**

- **FR-016**: Main SKILL.md body MUST contain <500 lines (target: <450 lines)
- **FR-017**: Verbose methodology explanations MUST move to \`shared-references/methodologies.md\` with pointers in SKILL.md
- **FR-018**: Detailed workflow instructions MUST move to \`workflows/lite-mode.md\` and \`workflows/full-mode.md\` with high-level overview in SKILL.md
- **FR-019**: Progressive disclosure MUST be implemented: templates loaded only when generating corresponding artifact (not upfront)
- **FR-020**: SKILL.md MUST use bullet points and tables over prose paragraphs (compression without clarity loss)

**Validation & Quality Gates**

- **FR-021**: Pre-flight check script MUST validate Python ≥3.11, required packages, and output directory writability before workflow start
- **FR-022**: Each artifact generation step MUST validate against schema immediately after creation (fail-fast)
- **FR-023**: Final validation step MUST confirm 100% schema compliance before handoff to \`/speckit.specify\`
- **FR-024**: Validation failures MUST display file path, specific error (e.g., "missing field: what_pain"), and suggested fix

### Key Entities

- **SKILL.md**: Main orchestrator file containing workflow sequence, decision points, and pointers to bundled resources. MUST be <500 lines and agent-agnostic.
- **Template**: Markdown file with YAML frontmatter defining artifact structure. MUST synchronize exactly with corresponding JSON schema.
- **Schema**: JSON Schema file defining validation rules for artifact YAML frontmatter. Source of truth for required fields, types, and enums.
- **Artifact**: Discovery output file (00-07) generated by agent following template structure. MUST pass schema validation before handoff.
- **Bundled Resource**: Supporting documentation (methodologies, glossary) referenced by SKILL.md but loaded on-demand (progressive disclosure).
- **Automation Script**: Python or Bash script for token-efficient operations (assumption extraction, validation, pre-flight checks).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Schema validation pass rate increases from 12.5% (1/8) to 100% (8/8) for full mode execution
- **SC-002**: Skill functions identically in Claude Code and Copilot CLI without path modifications (cross-agent test suite passes)
- **SC-003**: SKILL.md line count reduces from 549 to <450 lines (18%+ reduction)
- **SC-004**: Sub-skill count reduces from 9 SKILL.md files to 1 (flat architecture achieved)
- **SC-005**: Token consumption for full mode reduces by 20-30% through progressive disclosure (measured via token usage tracking)
- **SC-006**: Zero hardcoded agent-specific paths remain in SKILL.md or scripts (\`grep -r '~/.copilot' skill/ | wc -l\` outputs 0)
- **SC-007**: Pre-flight check correctly identifies missing dependencies in 100% of test scenarios (Python version, packages, permissions)
- **SC-008**: Validation script execution time remains <5 seconds for 8 artifacts (performance maintained)
- **SC-009**: Documentation accurately reflects all installation locations with working examples (README, CONTRIBUTING tested)
- **SC-010**: Constitution Principle I (Skills Spec Compliance) checklist passes 100% after fixes implemented

### Assumptions

- Python 3.11+ is available in user environments (documented as prerequisite)
- Users have write permissions to output directories (validated by pre-flight check)
- Git repository context is optional but recommended (skill works without it)
- Templates remain markdown with YAML frontmatter (no format migration)
- JSON Schema Draft 7 or later is used for validation
- Relative paths resolve correctly from skill installation directory in all agents
- Agents supporting Agent Skills specification follow progressive disclosure patterns
- User running discovery has sufficient token budget for multi-artifact generation
- Existing discovery artifacts are not automatically migrated (users re-run discovery for new validation-compliant outputs)
- Sub-skill consolidation preserves all functional logic (no feature removal, only restructuring)

### Dependencies

- Existing automation scripts (\`scripts/validate.py\`, \`scripts/extract_assumptions.py\`) continue working with updated templates
- Spec-kit integration (\`07_speckit-handoff.md\` format) remains unchanged
- Examples directory will require regeneration with validation-passing artifacts (handled in separate issue)
- CI/CD pipeline (if exists) needs update to run new validation gates
- Documentation updates required in README, CONTRIBUTING, and SKILL.md itself

### Out of Scope

- Adding new templates or artifacts (focus is compliance, not features)
- Improving automation script functionality beyond path fixes
- Multi-language template support (English only for this phase)
- Interactive mode selection questionnaire (tracked in separate issue)
- Evaluation framework creation (tracked in separate issue)
- Examples directory population (tracked in separate issue)
- Performance optimization beyond progressive disclosure token savings
