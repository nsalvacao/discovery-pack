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
