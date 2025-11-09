# FinRobot-AF Project Structure

This document describes the project structure and organization standards followed by FinRobot-AF.

## 📁 Directory Structure

```
FinRobot-AF/
├── README.md                       # Project overview and quick start
├── ORGANIZATION_SUMMARY.md         # Organization and cleanup documentation
├── LICENSE                         # Project license
├── Makefile                        # Build automation
├── setup.py                        # Package installation
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── config_api_keys                 # API keys configuration (gitignored)
├── config_api_keys_sample         # Sample API keys template
├── OAI_CONFIG_LIST                # LLM configuration (gitignored)
├── OAI_CONFIG_LIST_sample         # Sample LLM config template
│
├── finrobot/                       # 📦 Source Code
│   ├── __init__.py
│   ├── agents/                     # Agent implementations
│   │   ├── agent_library.py        # Pre-configured agents
│   │   ├── workflows.py            # Workflow patterns
│   │   ├── prompts.py              # System prompts
│   │   └── response_utils.py       # Response handling
│   ├── data_source/                # Financial data integrations
│   │   ├── finnhub_utils.py
│   │   ├── yfinance_utils.py
│   │   ├── fmp_utils.py
│   │   ├── sec_utils.py
│   │   └── ...
│   ├── functional/                 # Functional modules
│   │   ├── analyzer.py
│   │   ├── charting.py
│   │   ├── coding.py
│   │   ├── rag.py
│   │   └── ...
│   ├── workflows/                  # Workflow implementations
│   ├── utils/                      # Utility modules
│   ├── config.py                   # Configuration management
│   └── toolkits.py                 # Tool registration
│
├── docs/                           # 📚 Documentation
│   ├── README.md                   # Documentation hub
│   ├── quick-start.md              # Quick start guide
│   ├── installation.md             # Installation instructions
│   ├── configuration.md            # Configuration guide
│   ├── DOCUMENTATION_INDEX.md      # Complete documentation index
│   ├── DEVELOPMENT_GUIDE.md        # Development guidelines
│   ├── REPORT_MANAGEMENT.md        # Report management guide
│   ├── QUICK_REFERENCE.md          # Quick reference
│   ├── PROJECT_STRUCTURE.md        # This file
│   │
│   ├── user-guide/                 # User guides
│   │   ├── agents.md
│   │   └── workflows.md
│   │
│   ├── tutorials/                  # Tutorial documentation
│   │   └── 01-market-analysis.md
│   │
│   ├── migration/                  # Migration guides
│   │   └── from-autogen.md
│   │
│   ├── api/                        # API reference
│   │   └── agents.md
│   │
│   ├── reference/                  # Reference materials
│   │   └── faq.md
│   │
│   ├── advanced/                   # Advanced topics (planned)
│   ├── examples/                   # Example docs (planned)
│   │
│   └── development-reports/        # Development history (archived)
│       ├── README.md               # Reports index
│       └── *.md                    # Development reports
│
├── examples/                       # 💡 Code Examples
│   ├── basic_market_analysis.py
│   ├── investment_report_generation.py
│   └── multi_agent_collaboration.py
│
├── tests/                          # 🧪 Test Suite
│   ├── test_workflows.py
│   ├── test_agents.py
│   └── ...
│
├── scripts/                        # 🛠️ Utility Scripts
│   └── organize_reports.sh         # Report organization script
│
├── data/                           # 📊 Data Directory
│   └── README.md
│
└── results/                        # 📈 Results Output
    └── README.md
```

## 🎯 Design Principles

This structure follows GitHub open source project best practices:

### 1. **Clear Separation of Concerns**

- **Source code** in `finrobot/`
- **Documentation** in `docs/`
- **Examples** in `examples/`
- **Tests** in `tests/`

### 2. **Standard Naming Conventions**

- Lowercase with underscores for Python modules
- Descriptive directory names
- No redundant or empty directories

### 3. **Documentation-First Approach**

- Comprehensive `docs/` directory
- Multiple documentation types:
  - User guides
  - Tutorials
  - API reference
  - Migration guides

### 4. **Configuration Management**

- Sample configs provided (`*_sample`)
- Actual configs gitignored
- Clear separation of development and production configs

### 5. **Development History Preserved**

- Development reports archived in `docs/development-reports/`
- Not mixed with user-facing documentation
- Properly indexed and organized

## 📚 Documentation Organization

### User-Facing Documentation
Located in `docs/` root and subdirectories:
- Getting started guides
- User guides
- Tutorials
- API reference
- FAQ and troubleshooting

### Development Documentation
Located in `docs/development-reports/`:
- Project summaries
- Migration reports
- Test reports
- Implementation reports

## 💡 Code Organization

### Source Code (`finrobot/`)
- **agents/**: Agent definitions and workflows
- **data_source/**: Financial data integrations
- **functional/**: Reusable functional modules
- **workflows/**: Workflow implementations
- **config.py**: Configuration management
- **toolkits.py**: Tool registration system

### Examples (`examples/`)
Runnable Python scripts demonstrating:
- Basic market analysis
- Investment report generation
- Multi-agent collaboration

### Tests (`tests/`)
Comprehensive test suite covering:
- Agent functionality
- Workflow patterns
- Data integrations
- Configuration

## 🔧 Configuration Files

### Root Level
- `README.md` - Project overview
- `setup.py` - Package installation
- `requirements.txt` - Dependencies
- `Makefile` - Build commands
- `.gitignore` - Git ignore rules

### Config Files (Gitignored)
- `config_api_keys` - API keys
- `OAI_CONFIG_LIST` - LLM configuration

### Config Templates (Committed)
- `config_api_keys_sample` - API keys template
- `OAI_CONFIG_LIST_sample` - LLM config template

## 📊 Comparison with Popular Projects

### Similar Structure To:

**TensorFlow**
```
tensorflow/
├── tensorflow/          # Source (like our finrobot/)
├── docs/                # Documentation
├── examples/            # Examples
└── tests/               # Tests
```

**Django**
```
django/
├── django/              # Source
├── docs/                # Documentation
├── examples/            # Examples
└── tests/               # Tests
```

**FastAPI**
```
fastapi/
├── fastapi/             # Source
├── docs/                # Documentation
├── examples/            # Examples
└── tests/               # Tests
```

## ✅ Standards Compliance

FinRobot-AF follows these industry standards:

### 1. Python Project Structure
- ✅ Package in named directory (`finrobot/`)
- ✅ `setup.py` for installation
- ✅ `requirements.txt` for dependencies
- ✅ `tests/` for test suite
- ✅ `README.md` as entry point

### 2. Documentation Best Practices
- ✅ Comprehensive `docs/` directory
- ✅ Multiple documentation types
- ✅ Clear navigation and index
- ✅ Separation of user and developer docs

### 3. Open Source Standards
- ✅ No empty directories
- ✅ Clear project structure
- ✅ Sample configurations provided
- ✅ Secrets gitignored
- ✅ Examples included

### 4. GitHub Best Practices
- ✅ Descriptive README
- ✅ License file (if applicable)
- ✅ Contribution guidelines (planned)
- ✅ Issue templates (planned)
- ✅ CI/CD configs (planned)

## 🚫 What We Avoid

### Anti-Patterns Not Used:
- ❌ Empty directories
- ❌ Redundant directory structures
- ❌ Mixed documentation types
- ❌ Inconsistent naming
- ❌ Scattered configuration files
- ❌ Undocumented code structure

## 🔄 Recent Changes

### November 9, 2025
**Removed Empty Directories**:
- ✅ Deleted `reports/` (content moved to `docs/development-reports/`)
- ✅ Deleted `tutorials/` (content in `docs/tutorials/` and `examples/`)

**Rationale**:
- Follows GitHub open source standards
- Eliminates confusion
- Clearer project structure

## 📝 Directory Purpose Reference

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `finrobot/` | Source code | Agent implementations, utilities |
| `docs/` | Documentation | All user and developer docs |
| `examples/` | Code examples | Runnable example scripts |
| `tests/` | Test suite | Unit and integration tests |
| `scripts/` | Utilities | Development and maintenance scripts |
| `data/` | Data files | Sample data, datasets |
| `results/` | Output | Generated reports and results |

## 🎓 Best Practices

### Adding New Files

**Source Code**:
```bash
# Add to finrobot/ subdirectories
finrobot/new_module/new_file.py
```

**Documentation**:
```bash
# Add to appropriate docs/ subdirectory
docs/user-guide/new-guide.md
docs/tutorials/02-new-tutorial.md
```

**Examples**:
```bash
# Add to examples/
examples/new_example.py
```

**Tests**:
```bash
# Add to tests/
tests/test_new_feature.py
```

### Maintaining Structure

1. **No empty directories** - Remove if not needed
2. **Clear naming** - Descriptive directory names
3. **Proper placement** - Follow established patterns
4. **Documentation** - Update this file when structure changes

## 📖 Related Documentation

- [ORGANIZATION_SUMMARY.md](../ORGANIZATION_SUMMARY.md) - Organization history
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - Development guidelines
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Complete docs index

## 🆘 Questions?

If unsure where to place files:
1. Check this document
2. Look at similar projects
3. Follow the principle of separation of concerns
4. When in doubt, ask in discussions

---

**Last Updated**: November 9, 2025
**Version**: 1.0
**Status**: Active
**Compliance**: GitHub Open Source Standards ✅
