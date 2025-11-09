# Report Management Guide

How to manage AI-generated development reports in the FinRobot-AF project.

## 🎯 Problem Statement

When using AI coding agents (such as Claude Code) to generate reports, these files are **not automatically** placed in the `docs/development-reports/` directory by default, but instead are placed in the current working directory (usually the project root directory).

## ✅ Solutions

We provide multiple methods to manage this issue:

---

## Method 1: Use Automation Script (Recommended)

### Quick Usage

```bash
# Run organization script
./scripts/organize_reports.sh
```

The script will automatically:
- ✅ Scan the project root directory
- ✅ Find all report files (`*_REPORT.md`, `*_SUMMARY.md`, etc.)
- ✅ Move to `docs/development-reports/`
- ✅ Skip important root directory files (README.md, etc.)
- ✅ Display move results

### Regular Execution

Recommended to run the script in the following situations:
- After using AI agent to generate reports
- Weekly cleanup
- Before committing code

---

## Method 2: Explicitly Specify File Path

When requesting AI agent to generate reports, **explicitly specify the full path**:

### ❌ Bad Practice
```
"Generate a test report"
"Create a project summary"
```

### ✅ Good Practice
```
"Generate a test report, save to docs/development-reports/NEW_FEATURE_TEST_REPORT.md"
"Create a project summary, save to docs/development-reports/PROJECT_STATUS_20241109.md"
```

### Example Conversation

```
User: Please create a test report for the new feature

AI: I will create a test report. Where should the file be saved?

User: Save to docs/development-reports/RAG_FEATURE_TEST_REPORT.md
```

---

## Method 3: Manually Move Files

If reports have already been generated in the root directory, move them manually:

```bash
# Single file
mv MY_REPORT.md docs/development-reports/

# Batch move all reports
mv *_REPORT.md docs/development-reports/
mv *_SUMMARY.md docs/development-reports/
mv *_ANALYSIS.md docs/development-reports/
```

---

## Method 4: Git Ignore Rules

The project's `.gitignore` is configured to ignore report files in the root directory:

```gitignore
# Reports generated in root directory
*_REPORT.md
*_SUMMARY.md
*_ANALYSIS.md
*_GUIDE.md

# Exceptions
!README.md
!ORGANIZATION_SUMMARY.md
```

**Benefits**:
- ❌ Will not accidentally commit report files in root directory to Git
- ✅ Reminds you to move files to the correct location

**Note**: This will not automatically move files, it only prevents commits

---

## 📋 Standard Workflow

### Complete Process for Generating New Reports

#### Step 1: Generate Report (Specify Path)

```
Please generate test report for [feature], save to:
docs/development-reports/[FEATURE]_TEST_REPORT.md
```

#### Step 2: If Generated in Root Directory

```bash
# Run organization script
./scripts/organize_reports.sh

# Or move manually
mv *_REPORT.md docs/development-reports/
```

#### Step 3: Update Index

Edit `docs/development-reports/README.md`, add new report information:

```markdown
### [NEW_FEATURE_TEST_REPORT.md](NEW_FEATURE_TEST_REPORT.md)
**Date**: 2024-11-09
**Size**: 15K
**Purpose**: Testing results for new feature

Description of what the report contains...
```

#### Step 4: Commit

```bash
git add docs/development-reports/NEW_FEATURE_TEST_REPORT.md
git add docs/development-reports/README.md
git commit -m "Add test report for new feature"
```

---

## 🔍 Checking and Verification

### Check for Missing Reports

```bash
# List all .md files in root directory
ls -1 *.md

# Should only see:
# - README.md
# - ORGANIZATION_SUMMARY.md
# - (other important root documents)
```

### If You See Other `*_REPORT.md` or `*_SUMMARY.md`

```bash
# Run organization script
./scripts/organize_reports.sh
```

### View All Organized Reports

```bash
# List all reports
ls -1 docs/development-reports/*.md

# View report count
ls -1 docs/development-reports/*.md | wc -l
```

---

## 📊 Naming Conventions

Use the following naming patterns when generating reports:

### Test Reports
```
[FEATURE]_TEST_REPORT.md
Example: RAG_INTEGRATION_TEST_REPORT.md
```

### Project Summaries
```
PROJECT_[TOPIC]_SUMMARY.md
Example: PROJECT_STATUS_SUMMARY.md
```

### Analysis Reports
```
[TOPIC]_ANALYSIS.md
Example: PERFORMANCE_ANALYSIS.md
```

### Implementation Reports
```
[FEATURE]_IMPLEMENTATION.md
Example: MULTI_AGENT_IMPLEMENTATION.md
```

### Debug Reports
```
[ISSUE]_DEBUG_REPORT.md
Example: MEMORY_LEAK_DEBUG_REPORT.md
```

### Example Outputs
```
[SYMBOL]_Analysis_[TIMESTAMP].md
Example: AAPL_Analysis_20241109_143022.md
```

---

## 🤖 Best Practices for AI Agent Collaboration

### 1. Clearly Specify File Location

```
✅ "Create test report to docs/development-reports/TEST_REPORT.md"
❌ "Create test report"
```

### 2. Use Full Path

```
✅ docs/development-reports/FEATURE_ANALYSIS.md
❌ development-reports/FEATURE_ANALYSIS.md
❌ FEATURE_ANALYSIS.md
```

### 3. Include Date and Descriptive Name

```
✅ INTEGRATION_TEST_REPORT_20241109.md
✅ RAG_PERFORMANCE_ANALYSIS.md
❌ report.md
❌ test.md
```

### 4. Run Organization Script After Completion

```bash
./scripts/organize_reports.sh
```

---

## 🛠️ Maintenance Tasks

### Weekly Cleanup (Recommended)

```bash
# 1. Run organization script
./scripts/organize_reports.sh

# 2. Check root directory
ls -1 *.md

# 3. Update report index
vim docs/development-reports/README.md

# 4. Commit changes
git add docs/development-reports/
git commit -m "Weekly report organization"
```

### Monthly Review

1. Review all reports
2. Archive outdated reports
3. Update statistics
4. Clean up unnecessary reports

---

## 📁 Directory Structure Reference

```
FinRobot-AF/
├── README.md                         ✅ Keep in root directory
├── ORGANIZATION_SUMMARY.md           ✅ Keep in root directory
│
├── docs/
│   ├── development-reports/          ← All development reports go here
│   │   ├── README.md                 ← Report index
│   │   ├── *_REPORT.md              ← Test reports
│   │   ├── *_SUMMARY.md             ← Project summaries
│   │   ├── *_ANALYSIS.md            ← Analysis reports
│   │   └── ...
│   │
│   ├── user-guide/                   ← User guides
│   ├── tutorials/                    ← Tutorials
│   └── ...
│
└── scripts/
    └── organize_reports.sh           ← Automatic organization script
```

---

## ❓ Frequently Asked Questions

### Q: AI generated reports are always in root directory, what to do?

**A**: Use any of the following methods:
1. Explicitly specify path when requesting
2. Run `./scripts/organize_reports.sh` after generation
3. Move files manually

### Q: How to prevent accidentally committing reports in root directory?

**A**: `.gitignore` is configured to automatically ignore report files in root directory

### Q: Which files will the organization script move?

**A**: Files matching the following patterns:
- `*_REPORT.md`
- `*_SUMMARY.md`
- `*_ANALYSIS.md`
- `*_GUIDE.md`
- `*_TEST*.md`
- `*_DEBUG*.md`

**But will preserve**:
- `README.md`
- `ORGANIZATION_SUMMARY.md`
- Other important root documents

### Q: Can the organization script run automatically?

**A**: You can set up Git hooks:

```bash
# Add to .git/hooks/pre-commit:
#!/bin/bash
./scripts/organize_reports.sh
```

### Q: What if I accidentally delete a report?

**A**: Restore using Git:
```bash
git checkout docs/development-reports/REPORT_NAME.md
```

---

## 📚 Related Documentation

- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - Development Guide
- [ORGANIZATION_SUMMARY.md](../ORGANIZATION_SUMMARY.md) - Project Organization Summary
- [development-reports/README.md](development-reports/README.md) - Report Index

---

## 🎯 Quick Reference

```bash
# Run immediately after generating report
./scripts/organize_reports.sh

# Check root directory
ls -1 *.md

# View all reports
ls -1 docs/development-reports/*.md

# Move manually
mv *_REPORT.md docs/development-reports/

# Update index
vim docs/development-reports/README.md
```

---

**Last Updated**: November 9, 2024
**Version**: 1.0
**Status**: Active
