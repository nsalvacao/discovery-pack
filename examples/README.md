# Discovery Pack Examples

This directory contains example discovery artifacts.

## Using the Templates

To start a discovery, your AI agent will use the templates in `../templates/` and generate artifacts in your project's `docs/discovery/YYYY-MM-DD-project-name/` directory.

## Example Workflow (Lite Mode)

**User prompt:**
```
"I want to build a local dashboard that syncs GitHub project status across 5+ repos"
```

**Agent response:**
```
I'll run discovery in lite mode to frame the problem and explore options.

Creating: docs/discovery/2026-01-06-github-sync-dashboard/

Phase 1/3: Problem framing...
✅ Generated 00_problem-frame.md
   - JTBD: "When I context-switch, I want to see all project statuses, so I can prioritize work"
   - North star metric: Time to triage 5 projects (15min → 2min)

Phase 2/3: Option analysis...
✅ Generated 03_option-space.md
   - Option A: GitHub API + Electron (score: 4.2)
   - Option B: MCP Server + existing tools (score: 3.8)
   - Option C: Use GitHub Projects (score: 2.1)
   Recommendation: Option A (offline-first, full control)

Phase 3/3: Spec-kit handoff...
✅ Generated 07_speckit-handoff.md
   - Constitution section ready to copy
   - Specify section ready to copy

✅ Discovery complete!
```

## Artifact Structure

Each generated artifact contains:

### YAML Frontmatter (machine-readable)
```yaml
---
project: "Project Name"
date: "2026-01-06"
status: "draft"
metadata:
  generated_at: "2026-01-06T14:30:00Z"
  generated_by: "claude-sonnet-4.5"
  discovery_pack_version: "1.0.0"

# ... structured data matching JSON schema
---
```

### Markdown Body (human-readable)
```markdown
# Problem Frame

## Problem Statement
[FACT] Clear description of pain point...

## Primary Users
**Solo Developer** - When I..., I want to..., so I can...
```

## Validation

Validate your generated artifacts:

```bash
python3 scripts/validate.py docs/discovery/2026-01-06-project-name/
```

## Full Mode Example

For enterprise projects, full mode generates 7 artifacts:

```
docs/discovery/2026-01-06-compliance-tracker/
├── 00_problem-frame.md
├── 01_constraints-nfr.md      # Security, performance, compliance
├── 02_domain-model.md          # Entities, events, glossary
├── 03_option-space.md
├── 04_assumptions-unknowns.md  # Auto-extracted
├── 05_validation-plan.md       # Experiments
├── 06_decision-log.md          # ADR-style decisions
└── 07_speckit-handoff.md
```

Use automation scripts to extract assumptions and detect decision gates:

```bash
python3 scripts/extract_assumptions.py docs/discovery/2026-01-06-project/
python3 scripts/gate_detector.py docs/discovery/2026-01-06-project/
```

## Methodologies Applied

- **JTBD** (00_): User motivation
- **PR/FAQ** (00_): Problem clarity
- **DDD** (02_): Domain model
- **Lean** (05_): Validation
- **ADR** (06_): Decision rationale

See `../shared-references/methodologies.md` for details.
