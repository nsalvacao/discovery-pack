---
name: discovery-constraints
description: Define non-functional requirements, security/privacy constraints, performance targets, and trust model. Use in full discovery mode after problem framing. Creates 01_constraints-nfr.md with compliance, performance, observability, and operational constraints.
---

# Constraints & NFRs

Generate `01_constraints-nfr.md` from template, focusing on security, performance, availability, and operational requirements.

## Key Sections
- Security & Privacy (auth, encryption, compliance, trust boundaries)
- Performance & Scalability (response times, throughput, RTO/RPO)
- Availability & Reliability (SLA, fault tolerance)
- Observability (logging, metrics, tracing)
- Compatibility (browser/platform support, dependencies)
- Operational (deployment, cost constraints)

Use `[CONSTRAINT]` tag for non-negotiables. Output to `/docs/discovery/<date>-<topic>/01_constraints-nfr.md`.
