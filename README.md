# Discovery Pack

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/spec-agent%20skills-purple.svg)](https://agentskills.io/specification)

**Transform ambiguous ideas into structured specifications using proven methodologies.**

---

## Overview

Discovery Pack is a comprehensive AI agent skill package containing 8 interconnected skills for rigorous project discovery. Combines Jobs-to-be-Done, Amazon PR/FAQ, Architecture Decision Records, and Lean Startup validation into a repeatable workflow that produces spec-kit compatible outputs.

**Key Benefits:**
- ✅ Reduce rework from unclear requirements
- ✅ Distinguish facts from assumptions explicitly
- ✅ Document decisions with rationale
- ✅ Validate critical assumptions before building
- ✅ Generate implementation-ready specifications

---

## Quick Installation

```bash
# Clone repository
git clone https://github.com/nsalvacao/discovery-pack.git
cd discovery-pack

# Install skill package
cp -r skill/discovery-pack ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/discovery-pack/SKILL.md
```

**For other agents:**
```bash
# GitHub Copilot CLI
cp -r skill/discovery-pack ~/.copilot/skills/

# Project-specific (any agent)
cp -r skill/discovery-pack .claude/skills/
```

---

## Quick Start

Tell your AI agent:

```
"I want to build a local dashboard that syncs GitHub status. Run discovery in lite mode."
```

The agent will automatically:
1. Activate discovery-pack skills
2. Create `docs/discovery/2026-01-06-project-name/`
3. Generate 3 artifacts (problem frame, options, handoff)
4. Produce spec-kit compatible outputs

**Time:** 15-30 minutes for lite mode, 1-2 hours for full mode.

---

## What's Included

### 8 Discovery Skills

| Skill | Purpose |
|-------|---------|
| **discovery-run** | Orchestrator - executes full workflow |
| **discovery-frame** | Problem framing using JTBD |
| **discovery-constraints** | Non-functional requirements |
| **discovery-domain** | Domain modeling with DDD |
| **discovery-options** | Option analysis with trade-offs |
| **discovery-validate** | Validation experiments |
| **discovery-decide** | Decision log (ADR format) |
| **discovery-handoff** | Spec-kit integration |

### Resources

- **Templates** (8) - Markdown with YAML frontmatter
- **Schemas** (9) - JSON Schema validation
- **Scripts** (6) - Python automation tools
- **References** - Methodologies and glossary

### Methodologies

- Jobs-to-be-Done (JTBD)
- Amazon PR/FAQ
- Architecture Decision Records (ADR)
- Lean Startup Validation
- Domain-Driven Design (DDD)

---

## Usage Modes

### Lite Mode (Recommended for Most Projects)

**3 artifacts, 15-30 minutes**

Use for: Personal projects, < 5 people, low risk

Generates:
- `00_problem-frame.md` - Problem, users, JTBD, metrics
- `03_option-space.md` - Alternative approaches
- `07_speckit-handoff.md` - Ready for implementation

### Full Mode (Enterprise/Compliance)

**7 artifacts, 1-2 hours**

Use for: Enterprise, compliance-critical, security-sensitive, high-risk

Generates all lite mode artifacts plus:
- `01_constraints-nfr.md` - Security, performance, compliance
- `02_domain-model.md` - Entities, events, glossary
- `04_assumptions-unknowns.md` - Extracted assumptions
- `05_validation-plan.md` - Experiments to test assumptions
- `06_decision-log.md` - Architectural decisions

### Individual Skills

Invoke specific skills independently:

- "Help me frame this problem using JTBD" → `discovery-frame`
- "What are our constraints?" → `discovery-constraints`
- "Compare these approaches" → `discovery-options`

---

## Automation Scripts (Optional)

Python scripts for automation (30-40% token savings):

```bash
# Install dependencies
pip install -r skill/discovery-pack/scripts/requirements.txt

# Validate artifacts
python skill/discovery-pack/scripts/validate.py docs/discovery/project/

# Auto-extract assumptions
python skill/discovery-pack/scripts/extract_assumptions.py docs/discovery/project/

# Detect decision gates
python skill/discovery-pack/scripts/gate_detector.py docs/discovery/project/
```

See [scripts/README.md](skill/discovery-pack/scripts/README.md) for details.

---

## Examples

See [examples/README.md](examples/README.md) for:
- Complete lite mode workflow walkthrough
- Full mode enterprise example
- Individual skill usage patterns
- Artifact structure and validation

---

## Integration with Spec-Kit

Discovery Pack generates spec-kit compatible outputs:

```
1. Run discovery-run → Generates 07_speckit-handoff.md
2. Review handoff artifact
3. Copy constitution section → /speckit.constitution
4. Copy specify section → /speckit.specify
5. Continue spec-kit workflow
```

Learn more: [GitHub Spec-Kit](https://github.com/github/spec-kit)

---

## Vendor Neutrality

Works with any AI agent supporting [Agent Skills specification](https://agentskills.io/specification):

- ✅ Claude Code (Claude AI Desktop)
- ✅ GitHub Copilot CLI
- ✅ VS Code Insiders (agent mode)
- ✅ Cursor IDE
- ✅ Gemini CLI
- ✅ Any agent with skills support

---

## Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[LICENSE](LICENSE)** - MIT License
- **[Methodologies](skill/discovery-pack/shared-references/methodologies.md)** - Deep dive into JTBD, PR/FAQ, ADR, Lean, DDD
- **[Glossary](skill/discovery-pack/shared-references/glossary.md)** - Complete terminology

---

## Repository Structure

```
discovery-pack/                          ← Git repository
├── README.md                            ← This file
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
│
├── skill/                               ← Installable skill
│   └── discovery-pack/                  ← Copy this to ~/.claude/skills/
│       ├── SKILL.md                     ← Package orchestrator
│       ├── discovery-run/               ← 8 individual skills
│       ├── discovery-frame/
│       ├── ...
│       ├── templates/                   ← Shared resources
│       ├── schemas/
│       ├── scripts/
│       └── shared-references/
│
├── examples/                            ← Usage examples
│   └── README.md
│
└── docs/                                ← Additional documentation
```

---

## Support & Contributing

- **Issues:** [GitHub Issues](https://github.com/nsalvacao/discovery-pack/issues)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **License:** MIT - see [LICENSE](LICENSE)

---

## Version

**Current:** 1.0.0  
**Status:** Production Ready  
**Maintained:** Yes

---

**Ready to transform ambiguous ideas into structured specifications!** 🚀

[View on GitHub](https://github.com/nsalvacao/discovery-pack) • [Report Issue](https://github.com/nsalvacao/discovery-pack/issues) • [Contribute](CONTRIBUTING.md)
