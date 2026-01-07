#!/bin/bash
# Discovery Pack Pre-Flight Check
# Garante compliance com workflow antes de começar

set -e

SKILL_DIR="$HOME/.copilot/skills/discovery-pack"
OUTPUT_DIR="${1:-}"
MODE="${2:-}"

echo "🚀 Discovery Pack Pre-Flight Check"
echo "===================================="
echo ""

# Validar argumentos
if [ -z "$OUTPUT_DIR" ] || [ -z "$MODE" ]; then
    echo "❌ Usage: $0 <output-dir> <mode>"
    echo ""
    echo "Example:"
    echo "  $0 /mnt/d/GitHub/PROJECT/docs/discovery/2026-01-06-topic full"
    echo ""
    echo "Modes:"
    echo "  lite - 3 artifacts (15-30 min)"
    echo "  full - 7 artifacts (1-2 hours)"
    exit 1
fi

if [ "$MODE" != "lite" ] && [ "$MODE" != "full" ]; then
    echo "❌ Mode must be 'lite' or 'full'"
    exit 1
fi

echo "📋 Configuration:"
echo "  Output: $OUTPUT_DIR"
echo "  Mode:   $MODE"
echo ""

# Check automation
echo "🤖 Checking automation availability..."
if python3 -c "import jsonschema, yaml" 2>/dev/null; then
    echo "  ✅ Python + jsonschema + PyYAML available"
    AUTOMATION=true
else
    echo "  ⚠️  Automation not available"
    echo "  Install: pip install -r $SKILL_DIR/scripts/requirements.txt"
    AUTOMATION=false
fi
echo ""

# Create output directory
echo "📁 Creating output directory..."
mkdir -p "$OUTPUT_DIR"
echo "  ✅ $OUTPUT_DIR"
echo ""

# List required artifacts
echo "📝 Required Artifacts ($MODE mode):"
if [ "$MODE" = "lite" ]; then
    echo "  [ ] 00_problem-frame.md"
    echo "  [ ] 03_option-space.md"
    echo "  [ ] 07_speckit-handoff.md"
elif [ "$MODE" = "full" ]; then
    echo "  [ ] 00_problem-frame.md"
    echo "  [ ] 01_constraints-nfr.md"
    echo "  [ ] 02_domain-model.md"
    echo "  [ ] 03_option-space.md"
    echo "  [ ] 04_assumptions-unknowns.md (auto-generated)"
    echo "  [ ] 05_validation-plan.md"
    echo "  [ ] 06_decision-log.md"
    echo "  [ ] 07_speckit-handoff.md"
fi
echo ""

# Show workflow
echo "🔄 Workflow Steps:"
echo "  1. Read template from $SKILL_DIR/templates/"
echo "  2. Fill with YAML frontmatter + structured content"
echo "  3. Apply epistemic tags [FACT|ASSUMPTION|HYPOTHESIS|CONSTRAINT]"
echo "  4. Save with correct filename (00_, 01_, etc.)"
echo "  5. Validate: python3 $SKILL_DIR/scripts/validate.py $OUTPUT_DIR"
echo ""

# Validation reminder
echo "⚠️  CRITICAL REQUIREMENTS:"
echo "  • YAML frontmatter MANDATORY (delimited by ---)"
echo "  • Filenames MUST match: 00_problem-frame.md (not 01-jtbd.md)"
echo "  • Templates from $SKILL_DIR/templates/ MUST be used"
echo "  • Epistemic tags MUST be applied to all claims"
echo "  • validate.py MUST pass before completion"
echo ""

# Final prompt
echo "✅ Pre-flight check complete!"
echo ""
echo "Next steps:"
echo "  1. Generate artifacts following templates"
echo "  2. Run validation: python3 $SKILL_DIR/scripts/validate.py $OUTPUT_DIR"
echo "  3. Fix any validation errors"
echo "  4. Review 07_speckit-handoff.md"
echo ""
