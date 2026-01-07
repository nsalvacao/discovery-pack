---
$schema: "../../skill/discovery-pack/schemas/decision-log.schema.json"
project: "LedgerCore"
date: "2026-01-07"
metadata:
  generated_at: "2026-01-07T10:20:00Z"
  generated_by: "claude-3-5-sonnet"
  discovery_pack_version: "2.0.0"
  validated: true

decisions:
  - id: "ADR-001"
    title: "Use PostgreSQL for Core Ledger"
    status: "accepted"
    date: "2026-01-07"
    context: "We need a database that ensures strong consistency and can handle high write throughput. We evaluated DynamoDB and TigerBeetle."
    decision: "We will use PostgreSQL 16 with optimistic locking."
    consequences:
      positive:
        - "Strong ACID guarantees verified by decades of use."
        - "Team has existing expertise."
      negative:
        - "Vertical scaling ceiling is lower than DynamoDB."
        - "Requires careful vacuum tuning."
    related_artifacts: ["03_option-space.md"]

  - id: "ADR-002"
    title: "Integer Math for all Monetary Values"
    status: "accepted"
    date: "2026-01-07"
    context: "Floating point math introduces rounding errors which are unacceptable for financial ledgers."
    decision: "Store all amounts as 64-bit Integers representing 'micros' (1/1,000,000 of a unit)."
    consequences:
      positive:
        - "Mathematically precise operations."
        - "Language agnostic (works in Go, Python, SQL)."
      negative:
        - "Frontend needs to handle formatting/parsing carefully."

  - id: "ADR-003"
    title: "Synchronous Replication Requirement"
    status: "proposed"
    date: "2026-01-07"
    context: "RPO of 0 seconds is required by Risk constraints."
    decision: "Configure RDS Multi-AZ with synchronous replication enabled."
    consequences:
      positive:
        - "Zero data loss on primary failure."
      negative:
        - "Write latency increases by ~2-5ms (RTT to secondary)."
    related_artifacts: ["01_constraints-nfr.md"]
---

# Decision Log (ADR)

## ADR-001: Database Choice
See `03_option-space.md` for the full trade-off matrix. The key deciding factor was **Team Familiarity** vs **Performance Risk**. We chose familiarity (Postgres) but added a validation gate (Load Test) to verify the performance hypothesis.

## ADR-002: Monetary Storage
Standard industry practice. We selected "micros" (6 decimals) instead of "cents" (2 decimals) to support future crypto/FX use cases without database migration.
