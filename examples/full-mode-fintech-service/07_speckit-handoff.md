---
$schema: "../../skill/discovery-pack/schemas/speckit-handoff.schema.json"
project: "LedgerCore"
date: "2026-01-07"
metadata:
  generated_at: "2026-01-07T11:00:00Z"
  generated_by: "claude-3-5-sonnet"
  discovery_pack_version: "2.0.0"
  validated: true

ready_for_speckit: true
handoff_status: "approved"

core_context:
  problem_summary: "Replace legacy payment processor to handle 10k TPS with strong consistency."
  primary_user: "API Integrator (Merchant Developer)"
  key_constraints:
    - "PCI-DSS v4.0 Compliance"
    - "Run on EKS (EU-West-1)"
    - "PostgreSQL Backend (verified via EXP-01)"
  selected_architecture: "Option A: PostgreSQL with Optimistic Locking"

constitution_inputs:
  principles:
    - "Immutability: Ledger entries are never updated, only appended."
    - "Double-Entry: Every transaction must have balanced debits and credits."
    - "Security First: Compliance trumps performance."
  rules:
    - "All monetary values must be stored as integers (micros)."
    - "No external API calls within a database transaction."

specify_inputs:
  functional_requirements:
    - "System must expose a gRPC API for transaction ingestion."
    - "System must enforce idempotency keys for 24 hours."
  data_models:
    - "Account: {id, currency, balance_snapshot}"
    - "Entry: {id, account_id, amount, transaction_id}"
    - "Transaction: {id, timestamp, metadata, entries[]}"

risk_register:
  critical_assumptions:
    - "Postgres vacuuming will not degrade performance under load (Mitigated by EXP-01)"
  open_questions:
    - "Specific log retention policy for PCI audit logs?"

links:
  problem_frame: "00_problem-frame.md"
  option_space: "03_option-space.md"
  domain_model: "02_domain-model.md"
---

# Spec-Kit Handoff

**Status:** ✅ APPROVED for Specification Phase.

## Instructions for Spec-Kit

1. **Copy `constitution_inputs`** to your `/speckit.constitution` prompt.
2. **Copy `specify_inputs`** to your `/speckit.specify` prompt.
3. **Reference**: "We are building the LedgerCore system defined in `docs/discovery/LedgerCore/`."

## Executive Summary
Discovery is complete. We have validated that PostgreSQL can handle our load (10k TPS) and confirmed our compliance strategy with the auditor. We are ready to specify the gRPC interfaces and database schema details.
