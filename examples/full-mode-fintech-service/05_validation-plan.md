---
$schema: "../../skill/discovery-pack/schemas/validation-plan.schema.json"
project: "LedgerCore"
date: "2026-01-07"
status: "planning"
metadata:
  generated_at: "2026-01-07T10:45:00Z"
  generated_by: "claude-3-5-sonnet"
  discovery_pack_version: "2.0.0"
  validated: true

experiments:
  - id: "EXP-01"
    title: "Postgres Load Test (Spike)"
    hypothesis: "We believe that Postgres 16 can handle 10k TPS. We'll know we're right when we run a 24h stress test."
    assumption_tested: "A001"
    method:
      type: "spike"
      steps:
        - "Provision r6g.4xlarge RDS instance"
        - "Generate 100M dummy ledger rows"
        - "Run k6 script with 10k TPS write rate"
      duration: "3 days"
      tools_needed: ["k6", "AWS RDS", "Datadog"]
    success_criteria:
      quantitative:
        pass_if: "p99_latency < 200ms AND error_rate < 0.01%"
        fail_if: "p99_latency > 200ms OR CPU > 80% sustained"
      qualitative:
        pass_if: "No deadlocks observed in logs"
        fail_if: "Manual intervention required during test"
    result:
      status: "pending"

  - id: "EXP-02"
    title: "QSA Scope Review"
    hypothesis: "We believe existing EKS is compliant. We'll know right when QSA approves design."
    assumption_tested: "A002"
    method:
      type: "user_interview"
      steps:
        - "Draft architecture diagram"
        - "Schedule review with Security Team & Ext Auditor"
      duration: "1 week"
      participants: "Auditor, Tech Lead"
    success_criteria:
      quantitative:
        pass_if: "0 critical compliance blockers found"
        fail_if: "> 0 critical blockers"
      qualitative:
        pass_if: "Auditor signs off on architecture document"
        fail_if: "Auditor requires physical segmentation"
    result:
      status: "pending"

exit_criteria:
  proceed_if:
    - "EXP-01 passes (Postgres viable)"
    - "EXP-02 passes (Compliance OK)"
  pivot_if:
    - "EXP-01 fails -> Evaluate TigerBeetle"
  kill_if:
    - "EXP-02 fails AND New Cluster budget > $50k"
  confidence_threshold: "high"
---

# Validation Plan

## EXP-01: The Performance Gate
This is the "make or break" experiment. If Postgres fails, we change the entire architecture (See Option Space).

## EXP-02: The Compliance Gate
We cannot write code until we know where the code is allowed to run.

