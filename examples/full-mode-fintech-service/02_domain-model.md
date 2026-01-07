---
$schema: "../../skill/discovery-pack/schemas/domain-model.schema.json"
project: "LedgerCore"
date: "2026-01-07"
metadata:
  generated_at: "2026-01-07T10:10:00Z"
  generated_by: "claude-3-5-sonnet"
  discovery_pack_version: "2.0.0"
  validated: true

ubiquitous_language:
  - term: "Entry"
    definition: "An atomic record of value movement affecting a single account."
  - term: "Transaction"
    definition: "A grouped set of Entries that must balance to zero."
  - term: "Posting"
    definition: "The act of committing a Transaction to the permanent log."
  - term: "Settlement"
    definition: "The actual movement of funds between external banking rails."

entities:
  - name: "Account"
    type: "Aggregate Root"
    description: "Holds the current balance and metadata for a specific user/currency pair."
    properties:
      - "id: UUID"
      - "currency: ISO 4217"
      - "balance: Integer (Micros)"
      - "version: BigInt (Optimistic Lock)"
  
  - name: "Transaction"
    type: "Entity"
    description: "The source of truth for all changes."
    properties:
      - "id: UUID"
      - "entries: List[Entry]"
      - "state: Enum(PENDING, POSTED, VOIDED)"
      - "timestamp: UTC"

relationships:
  - "Account has many Entries"
  - "Transaction contains 2+ Entries"
  - "Entry belongs to exactly 1 Account"

bounded_contexts:
  - name: "Ledger Context"
    responsibility: "Recording immutable history and calculating balances."
  - name: "Payment Gateway Context"
    responsibility: "Talking to Visa/Mastercard and external providers."
---

# Domain Model

## Core Invariant: The Accounting Equation
For every `Transaction`, the sum of `amount` in all child `Entries` must equal **ZERO**. 
If `Sum(Entries) != 0`, the transaction is invalid and must be rejected by the domain layer.

## Concurrency Model
We use `Account.version` for Optimistic Concurrency Control (OCC). 
1. Read Account (v1)
2. Calculate new balance
3. Write Account (v2) WHERE version = 1
4. If rows_affected == 0, retry.
