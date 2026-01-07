# Discovery Pack - Lite Mode Workflow

**Duration**: 15-30 minutes  
**Artifacts**: 3 (00_problem-frame, 03_option-space, 07_speckit-handoff)  
**Best For**: Small projects, <5 people, low risk, personal/startup

---

## Phase 1: Problem Framing (00_problem-frame.md)

### Step 1.1: Load Template
Read template: `templates/00_problem-frame.md`

### Step 1.2: Problem Statement
Fill YAML frontmatter:
```yaml
problem_statement:
  what_pain: "[Clear problem description]"
  who_experiences: "[User groups affected]"
  why_now: "[Urgency/timing rationale]"
```

**Guiding Questions**:
- What pain are we solving? (not solution - just the problem)
- Who experiences this pain? (personas, not demographics)
- Why does this matter now? (urgency, opportunity)

### Step 1.3: Jobs-to-be-Done
```yaml
jobs_to_be_done:
  functional:
    - "When I [situation], I want to [action], so I can [outcome]"
  emotional:
    - "[How user wants to feel]"
  social:
    - "[How user wants to be perceived]"
```

### Step 1.4: Success Metrics
```yaml
success_metrics:
  - metric: "[Observable outcome]"
    target: "[Measurable goal]"
    baseline: "[Current state]"
```

### Step 1.5: Save & Validate
Save to: `<output-dir>/00_problem-frame.md`
Validate: `python3 scripts/validate.py <output-dir>/00_problem-frame.md`

---

## Phase 2: Option Analysis (03_option-space.md)

### Step 2.1: Load Template
Read template: `templates/03_option-space.md`

### Step 2.2: Option Generation
For each option (minimum 2):
```yaml
options:
  - name: "[Option name]"
    description: "[What this solution does]"
    approach: "[Technical approach]"
    pros:
      - "[Advantage 1]"
      - "[Advantage 2]"
    cons:
      - "[Trade-off 1]"
      - "[Trade-off 2]"
```

**Heuristic**: Always include "Do Nothing" as baseline option

### Step 2.3: Trade-off Matrix
```yaml
trade_off_matrix:
  - dimension: "complexity"
    options:
      - option: "[Option 1]"
        score: "low"
      - option: "[Option 2]"
        score: "high"
```

**Common Dimensions**: complexity, cost, time, risk, vendor_lock_in, scalability

### Step 2.4: Recommendation
```yaml
recommended_option: "[Option name]"
rationale: "[Why this option wins]"
```

### Step 2.5: Save & Validate
Save to: `<output-dir>/03_option-space.md`
Validate: `python3 scripts/validate.py <output-dir>/03_option-space.md`

---

## Phase 3: Handoff (07_speckit-handoff.md)

### Step 3.1: Load Template
Read template: `templates/07_speckit-handoff.md`

### Step 3.2: Constitution Input
```yaml
constitution_input:
  principles:
    - principle: "[Non-negotiable rule]"
      rationale: "[Why this matters]"
  constraints:
    - constraint: "[Hard limit]"
      category: "security|performance|cost"
  glossary:
    - term: "[Domain term]"
      definition: "[Clear definition]"
```

### Step 3.3: Specify Input
```yaml
specify_input:
  users:
    - persona: "[Persona name]"
      jtbd: "When I ___, I want to ___, so I can ___"
  acceptance_criteria:
    - criterion: "[Observable outcome]"
      metric: "[How measured]"
```

### Step 3.4: Artifacts Checklist
```yaml
artifacts_included:
  - artifact: "00_problem-frame.md"
    status: "complete"
  - artifact: "03_option-space.md"
    status: "complete"
  - artifact: "07_speckit-handoff.md"
    status: "complete"

ready_for_speckit: true
```

### Step 3.5: Save & Validate
Save to: `<output-dir>/07_speckit-handoff.md`
Validate: `python3 scripts/validate.py <output-dir>/`

---

## Final Validation

```bash
# Validate all artifacts
python3 scripts/validate.py <output-dir>/

# Expected output:
✅ 00_problem-frame.md: Valid
✅ 03_option-space.md: Valid
✅ 07_speckit-handoff.md: Valid

📊 Summary: 3/3 artifacts valid (100%)
```

---

## Troubleshooting

### Validation Fails
1. Check YAML frontmatter syntax (colons, indentation)
2. Verify required fields present (see schema error message)
3. Check enum values (e.g., vendor_lock_in: low|medium|high)

### Missing Fields
Error message shows: `Missing required field: X.Y.Z`
→ Add field to YAML frontmatter following template structure

### Type Mismatch
Error: `Expected array, got object`
→ Check schema definition, convert format (e.g., single value → list)

---

## Time Budget

- Phase 1 (Problem Frame): 5-10 minutes
- Phase 2 (Option Space): 5-10 minutes
- Phase 3 (Handoff): 5-10 minutes
- **Total**: 15-30 minutes

---

## Next Steps

After validation passes:
1. Review artifacts with stakeholders
2. Use 07_speckit-handoff.md to start `/speckit.constitution`
3. Discovery complete → Proceed to specification phase
