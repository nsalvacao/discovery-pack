#!/bin/bash
# Discovery Pack CI Validation Script
# Validates all discovery artifacts in a repository

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISCOVERY_DIR="${1:-docs/discovery}"

echo "🔍 Discovery Pack CI Validation"
echo "================================"
echo "Validating artifacts in: $DISCOVERY_DIR"
echo ""

if [ ! -d "$DISCOVERY_DIR" ]; then
  echo "⚠️  No discovery directory found at $DISCOVERY_DIR"
  echo "Skipping validation (no artifacts to validate)"
  exit 0
fi

# Count discovery subdirectories
DISCOVERY_COUNT=$(find "$DISCOVERY_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)

if [ "$DISCOVERY_COUNT" -eq 0 ]; then
  echo "⚠️  No discovery subdirectories found"
  echo "Skipping validation (no artifacts to validate)"
  exit 0
fi

echo "Found $DISCOVERY_COUNT discovery project(s)"
echo ""

# Validate each discovery directory
FAILED=0
PASSED=0

for dir in "$DISCOVERY_DIR"/*/ ; do
  if [ -d "$dir" ]; then
    DIR_NAME=$(basename "$dir")
    echo "📁 Validating: $DIR_NAME"
    
    if python3 "$SCRIPT_DIR/validate.py" "$dir" --quiet; then
      echo "   ✅ Passed"
      ((PASSED++))
    else
      echo "   ❌ Failed"
      ((FAILED++))
    fi
    echo ""
  fi
done

# Summary
echo "================================"
echo "📊 Summary"
echo "   Passed: $PASSED"
echo "   Failed: $FAILED"
echo ""

if [ $FAILED -gt 0 ]; then
  echo "❌ Validation failed for $FAILED project(s)"
  exit 1
else
  echo "✅ All discovery artifacts valid"
  exit 0
fi
