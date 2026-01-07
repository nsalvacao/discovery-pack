# Discovery Pack - Full Mode Workflow

**Duration**: 1-2 hours  
**Artifacts**: 8 (00-07, with 04 auto-generated)  
**Best For**: Enterprise, compliance, security-critical, high risk, multi-team

---

## Workflow Overview

**Phase Sequence**:
1. Problem Framing (00) → Foundation
2. Constraints & NFRs (01) → Boundaries
3. Domain Modeling (02) → Language
4. Option Analysis (03) → Alternatives
5. **Auto-generate Assumptions (04)** → Extract from 00-03
6. Validation Planning (05) → Experiments
7. Decision Logging (06) → Rationale
8. Handoff (07) → Spec-kit integration

**Dependencies**:
- 00 must complete before 01-03
- 04 auto-generated after 00-03 complete
- 05 depends on 04
- 06-07 can run after 05

---

## Phase 1: Problem Framing (00_problem-frame.md)

See `lite-mode.md` Phase 1 for detailed instructions.

**Additional Full Mode Fields**:
```yaml
anti_goals:
  - goal: "[What we're NOT solving]"
    rationale: "[Why explicitly out of scope]"

context:
  - factor: "[Market/tech/org context]"
    impact: "[How this affects solution]"
```

---

## Phase 2: Constraints & NFRs (01_constraints-nfr.md)

### Step 2.1: Load Template
Read template: `templates/01_constraints-nfr.md`

### Step 2.2: Security Constraints
```yaml
security:
  authentication:
    description: "[Auth method: SSO/OAuth/API keys]"
    tag: "CONSTRAINT"
  data_protection:
    - requirement: "[PII handling, encryption]"
      tag: "CONSTRAINT"
```

### Step 2.3: Performance Requirements
```yaml
performance:
  response_time_targets:
    - operation: "[API endpoint]"
      target: "p95 [200ms]"
      tag: "ASSUMPTION"
  throughput:
    - metric: "requests_per_second"
      value: "[Target RPS]"
      tag: "ASSUMPTION"
```

### Step 2.4: Availability & Observability
```yaml
availability:
  sla_target: "[99.9%]"
  rto: "[Recovery Time Objective]"
  rpo: "[Recovery Point Objective]"

observability:
  logging:
    - description: "[Log retention, levels]"
      tag: "CONSTRAINT"
  metrics:
    - "[Business/technical metrics]"
```

### Step 2.5: Save & Validate
Save to: `<output-dir>/01_constraints-nfr.md`
Validate: `python3 scripts/validate.py <output-dir>/01_constraints-nfr.md`

---

## Phase 3: Domain Modeling (02_domain-model.md)

### Step 3.1: Load Template
Read template: `templates/02_domain-model.md`

### Step 3.2: Glossary (Required)
```yaml
glossary:
  - term: "[Domain term]"
    definition: "[Clear definition]"
    synonyms_to_avoid:
      - "[Ambiguous alternative]"
```

### Step 3.3: Entities
```yaml
entities:
  - name: "[Entity name]"
    definition: "[What this represents]"
    attributes:
      - name: "[Field name]"
        type: "[Type]"
        description: "[Purpose]"
    lifecycle:
      - "Created"
      - "Active"
      - "Archived"
```

### Step 3.4: Bounded Contexts (Required)
```yaml
bounded_contexts:
  - name: "[Context name]"
    responsibility: "[Domain area covered]"
    entities:
      - "[Entity 1]"
      - "[Entity 2]"
```

### Step 3.5: Save & Validate
Save to: `<output-dir>/02_domain-model.md`
Validate: `python3 scripts/validate.py <output-dir>/02_domain-model.md`

---

## Phase 4: Option Analysis (03_option-space.md)

See `lite-mode.md` Phase 2 for core instructions.

**Additional Full Mode Analysis**:
```yaml
options:
  - name: "[Option]"
    # ... core fields ...
    lock_in:
      vendor_lock_in: "low|medium|high"
      reversibility: true
      exit_strategy: "[How to migrate away]"
    maturity:
      stage: "prototype|mature|legacy"
      community: "[Ecosystem size]"
```

---

## Phase 5: Auto-Generate Assumptions (04_assumptions-unknowns.md)

### Step 5.1: Run Extraction Script
```bash
python3 scripts/extract_assumptions.py <output-dir>
```

**Script behavior**:
- Scans 00-03 for epistemic tags ([ASSUMPTION], [HYPOTHESIS], [CONSTRAINT])
- Extracts tagged statements
- Generates 04_assumptions-unknowns.md automatically
- Cross-references source artifacts

### Step 5.2: Review & Enhance
```yaml
assumptions:
  - id: "A1"
    statement: "[Auto-extracted]"
    priority: "critical|high|medium"
    validation_method: "[How to validate]"
    impact_if_wrong: "[Consequences]"
```

**Manual additions**:
- Add falsification_criteria
- Prioritize assumptions (critical first)
- Link to validation experiments (Phase 6)

### Step 5.3: Save & Validate
Script auto-validates. Manual check: `python3 scripts/validate.py <output-dir>/04_assumptions-unknowns.md`

---

## Phase 6: Validation Planning (05_validation-plan.md)

### Step 6.1: Load Template
Read template: `templates/05_validation-plan.md`

### Step 6.2: Exit Criteria (Required)
```yaml
exit_criteria: "[Conditions to proceed from discovery to implementation]"
```

### Step 6.3: Experiments
```yaml
experiments:
  - id: "E1"
    hypothesis: "If [we do X], then [we expect Y], because [reasoning Z]"
    assumption_id: "A1"
    method: "[Prototype/Interview/A-B test]"
    duration: "[Time estimate]"
    success_criteria:
      quantitative:
        - metric: "[Metric]"
          target: "[Value]"
      qualitative:
        - "[Observable outcome]"
```

**Link to Phase 5**: Map each experiment to assumption ID from 04

### Step 6.4: Save & Validate
Save to: `<output-dir>/05_validation-plan.md`
Validate: `python3 scripts/validate.py <output-dir>/05_validation-plan.md`

---

## Phase 7: Decision Logging (06_decision-log.md)

### Step 7.1: Load Template
Read template: `templates/06_decision-log.md`

### Step 7.2: Log Key Decisions
```yaml
decisions:
  - id: "D1"
    title: "[Decision title]"
    date: "YYYY-MM-DD"
    status: "proposed|accepted|deprecated"
    context: "[Why this decision needed]"
    decision: "[What we decided]"
    consequences:
      positive:
        - "[Benefit 1]"
      negative:
        - "[Trade-off 1]"
    alternatives_rejected:
      - option: "[Alternative]"
        reason: "[Why rejected]"
```

**Best Practice**: One decision per major choice in Phase 4 (Option Analysis)

### Step 7.3: Save & Validate
Save to: `<output-dir>/06_decision-log.md`
Validate: `python3 scripts/validate.py <output-dir>/06_decision-log.md`

---

## Phase 8: Handoff (07_speckit-handoff.md)

See `lite-mode.md` Phase 3 for core instructions.

**Additional Full Mode Content**:
```yaml
artifacts_included:
  - artifact: "00_problem-frame.md"
    status: "complete"
  - artifact: "01_constraints-nfr.md"
    status: "complete"
  - artifact: "02_domain-model.md"
    status: "complete"
  - artifact: "03_option-space.md"
    status: "complete"
  - artifact: "04_assumptions-unknowns.md"
    status: "complete"
  - artifact: "05_validation-plan.md"
    status: "complete"
  - artifact: "06_decision-log.md"
    status: "complete"
  - artifact: "07_speckit-handoff.md"
    status: "complete"

ready_for_speckit: true
```

---

## Final Validation

```bash
# Validate all 8 artifacts
python3 scripts/validate.py <output-dir>/

# Expected output:
✅ 00_problem-frame.md: Valid
✅ 01_constraints-nfr.md: Valid
✅ 02_domain-model.md: Valid
✅ 03_option-space.md: Valid
✅ 04_assumptions-unknowns.md: Valid
✅ 05_validation-plan.md: Valid
✅ 06_decision-log.md: Valid
✅ 07_speckit-handoff.md: Valid

📊 Summary: 8/8 artifacts valid (100%)
```

---

## Token Optimization Tips

1. **Progressive disclosure**: Load templates only when generating that artifact (not all upfront)
2. **Automation first**: Use `extract_assumptions.py` for 04 (saves ~2k tokens)
3. **Batch validation**: Run `validate.py <output-dir>` once at end (not per artifact)
4. **Reference shared-references**: Point to glossary.md, methodologies.md (don't duplicate)

**Target**: ≤25k tokens for full mode execution

---

## Troubleshooting

### Common Validation Errors

**Missing required field**:
```
❌ 02_domain-model.md: Missing required field: bounded_contexts[0].name
```
→ Add `name:` field to bounded_contexts array

**Type mismatch**:
```
❌ 01_constraints-nfr.md: Expected array, got object at performance.throughput
```
→ Convert object to array: `throughput: [{metric: "...", value: "..."}]`

### Automation Script Failures

**extract_assumptions.py fails**:
1. Check 00-03 exist and are valid
2. Ensure tags present: `[ASSUMPTION]`, `[HYPOTHESIS]`, `[CONSTRAINT]`
3. Run with verbose: `python3 scripts/extract_assumptions.py <dir> --verbose`

---

## Time Budget

- Phase 1 (Problem Frame): 10-15 minutes
- Phase 2 (Constraints): 10-15 minutes
- Phase 3 (Domain Model): 15-20 minutes
- Phase 4 (Option Space): 10-15 minutes
- Phase 5 (Assumptions - Auto): 2-5 minutes
- Phase 6 (Validation Plan): 15-20 minutes
- Phase 7 (Decision Log): 10-15 minutes
- Phase 8 (Handoff): 5-10 minutes
- **Total**: 60-120 minutes

---

## Next Steps

After validation passes:
1. Review all 8 artifacts with stakeholders
2. Execute validation experiments from 05
3. Use 07_speckit-handoff.md to start spec-kit workflow
4. Discovery complete → Proceed to specification phase
