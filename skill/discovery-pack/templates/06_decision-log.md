---
$schema: "../schemas/decision-log.schema.json"
project: "[Project Name]"
date: "YYYY-MM-DD"
metadata:
  generated_at: "2026-01-06T00:00:00Z"
  generated_by: "[AI Model]"
  discovery_pack_version: "2.0.0"
  validated: false

decisions:
  - id: "D1"
    title: "[Decision Title]"
    date: "YYYY-MM-DD"
    status: "accepted"
    decision_makers:
      - "[Name/Role]"
    context: "[What situation led to this decision]"
    decision: "[What was decided - specific and actionable]"
    rationale: "[Why this over alternatives? Trade-offs made?]"
    consequences:
      positive:
        - "[Benefit 1]"
      negative:
        - "[Cost/limitation 1]"
    alternatives_rejected:
      - option: "[Alternative 1]"
        reason: "[Why rejected]"
    open_questions:
      - "[Question still unresolved]"
---

# Decision Log

**This template includes YAML frontmatter for validation and automation.**

The frontmatter above contains structured data that:
- ✅ Validates against JSON schema
- ✅ Records decision history systematically
- ✅ Tracks decision status and ownership
- ✅ Documents alternatives and trade-offs
- ✅ Provides audit trail

Keep the markdown body below for human narrative and detailed analysis.

---

## Purpose

Record **what** was decided, **why**, **by whom**, and **when** - creating a historical record for future reference and onboarding.

**Principle:** Future teams (including future you) will ask "Why did we do it this way?" This document answers that.

---

## Decision Template

### Decision [ID]: [Title]

**Date:** [YYYY-MM-DD]
**Status:** [Proposed | Accepted | Deprecated | Superseded by [Decision ID]]
**Decision maker(s):** [Names/Roles]

**Context:**
[What situation led to needing this decision?]

**Decision:**
[What was decided? Be specific and actionable.]

**Rationale:**
[Why this decision over alternatives? What trade-offs were made?]

**Consequences:**
**Positive:**
- [Benefit 1]
- [Benefit 2]

**Negative/Trade-offs:**
- [Cost 1]
- [Cost 2]

**Risks accepted:**
- [Risk 1]
- [Risk 2]

**Alternatives considered:**
1. **Option:** [Name]
   **Why rejected:** [Reason]

2. **Option:** [Name]
   **Why rejected:** [Reason]

**Related decisions:**
- [Link to Decision X] (depends on this)
- [Link to Decision Y] (related context)

**Review date:** [When to revisit this decision]

---

## Active Decisions

### Decision 001: [Example - Architecture Pattern]

**Date:** 2026-01-06
**Status:** Accepted
**Decision maker(s):** Tech Lead, Engineering Team

**Context:**
We need to choose an architecture pattern for the new project. The system must support multiple projects with agent assignment and GitHub sync.

**Decision:**
Use **MCP Server + Local Dashboard** architecture (Option 2 from option-space analysis).

**Rationale:**
- Lightweight (zero Docker overhead)
- Offline-first with sync
- Agent-native via MCP tools
- Desktop shortcut trivial

**Consequences:**
**Positive:**
- Fast startup (<1 second)
- Works offline
- Easy to extend with new agents
- Minimal resource usage

**Negative/Trade-offs:**
- Need to build MCP server from scratch (~200-300 lines)
- Less mature than using existing PM tool
- Custom UI development needed

**Risks accepted:**
- Risk: MCP protocol may change - Mitigation: Design for abstraction layer
- Risk: Limited team familiarity with MCP - Mitigation: Start with simple implementation

**Alternatives considered:**
1. **Option:** GitHub Projects Native
   **Why rejected:** Still requires browser, less control over UX

2. **Option:** Plane (full PM tool)
   **Why rejected:** Overkill, heavy infrastructure, state sync limitation

**Related decisions:**
- Decision 002 (UI framework choice) depends on this
- Links to: 03_option-space.md

**Review date:** 2026-04-01 (after 3 months of usage)

---

### Decision 002: [Title]

[Same structure as Decision 001]

---

## Deferred Decisions

**Decisions we explicitly chose NOT to make yet:**

| Decision | Why Deferred | When to Decide | Owner |
|----------|--------------|----------------|-------|
| [What needs deciding] | [Reason - lack of info, not blocking, etc.] | [Trigger/deadline] | [Name] |
| UI framework (React vs Vue) | Wait for team preference after dashboard requirements finalized | Week 2 | Frontend Lead |

---

## Open Questions

**Questions raised during discovery that don't have answers yet:**

1. **Q:** [Question]
   **Impact:** [What decision this blocks]
   **Next step:** [How to get answer]
   **Owner:** [Name]

---

## Superseded Decisions

**Decisions we made and later changed:**

### ~~Decision 003: [Old Title]~~

**Original decision date:** [Date]
**Superseded by:** [Decision ID] on [Date]
**Why changed:** [What we learned that invalidated this]

[Original decision content preserved for history]

---

## Decision Categories

### Architecture Decisions
- [Decision 001]: [Title]
- [Decision 002]: [Title]

### Technology Choices
- [Decision ID]: [Title]

### Process Decisions
- [Decision ID]: [Title]

### Product/UX Decisions
- [Decision ID]: [Title]

---

## Decision Dependencies

**Visual map of which decisions depend on others:**

```
Decision 001 (Architecture)
  ├─ Enables → Decision 002 (UI Framework)
  ├─ Enables → Decision 003 (Data Model)
  └─ Constrains → Decision 004 (Deployment)
```

---

## Assumptions Behind Decisions

**Link decisions to assumptions they depend on:**

| Decision | Critical Assumptions | Validation Status |
|----------|---------------------|-------------------|
| [Decision 001] | [Assumption from 04_] | ✅ Validated / ⏳ Pending |
| [Decision 002] | [Assumption from 04_] | ✅ Validated / ⏳ Pending |

**If assumptions are invalidated, these decisions may need revisiting.**

---

## Stakeholder Input

**Who was consulted and what was their input?**

| Stakeholder | Role | Input | Impact on Decision |
|-------------|------|-------|-------------------|
| [Name] | [Role] | [Key feedback] | [Incorporated/Considered/Noted] |

---

## Decision Timeline

**Chronological view:**

| Date | Decision ID | Title | Status |
|------|-------------|-------|--------|
| 2026-01-06 | 001 | Architecture pattern | ✅ Accepted |
| 2026-01-08 | 002 | [Title] | ⏳ Proposed |

---

## Lessons Learned

**Reflections on the decision-making process:**

1. **What went well:**
   - [Positive aspect of decision process]

2. **What could improve:**
   - [How to make better decisions next time]

3. **Surprises:**
   - [Unexpected outcomes or insights]
