---
$schema: "../schemas/option-space.schema.json"
project: "[Project Name]"
date: "YYYY-MM-DD"
decision_status: "pending"
metadata:
  generated_at: "2026-01-06T00:00:00Z"
  generated_by: "[AI Model]"
  discovery_pack_version: "1.0.0"
  validated: false

decision_context:
  what_deciding: "[Clear statement of the decision]"
  why_matters: "[Impact on architecture, UX, cost, timeline]"
  deadline: "[Deadline or trigger]"

options:
  - id: "A"
    name: "[Option A Name]"
    description: "[Detailed explanation]"
    pros:
      - "[Benefit 1]"
      - "[Benefit 2]"
      - "[Benefit 3]"
    cons:
      - "[Drawback 1]"
      - "[Drawback 2]"
      - "[Drawback 3]"
    implementation_complexity:
      effort_estimate: "[Hours/Days/Weeks]"
      key_challenges:
        - "[Challenge 1]"
        - "[Challenge 2]"
    scores:
      performance: 4
      cost: 3
      time_to_ship: 5
      maintainability: 3
      scalability: 4
    weighted_total: 3.8  # Auto-calculated by scripts
    lock_in:
      vendor_lock_in: "low"
      reversibility: true
      exit_strategy: "[Migration path if needed]"
  
  - id: "B"
    name: "[Option B Name]"
    description: "[Detailed explanation]"
    pros:
      - "[Benefit 1]"
    cons:
      - "[Drawback 1]"
    scores:
      performance: 3
      cost: 5
      time_to_ship: 4
      maintainability: 4
      scalability: 3
    weighted_total: 3.9

decision_criteria:
  - name: "performance"
    weight: 0.3
    rationale: "[Why this matters]"
  - name: "cost"
    weight: 0.2
  - name: "time_to_ship"
    weight: 0.2
  - name: "maintainability"
    weight: 0.15
  - name: "scalability"
    weight: 0.15

risk_analysis:
  - option_id: "A"
    risks:
      - description: "[Risk description]"
        likelihood: "medium"
        impact: "high"
        mitigation: "[How to address]"
        owner: "[Name/Role]"

recommendation: "A"
confidence: "high"
rationale: "[Why this option best balances trade-offs]"
conditions: "[Under what conditions might we choose differently]"
---

# Option Space Analysis

**This template includes YAML frontmatter for validation and automation.**

The frontmatter above contains structured data that:
- ✅ Validates against JSON schema
- ✅ Auto-calculates weighted scores
- ✅ Enables gate detection (tied options)
- ✅ Generates handoff artifacts

Keep the markdown body below for human narrative and detailed analysis.

---

## Decision Context

**What are we deciding?**
[Narrative explanation - complements frontmatter]

**Why does this decision matter?**
[Additional context and rationale]

---

## Option A: [Name]

### Description
[Detailed explanation of this approach]

### Pros
- ✅ [Benefit 1]
- ✅ [Benefit 2]

### Cons
- ❌ [Drawback 1]
- ❌ [Drawback 2]

### Trade-offs
[What we gain vs what we give up]

---

## Option B: [Name]

[Same structure as Option A]

---

## Trade-off Matrix

**Auto-generated from frontmatter by validation scripts.**

| Criteria | Weight | Option A | Option B |
|----------|--------|----------|----------|
| Performance | 0.3 | 🟢 4 | 🟡 3 |
| Cost | 0.2 | 🟡 3 | 🟢 5 |
| Time to ship | 0.2 | 🟢 5 | 🟢 4 |
| Maintainability | 0.15 | 🟡 3 | 🟢 4 |
| Scalability | 0.15 | 🟢 4 | 🟡 3 |
| **Weighted Total** | | **3.8** | **3.9** |

🟢 Strong (4-5) | 🟡 Acceptable (2-3) | 🔴 Concern (1)

---

## Recommendation

**Recommended option:** [A/B] (from frontmatter)

**Rationale:**
[Why this option best balances trade-offs given our context]

**Confidence level:** [High/Medium/Low]

**Conditions:**
[Under what conditions might we choose differently?]

---

**Scripts Usage:**

```bash
# Validate this artifact
python scripts/validate.py 03_option-space.md

# Detect if options are tied (critical gate)
python scripts/gate_detector.py ./

# Generate handoff (uses this data)
python scripts/generate_handoff.py ./
```
