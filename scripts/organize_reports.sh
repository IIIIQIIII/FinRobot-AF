#!/bin/bash

# organize_reports.sh
# Automatically move development reports from root to docs/development-reports/

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  FinRobot-AF Report Organization Script  "
echo "=========================================="
echo ""

# Change to script's parent directory (project root)
cd "$(dirname "$0")/.." || exit 1

# Ensure target directory exists
mkdir -p docs/development-reports

# Counter for moved files
moved_count=0

# Patterns to match (reports that should be in development-reports/)
patterns=(
    "*_REPORT.md"
    "*_SUMMARY.md"
    "*_ANALYSIS.md"
    "*_GUIDE.md"
    "*_TEST*.md"
    "*_DEBUG*.md"
    "*_IMPLEMENTATION*.md"
    "*_FEASIBILITY*.md"
)

# Files to exclude (keep in root)
exclude=(
    "README.md"
    "ORGANIZATION_SUMMARY.md"
    "CONTRIBUTING.md"
    "CHANGELOG.md"
    "LICENSE.md"
)

# Function to check if file should be excluded
should_exclude() {
    local file=$1
    for excluded in "${exclude[@]}"; do
        if [ "$file" = "$excluded" ]; then
            return 0
        fi
    done
    return 1
}

# Find and move matching files
echo "Scanning for misplaced reports in project root..."
echo ""

for pattern in "${patterns[@]}"; do
    for file in $pattern; do
        # Check if file exists (pattern might not match anything)
        if [ -f "$file" ]; then
            # Check if should be excluded
            if should_exclude "$file"; then
                echo -e "${YELLOW}[SKIP]${NC} $file (excluded)"
                continue
            fi

            # Check if already in development-reports
            if [ "$file" = "docs/development-reports/"* ]; then
                continue
            fi

            # Move the file
            echo -e "${GREEN}[MOVE]${NC} $file → docs/development-reports/"
            mv "$file" docs/development-reports/
            ((moved_count++))
        fi
    done
done

echo ""
echo "=========================================="

if [ $moved_count -eq 0 ]; then
    echo -e "${GREEN}✓ No misplaced reports found. All clean!${NC}"
else
    echo -e "${GREEN}✓ Moved $moved_count report(s) to docs/development-reports/${NC}"
    echo ""
    echo -e "${YELLOW}⚠ Remember to update docs/development-reports/README.md${NC}"
fi

echo "=========================================="
echo ""

# List current reports in development-reports
echo "Current reports in docs/development-reports/:"
echo ""
ls -1 docs/development-reports/*.md 2>/dev/null | while read -r file; do
    basename "$file"
done

echo ""
echo "Done!"
