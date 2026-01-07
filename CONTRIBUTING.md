# Contributing to Discovery Pack

Thank you for your interest in contributing! Discovery Pack is an open-source project following the [Agent Skills specification](https://agentskills.io/specification).

## Ways to Contribute

- **Report bugs** via GitHub Issues
- **Suggest improvements** to skills or documentation
- **Share examples** of discovery artifacts from real projects
- **Submit pull requests** for fixes or enhancements
- **Write tutorials** showing Discovery Pack in action

## Getting Started

### Prerequisites

```bash
# Python 3.8+ required
python3 --version

# Install dependencies
pip install -r scripts/requirements.txt
```

### Project Structure

```
discovery-pack/
├── discovery-{name}/     # Individual skill directories
│   ├── SKILL.md         # Required: skill definition
│   └── assets/          # Symlink to ../templates
├── templates/            # Shared markdown templates
├── schemas/              # JSON Schema validation
├── scripts/              # Python automation
├── shared-references/    # Methodology documentation
└── examples/             # Sample artifacts
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

**For new skills:**
- Create `discovery-{name}/` directory
- Write `SKILL.md` with required frontmatter
- Add template to `templates/` if needed
- Create schema in `schemas/` if new artifact type
- Symlink assets: `ln -s ../templates discovery-{name}/assets`

**For template changes:**
- Edit template in `templates/`
- Update corresponding schema in `schemas/`
- Run validation: `python3 scripts/validate.py examples/`

**For script changes:**
- Update script in `scripts/`
- Test with example artifacts
- Update `scripts/README.md` if behavior changes

### 3. Validate Changes

```bash
# Validate all templates parse correctly
for f in templates/*.md; do
  python3 -c "import yaml, re; content=open('$f').read(); match=re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL); yaml.safe_load(match.group(1))"
done

# Run schema validation
python3 scripts/validate.py examples/lite-mode-sample/

# Test CI script
bash scripts/ci-validate.sh examples/
```

### 4. Update Documentation

- Add entry to `CHANGELOG.md` under `[Unreleased]`
- Update `README.md` if adding new skill or major feature
- Update `shared-references/glossary.md` if introducing new terms

### 5. Submit Pull Request

**PR Title Format:**
```
[Type] Brief description

Examples:
[Fix] Correct YAML syntax in constraints template
[Feature] Add discovery-architecture skill
[Docs] Improve validation script examples
```

**PR Description Must Include:**
- What changed and why
- How to test the changes
- Screenshots (if UI/documentation)
- Breaking changes (if any)
- Related issues (if applicable)

## Code Standards

### SKILL.md Format

```yaml
---
name: skill-name              # lowercase, hyphens only
description: What it does and when to use it. Include trigger phrases.
license: MIT
metadata:
  author: your-name
  version: "1.0.0"
---

# Skill body in markdown
```

**Requirements:**
- Name must match directory name
- Description < 1024 characters
- Include "Use when..." and trigger phrases
- Keep body < 500 lines (move details to references/)

### Python Scripts

- **Style:** PEP 8 compliant
- **Shebang:** `#!/usr/bin/env python3`
- **Permissions:** `chmod 755 *.py`
- **Error handling:** Graceful failures with helpful messages
- **Exit codes:** 0 for success, non-zero for errors

### Templates

- **YAML frontmatter:** Must be valid YAML between `---` markers
- **Schema reference:** Include `$schema` pointing to correct schema
- **Tags:** Use consistently: FACT, ASSUMPTION, HYPOTHESIS, CONSTRAINT
- **Placeholders:** Use `[Description in brackets]` for fillable fields

### Schemas

- **Standard:** JSON Schema Draft 07
- **Reuse:** Reference `common.schema.json` via `$ref`
- **Validation:** Test with example artifacts
- **Required fields:** Mark truly mandatory fields only

## Testing

### Manual Testing

```bash
# Test skill workflow
cd examples/lite-mode-sample
# Manually invoke discovery-run logic
# Verify outputs match expectations

# Test validation
python3 scripts/validate.py examples/lite-mode-sample/

# Test assumption extraction
python3 scripts/extract_assumptions.py examples/lite-mode-sample/
```

### Automated Testing (Planned)

```bash
# Unit tests (coming soon)
pytest tests/

# Integration tests (coming soon)
bash tests/integration-test.sh
```

## Pull Request Review Process

1. **Automated checks** (when available):
   - YAML syntax validation
   - Schema validation
   - Linting

2. **Manual review:**
   - Code quality
   - Documentation completeness
   - Backward compatibility

3. **Approval:**
   - At least 1 maintainer approval required
   - All comments addressed

4. **Merge:**
   - Squash and merge (keep history clean)
   - Delete source branch

## Release Process

1. Update version in all `SKILL.md` files
2. Move `[Unreleased]` section to `[X.Y.Z] - YYYY-MM-DD` in CHANGELOG.md
3. Create GitHub release with tag `vX.Y.Z`
4. Update dist/ packages if needed

## Communication

- **Issues:** For bugs and feature requests
- **Discussions:** For questions and ideas (GitHub Discussions)
- **Pull Requests:** For code contributions

## Code of Conduct

- Be respectful and constructive
- Focus on improving the project
- Help newcomers get started
- Assume good intent

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Questions?** Open an issue or start a discussion. We're here to help!
