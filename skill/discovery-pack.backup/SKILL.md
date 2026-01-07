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

🛑 **STOP - Execute this BEFORE continuing:**

Run pre-flight check:
```bash
bash ~/.copilot/skills/discovery-pack/pre-flight-check.sh <output-dir> <mode>
```

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

✅ **Checkpoint:** Mode selected, pre-flight check passed

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

🛑 **ENFORCEMENT: Two Execution Modes**

**Mode A: Automated Executor (RECOMMENDED - Guaranteed Compliance)**
```bash
bash ~/.copilot/skills/discovery-pack/discovery-pack-run.sh <output-dir> <mode> "<project-name>"
```
- Enforces workflow with validation gates at each step
- Shows sub-skill instructions before generation
- Validates artifacts immediately after creation
- Blocks progression if validation fails
- **USE THIS to guarantee compliance**

**Mode B: Manual with Inline Instructions (High Discipline Required)**
Follow detailed sub-skill instructions below. Requires strict adherence to templates and validation.

---

#### Step 3.1: Problem Frame → `00_problem-frame.md`

**Sub-Skill:** `discovery-frame` | **Template:** `templates/00_problem-frame.md`

**Instructions:**
1. **Read template** - Load YAML frontmatter structure + markdown sections
2. **Fill sections:**
   - Problem statement (what pain, who, why now)
   - Users (primary/secondary with JTBD: "When I ___, I want to ___, so I can ___")
   - Anti-goals (explicitly NOT solving)
   - Success metrics (North Star + leading/lagging indicators)
   - Context (market/technical/organizational/regulatory)
3. **Apply tags** to every claim: `[FACT]`, `[ASSUMPTION]`, `[HYPOTHESIS]`, `[CONSTRAINT]`
4. **Batch mode default:** Infer from context, mark as `[ASSUMPTION]`, no questions unless problem absent

**Critical Requirements:**
- YAML frontmatter MANDATORY (--- delimiters)
- JTBD format: "When [situation], I want [action], so I can [outcome]"
- North Star metric must be quantitative

**Validation:** Must pass `validate.py` schema check

---

#### Step 3.2: Constraints & NFRs → `01_constraints-nfr.md` [FULL MODE ONLY]

**Sub-Skill:** `discovery-constraints` | **Template:** `templates/01_constraints-nfr.md`

**Instructions:**
1. Document non-functional requirements:
   - Security/Privacy (auth, encryption, threat model)
   - Performance (latency SLAs, throughput, scalability)
   - Compliance (GDPR, HIPAA, SOC2, etc.)
   - Observability (logging, metrics, tracing)
   - Operational (deployment, rollback, DR)
2. Each constraint tagged `[CONSTRAINT]` or `[ASSUMPTION]` if uncertain

**Output:** Structured NFR categories with measurable targets where possible

---

#### Step 3.3: Domain Model → `02_domain-model.md` [FULL MODE ONLY]

**Sub-Skill:** `discovery-domain` | **Template:** `templates/02_domain-model.md`

**Instructions:**
1. Create DDD domain model:
   - **Glossary:** Key terms + definitions (ubiquitous language)
   - **Entities:** Core objects with identity (User, Order, Tool, etc.)
   - **Events:** Domain events (UserRegistered, ToolScanned, etc.)
   - **Bounded Contexts:** System boundaries
   - **Relationships:** Entity connections
2. Optional: Mermaid diagrams for entity-relationship visualization

**Output:** Domain vocabulary + model that aligns team language

---

#### Step 3.4: Option Space → `03_option-space.md`

**Sub-Skill:** `discovery-options` | **Template:** `templates/03_option-space.md`

**Instructions:**
1. Compare 2-4 alternative approaches
2. For each option document:
   - Description + architectural overview
   - Pros/Cons
   - Trade-off matrix (score on: complexity, cost, lock-in, team fit, risk)
   - Risk analysis
3. Weighted scoring → recommendation with rationale

**🚨 CRITICAL GATE:**
- If options tie in weighted score, **ASK user for tiebreaker criteria**
- Do NOT proceed with arbitrary choice

**Output:** Evidence-based recommendation with transparent trade-offs

---

#### Step 3.5: Extract Assumptions → `04_assumptions-unknowns.md` [FULL MODE ONLY]

**Method:** Auto-generate OR manual extraction

**Auto (if Python available):**
```bash
python3 scripts/extract_assumptions.py <output-dir>
```
Scans artifacts 00-03, extracts all `[ASSUMPTION]` and `[HYPOTHESIS]` tags into structured list.

**Manual:** Copy-paste tagged assumptions from 00-03 into template structure.

**Output:** Consolidated list of untested assumptions requiring validation

---

#### Step 3.6: Validation Plan → `05_validation-plan.md` [FULL MODE ONLY]

**Sub-Skill:** `discovery-validate` | **Template:** `templates/05_validation-plan.md`

**Instructions:**
1. Read `04_assumptions-unknowns.md`
2. For each critical assumption, design experiment:
   - **Hypothesis:** Testable statement
   - **Method:** Survey, prototype, A/B test, spike, etc.
   - **Success Criteria:** Quantitative thresholds (proceed > X, pivot if Y, kill if < Z)
   - **Timeline:** Duration + resource estimate
3. Prioritize by (risk × impact)

**🚨 CRITICAL GATE:**
- If validation lacks quantitative success criteria, **ASK user for measurement definition**
- Do NOT accept vague "we'll see if it works"

**Output:** Testable hypotheses with clear proceed/pivot/kill thresholds

---

#### Step 3.7: Decision Log → `06_decision-log.md` [FULL MODE ONLY]

**Sub-Skill:** `discovery-decide` | **Template:** `templates/06_decision-log.md`

**Instructions:**
1. Document decisions in ADR (Architecture Decision Record) format
2. For each decision:
   - **ID:** ADR-001, ADR-002, etc.
   - **Title:** Short summary
   - **Status:** Proposed | Accepted | Deprecated | Superseded
   - **Context:** Why decision needed
   - **Decision:** What was decided
   - **Alternatives:** Options rejected + why
   - **Consequences:** Positive and negative impacts
3. Link related decisions (supersedes/superseded-by)

**Output:** Auditable decision history with rationale

---

#### Step 3.8: Spec-Kit Handoff → `07_speckit-handoff.md`

**Sub-Skill:** `discovery-handoff` | **Template:** `templates/07_speckit-handoff.md`

**Instructions:**
1. Transform discovery artifacts into spec-kit format
2. Extract and structure:
   - **Constitution Section:**
     - Core principles (from 00_problem-frame)
     - Constraints (from 01_constraints-nfr)
     - Glossary (from 02_domain-model)
   - **Specify Section:**
     - Users + JTBD (from 00_problem-frame)
     - Requirements (from 00 + 03_option-space chosen approach)
     - Success metrics (from 00 + 05_validation-plan)
     - Non-goals (from 00_problem-frame anti-goals)
3. Format as **copy-paste ready** for `/speckit.constitution` and `/speckit.specify`

**Output:** Ready-to-use spec-kit inputs

---

### Step 3 Validation Checkpoint (MANDATORY)

After artifact generation, VALIDATE ALL:

```bash
python3 ~/.copilot/skills/discovery-pack/scripts/validate.py <output-dir>
```

**Expected output:**
```
✅ 00_problem-frame.md: Valid
✅ 01_constraints-nfr.md: Valid
✅ 02_domain-model.md: Valid
...
```

**If validation fails:**
1. Read error message (shows artifact + line + reason)
2. Fix error in artifact
3. Re-run validation
4. Repeat until all ✅

🛑 **DO NOT proceed without passing validation.**

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
