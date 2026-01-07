---
$schema: "../../skill/discovery-pack/schemas/option-space.schema.json"
project: "LedgerCore"
date: "2026-01-07"
decision_status: "pending"
metadata:
  generated_at: "2026-01-07T10:15:00Z"
  generated_by: "claude-3-5-sonnet"
  discovery_pack_version: "2.0.0"
  validated: true

decision_context:
  what_deciding: "Database architecture for the core ledger"
  why_matters: "Determines throughput, consistency, and maintenance burden."
  deadline: "2026-02-01"

decision_criteria:
  - name: "Consistency"
    weight: 0.4
    rationale: "Financial data requires ACID guarantees."
  - name: "Throughput (Write)"
    weight: 0.3
    rationale: "Must handle Black Friday peaks (10k TPS)."
  - name: "Operational Complexity"
    weight: 0.2
    rationale: "Team is small (4 engineers)."
  - name: "Cost"
    weight: 0.1
    rationale: "Budget is healthy but not infinite."

options:
  - id: "A"
    name: "PostgreSQL with Optimistic Locking"
    description: "Traditional RDBMS using MVCC and optimistic concurrency control."
    pros:
      - "Mature ecosystem"
      - "Strong ACID compliance"
      - "Team already knows SQL"
    cons:
      - "Write scaling limit (vertical scaling)"
      - "Vacuum management overhead"
    scores:
      "Consistency": 5
      "Throughput (Write)": 3
      "Operational Complexity": 5
      "Cost": 4
    weighted_total: 4.3
    lock_in:
      vendor_lock_in: "low"
      reversibility: true
      exit_strategy: "Standard SQL dump"

  - id: "B"
    name: "DynamoDB with Transactions"
    description: "NoSQL with transactional support for items."
    pros:
      - "Infinite horizontal scaling"
      - "Serverless (low ops)"
    cons:
      - "Transactions are expensive ($)"
      - "Limited query patterns"
      - "Hard limit on item size"
    scores:
      "Consistency": 4
      "Throughput (Write)": 5
      "Operational Complexity": 4
      "Cost": 2
    weighted_total: 4.1
    lock_in:
      vendor_lock_in: "high"
      reversibility: false
      exit_strategy: "Complex ETL pipeline required"

  - id: "C"
    name: "TigerBeetle"
    description: "Specialized financial accounting database."
    pros:
      - "Extreme performance (1M TPS)"
      - "Built-in double-entry logic"
    cons:
      - "New/Niche technology"
      - "Small hiring pool"
      - "Vendor risk"
    scores:
      "Consistency": 5
      "Throughput (Write)": 5
      "Operational Complexity": 2
      "Cost": 4
    weighted_total: 4.3
    lock_in:
      vendor_lock_in: "critical"
      reversibility: false
      exit_strategy: "None currently"

recommendation: "A"
confidence: "medium"
rationale: "While TigerBeetle is promising, Option A (Postgres) provides the best balance of risk vs reward for our target of 10k TPS. Postgres on high-end hardware can handle this load without the adoption risk of a niche DB."
conditions: "If load testing shows Postgres cannot sustain 10k TPS with <200ms latency, we will pivot to Option C."
---

# Option Space: Ledger Database

## Analysis

### Option A: PostgreSQL
The safe bet. With careful schema design (append-only ledger table) and partitioning, Postgres can handle high write loads.

### Option C: TigerBeetle
The "Ferrari" option. Technically superior for this exact use case, but introduces significant organizational risk due to lack of in-house expertise.

## Recommendation
Proceed with **Option A**. The team's familiarity with Postgres reduces delivery risk significantly.
