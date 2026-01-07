---
description: "Atomic task breakdown for P0-P1 spec compliance fixes"
---

# Tasks: Spec Compliance Fixes (Issues #1-4)

**Input**: Design documents from `/specs/001-spec-compliance-fixes/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅

**Tests**: Not requested for this refactoring/compliance project. Validation via existing `scripts/validate.py` and manual cross-agent testing.

**Organization**: Tasks grouped by user story (P0 → P1) with independent test checkpoints.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Single project at repository root:
- `skill/discovery-pack/` - Skill artifacts (SKILL.md, templates, schemas, scripts)
- `specs/001-spec-compliance-fixes/` - Spec-kit feature directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Pre-flight checks and validation baseline

- [X] T001 Verify all prerequisite tools installed (Python 3.11+, Bash 5.0+, jq) *(Note: Validates development environment. See T026 for runtime skill pre-flight check.)*
- [X] T002 Run baseline validation: `python skill/discovery-pack/scripts/validate.py` to confirm 7/8 failures
- [X] T003 [P] Backup current skill directory: `cp -r skill/discovery-pack skill/discovery-pack.backup`
- [X] T004 [P] Create working branch: `git checkout -b 001-spec-compliance-fixes` (if not exists)

**Checkpoint**: Environment ready - proceeding to P0 critical fixes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure changes that MUST be complete before user stories

**⚠️ CRITICAL**: No user story work can begin until path resolution updated

- [X] T005 Create `skill/discovery-pack/shared-references/workflows/` directory structure
- [X] T006 Update `scripts/validate.py` to use relative paths via `Path(__file__).parent.parent`
- [X] T007 [P] Update `scripts/extract_assumptions.py` to use relative paths via `Path(__file__).parent.parent`
- [X] T008 [P] Update `scripts/gate_detector.py` to use relative paths (if has absolute paths)
- [X] T009 [P] Update `scripts/template_filler.py` to use relative paths (if has absolute paths)
- [X] T010 Test scripts: Run `python skill/discovery-pack/scripts/validate.py` from different working directories

**Checkpoint**: Scripts portable - user story implementation can now begin

---

## Phase 3: User Story 1 - Schema Validation Success (Priority: P0) 🎯

**Goal**: Fix 7/8 template-schema mismatches to achieve 100% validation success

**Independent Test**: `python skill/discovery-pack/scripts/validate.py` outputs 8/8 artifacts pass

### Template Fixes (Based on research.md R1 audit matrix)

- [X] T011 [P] [US1] Fix `templates/00_problem-frame.md`: Add missing YAML fields per schema (business_impact, success_criteria_preview, initial_unknowns)
- [X] T012 [P] [US1] Fix `templates/01_constraints-nfr.md`: Convert incompatible structures to match schema arrays/objects
- [X] T013 [P] [US1] Fix `templates/02_domain-model.md`: Add required 'name' field to domain entity structure
- [X] T014 [P] [US1] Fix `templates/03_option-space.md`: Update vendor_lock_in enum values to ["low", "medium", "high"] (remove "none")
- [X] T015 [P] [US1] Fix `templates/04_assumptions-unknowns.md`: Validate structure matches schema (may already be valid)
- [X] T016 [P] [US1] Fix `templates/05_validation-plan.md`: Add missing exit_criteria field to YAML frontmatter
- [X] T017 [P] [US1] Fix `templates/06_decision-log.md`: Fix superseded_by field nullable constraint per schema
- [X] T018 [P] [US1] Fix `templates/07_speckit-handoff.md`: Add missing glossary field to YAML frontmatter

### Validation & Documentation

- [X] T019 [US1] Run validation: `python skill/discovery-pack/scripts/validate.py` → expect 8/8 pass
- [X] T020 [US1] Update CHANGELOG.md: Document Issue #1 resolution (schema-template sync 12.5%→100%)
- [X] T021 [US1] Commit atomically: `fix(templates): synchronize 7 templates with JSON schemas (Issue #1)`

**✅ US1 Complete**: All artifacts pass schema validation

---

## Phase 4: User Story 2 - Cross-Agent Portability (Priority: P0) 🎯

**Goal**: Remove hardcoded `~/.copilot/` paths from SKILL.md for vendor-neutral portability

**Independent Test**: Install in `~/.claude/skills/discovery-pack/` and run lite mode without "file not found" errors

### SKILL.md Path Fixes

- [X] T022 [US2] Audit SKILL.md: `grep -n "~/.copilot" skill/discovery-pack/SKILL.md` to identify hardcoded paths
- [X] T023 [US2] Replace hardcoded paths with relative references: `skill/discovery-pack/templates/`, `skill/discovery-pack/schemas/`, `skill/discovery-pack/scripts/`
- [X] T024 [US2] Update script invocation examples in SKILL.md to use relative paths (e.g., `python scripts/validate.py` not `~/.copilot/.../validate.py`)
- [X] T025 [US2] Add path assumptions section to SKILL.md: Document skill root as working directory convention

### Pre-Flight Check Script

- [X] T026 [US2] Create `scripts/pre-flight-check.sh`: Verify templates/, schemas/, scripts/ dirs exist relative to skill root *(Note: Runtime check for end users. See T001 for development environment validation.)*
- [X] T027 [US2] Add usage instructions for pre-flight check in SKILL.md

### Cross-Agent Testing

- [ ] T028 [US2] Test in Copilot CLI: Install in `~/.copilot/skills/` and run lite mode
- [ ] T029 [US2] Test in Claude Code: Install in `~/.claude/skills/` and run lite mode
- [ ] T030 [US2] Test project-local: Install in `.claude/skills/` and run lite mode
- [ ] T031 [US2] Update CHANGELOG.md: Document Issue #2 resolution (cross-agent portability achieved)
- [ ] T032 [US2] Commit atomically: `fix(skill): remove hardcoded paths for cross-agent portability (Issue #2)`

**✅ US2 Complete**: Skill works in any agent or installation location

---

## Phase 5: User Story 3 - Flat Architecture Compliance (Priority: P1) 🎯

**Goal**: Consolidate 9 SKILL.md files (1,445 lines total) into 1 file <450 lines

**Independent Test**: `wc -l skill/discovery-pack/SKILL.md` outputs <500 AND `find skill/discovery-pack -name SKILL.md | wc -l` outputs 1

### Content Analysis & Migration Planning

- [ ] T033 [US3] Audit sub-skill content: Identify unique content vs duplication across 8 sub-skills (discovery-frame, discovery-decide, etc.)
- [ ] T034 [US3] Create migration map: Allocate 440 lines per research.md R2 consolidation blueprint
- [ ] T035 [US3] Extract workflow details: Move Phase 1-3 steps to `shared-references/workflows/lite-mode.md` (target ~150 lines)
- [ ] T036 [US3] Extract workflow details: Move Phase 4-8 steps to `shared-references/workflows/full-mode.md` (target ~250 lines)

### Consolidation Implementation

- [ ] T037 [US3] Rewrite `skill/discovery-pack/SKILL.md`: Consolidate core instructions (<450 lines) with pointers to workflow files
- [ ] T038 [US3] Apply progressive disclosure: Replace verbose methodology text with references to `shared-references/methodologies.md`
- [ ] T039 [US3] Delete sub-skill directories: `rm -rf skill/discovery-pack/discovery-{frame,decide,domain,validate,risk,decide-adv,coordinate,handoff}/`
- [ ] T040 [US3] Update `.gitignore` if sub-skill dirs were tracked

### Validation & Documentation

- [ ] T041 [US3] Verify line count: `wc -l skill/discovery-pack/SKILL.md` (target: 400-450 lines)
- [ ] T042 [US3] Verify single file: `find skill/discovery-pack -name SKILL.md | wc -l` outputs 1
- [ ] T043 [US3] Test lite mode: Run discovery-run to ensure workflow file references load correctly
- [ ] T044 [US3] Update CHANGELOG.md: Document Issue #3 resolution (flat architecture: 9→1 SKILL.md, 1445→<450 lines)
- [ ] T045 [US3] Commit atomically: `refactor(skill): consolidate to flat architecture <450 lines (Issue #3)`

**✅ US3 Complete**: Anthropic flat architecture spec compliance achieved

---

## Phase 6: User Story 4 - Progressive Disclosure Token Efficiency (Priority: P1) 🎯

**Goal**: Lazy-load templates only when generating specific artifacts (20-30% token savings)

**Independent Test**: Monitor token usage during lite mode - template 03 NOT loaded before Step 3.3

### Workflow File Updates

- [ ] T046 [US4] Update `shared-references/workflows/lite-mode.md`: Add just-in-time template loading pattern before each artifact generation step
- [ ] T047 [US4] Update `shared-references/workflows/full-mode.md`: Add just-in-time template loading pattern before each artifact generation step
- [ ] T048 [US4] Remove eager loading: Audit SKILL.md for upfront "Load all templates" instructions and delete

### SKILL.md Progressive Disclosure

- [ ] T049 [US4] Update SKILL.md: Add instruction to load workflow files on-demand (not upfront)
- [ ] T050 [US4] Update SKILL.md: Add instruction to load methodology references only when user asks clarifying questions
- [ ] T051 [US4] Update SKILL.md: Document token efficiency guidance (target: ≤25k tokens full mode, ≤15k lite mode)

### Validation & Documentation

- [ ] T052 [US4] Test lite mode: Run discovery and verify templates load lazily (manual token monitoring)
- [ ] T053 [US4] Measure baseline: Record token usage for full mode execution (compare against 19k baseline)
- [ ] T054 [US4] Update CHANGELOG.md: Document Issue #4 resolution (progressive disclosure: 20-30% token savings)
- [ ] T055 [US4] Commit atomically: `perf(skill): implement progressive disclosure for token efficiency (Issue #4)`

**✅ US4 Complete**: Token efficiency optimized via lazy loading

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and quality gates

- [ ] T056 Run full compliance validation: Check constitution.md Principles I-IV all pass
- [ ] T057 [P] Update README.md: Add "Spec Compliance" badge and validation instructions
- [ ] T058 [P] Update INSTALLATION.md: Document cross-agent installation (Copilot CLI, Claude Code, project-local)
- [ ] T059 [P] Create quickstart guide: `specs/001-spec-compliance-fixes/quickstart.md` (developer onboarding)
- [ ] T060 Run end-to-end test: Execute full mode in production-like environment
- [ ] T061 Verify all success criteria from spec.md: 12.5%→100% validation, 549→<450 lines, 19k→≤25k tokens, 3→3 agent compatibility
- [ ] T062 Final commit: `docs: update compliance artifacts and close Issues #1-4`
- [ ] T063 Merge to main: Create PR with spec.md, plan.md, research.md, tasks.md links

**✅ Project Complete**: 100% Anthropic Skills Spec compliance achieved

---

## Dependencies

### User Story Completion Order

```
Setup (Phase 1)
  ↓
Foundational (Phase 2) - Path resolution fixes
  ↓
US1 (Schema Validation) + US2 (Cross-Agent) ← Can be done in parallel
  ↓
US3 (Flat Architecture) ← Depends on US1, US2 complete
  ↓
US4 (Progressive Disclosure) ← Depends on US3 complete (needs workflow files)
  ↓
Polish (Phase 7)
```

**Critical Path**: Setup → Foundational → US1 → US3 → US4 → Polish  
**Parallel Opportunities**: US1 + US2 can execute simultaneously

### Within User Stories

- **US1**: All template fixes (T011-T018) are parallelizable
- **US2**: Script updates (T006-T009) parallelizable, testing (T028-T030) sequential
- **US3**: Content analysis (T033-T036) sequential, validation (T041-T042) parallelizable
- **US4**: Workflow updates (T046-T047) parallelizable

---

## Parallel Execution Examples

### Phase 2 Foundational (5 parallel tasks)
```bash
# Terminal 1
git checkout 001-spec-compliance-fixes
task T005  # Create workflow directories

# Terminal 2-5 (parallel)
task T006  # validate.py path fix
task T007  # extract_assumptions.py path fix
task T008  # gate_detector.py path fix
task T009  # template_filler.py path fix

# Terminal 1 (after parallel complete)
task T010  # Test scripts
```

### Phase 3 US1 (8 parallel template fixes)
```bash
# Terminals 1-8 (parallel)
task T011  # Fix template 00
task T012  # Fix template 01
task T013  # Fix template 02
task T014  # Fix template 03
task T015  # Fix template 04
task T016  # Fix template 05
task T017  # Fix template 06
task T018  # Fix template 07

# Terminal 1 (after parallel complete)
task T019  # Run validation
task T020  # Update CHANGELOG
task T021  # Commit
```

### Phase 4 US2 (Cross-agent testing)
```bash
# Sequential: T022-T027 (SKILL.md updates, pre-flight script)

# Terminals 1-3 (parallel testing)
task T028  # Test Copilot CLI
task T029  # Test Claude Code
task T030  # Test project-local

# Terminal 1 (after parallel complete)
task T031  # Update CHANGELOG
task T032  # Commit
```

---

## Implementation Strategy

### MVP Scope (Recommended)
- **Phase 1**: Setup (T001-T004)
- **Phase 2**: Foundational (T005-T010)
- **Phase 3**: User Story 1 - Schema Validation (T011-T021) ← **DELIVER FIRST**

**Rationale**: US1 (P0) unblocks downstream automation and provides immediate validation feedback. Delivers 8/8 artifacts passing schema checks.

### Full Delivery Sequence
1. **Sprint 1** (6-8h): MVP (Phases 1-3) → Schema validation 100%
2. **Sprint 2** (2-3h): US2 (Phase 4) → Cross-agent portability
3. **Sprint 3** (8-10h): US3 (Phase 5) → Flat architecture compliance
4. **Sprint 4** (4-6h): US4 (Phase 6) → Token efficiency optimization
5. **Sprint 5** (2-3h): Polish (Phase 7) → Final validation and documentation

**Total Effort**: 22-30 hours across 5 sprints

### Incremental Testing Strategy
- After each phase: Run `scripts/validate.py` to ensure no regressions
- After US1: 8/8 validation must pass
- After US2: Cross-agent testing in 3 environments
- After US3: Line count + file count validation
- After US4: Token usage measurement
- Final: Constitution Principles I-IV compliance check

---

## Format Validation

✅ **All 63 tasks follow required checklist format**:
- Checkbox: `- [ ]` prefix
- Task ID: Sequential T001-T063
- [P] marker: Present for parallelizable tasks
- [Story] label: Present for US1-US4 phase tasks (not Setup/Foundational/Polish)
- Description: Clear action with exact file path
- File paths: Absolute or relative from repository root

✅ **Organization by user story**: Phases 3-6 map to US1-US4 from spec.md

✅ **Independent test criteria**: Each user story phase includes verification checkpoint

✅ **Parallel opportunities**: Documented in dependencies section with terminal examples
