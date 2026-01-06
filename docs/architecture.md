# Discovery Pack Architecture

## Design Principles

### 1. Progressive Disclosure

Skills are structured in 3 levels:
- **Level 1:** Skill names/descriptions (loaded at agent startup)
- **Level 2:** Full SKILL.md content (loaded when skill activated)
- **Level 3:** Referenced files (loaded as needed)

### 2. Package + Individual Skills

The structure supports both:
- **Package installation:** Full discovery-pack with all resources
- **Individual skills:** Each skill can reference shared resources via relative paths

### 3. Vendor Neutrality

No platform-specific dependencies. Uses standard:
- Markdown + YAML frontmatter
- JSON Schema Draft 07
- Python (optional automation)

## Component Architecture

### Skills Layer

```
discovery-pack/               ← Package skill (orchestrator)
├── discovery-run/            ← Workflow orchestrator
├── discovery-frame/          ← Problem framing
├── discovery-constraints/    ← NFRs
├── discovery-domain/         ← Domain modeling
├── discovery-options/        ← Option analysis
├── discovery-validate/       ← Validation experiments
├── discovery-decide/         ← Decision log
└── discovery-handoff/        ← Spec-kit integration
```

### Resources Layer

Shared across all skills:
- **Templates:** Markdown with YAML frontmatter
- **Schemas:** JSON Schema validation
- **Scripts:** Python automation tools
- **References:** Methodologies and glossary

### Workflow Modes

**Lite Mode (3 artifacts):**
```
discovery-run → discovery-frame → discovery-options → discovery-handoff
```

**Full Mode (7 artifacts):**
```
discovery-run → all 8 skills sequentially with validation gates
```

## Token Economy

Scripts provide 30-40% token savings by automating:
- Assumption extraction from tagged statements
- Schema validation
- Decision gate detection
- Handoff generation

## Integration Points

### Input
- User prompt with project idea
- Optional: existing documentation

### Output
- Structured markdown artifacts with YAML frontmatter
- Spec-kit compatible handoff
- Validation reports (if scripts used)

### External Tools
- Spec-kit (optional) - Implementation phase
- CI/CD (optional) - Validation automation
