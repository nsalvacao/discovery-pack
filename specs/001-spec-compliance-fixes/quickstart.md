# Discovery Pack - Developer Quickstart

**Purpose**: Get developers productive with Discovery Pack in 5 minutes.

---

## Installation (30 seconds)

```bash
# Clone repository
git clone https://github.com/nsalvacao/discovery-pack.git
cd discovery-pack

# Install to your agent (choose one):
cp -r skill/discovery-pack ~/.claude/skills/        # Claude Code
cp -r skill/discovery-pack ~/.copilot/skills/      # Copilot CLI
cp -r skill/discovery-pack .claude/skills/         # Project-local

# Verify
ls ~/.claude/skills/discovery-pack/SKILL.md  # or your chosen path
```

---

## First Discovery (5 minutes)

### Step 1: Activate Skill

Tell your AI agent:
```
"Run discovery-pack in lite mode for a GitHub status dashboard."
```

### Step 2: Agent Execution

The agent automatically:
1. Asks mode selection (lite/full)
2. Creates output directory: `docs/discovery/2026-01-07-github-dashboard/`
3. Generates 3 artifacts:
   - `00_problem-frame.md` - Problem, users, JTBD
   - `03_option-space.md` - Solution alternatives
   - `07_speckit-handoff.md` - Implementation handoff

### Step 3: Validate Output

```bash
# Schema validation (100% pass required)
python3 ~/.claude/skills/discovery-pack/scripts/validate.py docs/discovery/2026-01-07-github-dashboard/

# Expected:
# ✅ 00_problem-frame.md: Valid
# ✅ 03_option-space.md: Valid
# ✅ 07_speckit-handoff.md: Valid
# 📊 Summary: 3/3 artifacts valid (100%)
```

---

## Understanding Output Artifacts

### 00_problem-frame.md
**Purpose**: Problem definition with JTBD analysis  
**Key Sections**:
- `problem_statement` - What pain, who experiences, why now
- `jobs_to_be_done` - Functional, emotional, social jobs
- `success_metrics` - Measurable outcomes

**Use**: Validate you're solving the right problem before building

### 03_option-space.md
**Purpose**: Compare solution alternatives with trade-offs  
**Key Sections**:
- `options[]` - At least 2 alternatives (incl. "Do Nothing")
- `trade_off_matrix` - Complexity, cost, time, risk comparison
- `recommended_option` - Final choice with rationale

**Use**: Ensure you've considered alternatives before committing

### 07_speckit-handoff.md
**Purpose**: Package discovery for spec-kit implementation phase  
**Key Sections**:
- `constitution_input` - Non-negotiable principles, constraints
- `specify_input` - User stories, acceptance criteria
- `ready_for_speckit: true` - Handoff marker

**Use**: Input to `/speckit.constitution` command for implementation

---

## Common Workflows

### Lite Mode (15-30 min)
**When**: Small projects, <5 people, low risk  
**Generates**: 3 artifacts (00, 03, 07)

```
Agent: "Run discovery in lite mode for [project description]"
```

### Full Mode (1-2 hours)
**When**: Enterprise, compliance, high risk  
**Generates**: 8 artifacts (00-07, with 04 auto-generated)

```
Agent: "Run discovery in full mode for [project description]"
```

### Just Validation
**When**: Already have artifacts, need validation

```bash
python3 ~/.claude/skills/discovery-pack/scripts/validate.py <output-dir>
```

---

## Troubleshooting

### "Validation failed"
**Symptom**: `❌ Missing required field: X.Y.Z`  
**Fix**: Add field to YAML frontmatter (check schema for expected format)

### "Template not found"
**Symptom**: `FileNotFoundError: templates/00_problem-frame.md`  
**Fix**: Verify skill directory structure with pre-flight check:
```bash
bash ~/.claude/skills/discovery-pack/scripts/pre-flight-check.sh /tmp/test lite
```

### "Scripts not working"
**Symptom**: `ModuleNotFoundError: No module named 'jsonschema'`  
**Fix**: Install automation dependencies:
```bash
pip install -r ~/.claude/skills/discovery-pack/scripts/requirements.txt
```

---

## Next Steps

1. **Read workflows**: 
   - `shared-references/workflows/lite-mode.md` - Detailed lite mode steps
   - `shared-references/workflows/full-mode.md` - Detailed full mode steps

2. **Review methodologies**:
   - `shared-references/methodologies.md` - JTBD, ADR, Lean Startup guidance
   - `shared-references/glossary.md` - Domain terminology

3. **Explore templates**:
   - `templates/*.md` - See YAML structure for each artifact
   - `schemas/*.schema.json` - Validation rules

4. **Integration**:
   - Use `07_speckit-handoff.md` with [GitHub Spec-Kit](https://github.com/github/spec-kit)
   - Run `/speckit.constitution` to start implementation phase

---

## Developer Tips

**Token Optimization**:
- Use automation scripts (30-40% token savings)
- Load templates just-in-time (not all upfront)
- Reference methodologies (don't duplicate inline)

**Quality Gates**:
- Always validate before progression (100% pass required)
- Use epistemic tags: [ASSUMPTION], [HYPOTHESIS], [CONSTRAINT]
- Cross-reference artifacts (e.g., 05 links to 04 assumption IDs)

**Cross-Agent**:
- Skill works identically in Claude Code, Copilot CLI, project-local
- No agent-specific paths in scripts (relative resolution)
- Test in multiple agents for portability verification

---

## Resources

- **Changelog**: [CHANGELOG.md](../CHANGELOG.md) - Version history
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guidelines
- **License**: [LICENSE](../LICENSE) - MIT
- **Issues**: https://github.com/nsalvacao/discovery-pack/issues

---

**Time to first discovery**: ~5 minutes  
**Skill mastery**: ~2-3 discovery runs  
**Version**: 2.0.0 (flat architecture, 100% schema compliant)
