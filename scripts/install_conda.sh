#!/bin/bash
# Conda installation script for FinRobot-AF
# This script creates a conda environment and installs all dependencies

set -e  # Exit on error

echo "======================================"
echo "FinRobot-AF Conda Installation Script"
echo "======================================"
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Error: conda is not installed"
    echo "Please install Miniconda or Anaconda first:"
    echo "  - Miniconda: https://docs.conda.io/en/latest/miniconda.html"
    echo "  - Anaconda: https://www.anaconda.com/download"
    exit 1
fi

echo "✓ Conda is installed"
echo ""

# Create conda environment
echo "Creating conda environment 'finrobot' with Python 3.10..."
conda create -n finrobot python=3.10 -y

echo ""
echo "✓ Conda environment created"
echo ""

# Activate environment and install dependencies
echo "Installing dependencies..."
echo "Note: This may take 2-5 minutes..."
echo ""

# Use conda run to execute in the environment
conda run -n finrobot pip install --pre -r requirements.txt
conda run -n finrobot pip install -e .

echo ""
echo "======================================"
echo "✅ Installation completed successfully!"
echo "======================================"
echo ""
echo "To activate the environment, run:"
echo "  conda activate finrobot"
echo ""
echo "To verify installation, run:"
echo "  python -c 'import finrobot; print(\"FinRobot installed successfully!\")'"
echo ""
