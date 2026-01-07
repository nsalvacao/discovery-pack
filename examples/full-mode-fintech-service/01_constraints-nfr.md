---
$schema: "../../skill/discovery-pack/schemas/constraints-nfr.schema.json"
project: "LedgerCore"
date: "2026-01-07"
metadata:
  generated_at: "2026-01-07T10:05:00Z"
  generated_by: "claude-3-5-sonnet"
  discovery_pack_version: "2.0.0"
  validated: true

compliance:
  - id: "C01"
    requirement: "PCI-DSS v4.0 Requirement 3.4"
    impact: "PANs must be unreadable anywhere they are stored."
    source: "Security Policy"
  - id: "C02"
    requirement: "GDPR Article 17 (Right to Erasure)"
    impact: "Must support PII deletion without breaking ledger integrity (crypto-shredding)."
    source: "Legal"

security:
  - category: "Authentication"
    requirement: "mTLS required for all service-to-service communication."
  - category: "Audit"
    requirement: "All write operations must generate a tamper-evident audit log."

performance:
  - metric: "Write Throughput"
    target: "10,000 TPS"
    condition: "Peak load (Black Friday)"
  - metric: "End-to-End Latency"
    target: "< 200ms p99"
    condition: "Synchronous API calls"

reliability:
  availability_target: "99.99%"
  rpo: "0 seconds (No data loss allowed)"
  rto: "15 minutes"

observability:
  - "Distributed tracing (OpenTelemetry) required."
  - "Business metrics (Money moved) must be emitted as high-cardinality events."
---

# Constraints & NFRs

## Compliance Strategy
Due to **C01 (PCI-DSS)**, we will isolate the Cardholder Data Environment (CDE) from the Ledger core. The Ledger will only store tokenized references, never raw PANs.

## Data Integrity
**RPO of 0 seconds** dictates that we cannot use asynchronous replication for the primary commit path. We must use synchronous replication with quorum writes.
