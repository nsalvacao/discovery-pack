---
$schema: "../schemas/validation-plan.schema.json"
project: "[Project Name]"
date: "YYYY-MM-DD"
status: "planning"
metadata:
  generated_at: "2026-01-06T00:00:00Z"
  generated_by: "[AI Model]"
  discovery_pack_version: "2.0.0"
  validated: false

validation_strategy:
  priorities:
    - priority: "critical"
      description: "[Blockers if wrong - validate first]"
    - priority: "high"
      description: "[Significant impact - validate early]"
    - priority: "medium"
      description: "[Nice to know - validate if time permits]"
  budget:
    time: "[X days/weeks]"
    cost: "[$ or effort]"
    resources: "[Team availability, tools needed]"

experiments:
  - id: "E1"
    title: "[Experiment Title]"
    hypothesis: "If [we do X], then [we expect Y], because [reasoning Z]"
    assumption_id: "A1"
    method: "[Prototype/Interview/A-B test/Spike/etc]"
    duration: "[Time estimate]"
    resources_needed:
      - "[Resource 1]"
    success_criteria:
      quantitative:
        - metric: "[Metric name]"
          target: "[Target value]"
          threshold: "[Pass/fail threshold]"
      qualitative:
        - "[Observable outcome]"
    exit_criteria:
      proceed_if: "[Confidence threshold met]"
      pivot_if: "[Hypothesis partially invalidated]"
      kill_if: "[Fundamental blocker discovered]"
---

# Validation Plan

**This template includes YAML frontmatter for validation and automation.**

The frontmatter above contains structured data that:
- ✅ Validates against JSON schema
- ✅ Documents experiments systematically
- ✅ Defines exit criteria (proceed/pivot/kill)
- ✅ Tracks validation progress
- ✅ Provides audit trail

Keep the markdown body below for human narrative and detailed analysis.

---

## Purpose

Design **minimal experiments** to validate critical assumptions and reduce uncertainty before committing to full implementation.

**Principle:** Fail fast, learn cheap.

---

## Validation Strategy

### What We Need to Learn

**Priority order:**
1. 🔴 **Critical unknowns** - Blockers if wrong (validate first)
2. 🟡 **Important unknowns** - Significant impact (validate early)
3. 🟢 **Minor unknowns** - Nice to know (validate if time permits)

### Validation Budget

**Time budget:** [X days/weeks]
**Cost budget:** [$ or effort]
**Resource constraints:** [Team availability, tools needed]

---

## Experiment 1: [Title]

### Hypothesis
[HYPOTHESIS] **We believe that** [statement]
**We'll know we're right when** [observable outcome]

### What We're Testing
[Specific assumption or unknown from 04_assumptions-unknowns.md]

### Experiment Design

**Type:** [A/B test | User interview | Prototype | Spike | Market research]

**Method:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Duration:** [Time needed]
**Participants:** [Who/how many]
**Tools needed:** [What's required]

### Success Criteria

**Quantitative:**
- ✅ Pass if: [Specific measurable threshold]
- ❌ Fail if: [Specific measurable threshold]

**Qualitative:**
- ✅ Pass if: [Observable behavior/feedback]
- ❌ Fail if: [Observable behavior/feedback]

**Example:**
- ✅ Pass if: 8/10 users complete task without assistance
- ❌ Fail if: <5/10 users complete task OR >50% express confusion

### Expected Signals

**If hypothesis is TRUE, we expect:**
- [Signal 1]
- [Signal 2]

**If hypothesis is FALSE, we expect:**
- [Counter-signal 1]
- [Counter-signal 2]

### Data Collection

**Metrics to track:**
1. [Metric 1]: [How measured]
2. [Metric 2]: [How measured]

**Artifacts to capture:**
- [Screenshots, recordings, quotes, etc.]

---

## Experiment 2: [Title]

[Same structure as Experiment 1]

---

## Exit Criteria

**When do we stop experimenting and make a decision?**

### Proceed if:
- ✅ [Criterion 1] - e.g., "3/4 critical hypotheses validated"
- ✅ [Criterion 2] - e.g., "User success rate >80%"
- ✅ [Criterion 3] - e.g., "Technical feasibility proven"

**Confidence threshold:** [e.g., "High confidence = proceed, Medium = one more experiment, Low = pivot"]

### Pivot if:
- ⚠️ [Criterion 1] - e.g., "2/4 critical hypotheses rejected"
- ⚠️ [Criterion 2] - e.g., "User confusion rate >40%"
- ⚠️ [Criterion 3] - e.g., "Cost exceeds budget by >50%"

**Pivot strategy:** [What we change and re-test]

### Kill if:
- ❌ [Criterion 1] - e.g., "Fundamental technical blocker discovered"
- ❌ [Criterion 2] - e.g., "Zero user interest across all segments"
- ❌ [Criterion 3] - e.g., "Legal/compliance impossibility"

**Kill criteria:** [Conditions that make this not worth pursuing]

---

## Validation Roadmap

| Week | Experiment | Owner | Dependencies | Status |
|------|------------|-------|--------------|--------|
| 1 | [Experiment 1] | [Name] | [None/Blocker] | ⏳ Pending |
| 2 | [Experiment 2] | [Name] | [Experiment 1 results] | ⏳ Pending |
| 3 | [Experiment 3] | [Name] | [None] | ⏳ Pending |

**Critical path:** [Which experiments must complete before others can start]

---

## Results Log

### Experiment 1: [Title]

**Date completed:** [YYYY-MM-DD]
**Result:** ✅ Validated | ⚠️ Inconclusive | ❌ Rejected

**Data collected:**
- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

**Interpretation:**
[What this means for our decisions]

**Next action:**
- [Decision made or next experiment needed]

**Artifacts:**
- [Links to recordings, data files, etc.]

---

### Experiment 2: [Title]

[Same structure as Experiment 1 results]

---

## Learning Backlog

**Questions we want to answer but aren't critical for v1:**

1. [Question 1] - *Priority:* Low - *Defer to:* [Phase/version]
2. [Question 2] - *Priority:* Low - *Defer to:* [Phase/version]

---

## Validation Decision

**Date:** [YYYY-MM-DD]
**Decision:** [Proceed | Pivot | Kill]

**Rationale:**
[Based on exit criteria, what did we learn and why are we making this choice?]

**Confidence level:** [High/Medium/Low]

**Validated assumptions:**
1. ✅ [Assumption 1]
2. ✅ [Assumption 2]

**Invalidated assumptions:**
1. ❌ [Assumption 3] - *Impact:* [How this changes our approach]

**Remaining uncertainties:**
1. ⚠️ [Uncertainty 1] - *Risk level:* [Low/Med/High]
2. ⚠️ [Uncertainty 2] - *Risk level:* [Low/Med/High]

**Ready to proceed to:** [Spec-kit constitution/specify phase]
