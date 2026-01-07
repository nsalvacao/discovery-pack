#!/bin/bash
# Discovery Pack Workflow Executor
# Forces correct sub-skill execution with validation gates
# Usage: discovery-pack-run.sh <output-dir> <mode> <project-name>

set -e

SKILL_DIR="$HOME/.copilot/skills/discovery-pack"
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
echo ""

# Check automation
if ! python3 -c "import jsonschema, yaml" 2>/dev/null; then
    log_warning "Automation not available (Python dependencies missing)"
    log_info "Install: pip install -r $SKILL_DIR/scripts/requirements.txt"
    echo ""
    read -p "Continue without automation? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Define artifacts for each mode
if [ "$MODE" = "lite" ]; then
    ARTIFACTS=(
        "00_problem-frame.md:discovery-frame:Problem Framing (JTBD)"
        "03_option-space.md:discovery-options:Option Analysis"
        "07_speckit-handoff.md:discovery-handoff:Spec-Kit Handoff"
    )
else
    ARTIFACTS=(
        "00_problem-frame.md:discovery-frame:Problem Framing (JTBD)"
        "01_constraints-nfr.md:discovery-constraints:Constraints & NFRs"
        "02_domain-model.md:discovery-domain:Domain Model (DDD)"
        "03_option-space.md:discovery-options:Option Analysis"
        "04_assumptions-unknowns.md:AUTO:Extract Assumptions"
        "05_validation-plan.md:discovery-validate:Validation Plan"
        "06_decision-log.md:discovery-decide:Decision Log (ADR)"
        "07_speckit-handoff.md:discovery-handoff:Spec-Kit Handoff"
    )
fi

log_info "Discovery Pack Executor - Mode: $MODE"
log_info "Project: $PROJECT_NAME"
log_info "Artifacts to generate: ${#ARTIFACTS[@]}"
echo ""

# Function to show sub-skill instructions
show_subskill_instructions() {
    local subskill_name="$1"
    local subskill_path="$SKILL_DIR/$subskill_name/SKILL.md"
    
    if [ -f "$subskill_path" ]; then
        log_step "Sub-Skill Instructions: $subskill_name"
        echo ""
        # Show key sections from sub-skill
        sed -n '/## Execution/,/## Output Sections/p' "$subskill_path" | head -20
        echo ""
    fi
}

# Function to validate artifact
validate_artifact() {
    local artifact_file="$1"
    local artifact_path="$OUTPUT_DIR/$artifact_file"
    
    if [ ! -f "$artifact_path" ]; then
        log_error "Artifact not found: $artifact_file"
        return 1
    fi
    
    # Check for YAML frontmatter
    if ! head -1 "$artifact_path" | grep -q "^---$"; then
        log_error "Missing YAML frontmatter in $artifact_file"
        log_info "Expected format:"
        echo "---"
        echo "project: \"...\""
        echo "date: \"YYYY-MM-DD\""
        echo "..."
        echo "---"
        return 1
    fi
    
    # Validate with schema if Python available
    if python3 -c "import jsonschema, yaml" 2>/dev/null; then
        if python3 "$SCRIPTS_DIR/validate.py" "$artifact_path" 2>&1 | grep -q "✅"; then
            log_success "Schema validation passed: $artifact_file"
        else
            log_error "Schema validation failed: $artifact_file"
            python3 "$SCRIPTS_DIR/validate.py" "$artifact_path"
            return 1
        fi
    else
        log_warning "Skipping schema validation (dependencies missing)"
    fi
    
    return 0
}

# Main execution loop
STEP=1
TOTAL=${#ARTIFACTS[@]}

for artifact_spec in "${ARTIFACTS[@]}"; do
    IFS=':' read -r artifact_file subskill_name artifact_title <<< "$artifact_spec"
    
    echo ""
    log_step "Step $STEP/$TOTAL: $artifact_title"
    echo ""
    
    # Show template location
    if [ "$subskill_name" != "AUTO" ]; then
        template_file="$TEMPLATES_DIR/$artifact_file"
        log_info "Template: $template_file"
        
        # Show sub-skill instructions
        if [ -d "$SKILL_DIR/$subskill_name" ]; then
            show_subskill_instructions "$subskill_name"
        fi
        
        log_warning "🛑 GATE: Generate $artifact_file following template and sub-skill instructions"
        echo ""
        echo "Required:"
        echo "  1. Read template: $template_file"
        echo "  2. Include YAML frontmatter (delimited by ---)"
        echo "  3. Apply epistemic tags: [FACT|ASSUMPTION|HYPOTHESIS|CONSTRAINT]"
        echo "  4. Fill all required sections"
        echo "  5. Save to: $OUTPUT_DIR/$artifact_file"
        echo ""
        
        read -p "Press ENTER when artifact is generated and ready for validation..." 
        echo ""
        
        # Validate
        if ! validate_artifact "$artifact_file"; then
            log_error "Validation failed. Fix errors and re-run validation."
            log_info "Manual validation: python3 $SCRIPTS_DIR/validate.py $OUTPUT_DIR/$artifact_file"
            exit 1
        fi
    else
        # Auto-generate assumptions extraction
        log_info "Auto-generating $artifact_file from tagged assumptions..."
        
        if python3 -c "import yaml" 2>/dev/null; then
            if python3 "$SCRIPTS_DIR/extract_assumptions.py" "$OUTPUT_DIR" > /dev/null 2>&1; then
                log_success "Generated: $artifact_file"
                
                if [ -f "$OUTPUT_DIR/$artifact_file" ]; then
                    validate_artifact "$artifact_file" || true
                fi
            else
                log_warning "Auto-extraction failed. Generate manually using template."
            fi
        else
            log_warning "Python dependencies missing. Generate $artifact_file manually."
        fi
    fi
    
    log_success "Step $STEP/$TOTAL complete"
    STEP=$((STEP + 1))
done

echo ""
log_step "Discovery Pack Execution Complete"
echo ""

# Final validation report
log_info "Running final validation..."
echo ""

VALIDATION_PASSED=true
for artifact_spec in "${ARTIFACTS[@]}"; do
    IFS=':' read -r artifact_file _ _ <<< "$artifact_spec"
    
    if [ -f "$OUTPUT_DIR/$artifact_file" ]; then
        if validate_artifact "$artifact_file" 2>&1 | grep -q "✅"; then
            echo "  ✅ $artifact_file"
        else
            echo "  ❌ $artifact_file (validation failed)"
            VALIDATION_PASSED=false
        fi
    else
        echo "  ❌ $artifact_file (not found)"
        VALIDATION_PASSED=false
    fi
done

echo ""

if [ "$VALIDATION_PASSED" = true ]; then
    log_success "All artifacts validated successfully!"
    echo ""
    log_info "Next steps:"
    echo "  1. Review artifacts in: $OUTPUT_DIR"
    echo "  2. Check 07_speckit-handoff.md for spec-kit integration"
    echo "  3. Copy Constitution section → /speckit.constitution"
    echo "  4. Copy Specify section → /speckit.specify"
else
    log_error "Some artifacts failed validation. Fix errors and re-validate."
    log_info "Manual validation: python3 $SCRIPTS_DIR/validate.py $OUTPUT_DIR"
    exit 1
fi
