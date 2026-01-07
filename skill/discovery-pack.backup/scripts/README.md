# Discovery Pack Scripts

Enterprise-grade automation for discovery artifacts.

## Installation

```bash
pip install -r requirements.txt
```

## Scripts

### 1. validate.py
**Purpose:** Validate artifacts against JSON schemas

**Usage:**
```bash
# Validate entire discovery directory
python validate.py /docs/discovery/2026-01-06-topic/

# Validate single artifact
python validate.py /docs/discovery/2026-01-06-topic/03_option-space.md

# Verbose mode
python validate.py /docs/discovery/2026-01-06-topic/ --verbose
```

**Output:**
```
🔍 Validating 7 artifacts in 2026-01-06-topic/

✅ 00_problem-frame.md: Valid
✅ 03_option-space.md: Valid
❌ 05_validation-plan.md: Validation failed
   Error: 'quantitative' is a required property
   Path: experiments > 0 > success_criteria

📊 Results: 6 passed, 1 failed
```

---

### 2. extract_assumptions.py
**Purpose:** Auto-generate 04_assumptions-unknowns.md from tagged statements

**Usage:**
```bash
python extract_assumptions.py /docs/discovery/2026-01-06-topic/
```

**What it does:**
1. Scans 00-03 for `[FACT]`, `[ASSUMPTION]`, `[HYPOTHESIS]`, `[CONSTRAINT]` tags
2. Prioritizes by context (critical/high/medium/low)
3. Generates structured 04_ with frontmatter + markdown

**Output:**
```
🔍 Scanning 00_problem-frame.md...
🔍 Scanning 01_constraints-nfr.md...
🔍 Scanning 02_domain-model.md...
🔍 Scanning 03_option-space.md...

📊 Found 18 tagged statements

✅ Generated: 04_assumptions-unknowns.md
   12 assumptions extracted
```

---

### 3. generate_handoff.py
**Purpose:** Auto-generate 07_speckit-handoff.md from all artifacts

**Usage:**
```bash
python generate_handoff.py /docs/discovery/2026-01-06-topic/
```

**What it does:**
1. Extracts frontmatter from 00-06
2. Maps to constitution input (principles, constraints, glossary)
3. Maps to specify input (users, journeys, metrics)
4. Generates ready-to-copy sections

**Output:**
```
✅ Generated: 07_speckit-handoff.md
```

---

### 4. gate_detector.py
**Purpose:** Detect critical decision gates automatically

**Usage:**
```bash
python gate_detector.py /docs/discovery/2026-01-06-topic/
```

**What it detects:**
1. **Equivalent options:** Weighted scores within ±5%
2. **Unmeasurable validation:** Experiments lacking quantitative metrics
3. **Contradictory assumptions:** Conflicting constraints (basic keyword detection)

**Output:**
```
🚨 2 Critical Gates Detected

⚠️  GATE: Options tied (scores: [4.2, 4.3, 2.1])
   Action: Ask user for decision criteria

⚠️  GATE: Experiment 'User interviews' lacks quantitative metrics
   Action: Define measurable success criteria
```

---

### 5. audit_logger.py
**Purpose:** Add generation metadata to artifacts

**Usage:**
```bash
# Add metadata to all artifacts in directory
python audit_logger.py /docs/discovery/2026-01-06-topic/ claude-sonnet-4.5

# Add metadata to single artifact
python audit_logger.py /docs/discovery/2026-01-06-topic/00_problem-frame.md gpt-5.1-codex-max
```

**What it adds:**
```yaml
metadata:
  generated_at: "2026-01-06T15:23:45Z"
  generated_by: "claude-sonnet-4.5"
  discovery_pack_version: "1.0.0"
  validated: false
```

---

## Workflow Integration

### Lite Mode (3 artifacts)
```bash
# 1. Generate artifacts with AI
/discovery-run --lite

# 2. Add metadata
python audit_logger.py /docs/discovery/2026-01-06-pm-tool/ claude-sonnet-4.5

# 3. Validate
python validate.py /docs/discovery/2026-01-06-pm-tool/

# 4. Generate handoff
python generate_handoff.py /docs/discovery/2026-01-06-pm-tool/
```

### Full Mode (7 artifacts)
```bash
# 1. Generate 00-03 with AI
/discovery-run --full

# 2. Extract assumptions (auto-generates 04_)
python extract_assumptions.py /docs/discovery/2026-01-06-topic/

# 3. Generate 05-06 with AI
# (validation plan, decision log)

# 4. Check for gates
python gate_detector.py /docs/discovery/2026-01-06-topic/
# → If gates found, resolve before continuing

# 5. Generate handoff
python generate_handoff.py /docs/discovery/2026-01-06-topic/

# 6. Add metadata
python audit_logger.py /docs/discovery/2026-01-06-topic/

# 7. Final validation
python validate.py /docs/discovery/2026-01-06-topic/
```

---

## Continuous Validation (CI/CD)

```bash
#!/bin/bash
# .github/workflows/validate-discovery.sh

set -e

# Install dependencies
pip install -r scripts/requirements.txt

# Validate all discovery directories
for dir in docs/discovery/*/; do
  echo "Validating $dir"
  python scripts/validate.py "$dir"
done

echo "✅ All discovery artifacts valid"
```

---

## Troubleshooting

**Q: `jsonschema` import error?**
```bash
pip install jsonschema PyYAML
```

**Q: Validation fails with "No YAML frontmatter"?**
A: Artifacts need `---` delimited frontmatter. Use updated templates.

**Q: `$ref` resolution errors?**
A: Ensure `common.schema.json` exists in `schemas/` directory.

**Q: Gate detector finds no gates?**
A: Good! No critical decision points detected. Proceed with confidence.

---

**Token Efficiency:** Using scripts saves ~30-40% tokens vs manual AI generation of these artifacts.

**Reproducibility:** Same inputs → deterministic outputs.

**Enterprise Audit Trail:** Full metadata tracking for compliance.
