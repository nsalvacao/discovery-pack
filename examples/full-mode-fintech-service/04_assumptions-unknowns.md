---
$schema: "../../skill/discovery-pack/schemas/assumptions-unknowns.schema.json"
project: "LedgerCore"
date: "2026-01-07"
metadata:
  generated_at: "2026-01-07T10:30:00Z"
  generated_by: "extract_assumptions.py"
  discovery_pack_version: "2.0.0"
  validated: false

assumptions:
  - id: "A001"
    assumption: "PostgreSQL can handle 10k TPS on a single writer instance with optimized hardware."
    tag: "HYPOTHESIS"
    priority: "critical"
    falsification_test: "Load test with pgbench simulation of ledger workload."
    impact_if_wrong: "Must pivot to sharding or TigerBeetle (Option C)."
    source_artifact: "03_option-space.md"

  - id: "A002"
    assumption: "We can use existing Kubernetes cluster for PCI-DSS workload without re-audit."
    tag: "ASSUMPTION"
    priority: "high"
    falsification_test: "Consult with QSA auditor."
    impact_if_wrong: "Delay project by 3 months to build isolated VPC."
    source_artifact: "00_problem-frame.md"

  - id: "A003"
    assumption: "Merchants will accept a 200ms latency budget for synchronous transactions."
    tag: "ASSUMPTION"
    priority: "medium"
    falsification_test: "Survey top 5 merchants."
    impact_if_wrong: "Must implement async callback architecture."
    source_artifact: "00_problem-frame.md"
---

# Assumptions & Unknowns

**Purpose:** Explicitly capture what we assume to be true but haven't verified.

## Critical Risks

### 🔴 A001: Postgres Performance
We are betting the company on Postgres being "fast enough". This is a [HYPOTHESIS] because we haven't tested our specific access patterns (heavy write, low read) at scale.

### 🟡 A002: Compliance Scope
We assume the current EKS cluster is compliant. If the QSA decides that mixed workloads pollute the scope, we need a new cluster.

