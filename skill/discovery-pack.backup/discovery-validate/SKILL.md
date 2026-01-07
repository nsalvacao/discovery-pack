---
name: discovery-validate
description: Design validation experiments with exit criteria (proceed/pivot/kill thresholds). Auto-generates 04_assumptions-unknowns.md from tags, then creates 05_validation-plan.md with hypothesis tests and measurable success criteria. Use in full discovery mode. CRITICAL GATE - Ask for metrics if validation lacks observable outcomes.
---

# Validation Planning

Two artifacts: `04_assumptions-unknowns.md` (auto-generated from tags) and `05_validation-plan.md` (experiments).

## Phase 1: Assumptions Extraction
- Scan all previous artifacts for `[ASSUMPTION]` tags
- Prioritize by impact (critical/important/minor)
- List falsification criteria: "What would prove this wrong?"

## Phase 2: Experiments
- Design minimal experiments (A/B test, interviews, prototypes, spikes)
- Define pass/fail criteria (quantitative + qualitative)
- Set exit criteria:
  - Proceed if: [confidence threshold]
  - Pivot if: [invalidation threshold]
  - Kill if: [fundamental blocker]

**CRITICAL GATE:** If success criteria lacks metrics, ask: "How will we know this succeeds? What's measurable?"

Output to `/docs/discovery/<date>-<topic>/04_assumptions-unknowns.md` and `05_validation-plan.md`.
