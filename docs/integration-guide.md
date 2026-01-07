# Integration Guide: Discovery Pack in CI/CD

Discovery Pack includes automated validation tools to ensure your discovery artifacts remain valid, compliant, and logical throughout the project lifecycle. This guide explains how to integrate these checks into your CI pipeline.

## The Validation Script

The core tool is `scripts/ci-validate.sh`. It performs the following checks:
1. **Schema Compliance**: Validates strict JSON Schema adherence.
2. **Frontmatter Parsing**: Ensures all YAML metadata is correct.
3. **Project Structure**: Verifies the `docs/discovery/` hierarchy.

### Usage
```bash
./skill/discovery-pack/scripts/ci-validate.sh [path-to-docs]
```

---

## GitHub Actions Integration

Add this workflow file to your repository at `.github/workflows/discovery-check.yml`.

```yaml
name: Discovery Governance

on:
  push:
    paths:
      - 'docs/discovery/**'
      - 'skill/discovery-pack/**'
  pull_request:
    paths:
      - 'docs/discovery/**'

jobs:
  validate-specs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r skill/discovery-pack/scripts/requirements.txt

      - name: Run Schema Validation
        run: |
          bash skill/discovery-pack/scripts/ci-validate.sh docs/discovery/

      - name: Run Gate Detection (Optional)
        run: |
          # Fails build if CRITICAL gates are detected
          for d in docs/discovery/*/; do
            python3 skill/discovery-pack/scripts/gate_detector.py "$d"
          done
```

---

## GitLab CI Integration

Add to your `.gitlab-ci.yml`:

```yaml
discovery_validation:
  image: python:3.11
  stage: test
  script:
    - pip install -r skill/discovery-pack/scripts/requirements.txt
    - bash skill/discovery-pack/scripts/ci-validate.sh docs/discovery/
  rules:
    - changes:
        - docs/discovery/**/*
```

---

## Pre-Commit Hook

For local governance, add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: discovery-validate
        name: Validate Discovery Artifacts
        entry: bash skill/discovery-pack/scripts/ci-validate.sh
        language: system
        files: ^docs/discovery/
        pass_filenames: false
```

---

## Understanding Errors

### 1. Schema Errors
```text
ValidationError: 'pending' is not one of ['draft', 'review', 'approved']
On instance['status']:
    'pending'
```
**Fix:** Update the YAML frontmatter to use an allowed Enum value.

### 2. Gate Errors
```text
🚨 1 Critical Gates Detected
⚠️  GATE: Experiment 'Load Test' lacks quantitative metrics
```
**Fix:** Edit `05_validation-plan.md` and ensure `success_criteria.quantitative.pass_if` is defined.

