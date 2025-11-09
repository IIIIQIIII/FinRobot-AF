# FinRobot-AF Quick Reference

Quick reference guide for daily development and maintenance.

## 🚀 Common Commands

### Report Management

```bash
# Organize all report files to correct location
./scripts/organize_reports.sh

# Check if there are any missed reports in root directory
ls -1 *.md

# View all development reports
ls -1 docs/development-reports/*.md
```

### Documentation Viewing

```bash
# View documentation structure
tree docs/ -L 2

# Count documentation files
find docs/ -name "*.md" | wc -l

# View report index
cat docs/development-reports/README.md
```

### Development Workflow

```bash
# Run tests
pytest tests/

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## 📝 Standard Process for Generating Reports

### Step 1: Explicitly Specify Path

When requesting from AI agent:

```
Please create [feature] test report, save to:
docs/development-reports/[FEATURE]_TEST_REPORT_20241109.md
```

### Step 2: Run Organization Script

```bash
./scripts/organize_reports.sh
```

### Step 3: Update Index

```bash
vim docs/development-reports/README.md
# Add entry for new report
```

### Step 4: Commit

```bash
git add docs/development-reports/
git commit -m "Add [feature] test report"
```

## 📁 File Placement Rules

| File Type | Location | Example |
|---------|------|------|
| Project Main README | Root directory | `README.md` |
| Development Reports | `docs/development-reports/` | `TEST_REPORT.md` |
| User Guides | `docs/user-guide/` | `agents.md` |
| Tutorials | `docs/tutorials/` | `01-market-analysis.md` |
| API Documentation | `docs/api/` | `agents.md` |
| Example Code | `examples/` | `basic_market_analysis.py` |
| Test Code | `tests/` | `test_workflows.py` |
| Source Code | `finrobot/` | `agents/workflows.py` |

## 📋 Report Naming Conventions

```bash
# Test Reports
[FEATURE]_TEST_REPORT.md
Example: RAG_INTEGRATION_TEST_REPORT.md

# Project Summaries
PROJECT_[TOPIC]_SUMMARY.md
Example: PROJECT_STATUS_SUMMARY.md

# Analysis Reports
[TOPIC]_ANALYSIS.md
Example: PERFORMANCE_ANALYSIS.md

# Implementation Reports
[FEATURE]_IMPLEMENTATION.md
Example: MULTI_AGENT_IMPLEMENTATION.md

# Example Outputs
[SYMBOL]_Analysis_[TIMESTAMP].md
Example: AAPL_Analysis_20241109_143022.md
```

## 🔍 Checklists

### Pre-commit Checklist

- [ ] Run `./scripts/organize_reports.sh`
- [ ] Check `ls -1 *.md` shows only necessary files
- [ ] Updated `docs/development-reports/README.md`
- [ ] Code passes tests
- [ ] Documentation links are correct

### Weekly Maintenance

- [ ] Run organization script
- [ ] Review newly added reports
- [ ] Update documentation index
- [ ] Clean up temporary files

### Monthly Review

- [ ] Archive old reports
- [ ] Update statistics
- [ ] Review documentation completeness
- [ ] Update CHANGELOG

## 🎯 Quick Links

### Documentation
- [Main Documentation](README.md)
- [Quick Start](quick-start.md)
- [Installation Guide](installation.md)
- [Configuration Guide](configuration.md)
- [Development Guide](DEVELOPMENT_GUIDE.md)
- [Report Management](REPORT_MANAGEMENT.md)

### User Guides
- [Agents Guide](user-guide/agents.md)
- [Workflows Guide](user-guide/workflows.md)

### Tutorials
- [Market Analysis Tutorial](tutorials/01-market-analysis.md)

### API Reference
- [Agents API](api/agents.md)

### Development Reports
- [Report Index](development-reports/README.md)

## 💡 Common Tasks

### Create New Test Report

```bash
# 1. Generate report (via AI or manually)
touch docs/development-reports/NEW_FEATURE_TEST_REPORT.md

# 2. Write report content
vim docs/development-reports/NEW_FEATURE_TEST_REPORT.md

# 3. Update index
vim docs/development-reports/README.md

# 4. Commit
git add docs/development-reports/
git commit -m "Add test report for new feature"
```

### Move Misplaced Reports

```bash
# Method 1: Use script (recommended)
./scripts/organize_reports.sh

# Method 2: Move manually
mv MY_REPORT.md docs/development-reports/

# Update index
vim docs/development-reports/README.md
```

### View Project Statistics

```bash
# Documentation count
find docs/ -name "*.md" | wc -l

# Report count
ls -1 docs/development-reports/*.md | wc -l

# Code file count
find finrobot/ -name "*.py" | wc -l

# Total project size
du -sh .
```

## 🛠️ Troubleshooting

### Issue: Script has no permission

```bash
chmod +x scripts/organize_reports.sh
```

### Issue: Cannot find report

```bash
# Search all .md files
find . -name "*.md" -type f

# Search only report-type files
find . -name "*REPORT*.md" -o -name "*SUMMARY*.md"
```

### Issue: Git shows untracked files

```bash
# View untracked files
git status

# If it's a report file, move to correct location
./scripts/organize_reports.sh

# Or add to .gitignore
echo "MY_FILE.md" >> .gitignore
```

## 📞 Getting Help

### Documentation Issues
- See [FAQ](reference/faq.md)
- See [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)

### Report Management Issues
- See [REPORT_MANAGEMENT.md](REPORT_MANAGEMENT.md)
- See [development-reports/README.md](development-reports/README.md)

### Technical Issues
- See project README
- See API documentation
- Submit GitHub Issue

## 🎓 Best Practices

1. **Always specify full path** - Use complete path when generating files
2. **Run organization script regularly** - At least once per week
3. **Update documentation index** - Immediately after adding new files
4. **Use descriptive naming** - Clear file names with dates
5. **Check before committing** - Ensure no files are missed

---

**Last Updated**: November 9, 2024
**Version**: 1.0
