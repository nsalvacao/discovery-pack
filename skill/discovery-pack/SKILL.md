---
name: discovery-pack
description: Complete project discovery workflow using Jobs-to-be-Done, Amazon PR/FAQ, ADR, and Lean Startup validation. Transforms ambiguous ideas into structured specifications ready for implementation. Activate when user mentions "discovery", "requirements discovery", "project framing", "validate assumptions", "JTBD analysis", or before starting implementation of unclear ideas.
license: MIT
metadata:
  author: nsalvacao
  version: "1.1.0"
  requires: "Python 3.8+ for optional automation scripts"
  changelog:
    - "1.1.0: Enhanced mode selection enforcement, output directory fallback strategy, automation workflow, validation checkpoint"
    - "1.0.0: Initial release"
---

# Discovery Pack Workflow

This skill package guides structured project discovery using proven methodologies. You will help the user transform ambiguous ideas into clear specifications before implementation begins.

## Core Methodologies Applied

- **Jobs-to-be-Done (JTBD)**: Focus on user motivation and context, not just features
- **Amazon PR/FAQ**: Force clarity on problem and customer before solutions
- **Architecture Decision Records (ADR)**: Document decisions with context and rationale
- **Lean Startup**: Validate critical assumptions through experiments
- **Domain-Driven Design (DDD)**: Model problem domain with ubiquitous language

See `shared-references/methodologies.md` for methodology details.
See `shared-references/glossary.md` for terminology.

## When to Activate

Activate this skill when the user:
- Starts a new project with unclear requirements
- Asks to "frame the problem" or "understand requirements"
- Mentions "discovery", "JTBD", "validation", or "assumptions"
- Needs to compare multiple technical approaches
- Wants to generate spec-kit compatible outputs
- Asks "what should I build?" or "how do I validate this idea?"

Do NOT activate for:
- Well-defined implementation tasks
- Requirements already documented and clear
- Quick prototypes without rigorous discovery

## Sub-Skills Available

This package contains 8 specialized sub-skills. You can invoke them individually or orchestrate the full workflow:

| Sub-Skill | Purpose | Invoke When |
|-----------|---------|-------------|
| `discovery-run` | Orchestrator for complete workflow | User wants full discovery process |
| `discovery-frame` | Problem framing with JTBD | User asks "frame the problem" |
| `discovery-constraints` | Non-functional requirements | User asks about constraints, security, performance |
| `discovery-domain` | Domain modeling with DDD | User asks to model entities, events, glossary |
| `discovery-options` | Option analysis with trade-offs | User asks to compare approaches |
| `discovery-validate` | Validation experiments | User asks to validate assumptions |
| `discovery-decide` | Decision log in ADR format | User asks to document decisions |
| `discovery-handoff` | Spec-kit integration | User asks for handoff to implementation |

## Execution Modes

### Lite Mode (Recommended Default)

Generate 3 artifacts for small projects, low risk, < 5 people:

**Artifacts:**
1. `00_problem-frame.md` - Problem, users, JTBD, success metrics
2. `03_option-space.md` - Alternative approaches with trade-off matrix
3. `07_speckit-handoff.md` - Spec-kit compatible handoff

**Time:** 15-30 minutes of conversation

**When to use:** Personal projects, startups, prototypes, clear constraints

### Full Mode (Enterprise/Compliance)

Generate 7 artifacts for enterprise, compliance-critical, security-sensitive projects:

**Additional artifacts beyond lite mode:**
4. `01_constraints-nfr.md` - Security, performance, compliance requirements
5. `02_domain-model.md` - Entities, events, bounded contexts, glossary
6. `04_assumptions-unknowns.md` - Extracted tagged assumptions (auto-generated)
7. `05_validation-plan.md` - Experiments to test critical assumptions
8. `06_decision-log.md` - Architectural decisions with rationale

**Time:** 1-2 hours of conversation

**When to use:** Enterprise projects, regulated industries, high-risk systems

## Execution Workflow

### Step 1: Determine Mode (MANDATORY)

**ALWAYS ask this question first, before any artifact generation:**

> **Discovery mode selection:**
> - **lite** (3 artifacts): Small projects, < 5 people, low risk, personal/startup [15-30 min]
> - **full** (7 artifacts): Enterprise, compliance, security-critical, high risk [1-2 hours]
>
> **Your choice:** lite | full | (auto-detect from project context)

If user says "just start" or doesn't respond: infer from project context:
- Personal/startup/prototype → lite
- Enterprise/finance/healthcare/security → full (with confirmation)

**CRITICAL:** Never proceed to Step 2 without mode selection.

### Step 1.5: Check Automation Availability

Run these checks once per session:

```bash
# Check Python + dependencies
python3 -c "import jsonschema, yaml; print('✅ Automation available')" 2>&1
```

**If automation available:**
- Inform user: "Automation scripts available (30-40% token savings). Using enhanced workflow."
- Use `extract_assumptions.py`, `generate_handoff.py`, `validate.py` where applicable

**If automation unavailable:**
- Proceed manually (current behavior)
- Optionally suggest: `pip install -r ~/.copilot/skills/discovery-pack/scripts/requirements.txt`

### Step 2: Determine Output Directory

**Target:** `<project-root>/docs/discovery/$(date +%Y-%m-%d)-<topic-slug>`

**Fallback strategy if target inaccessible:**
1. Try `$HOME/docs/discovery/...` (user home directory)
2. If still blocked, try `/tmp/discovery-pack/...` AND warn user:
   ⚠️ "Artifacts in /tmp (temporary). Copy to project after generation."
3. If all fail, output as markdown code blocks for manual save

**Always inform user of final path before generation.**

```bash
mkdir -p <determined-output-directory>
```

All artifacts go into this timestamped directory.

### Step 3: Execute Discovery Sequence

**For lite mode:**
1. Invoke sub-skill `discovery-frame` → generates `00_problem-frame.md`
2. Invoke sub-skill `discovery-options` → generates `03_option-space.md`
3. Invoke sub-skill `discovery-handoff` → generates `07_speckit-handoff.md`

**For full mode:**
1. Invoke `discovery-frame` → `00_problem-frame.md`
2. Invoke `discovery-constraints` → `01_constraints-nfr.md`
3. Invoke `discovery-domain` → `02_domain-model.md`
4. Invoke `discovery-options` → `03_option-space.md`
5. Run `scripts/extract_assumptions.py` → `04_assumptions-unknowns.md` (or generate manually)
6. Invoke `discovery-validate` → `05_validation-plan.md`
7. Invoke `discovery-decide` → `06_decision-log.md`
8. Invoke `discovery-handoff` → `07_speckit-handoff.md`

### Step 4: Apply Tag System

Use epistemic tags consistently across all artifacts:

- `[FACT]` - Verified with data/research (e.g., "80% users on mobile [FACT - analytics]")
- `[ASSUMPTION]` - Testable hypothesis (e.g., "Users prefer dark mode [ASSUMPTION]")
- `[HYPOTHESIS]` - Educated guess (e.g., "Real-time sync increases retention [HYPOTHESIS]")
- `[CONSTRAINT]` - Non-negotiable (e.g., "Must run on WSL [CONSTRAINT - technical]")

This makes assumptions explicit and testable.

### Step 5: Use Templates

All templates are in `templates/` directory:
- `00_problem-frame.md`
- `01_constraints-nfr.md`
- `02_domain-model.md`
- `03_option-space.md`
- `04_assumptions-unknowns.md`
- `05_validation-plan.md`
- `06_decision-log.md`
- `07_speckit-handoff.md`

Each template contains:
- **YAML frontmatter** with structured data (validates against schemas in `schemas/`)
- **Markdown body** with section prompts

Read the template from `templates/` directory, fill sections based on conversation, maintain structure.

### Step 6: Batch vs Interactive Execution

**Batch Mode (default):**
- Ask minimal questions
- Mark unknowns as `[ASSUMPTION]`
- Faster execution

**Interactive Mode:**
- Ask questions ONLY at critical gates:
  1. Options tied in trade-off matrix (need decision criteria)
  2. Contradictory assumptions detected (need prioritization)
  3. Validation plan lacks quantitative metrics (need measurement definition)

For all other unknowns, make reasonable assumptions and tag them.

### Step 7: Validation & Handoff

**If automation available:**
```bash
python3 ~/.copilot/skills/discovery-pack/scripts/validate.py <output-dir>
```

**If validation fails:**
- Show errors with artifact + line number
- Offer to fix automatically (if simple) or guide manual fix
- Re-validate after fix

**If validation passes or unavailable:**
- Generate handoff summary:

```
✅ Discovery complete!

Artifacts: <output-dir>
  [List files with sizes and validation status]

Next steps:
1. Review 07_speckit-handoff.md
2. Copy Constitution section → /speckit.constitution
3. Copy Specify section → /speckit.specify

[If automation used] Token efficiency: ~35% savings via automation
```

## Artifact Structure

Each artifact you generate must contain:

**YAML Frontmatter:**
```yaml
---
project: "Project Name"
date: "YYYY-MM-DD"
status: "draft"  # or under_review, approved, deprecated
metadata:
  generated_at: "ISO-8601 timestamp"
  generated_by: "your-model-name"
  discovery_pack_version: "1.0.0"

# Structured data matching schema
---
```

**Markdown Body:**
- Clear section headings
- Tagged statements (FACT/ASSUMPTION/HYPOTHESIS/CONSTRAINT)
- Concrete examples and evidence
- Actionable next steps

## Automation Scripts (Optional)

If Python is available, these scripts enhance workflow:

| Script | Purpose | Command |
|--------|---------|---------|
| `validate.py` | Validate artifacts against JSON schemas | `python scripts/validate.py docs/discovery/project/` |
| `extract_assumptions.py` | Auto-extract tagged assumptions to 04_ | `python scripts/extract_assumptions.py docs/discovery/project/` |
| `generate_handoff.py` | Auto-generate 07_ from 00-06 | `python scripts/generate_handoff.py docs/discovery/project/` |
| `gate_detector.py` | Detect critical decision gates | `python scripts/gate_detector.py docs/discovery/project/` |

Scripts are optional. If unavailable, generate manually following templates.

## Integration with Spec-Kit

The final artifact `07_speckit-handoff.md` contains two ready-to-copy sections:

**Constitution Section:**
- Core principles from problem frame
- Constraints from NFRs
- Glossary from domain model

**Specify Section:**
- User journeys from JTBD analysis
- Requirements from problem frame
- Success metrics
- Non-goals (anti-goals)

User can copy these directly to `/speckit.constitution` and `/speckit.specify` commands.

## Best Practices

**DO:**
- Use templates consistently
- Apply tag system to every claim
- Keep sections focused and actionable
- Ask clarifying questions when truly blocked
- Mark assumptions explicitly
- Provide concrete examples

**DON'T:**
- Skip frontmatter YAML (breaks validation)
- Make assumptions without tagging them
- Generate verbose prose without structure
- Ask excessive questions (prefer batch mode)
- Copy user's words verbatim (synthesize and structure)

## Progressive Disclosure

You are currently reading **Level 2** (full SKILL.md content).

**Level 3 resources** available as needed:
- `templates/*.md` - Detailed artifact templates
- `schemas/*.json` - Validation schemas
- `shared-references/methodologies.md` - Methodology deep-dive
- `shared-references/glossary.md` - Complete terminology
- `scripts/README.md` - Automation documentation

Load Level 3 resources only when needed for the current task.

## Example Execution

**User:** "I want to build a local dashboard that syncs GitHub project status"

**Your response:**
```
I'll run discovery in lite mode to frame the problem and explore options.

Creating: docs/discovery/2026-01-06-github-dashboard/

Phase 1/3: Problem framing with JTBD...
[Read template 00_problem-frame.md]
[Generate structured artifact with YAML + markdown]
✅ Generated 00_problem-frame.md
   - JTBD: "When context-switching, I want to see all project statuses, so I can prioritize work"
   - North star: Time to triage 5 projects (15min → 2min)

Phase 2/3: Option analysis...
[Read template 03_option-space.md]
[Generate trade-off matrix comparing 3 approaches]
✅ Generated 03_option-space.md
   - Option A: GitHub API + Electron (score: 4.2/5)
   - Option B: MCP Server integration (score: 3.8/5)
   - Option C: Use GitHub Projects (score: 2.1/5)
   Recommendation: Option A (offline-first, full control)

Phase 3/3: Spec-kit handoff...
[Read template 07_speckit-handoff.md]
[Extract key sections from 00 and 03 into handoff format]
✅ Generated 07_speckit-handoff.md
   - Constitution section ready
   - Specify section ready

Discovery complete! Artifacts in docs/discovery/2026-01-06-github-dashboard/
Next: Review 07_speckit-handoff.md → copy to spec-kit
```

## Summary

You are the orchestrator of a rigorous discovery workflow. Guide the user through structured problem framing, option analysis, and validation using proven methodologies. Generate well-structured artifacts with epistemic tags. Default to batch mode with minimal questions. Focus on clarity, evidence, and actionable outputs.
