---
name: discovery-run
description: Orchestrate complete scientific project discovery from ambiguous idea to spec-kit handoff. Use when starting a new project/feature needing structured discovery before spec-kit. Combines JTBD, Amazon PR/FAQ, ADR, and Lean Startup validation. Triggers on "I have an idea...", "I want to build...", or before `/speckit.constitution`. Runs all discovery phases sequentially with critical gate questions only.
---

# Discovery Pack Orchestrator

Execute the full discovery sequence to transform ambiguous ideas into structured specifications ready for spec-kit.

## Activation Conditions

Activate when user says:
- "I have an idea for..."
- "I want to build..."
- "Let's explore this concept..."
- Before spec-kit constitution phase

Activate when:
- Starting new project without clear requirements
- Requirements are ambiguous or underspecified
- Choosing between multiple technical approaches
- Enterprise/compliance/high-risk context requires rigor

Do NOT activate when:
- Spec-kit constitution already exists (use `/speckit.specify`)
- Task is well-defined implementation work
- User needs quick exploration without rigor

## Execution Workflow

### Step 1: Determine Mode

Ask once:
> "Discovery mode: **lite** (3 artifacts, fast) or **full** (7 artifacts, rigorous)?"
>
> - Lite: Small projects, < 5 people, low risk
> - Full: Enterprise, compliance, security-critical, high risk

Default to lite if no answer.

**Batch mode (default):** Zero questions, mark unknowns as `[ASSUMPTION]`
**Interactive mode:** Ask at critical gates only

### Step 2: Create Output Directory

```bash
mkdir -p /docs/discovery/$(date +%Y-%m-%d)-<topic-slug>
cd /docs/discovery/$(date +%Y-%m-%d)-<topic-slug>
```

### Step 3: Execute Discovery Sequence

**Lite Mode (3 artifacts):**
1. Invoke `/discovery.frame` → `00_problem-frame.md`
2. Invoke `/discovery.options` → `03_option-space.md`
3. Invoke `/discovery.handoff` → `07_speckit-handoff.md`

**Full Mode (7 artifacts):**
1. Invoke `/discovery.frame` → `00_problem-frame.md`
2. Invoke `/discovery.constraints` → `01_constraints-nfr.md`
3. Invoke `/discovery.domain` → `02_domain-model.md`
4. Invoke `/discovery.options` → `03_option-space.md`
5. Auto-generate `04_assumptions-unknowns.md` (from `[ASSUMPTION]` tags)
6. Invoke `/discovery.validate` → `05_validation-plan.md`
7. Invoke `/discovery.decide` → `06_decision-log.md`
8. Invoke `/discovery.handoff` → `07_speckit-handoff.md`

### Step 4: Critical Gates (Question Points)

**Only ask questions when blocking a critical gate:**

1. **Equivalent options (in `/discovery.options`):**
   - If Options A/B/C are equally scored in trade-off matrix
   - Ask: "What's most important: cost, speed, or maintainability?"

2. **Contradictory assumptions (in `/discovery.validate`):**
   - If Assumption X conflicts with Assumption Y
   - Ask: "Which assumption is more foundational?"

3. **Unmeasurable validation (in `/discovery.validate`):**
   - If success criteria lacks observable metrics
   - Ask: "How will we know if this succeeds? What's measurable?"

**All other ambiguities:** Mark as `[ASSUMPTION]` and continue.

### Step 5: Handoff Summary

Output:

```
✅ Discovery complete!

Artifacts: /docs/discovery/YYYY-MM-DD-<topic>/
  [List files created]

Next:
1. Review 07_speckit-handoff.md
2. Run /speckit.constitution (copy Constitution section)
3. Run /speckit.specify (copy Specify section)
```

## Tag System

Use consistently across all artifacts:

| Tag | Meaning | Usage |
|-----|---------|-------|
| `[FACT]` | Verified through data/research | "Users are on mobile 80% of time [FACT - analytics]" |
| `[ASSUMPTION]` | Testable hypothesis | "Users prefer dark mode [ASSUMPTION]" |
| `[HYPOTHESIS]` | Educated guess | "Real-time sync increases retention [HYPOTHESIS]" |
| `[CONSTRAINT]` | Non-negotiable | "Must run on WSL [CONSTRAINT]" |

## Templates

All artifact templates are in `assets/` directory:
- `00_problem-frame.md`
- `01_constraints-nfr.md`
- `02_domain-model.md`
- `03_option-space.md`
- `04_assumptions-unknowns.md`
- `05_validation-plan.md`
- `06_decision-log.md`
- `07_speckit-handoff.md`

Each skill invocation uses the corresponding template.

## Filesystem Fallback

If no filesystem write access: output markdown artifacts in code blocks for manual save.

## Execution Example

User request: "I want to build a local PM tool that syncs with GitHub"

You execute:
```
1. Ask: "Discovery mode: lite or full? [Default: lite]"
2. Receive: "lite"
3. Create: /docs/discovery/2026-01-06-pm-tool/
4. Invoke: /discovery.frame → 00_problem-frame.md
5. Invoke: /discovery.options → 03_option-space.md
   - Detect tie between Option A (Plane) and B (Custom MCP)
   - Ask: "Priority: feature richness or lightweight?"
   - Receive: "lightweight" → recommend Option B
6. Invoke: /discovery.handoff → 07_speckit-handoff.md
7. Output: Completion summary with next steps
```
