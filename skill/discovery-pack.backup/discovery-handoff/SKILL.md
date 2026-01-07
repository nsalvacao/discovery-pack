---
name: discovery-handoff
description: Transform discovery artifacts into spec-kit inputs. Generates 07_speckit-handoff.md with ready-to-copy Constitution section (principles, constraints, glossary) and Specify section (users, journeys, requirements, metrics). Use as final discovery step before /speckit.constitution and /speckit.specify.
---

# Spec-Kit Handoff

Generate `07_speckit-handoff.md` with copy-paste ready inputs for spec-kit commands.

## Content Extraction

**From 00_problem-frame.md:**
- Users/personas → Specify input
- JTBD → User journeys
- Success metrics → Specify metrics

**From 01_constraints-nfr.md:**
- NFRs → Constitution constraints
- Trust model → Constitution security principles

**From 02_domain-model.md:**
- Glossary → Constitution ubiquitous language
- Boundaries → Constitution scope

**From 06_decision-log.md:**
- Active decisions → Constitution architectural constraints
- Principles → Constitution core principles

## Output Structure
1. Constitution Input (principles, constraints, glossary)
2. Specify Input (users, journeys, requirements, metrics, scope)
3. Reference links to all discovery artifacts
4. Handoff checklist
5. Quick-start commands

Output to `/docs/discovery/<date>-<topic>/07_speckit-handoff.md`.
