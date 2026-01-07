---
name: discovery-decide
description: Document decisions with rationale, alternatives rejected, and consequences. ADR-style decision log. Use in full discovery mode after validation. Creates 06_decision-log.md with decision ID, context, rationale, trade-offs, and superseded decisions.
---

# Decision Logging

Generate `06_decision-log.md` using ADR (Architecture Decision Record) format.

## Structure per Decision
- **Decision ID**: Sequential (001, 002, ...)
- **Date**: YYYY-MM-DD
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: Why this decision was needed
- **Decision**: What was chosen
- **Rationale**: Why this over alternatives
- **Consequences**: Positive and negative
- **Alternatives rejected**: With reasons

Link decisions to assumptions from `04_`. Track superseded decisions for history.

Output to `/docs/discovery/<date>-<topic>/06_decision-log.md`.
