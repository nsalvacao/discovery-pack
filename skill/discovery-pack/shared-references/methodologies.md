# Discovery Methodologies Reference

This document describes the core methodologies combined in Discovery Pack.

---

## Jobs-to-be-Done (JTBD)

**Purpose:** Understand user motivation beyond feature requests.

**Format:**
```
When I [situation],
I want to [action],
So I can [outcome]
```

**Example:**
```
When I switch between multiple projects,
I want to see all their statuses at a glance,
So I can prioritize work without context-switching overhead
```

**Key Principles:**
- Focus on the job, not the user demographics
- Separate functional, emotional, and social jobs
- Identify the "firing moment" (when user decides to act)

**Use in Discovery Pack:** Primary structure for `00_problem-frame.md`

---

## Amazon PR/FAQ

**Purpose:** Force clarity on problem, customer, and solution before building.

**Structure:**
1. **Press Release:** What you'd announce when shipping
2. **FAQ:** Anticipated questions from customers and internal stakeholders

**Key Questions:**
- Who is the customer?
- What is the problem?
- What is the benefit?
- How does it work?
- Why now?

**Use in Discovery Pack:** Influences problem statement and success metrics

---

## Architecture Decision Records (ADR)

**Purpose:** Document architectural decisions with context and consequences.

**Template:**
```markdown
# ADR-001: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Deciders:** [Names]

## Context
[Problem and forces at play]

## Decision
[What we decided]

## Consequences
- Positive: [Benefits]
- Negative: [Trade-offs]
- Neutral: [Side effects]

## Alternatives Considered
- Option A: [Why rejected]
- Option B: [Why rejected]
```

**Use in Discovery Pack:** Structure for `06_decision-log.md`

---

## Lean Startup Validation

**Purpose:** Test assumptions before full commitment.

**Build-Measure-Learn Loop:**
1. **Build:** Minimum viable experiment
2. **Measure:** Collect data against hypothesis
3. **Learn:** Pivot or persevere

**Types of Experiments:**
- **Smoke test:** Landing page to gauge interest
- **Concierge MVP:** Manual service before automation
- **Wizard of Oz:** Fake automation, human behind scenes
- **A/B test:** Compare alternatives with real users

**Success Criteria Must Be:**
- **Quantitative:** Numbers, not feelings
- **Actionable:** Clear next step based on result
- **Accessible:** Measurable within constraints

**Use in Discovery Pack:** Framework for `05_validation-plan.md`

---

## Domain-Driven Design (DDD) - Light

**Purpose:** Model the problem domain with ubiquitous language.

**Core Concepts:**
- **Entities:** Objects with identity (User, Order)
- **Value Objects:** Immutable descriptors (Email, Money)
- **Aggregates:** Consistency boundaries
- **Events:** Things that happened (OrderPlaced)
- **Bounded Contexts:** Semantic boundaries

**Ubiquitous Language:**
- Use domain expert terminology
- Avoid technical jargon in domain model
- Document in glossary

**Use in Discovery Pack:** Structure for `02_domain-model.md`

---

## Tag System (Epistemic Humility)

**Purpose:** Distinguish knowledge from assumptions.

| Tag | Meaning | Example |
|-----|---------|---------|
| `[FACT]` | Verified with data | "80% of users are on mobile [FACT - analytics]" |
| `[ASSUMPTION]` | Testable hypothesis | "Users prefer dark mode [ASSUMPTION]" |
| `[HYPOTHESIS]` | Educated guess | "Real-time sync increases retention [HYPOTHESIS]" |
| `[CONSTRAINT]` | Non-negotiable | "Must run on WSL [CONSTRAINT - technical]" |

**Why This Matters:**
- Forces explicit about unknowns
- Makes assumptions testable
- Enables risk-based prioritization

**Use in Discovery Pack:** Applied across all artifacts

---

## References

- **JTBD:** [When Coffee and Kale Compete](https://www.amazon.com/When-Coffee-Kale-Compete/dp/1539891941) by Alan Klement
- **Amazon PR/FAQ:** [Working Backwards](https://www.amazon.com/Working-Backwards-Insights-Stories-Secrets/dp/1250267595) by Colin Bryar & Bill Carr
- **ADR:** [Michael Nygard's blog](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- **Lean Startup:** [The Lean Startup](https://www.amazon.com/Lean-Startup-Entrepreneurs-Continuous-Innovation/dp/0307887898) by Eric Ries
- **DDD:** [Domain-Driven Design](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) by Eric Evans
