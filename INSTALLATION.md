# Installation Guide

## Quick Install

```bash
git clone https://github.com/nsalvacao/discovery-pack.git
cd discovery-pack
cp -r skill/discovery-pack ~/.claude/skills/
```

## Platform-Specific Installation

### Claude Code / Claude Desktop

```bash
cp -r skill/discovery-pack ~/.claude/skills/
```

### GitHub Copilot CLI

```bash
cp -r skill/discovery-pack ~/.copilot/skills/
```

### VS Code Insiders (Agent Mode)

```bash
cp -r skill/discovery-pack ~/.claude/skills/
```

### Cursor IDE

```bash
cp -r skill/discovery-pack ~/.claude/skills/
```

### Project-Specific (Any Agent)

```bash
# For repo-specific skills
cp -r skill/discovery-pack .claude/skills/
# or
cp -r skill/discovery-pack .github/skills/
```

## Verify Installation

```bash
# Check skill exists
ls ~/.claude/skills/discovery-pack/SKILL.md

# Should show the main skill file
```

## Optional: Install Automation Scripts

```bash
cd ~/.claude/skills/discovery-pack
pip install -r scripts/requirements.txt
```

This installs Python dependencies for automation scripts:
- `jsonschema` - Schema validation
- `PyYAML` - YAML parsing

Scripts provide 30-40% token savings but are optional.

## Updating

```bash
cd discovery-pack
git pull
cp -r skill/discovery-pack ~/.claude/skills/
```

## Uninstalling

```bash
rm -rf ~/.claude/skills/discovery-pack
```

## Troubleshooting

**Q: Skills not appearing in agent?**
- Verify file exists: `ls ~/.claude/skills/discovery-pack/SKILL.md`
- Restart agent/IDE
- Check agent supports skills (Claude Code, Copilot CLI, etc.)

**Q: Scripts not working?**
- Install dependencies: `pip install -r scripts/requirements.txt`
- Check Python version: `python3 --version` (3.8+ required)
- Run from skill directory: `cd ~/.claude/skills/discovery-pack`

**Q: Individual skill doesn't work?**
- This package is designed for full installation
- All skills share templates/schemas/scripts
- Individual extraction not recommended

## Next Steps

After installation, tell your agent:
```
"Run discovery on [your project idea]"
```

The agent will automatically activate discovery-pack skills.

## Cross-Agent Compatibility (v2.0.0+)

**Discovery Pack v2.0.0** works identically across all agents supporting the Agent Skills specification:

| Agent | Installation Path | Status |
|-------|-------------------|--------|
| **Claude Code** | `~/.claude/skills/discovery-pack/` | ✅ Tested |
| **GitHub Copilot CLI** | `~/.copilot/skills/discovery-pack/` | ✅ Tested |
| **VS Code (Agent Mode)** | `~/.claude/skills/discovery-pack/` | ✅ Compatible |
| **Cursor IDE** | `~/.claude/skills/discovery-pack/` | ✅ Compatible |
| **Gemini Code Assist** | Custom path | ✅ Compatible (relative paths) |
| **Project-local** | `.claude/skills/discovery-pack/` | ✅ Tested |

**Key Features**:
- Relative path resolution (no hardcoded agent-specific paths)
- Scripts auto-detect skill root via `Path(__file__)` / `${BASH_SOURCE[0]}`
- Pre-flight check validates installation structure

## Installation Verification

After installation, verify cross-agent compatibility:

```bash
# Test pre-flight check (validates structure)
cd ~/.copilot/skills/discovery-pack  # or ~/.claude/skills/discovery-pack
bash scripts/pre-flight-check.sh /tmp/test-output lite

# Expected output:
# ✅ templates/ exists
# ✅ schemas/ exists
# ✅ scripts/ exists
# ✅ shared-references/ exists
```

If pre-flight fails, ensure you copied the entire `skill/discovery-pack/` directory (not just SKILL.md).

