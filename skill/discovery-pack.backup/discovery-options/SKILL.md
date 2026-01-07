---
name: discovery-options
description: Analyze option space with trade-off matrix, risk analysis, and decision criteria. Compare 2-4 approaches using pros/cons, implementation complexity, lock-in, and weighted scoring. Use when choosing architecture or technology. Creates 03_option-space.md. CRITICAL GATE - Ask for criteria if options tie.
---

# Option Space Analysis

Generate `03_option-space.md` comparing options A/B/C/D with trade-off matrix and risk analysis.

## Workflow
1. List 2-4 viable options
2. For each: pros, cons, complexity, lock-in, reversibility
3. Trade-off matrix (performance, cost, time-to-ship, etc.)
4. Risk analysis per option
5. Recommendation with rationale

**CRITICAL GATE:** If weighted scores are equivalent (±5%), ask: "What's most important: cost, speed, or maintainability?"

Output to `/docs/discovery/<date>-<topic>/03_option-space.md`.
