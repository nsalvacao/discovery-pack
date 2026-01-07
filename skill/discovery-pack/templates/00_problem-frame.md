---
$schema: "../schemas/problem-frame.schema.json"
project: "[Project Name]"
date: "YYYY-MM-DD"
status: "draft"
metadata:
  generated_at: "2026-01-06T00:00:00Z"
  generated_by: "[AI Model]"
  discovery_pack_version: "2.0.0"
  validated: false

problem_statement:
  what_pain: "[Clear, concise description of the problem]"
  who_experiences: "[User groups affected]"
  why_now: "[Why this matters now]"

users:
  primary:
    - persona: "[Persona Name]"
      role: "[Role]"
      jtbd: "When I ___, I want to ___, so I can ___"
      pain_points:
        - "[Pain 1]"
        - "[Pain 2]"
      success_criteria: "[Observable outcome]"
  secondary:
    - "[Stakeholder 1]"
    - "[Stakeholder 2]"

jobs_to_be_done:
  functional:
    - job: "[Job 1]"
      when: "[Situation]"
      want: "[Desired action]"
      so_that: "[Outcome]"
  emotional:
    - "[Feeling/status desired]"
  social:
    - "[How user wants to be perceived]"

anti_goals:
  - goal: "[Anti-goal 1]"
    rationale: "[Why not solving this]"
  - goal: "[Anti-goal 2]"
    rationale: "[Another thing we're NOT solving]"

out_of_scope_v1:
  - "[Feature deferred to v2]"
  - "[Another deferred feature]"

success_metrics:
  north_star: "[Primary success metric]"
  leading_indicators:
    - metric: "[Metric 1]"
      baseline: "[Current value]"
      target: "[Goal value]"
      measurement: "[How measured]"
  lagging_indicators:
    - "[Long-term impact metric]"

context:
  market:
    description: "[Competitive landscape, trends]"
    tag: "ASSUMPTION"
  technical:
    description: "[Existing systems, tech stack]"
    tag: "CONSTRAINT"
  organizational:
    description: "[Team, timeline, budget]"
    tag: "CONSTRAINT"
  regulatory:
    description: "[Legal requirements, standards]"
    tag: "CONSTRAINT"
---

# Problem Frame

**This template includes YAML frontmatter for validation and automation.**

The frontmatter above contains structured data that:
- ✅ Validates against JSON schema
- ✅ Enables auto-extraction of assumptions
- ✅ Feeds into handoff generation
- ✅ Provides audit trail

Keep the markdown body below for human narrative and detailed analysis.

---

## Problem Statement

[FACT/ASSUMPTION/HYPOTHESIS/CONSTRAINT] Clear, concise description of the problem being solved.

**What pain exists today?**
[Describe current state and friction]

**Who experiences this pain?**
[Primary and secondary users/stakeholders]

**Why does this matter now?**
[Urgency, opportunity, or forcing function]

---

## Users & Personas

### Primary Users
| Persona | Role | JTBD | Pain Points | Success Looks Like |
|---------|------|------|-------------|---------------------|
| [Name]  | [Role] | When I ___, I want to ___, so I can ___ | [List 2-3] | [Observable outcome] |

### Secondary Users
[Stakeholders affected but not primary users]

---

## Jobs-to-be-Done (JTBD)

### Functional Jobs
1. **[Job 1]:** When I ___, I want to ___, so I can ___
2. **[Job 2]:** When I ___, I want to ___, so I can ___

### Emotional Jobs
- [What feelings/status does user want?]

### Social Jobs
- [How does user want to be perceived?]

---

## Anti-Goals

**What are we explicitly NOT solving?**

1. [Anti-goal 1] - *Why:* [Rationale]
2. [Anti-goal 2] - *Why:* [Rationale]

**Out of scope for v1:**
- [Feature/concern deferred]

---

## Success Metrics

### North Star Metric
[Primary metric that indicates success]

### Leading Indicators
| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| [Metric 1] | [Current] | [Goal] | [How measured] |
| [Metric 2] | [Current] | [Goal] | [How measured] |

### Lagging Indicators
- [Long-term impact metrics]

---

## Context & Constraints

### Market Context
[FACT/ASSUMPTION] [Competitive landscape, user expectations, trends]

### Technical Context
[CONSTRAINT] [Existing systems, tech stack, integrations required]

### Organizational Context
[CONSTRAINT] [Team, timeline, budget, political considerations]

### Regulatory/Compliance
[CONSTRAINT] [Legal requirements, industry standards]

---

## Tag Legend

- **[FACT]** - Verified through data/research
- **[ASSUMPTION]** - Testable hypothesis we believe is true
- **[HYPOTHESIS]** - Educated guess requiring validation
- **[CONSTRAINT]** - Non-negotiable requirement
