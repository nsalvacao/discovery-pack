# Discovery Pack Constitution

<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- Rationale: Initial constitution establishment (MAJOR bump)
- Added principles: 8 core principles + 2 additional sections
- Modified sections: All (initial creation)
- Templates requiring updates:
  ✅ constitution.md (this file)
  ⚠ plan-template.md (pending alignment with Quality Gates)
  ⚠ spec-template.md (pending alignment with Schema-Template Sync principle)
  ⚠ tasks-template.md (pending alignment with Methodology Rigor principle)
- Follow-up TODOs: None (all placeholders resolved)
-->

## Core Principles

### I. Anthropic Skills Specification Compliance (NON-NEGOTIABLE)

Discovery Pack **MUST** adhere to the [Agent Skills specification](https://agentskills.io/specification) without exception:

- **Flat architecture mandatory**: SKILL.md body <500 lines, no nested sub-skills
- **Progressive disclosure enforced**: Load templates/references on-demand, not upfront
- **Environment-agnostic paths only**: No hardcoded `~/.copilot/` or `~/.claude/` references
- **Cross-agent portability**: Support Claude Code, Copilot CLI, Gemini Code Assist, Cursor, VS Code agent mode

**Rationale**: Vendor neutrality and spec compliance are foundational to multi-agent adoption. Violations break portability and waste tokens.

### II. Schema-Template Synchronization

Templates and JSON schemas **MUST** remain perfectly synchronized:

- 100% validation pass rate required before any release
- Field-by-field audit mandatory when schemas or templates change
- Enum values in templates **MUST** match schema definitions exactly
- Type mismatches (array vs object, string vs null) are blocking defects

**Rationale**: Validation failures undermine trust and break automated workflows. 7/8 artifacts failing validation (baseline state) is unacceptable for production.

### III. Cross-Agent Portability

Skill **MUST** function identically across all agent implementations supporting the Agent Skills spec:

- Use relative paths only (\`scripts/\`, \`templates/\`) for bundled resources
- Detect agent environment dynamically if agent-specific behavior needed
- No assumptions about installation location (~/.claude/, ~/.copilot/, project-local)
- Test cross-agent compatibility before release

**Rationale**: Users choose agents based on preference/tooling. Skill lock-in to specific agents reduces adoption and creates maintenance burden.

### IV. Token Efficiency & Automation

Optimize for minimal token consumption without sacrificing quality:

- **Automation-first**: Python scripts preferred over manual agent workflows (target: 35%+ token savings)
- **Progressive disclosure**: Load Level 3 resources (templates, methodologies) only when explicitly needed
- **Batch operations**: Generate multiple artifacts in single pass when dependencies allow
- **Script delegation**: Use \`extract_assumptions.py\`, \`validate.py\` instead of agent re-implementation

**Rationale**: Token costs compound at scale. Efficient skills respect user budgets and enable broader accessibility.

### V. Methodology Rigor

Discovery artifacts **MUST** apply proven methodologies correctly:

- **JTBD**: Jobs, Context, Outcomes framework for problem framing
- **Amazon PR/FAQ**: Working Backwards approach for clarity
- **ADR**: Architectural Decision Records with context, decision, consequences
- **Lean Startup**: Build-Measure-Learn validation cycles
- **DDD**: Bounded contexts, ubiquitous language, domain events

**Epistemic tagging mandatory**:
- \`[FACT]\`: Verified, documented, objectively true
- \`[ASSUMPTION]\`: Unverified belief requiring validation
- \`[HYPOTHESIS]\`: Testable prediction for experiments
- \`[CONSTRAINT]\`: Non-negotiable boundary condition

**Rationale**: Methodologies are not decoration—they enforce structured thinking. Tagging distinguishes certainty from speculation, enabling risk-aware planning.

### VI. Spec-Kit Integration

Output artifacts **MUST** be directly consumable by [GitHub Spec-Kit](https://github.com/github/spec-kit):

- Handoff artifact (\`07_speckit-handoff.md\`) includes constitution + specify sections
- Format matches spec-kit expectations (YAML frontmatter + markdown body)
- Clear boundary: discovery-pack produces specifications, spec-kit produces implementations
- No duplication: spec-kit takes over at implementation phase

**Rationale**: Discovery and implementation are sequential, not overlapping. Clean handoff prevents scope creep and enables specialized tool usage.

### VII. Quality Gates

All artifacts **MUST** pass validation before progression to next phase:

- **Schema validation**: 100% pass rate via \`scripts/validate.py\`
- **Tag coverage**: ≥60% of claims tagged with epistemic markers
- **Assumption extraction**: Auto-generated \`04_assumptions-unknowns.md\` with ≥90% recall
- **Completeness**: Required sections present, no \`TODO\` markers in critical fields

**Gate enforcement**:
- Lite mode: Validate artifacts 00, 03, 07 before handoff
- Full mode: Validate all 8 artifacts before handoff
- Blocking: Do NOT proceed to \`/speckit.specify\` with failing artifacts

**Rationale**: Quality gates prevent garbage-in-garbage-out. Downstream tooling (spec-kit, implementation) assumes validated inputs.

### VIII. Naming Conventions & Structure

Maintain consistent, professional naming across all artifacts:

**File naming**:
- Discovery artifacts: \`NN_kebab-case-name.md\` (e.g., \`00_problem-frame.md\`)
- Scripts: \`snake_case.py\` (e.g., \`extract_assumptions.py\`)
- Templates: \`kebab-case-template.md\` (e.g., \`problem-frame-template.md\`)
- Documentation: \`SCREAMING-KEBAB-CASE.md\` for root-level guides (e.g., \`CONTRIBUTING.md\`)

**Directory structure**:
```
discovery-pack/
├── SKILL.md                    ← Orchestrator (<500 lines)
├── templates/                  ← Artifact templates (8)
├── schemas/                    ← JSON Schema validation (9)
├── scripts/                    ← Python automation (6+)
├── shared-references/          ← Methodologies, glossary
└── examples/                   ← Complete sample executions
```

**Code style**:
- Python: PEP 8 compliant, type hints for public APIs
- Bash: ShellCheck clean, POSIX-compatible where possible
- Markdown: CommonMark spec, <100 char lines (soft limit)

**Rationale**: Consistency reduces cognitive load. Professional naming signals quality and eases navigation for contributors.

## Contribution Standards

### Licensing

Discovery Pack is MIT licensed. All contributions **MUST**:
- Be compatible with MIT license terms
- Not introduce GPL, AGPL, or other copyleft dependencies
- Retain copyright header in modified files
- Acknowledge original authors in derivative works

### Community Guidelines

Contributors **MUST**:
- Follow [GitHub Community Guidelines](https://docs.github.com/en/site-policy/github-terms/github-community-guidelines)
- Respect Code of Conduct (welcoming, inclusive, harassment-free)
- Provide constructive feedback in reviews
- Credit others' work appropriately (no plagiarism)

### Issue Reporting

When opening issues at [github.com/nsalvacao/discovery-pack/issues](https://github.com/nsalvacao/discovery-pack/issues):

**Bug reports MUST include**:
- Steps to reproduce
- Expected vs actual behavior
- Environment (agent type, OS, Python version)
- Validation output if schema-related
- Minimal reproducible example

**Feature requests MUST include**:
- User story (As a [role], I want [capability], so that [benefit])
- Success criteria (How do we know it works?)
- Trade-offs considered (What alternatives were evaluated?)
- Spec compliance impact (Does this violate any principles?)

**Non-blocking issues**:
- Tasks that fail but don't block forward progress → Open GitHub issue immediately
- Include checkpoint SHA for rollback if needed
- Tag with \`non-blocker\`, \`technical-debt\`, or \`enhancement\` as appropriate

### Pull Request Standards

PRs **MUST**:
- Reference related issue number (\`Fixes #123\`, \`Relates to #456\`)
- Pass all validation scripts (\`scripts/validate.py\`, \`scripts/pre-flight-check.sh\`)
- Include tests for new features (Python: pytest, Bash: bats if available)
- Update CHANGELOG.md under \`[Unreleased]\` section
- Maintain or improve schema validation pass rate (never degrade from 100%)

Commit messages **MUST** follow [Conventional Commits](https://www.conventionalcommits.org/):
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types**: \`feat\`, \`fix\`, \`docs\`, \`refactor\`, \`test\`, \`chore\`
**Scopes**: \`skill\`, \`templates\`, \`schemas\`, \`scripts\`, \`docs\`

**Examples**:
```
fix(schemas): sync 00_problem-frame schema with template fields
feat(scripts): add pre-flight dependency checker
docs(readme): clarify cross-agent installation steps
```

**Atomic commits**: Each commit should be independently revertible without breaking functionality.

## Quality Gates

### Pre-Release Checklist

Before tagging a new version, **ALL** gates MUST pass:

**P0 - Blocking**:
- [ ] Schema validation: 8/8 artifacts pass \`scripts/validate.py\`
- [ ] SKILL.md size: <500 lines
- [ ] No hardcoded paths (grep for \`~/.copilot\`, \`~/.claude\`)
- [ ] Cross-agent tested (Claude Code, Copilot CLI minimum)
- [ ] All scripts executable and error-free

**P1 - High Priority**:
- [ ] Examples directory contains complete lite + full mode samples
- [ ] Documentation up-to-date (README, CONTRIBUTING, skill/SKILL.md)
- [ ] CHANGELOG.md reflects all changes since last release
- [ ] No TODO markers in critical paths (templates, SKILL.md workflow)

**P2 - Recommended**:
- [ ] Automation scripts tested with sample project
- [ ] Progressive disclosure measured (token usage <25k for full mode)
- [ ] Issue tracker triaged (P0/P1 issues resolved or deferred explicitly)

**Versioning**:
- MAJOR: Breaking changes (schema changes, workflow redesign, principle additions/removals)
- MINOR: New features (new templates, automation scripts, optional workflows)
- PATCH: Bug fixes (validation errors, typos, path corrections, documentation)

### Runtime Validation

During execution, enforce:
- **Step 1**: Pre-flight check passes (Python available, dependencies installed, output writable)
- **Step 3-8**: Each artifact generated validates against schema before proceeding
- **Step 9**: Final validation pass confirms 100% schema compliance before handoff

If validation fails:
1. Display error with file path and specific failure reason
2. Offer to fix automatically if error is correctable (e.g., missing optional field)
3. If uncorrectable, halt and request user intervention
4. Log failure details to \`.specify/memory/validation-log.json\` for debugging

## Development Workflow

### Branch Strategy

- **main**: Production-ready, tagged releases only
- **develop**: Integration branch for completed features
- **feature/\***: Individual feature branches (e.g., \`feature/issue-1-schema-sync\`)
- **fix/\***: Bug fix branches (e.g., \`fix/issue-2-hardcoded-paths\`)
- **docs/\***: Documentation-only changes

### Review Process

**Self-review checklist**:
- [ ] Run \`scripts/validate.py\` on test artifacts
- [ ] Check \`git diff\` for unintended changes
- [ ] Verify no credentials or sensitive data in commits
- [ ] Test manually with sample project (lite + full mode if applicable)

**Peer review requirements**:
- P0 fixes: Single approval required
- P1 features: Single approval + validation pass
- Constitution changes: Maintainer approval required

### Deployment Standards

**Release checklist**:
1. Update VERSION file (semantic versioning)
2. Update CHANGELOG.md (move \`[Unreleased]\` to \`[X.Y.Z] - YYYY-MM-DD\`)
3. Tag commit: \`git tag -a vX.Y.Z -m "Release X.Y.Z: <summary>"\`
4. Push tags: \`git push origin vX.Y.Z\`
5. Create GitHub release with CHANGELOG excerpt
6. Announce in README badge update

**Rollback procedure**:
- Atomic commits enable per-commit rollback: \`git revert <SHA>\`
- Checkpoint tags enable branch rollback: \`git reset --hard <tag>\`
- Document rollback reason in issue or CHANGELOG

**Hotfix process**:
- Branch from tagged release: \`git checkout -b hotfix/vX.Y.Z+1 vX.Y.Z\`
- Apply minimal fix, update CHANGELOG PATCH version
- Tag and release immediately without merging to develop first
- Merge hotfix to both main and develop afterward

## Governance

### Amendment Process

This constitution governs all development practices. Amendments:

**Procedure**:
1. Propose change via GitHub issue (label: \`constitution\`)
2. Discuss trade-offs, spec compliance impact, backward compatibility
3. If approved: Create PR with constitution update + version bump
4. Update dependent templates (plan, spec, tasks) for consistency
5. Commit atomically with message: \`docs: amend constitution to vX.Y.Z (<change summary>)\`
6. Push immediately (no staging/waiting)

**Version bumping**:
- MAJOR: Principle removal/redefinition, governance restructuring
- MINOR: New principle added, section expansion
- PATCH: Clarifications, typos, non-semantic edits

**Reversibility**:
- All changes committed atomically (can \`git revert\` single commit)
- Checkpoint tags enable branch-level rollback
- If change proves problematic, revert immediately and document reason in issue

### Compliance Review

**Continuous**:
- Every PR must verify compliance with applicable principles
- Reviewer checks: Schema sync (P2), Portability (P3), Token efficiency (P4)
- Automated checks where possible (schema validation, SKILL.md line count)

**Quarterly**:
- Audit against Anthropic Skills specification updates
- Review token efficiency metrics (has progressive disclosure degraded?)
- Check cross-agent compatibility (new agents released?)

**On-Demand**:
- When spec violations discovered: Open P0 issue, fix within 1 sprint
- When user reports compliance failure: Reproduce, fix, add test case

### Complexity Justification

Complexity (nested logic, verbose templates, esoteric patterns) **MUST** be justified:

**Allowed when**:
- Required by Anthropic spec (e.g., YAML frontmatter format)
- Proven token savings (e.g., automation scripts)
- No simpler alternative exists (document what was tried)

**Disallowed when**:
- "Future-proofing" without concrete use case
- Premature optimization (profile first)
- Cleverness for its own sake

**Approval**: Complexity additions require maintainer review + issue discussion.

### Runtime Development Guidance

For agent-specific runtime guidance (commands, hooks, memory), consult:
- \`.claude/commands/*.md\` — Claude Code slash commands
- \`.specify/scripts/\` — Automation scripts with inline help
- \`shared-references/methodologies.md\` — Methodology deep-dives
- \`examples/README.md\` — Complete execution walkthroughs

## Authority

This constitution supersedes all other practices, guidelines, or informal agreements. In conflict, constitution wins.

**Exception**: Anthropic Skills specification takes precedence over this constitution (Principle I enforcement).

**Version**: 1.0.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-07
