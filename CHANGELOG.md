# Changelog

All notable changes to Discovery Pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-06

### Added

#### Core Skills (8)
- `discovery-run` - Orchestrator for complete discovery workflow
- `discovery-frame` - Problem framing using JTBD methodology
- `discovery-constraints` - Non-functional requirements and constraints
- `discovery-domain` - Domain modeling with DDD principles
- `discovery-options` - Option space analysis with trade-off matrix
- `discovery-validate` - Validation experiments using Lean Startup
- `discovery-decide` - Decision log in ADR format
- `discovery-handoff` - Spec-kit integration handoff generator

#### Methodologies
- Jobs-to-be-Done (JTBD) for problem framing
- Amazon PR/FAQ for customer clarity
- Architecture Decision Records (ADR) for decisions
- Lean Startup validation for hypothesis testing
- Domain-Driven Design (DDD) for domain modeling

#### Automation (5 Python Scripts)
- `validate.py` - Schema validation against JSON schemas
- `extract_assumptions.py` - Auto-extract tagged assumptions
- `generate_handoff.py` - Auto-generate spec-kit handoff
- `gate_detector.py` - Detect critical decision gates
- `audit_logger.py` - Add generation metadata
- `ci-validate.sh` - CI/CD validation script

#### Schemas (9 JSON Schemas)
- `common.schema.json` - Reusable definitions
- 8 artifact-specific schemas (problem-frame, option-space, etc.)
- Full JSON Schema Draft 07 compliance
- $ref resolution support

#### Templates (8 Markdown)
- Complete YAML frontmatter examples
- Structured sections with prompts
- Tag system (FACT/ASSUMPTION/HYPOTHESIS/CONSTRAINT)
- Progressive disclosure design

#### Documentation
- Complete README with 3 usage scenarios
- Scripts documentation with workflow examples
- Methodologies reference guide
- Glossary of terms
- End-to-end lite-mode example
- Troubleshooting guide

#### Features
- **Lite Mode:** 3 artifacts (frame, options, handoff) for small projects
- **Full Mode:** 7 artifacts for enterprise/compliance projects
- **Batch Mode:** Zero-question execution (mark unknowns as ASSUMPTIONS)
- **Interactive Mode:** Questions at critical gates only
- **Tag System:** Epistemic humility (FACT/ASSUMPTION/HYPOTHESIS/CONSTRAINT)
- **Vendor Neutral:** Works with Claude Code, Copilot CLI, Gemini CLI, Cursor

### Technical

#### Standards Compliance
- Agent Skills specification (agentskills.io)
- GitHub Copilot agent skills format
- Progressive disclosure (metadata → instructions → resources)
- File references at maximum 1 level deep

#### Token Economy
- 30-40% token reduction via automation scripts
- Schemas eliminate validation token overhead
- Batch mode avoids conversation loops

#### Quality
- All templates validated against schemas
- All scripts executable with correct permissions
- Example artifacts included for reference
- CI/CD integration ready

### Project Structure
```
discovery-pack/
├── LICENSE (MIT)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
├── discovery-{name}/          (8 skills)
│   ├── SKILL.md
│   └── assets/ → ../templates
├── templates/                 (8 templates)
├── schemas/                   (9 JSON schemas)
├── scripts/                   (6 automation scripts)
├── shared-references/         (methodologies, glossary)
├── examples/                  (lite-mode sample)
└── dist/                      (packaged .skill files)
```

## [Unreleased]

### Planned
- Unit tests for Python scripts
- Additional examples (full-mode, enterprise)
- Integration with popular PM tools
- GitHub Actions workflow templates

---

## Version History

- **1.0.0** (2026-01-06) - Initial public release
