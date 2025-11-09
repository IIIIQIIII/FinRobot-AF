# Pre-Release Package Installation Note

## Why `--pre` Flag is Required

FinRobot-AF depends on **Microsoft Agent Framework**, which is currently in **preview/pre-release** status on PyPI.

### What is a Pre-Release Package?

Pre-release packages (also called preview or beta packages) are versions that are:
- Still under active development
- Not yet considered stable/production-ready
- Marked with version suffixes like `1.0.0b251105` (beta)

### How to Install Pre-Release Packages

By default, `pip` and `uv` **skip pre-release versions** for safety. You must explicitly allow them using the `--pre` flag:

```bash
# Standard pip installation (WILL FAIL)
pip install agent-framework-core
# ❌ Error: No matching distribution found

# Correct installation with --pre flag
pip install --pre agent-framework-core
# ✅ Success: Installs version 1.0.0b251105
```

## Installation Methods for FinRobot-AF

### Method 1: uv (Recommended)

```bash
uv venv
source .venv/bin/activate
uv pip install --pre -e .
```

### Method 2: pip + venv

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --pre -r requirements.txt
pip install -e .
```

### Method 3: conda

```bash
# Use installation script
./install_conda.sh  # Linux/macOS
install_conda.bat   # Windows

# Or manually
conda create -n finrobot python=3.10 -y
conda activate finrobot
pip install --pre -r requirements.txt
pip install -e .
```

## Current Agent Framework Versions

As of this documentation, `agent-framework-core` available versions are:
- `1.0.0b251001`
- `1.0.0b251007`
- `1.0.0b251016`
- `1.0.0b251028`
- `1.0.0b251104`
- `1.0.0b251105`
- `1.0.0b251108`

The `b` in the version indicates **beta** status.

## When Will `--pre` No Longer Be Needed?

The `--pre` flag will no longer be required when:
1. Microsoft releases Agent Framework `1.0.0` (stable)
2. We update FinRobot-AF to use the stable version

## Common Errors

### Error: "No matching distribution found for agent-framework-core"

**Cause**: Missing `--pre` flag

**Solution**:
```bash
# Add --pre flag
pip install --pre agent-framework-core
```

### Error: "typing-extensions version conflict"

**Cause**: Old version of `typing-extensions` in requirements

**Solution**: Already fixed in current `requirements.txt`:
```bash
typing-extensions>=4.11  # Compatible with agent-framework
```

## References

- [Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Agent Framework PyPI](https://pypi.org/project/agent-framework/)
- [PEP 440 - Version Identification](https://peps.python.org/pep-0440/)

## Summary

✅ **Always use `--pre` flag when installing FinRobot-AF and its dependencies**

```bash
# uv
uv pip install --pre -e .

# pip
pip install --pre -r requirements.txt

# Direct package install
pip install --pre agent-framework-core
```
