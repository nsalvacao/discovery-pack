#!/bin/bash
# Discovery Pack Workflow Executor
# Forces correct sub-skill execution with validation gates
# Usage: discovery-pack-run.sh <output-dir> <mode> <project-name>

set -e

# Relative path resolution (cross-agent compatible)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SCRIPTS_DIR="$SKILL_DIR/scripts"
TEMPLATES_DIR="$SKILL_DIR/templates"

OUTPUT_DIR="${1:-}"
MODE="${2:-}"
PROJECT_NAME="${3:-Project}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }
log_step() { echo -e "${BLUE}━━━${NC} $1 ${BLUE}━━━${NC}"; }

# Validation
if [ -z "$OUTPUT_DIR" ] || [ -z "$MODE" ]; then
    log_error "Usage: $0 <output-dir> <mode> [project-name]"
    echo ""
    echo "Example:"
    echo "  $0 ./docs/discovery/2026-01-06-nexus full 'NEXUS CLI FLEET'"
    echo ""
    echo "Modes: lite | full"
    exit 1
fi

if [ "$MODE" != "lite" ] && [ "$MODE" != "full" ]; then
    log_error "Mode must be 'lite' or 'full'"
    exit 1
fi

# Setup
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"
log_success "Output directory: $OUTPUT_DIR"
log_info "Skill root: $SKILL_DIR"
echo ""

# Pre-flight check
log_step "PRE-FLIGHT CHECK"
bash "$SCRIPTS_DIR/pre-flight-check.sh" "$OUTPUT_DIR" "$MODE"
echo ""

# Artifact generation based on mode
if [ "$MODE" = "lite" ]; then
    ARTIFACTS=("00_problem-frame" "03_option-space" "07_speckit-handoff")
else
    ARTIFACTS=("00_problem-frame" "01_constraints-nfr" "02_domain-model" "03_option-space" "04_assumptions-unknowns" "05_validation-plan" "06_decision-log" "07_speckit-handoff")
fi

log_info "Mode: $MODE (${#ARTIFACTS[@]} artifacts)"
echo ""

# Execute workflow
for artifact in "${ARTIFACTS[@]}"; do
    log_step "GENERATING: $artifact"
    
    # Copy template
    template_file="$TEMPLATES_DIR/${artifact}.md"
    output_file="$OUTPUT_DIR/${artifact}.md"
    
    if [ ! -f "$template_file" ]; then
        log_error "Template not found: $template_file"
        exit 1
    fi
    
    cp "$template_file" "$output_file"
    log_success "Template copied: ${artifact}.md"
    
    # Invoke template filler if available
    if [ -f "$SCRIPTS_DIR/template_filler.py" ]; then
        log_info "Invoking template filler..."
        python3 "$SCRIPTS_DIR/template_filler.py" "$output_file" "$PROJECT_NAME" || log_warning "Template filler failed (continue manually)"
    fi
    
    echo ""
done

# Validation gate
log_step "VALIDATION GATE"
if [ -f "$SCRIPTS_DIR/validate.py" ]; then
    python3 "$SCRIPTS_DIR/validate.py" "$OUTPUT_DIR"
else
    log_warning "Validation script not found (skip validation)"
fi

echo ""
log_success "Workflow complete! Artifacts in: $OUTPUT_DIR"
log_info "Next: Fill in templates and run validation again"
