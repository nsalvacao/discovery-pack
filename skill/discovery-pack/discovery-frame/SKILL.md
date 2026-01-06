---
name: discovery-frame
description: Frame the problem using Jobs-to-be-Done methodology. Generate problem statement, users/personas, JTBD analysis, anti-goals, and success metrics. Use when starting discovery process or user asks "help me understand the problem" or "who are the users". Creates 00_problem-frame.md with FACT/ASSUMPTION/HYPOTHESIS/CONSTRAINT tags.
---

# Problem Framing

Generate structured problem frame using JTBD methodology and create `00_problem-frame.md`.

## Execution

1. Read template from `assets/00_problem-frame.md`
2. Fill template sections based on user input and conversation context
3. Mark each statement with appropriate tag:
   - `[FACT]` - Verified data
   - `[ASSUMPTION]` - Testable hypothesis
   - `[HYPOTHESIS]` - Educated guess
   - `[CONSTRAINT]` - Non-negotiable

## Output Sections

- Problem statement (what pain, who experiences, why now)
- Primary/secondary users with JTBD format: "When I ___, I want to ___, so I can ___"
- Anti-goals (what we're NOT solving)
- Success metrics (North Star + leading/lagging indicators)
- Context (market, technical, organizational)

## Batch Mode (Default)

- Use conversation context to infer unknowns
- Mark inferences as `[ASSUMPTION]`
- No questions unless problem statement is completely absent

## Interactive Mode

- Ask 3-5 targeted questions:
  1. "Who is the primary user?"
  2. "What job are they trying to get done?"
  3. "What's the #1 pain point today?"
  4. "How will we measure success?"

Generate artifact at `/docs/discovery/<date>-<topic>/00_problem-frame.md`
