# Discovery Pack Glossary

## Core Terms

**Artifact**
- Output document from discovery process (e.g., 00_problem-frame.md)
- Contains YAML frontmatter + markdown body
- Validated against JSON schema

**Discovery Phase**
- Structured exploration before implementation
- Transforms ambiguous ideas into specifications
- Precedes spec-kit constitution

**Frontmatter**
- YAML metadata at top of markdown file
- Delimited by `---` markers
- Machine-readable, validated by schemas

**Gate**
- Critical decision point requiring human input
- Detected automatically by gate_detector.py
- Examples: tied options, contradictory assumptions

**Handoff**
- Final artifact (07_speckit-handoff.md)
- Maps discovery outputs to spec-kit inputs
- Ready-to-copy constitution and specify sections

**Lite Mode**
- Minimal discovery workflow (3 artifacts)
- For small projects, low risk, < 5 people
- Outputs: 00, 03, 07

**Full Mode**
- Complete discovery workflow (7 artifacts)
- For enterprise, compliance, high-risk projects
- Outputs: 00-07 (all phases)

**Orchestrator**
- The `discovery-run` skill
- Executes discovery sequence
- Coordinates other skills

**Tag**
- Epistemic marker in statements
- Types: FACT, ASSUMPTION, HYPOTHESIS, CONSTRAINT
- Applied consistently across artifacts

**Template**
- Starter document with structure and prompts
- Located in `templates/` directory
- Contains example YAML + markdown sections

---

## Methodologies

**JTBD (Jobs-to-be-Done)**
- Framework for understanding user motivation
- Format: "When I X, I want to Y, so I can Z"
- Used in problem framing

**PR/FAQ (Press Release / Frequently Asked Questions)**
- Amazon's approach to product clarity
- Write press release before building
- Forces customer focus

**ADR (Architecture Decision Record)**
- Document decisions with context and consequences
- Includes alternatives considered
- Enables future reasoning about choices

**Lean Startup**
- Build-Measure-Learn cycle
- Emphasizes validated learning
- Experiments over opinions

**DDD (Domain-Driven Design)**
- Model problem domain with ubiquitous language
- Entities, value objects, events, bounded contexts
- Shared vocabulary between domain experts and developers

---

## Technical Terms

**Schema**
- JSON Schema file defining artifact structure
- Located in `schemas/` directory
- Enables automated validation

**$ref**
- JSON Schema reference to reusable definitions
- All artifacts reference `common.schema.json`
- Enables DRY (Don't Repeat Yourself)

**Template Path**
- Templates located in `../templates/` directory
- Each sub-skill references templates from parent directory
- Avoids template duplication

**Batch Mode**
- Zero-question execution mode
- Marks unknowns as ASSUMPTIONS
- Default for discovery-run

**Interactive Mode**
- Asks questions at critical gates only
- Used for high-stakes decisions
- Opt-in via --interactive flag

---

## Validation Terms

**Success Criteria**
- Observable outcome indicating hypothesis is true/false
- Must be quantitative (numbers, not opinions)
- Required in validation experiments

**Exit Criteria**
- Conditions for proceeding past discovery phase
- Based on validated assumptions
- Documented in 05_validation-plan.md

**Critical Assumption**
- Assumption that, if false, invalidates approach
- Requires validation before proceeding
- Prioritized in validation plan

**Experiment**
- Structured test of assumption
- Includes hypothesis, method, success criteria
- Time-boxed and resource-constrained

---

## Spec-Kit Integration

**Constitution**
- Spec-kit's "laws" document
- Defines principles, constraints, vocabulary
- Generated from discovery artifacts

**Specify**
- Spec-kit's requirements document
- User journeys, acceptance criteria, non-goals
- Generated from discovery artifacts

**Handoff**
- Bridge between discovery and spec-kit
- Artifact 07 in discovery workflow
- Contains ready-to-copy sections

---

## Artifact-Specific Terms

**Problem Frame (00_)**
- First artifact in discovery
- JTBD analysis, users, success metrics
- Foundation for all subsequent work

**Constraints (01_)**
- Non-functional requirements
- Security, performance, compliance
- Hard limits and trade-offs

**Domain Model (02_)**
- Entities, events, bounded contexts
- Ubiquitous language/glossary
- Conceptual model of problem space

**Option Space (03_)**
- Alternative approaches to solution
- Trade-off matrix with weighted scores
- Decision criteria and rationale

**Assumptions (04_)**
- Auto-extracted from 00-03
- Tagged statements with testability
- Prioritized by criticality

**Validation Plan (05_)**
- Experiments to test assumptions
- Success criteria and exit criteria
- Risk mitigation strategy

**Decision Log (06_)**
- ADR-style documentation
- Decisions, rationale, consequences
- Alternatives considered and rejected

**Handoff (07_)**
- Final discovery output
- Maps to spec-kit inputs
- Ready for next phase
