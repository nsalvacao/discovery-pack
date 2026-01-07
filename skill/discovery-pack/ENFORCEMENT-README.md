# Discovery Pack Enforcement System

**Version:** 2.0 (Enhanced with Multi-Layer Compliance)  
**Purpose:** Guarantee correct workflow execution with automated enforcement

---

## 🎯 Problem Solved

Previously, discovery-pack execution relied on manual interpretation, leading to:
- ❌ Ignored sub-skill instructions
- ❌ Missing YAML frontmatter
- ❌ No epistemic tags applied
- ❌ Arbitrary filenames (not schema-validated)
- ❌ Ad-hoc markdown instead of templates

**Result:** Artifacts that don't validate and can't integrate with spec-kit.

---

## ✅ Solution: 3-Layer Enforcement

### Layer 1: Pre-Flight Check
**Script:** `pre-flight-check.sh`  
**Purpose:** Validate environment and show requirements BEFORE starting

```bash
bash ~/.copilot/skills/discovery-pack/pre-flight-check.sh <output-dir> <mode>
```

**What it does:**
- ✅ Validates mode selection (lite/full)
- ✅ Checks Python + dependencies availability
- ✅ Shows required artifacts checklist
- ✅ Explains workflow steps
- ✅ Highlights critical requirements (YAML, tags, templates)

**When to use:** ALWAYS run this first before starting discovery

---

### Layer 2: Workflow Executor (RECOMMENDED)
**Script:** `discovery-pack-run.sh`  
**Purpose:** Enforce correct workflow with validation gates at each step

```bash
bash ~/.copilot/skills/discovery-pack/discovery-pack-run.sh <output-dir> <mode> "<project-name>"
```

**Example:**
```bash
bash ~/.copilot/skills/discovery-pack/discovery-pack-run.sh \
  ./docs/discovery/2026-01-06-nexus \
  full \
  "NEXUS CLI FLEET"
```

**What it does:**
- ✅ Shows sub-skill instructions before each artifact
- ✅ Pauses for artifact generation (interactive gate)
- ✅ Validates artifact immediately after creation
- ✅ BLOCKS progression if validation fails
- ✅ Auto-generates 04_assumptions-unknowns.md via script
- ✅ Final compliance report at end

**Workflow:**
```
For each artifact:
  1. Show template location
  2. Show sub-skill instructions (inline)
  3. Pause: "Generate artifact and press ENTER"
  4. Validate artifact (YAML, schema, tags)
  5. If FAIL → exit with error
  6. If PASS → continue to next
```

**When to use:** ALWAYS for production/serious discovery work

---

### Layer 3: Post-Validation Compliance
**Script:** `compliance_checker.py`  
**Purpose:** Final safety net - verify ALL requirements met

```bash
python3 ~/.copilot/skills/discovery-pack/scripts/compliance_checker.py <output-dir> <mode>
```

**What it checks:**
- ✅ All required artifacts exist
- ✅ YAML frontmatter present and valid
- ✅ Epistemic tags applied (`[FACT]`, `[ASSUMPTION]`, etc.)
- ✅ Template structure followed (key sections present)

**Output:**
```
🔍 Discovery Pack Compliance Report
====================================
Output Directory: ./docs/discovery/...
Mode: full

📁 Check 1: Artifact Files
  ✅ Found: 00_problem-frame.md
  ✅ Found: 01_constraints-nfr.md
  ...

📄 Check 2: YAML Frontmatter
  ✅ Valid YAML frontmatter: 00_problem-frame.md
  ...

🏷️  Check 3: Epistemic Tags
  ✅ Epistemic tags present (47 total): 00_problem-frame.md
     Tags: {"FACT": 12, "ASSUMPTION": 28, "CONSTRAINT": 7}
  ...

📋 Check 4: Template Structure
  ✅ Template structure followed: 00_problem-frame.md
  ...

====================================
✅ COMPLIANCE: PASS
====================================
```

**When to use:** ALWAYS after discovery completion (safety check)

---

## 🚀 Usage Patterns

### Pattern A: Full Automation (RECOMMENDED)
```bash
# Step 1: Pre-flight check
bash ~/.copilot/skills/discovery-pack/pre-flight-check.sh ./docs/discovery/2026-01-06-topic full

# Step 2: Run workflow executor
bash ~/.copilot/skills/discovery-pack/discovery-pack-run.sh ./docs/discovery/2026-01-06-topic full "Project Name"
# (Script guides you through each artifact with validation)

# Step 3: Final compliance check (automatic in executor, but can re-run)
python3 ~/.copilot/skills/discovery-pack/scripts/compliance_checker.py ./docs/discovery/2026-01-06-topic full
```

**Result:** Guaranteed compliant artifacts

---

### Pattern B: Manual with Inline Instructions
If executor not used (not recommended), follow inline sub-skill instructions in `SKILL.md` Step 3.

**Requirements:**
1. Read SKILL.md Step 3 completely
2. For each artifact:
   - Read template from `templates/<artifact-name>.md`
   - Follow sub-skill instructions (inline in SKILL.md)
   - Apply YAML frontmatter
   - Apply epistemic tags
   - Save with exact filename
3. Validate after EACH artifact: `python3 scripts/validate.py <output-dir>`
4. Final compliance check: `python3 scripts/compliance_checker.py <output-dir> <mode>`

**Risk:** Higher chance of deviation without automated gates

---

## 📋 Enforcement Checklist

Before starting discovery, confirm:
- [ ] Pre-flight check executed
- [ ] Mode selected (lite/full)
- [ ] Output directory created
- [ ] Python + dependencies available (for validation)

During discovery, confirm for EACH artifact:
- [ ] Template loaded from `templates/` directory
- [ ] YAML frontmatter included (--- delimiters)
- [ ] Epistemic tags applied to all claims
- [ ] Filename matches exactly (00_, 01_, not 01-, 01_jtbd, etc.)
- [ ] Artifact validates with `validate.py`

After discovery, confirm:
- [ ] All artifacts present (lite: 3, full: 8)
- [ ] Compliance checker passes
- [ ] `07_speckit-handoff.md` reviewed and ready for spec-kit

---

## 🔧 Helper Scripts

### Template Filler (Alternative to Manual)
```bash
python3 scripts/template_filler.py 00_problem-frame.md ./output/00_problem-frame.md --project "My Project" --validate
```

Generates artifact with correct YAML frontmatter from template.

### Extract Assumptions (Auto)
```bash
python3 scripts/extract_assumptions.py <output-dir>
```

Scans artifacts 00-03 for `[ASSUMPTION]` and `[HYPOTHESIS]` tags, generates `04_assumptions-unknowns.md`.

### Validation (Single Artifact)
```bash
python3 scripts/validate.py <output-dir>/00_problem-frame.md
```

Validates single artifact against JSON schema.

### Validation (All Artifacts)
```bash
python3 scripts/validate.py <output-dir>
```

Validates all artifacts in directory.

---

## 🛡️ Why This Guarantees Compliance

**Problem:** Manual execution allows deviation (human error, overconfidence, time pressure)

**Solution:** Multi-layer defense

1. **Pre-flight** → Shows requirements upfront (can't claim ignorance)
2. **Executor** → Gates at each step, validation blocking (can't skip)
3. **Compliance Checker** → Final verification (catches edge cases)
4. **Inline Instructions** → No need to "invoke sub-skills" (instructions embedded in SKILL.md)

**Result:** Even if one layer fails (e.g., executor not used), others catch deviations.

---

## 📚 File Structure

```
~/.copilot/skills/discovery-pack/
├── SKILL.md                     # Main skill (with inline sub-skills)
├── SKILL.md.backup              # Original (before enhancement)
├── pre-flight-check.sh          # Layer 1: Pre-flight
├── discovery-pack-run.sh        # Layer 2: Executor
├── scripts/
│   ├── validate.py              # Schema validation
│   ├── extract_assumptions.py  # Auto-generate 04_
│   ├── compliance_checker.py   # Layer 3: Post-validation
│   ├── template_filler.py      # Template helper
│   └── requirements.txt         # Python deps
├── templates/
│   ├── 00_problem-frame.md     # All templates with YAML
│   ├── 01_constraints-nfr.md
│   └── ...
├── schemas/
│   ├── problem-frame.schema.json  # Validation schemas
│   └── ...
└── discovery-*/                 # Sub-skill directories (reference)
```

---

## 🎓 For AI Executors (Claude, etc.)

When invoking `discovery-pack` skill:

**MUST DO:**
1. ✅ Run `pre-flight-check.sh` first
2. ✅ Use `discovery-pack-run.sh` executor (not manual)
3. ✅ Read inline sub-skill instructions in SKILL.md Step 3
4. ✅ Use templates from `templates/` directory
5. ✅ Include YAML frontmatter in ALL artifacts
6. ✅ Apply epistemic tags to ALL claims
7. ✅ Validate after each artifact with `validate.py`
8. ✅ Run `compliance_checker.py` at end

**MUST NOT DO:**
- ❌ Create arbitrary filenames (must match 00_, 01_, etc.)
- ❌ Skip YAML frontmatter
- ❌ Generate markdown without templates
- ❌ Skip validation steps
- ❌ Proceed if validation fails

**Cognitive Aid:**
- Treat workflow as PIPELINE with GATES (not buffet)
- Validation failure = STOP, not warning
- Templates are MANDATORY, not optional
- Sub-skill instructions are EMBEDDED (not separate invocations)

---

## ✅ Success Criteria

Discovery execution is compliant when:
1. All artifacts exist with correct filenames
2. YAML frontmatter validates against schemas
3. Epistemic tags applied (>0 tags per artifact, ideally >10)
4. Template structure followed
5. `compliance_checker.py` reports: **COMPLIANCE: PASS**

---

## 🔄 Maintenance

This enforcement system is **persistent** (survives across sessions) because:
- Scripts are filesystem-based (not memory-based)
- SKILL.md has inline instructions (no external dependencies)
- Validation schemas are versioned
- Can be run independently by user OR AI

**Updates:** Modify scripts/SKILL.md as needed. System is modular.

---

**Version:** 2.0.0  
**Last Updated:** 2026-01-06  
**Author:** Enhanced discovery-pack enforcement system
