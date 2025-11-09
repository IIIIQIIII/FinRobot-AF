@echo off
REM Conda installation script for FinRobot-AF (Windows)
REM This script creates a conda environment and installs all dependencies

echo ======================================
echo FinRobot-AF Conda Installation Script
echo ======================================
echo.

REM Check if conda is installed
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: conda is not installed
    echo Please install Miniconda or Anaconda first:
    echo   - Miniconda: https://docs.conda.io/en/latest/miniconda.html
    echo   - Anaconda: https://www.anaconda.com/download
    exit /b 1
)

echo Conda is installed
echo.

REM Create conda environment
echo Creating conda environment 'finrobot' with Python 3.10...
call conda create -n finrobot python=3.10 -y

echo.
echo Conda environment created
echo.

REM Install dependencies
echo Installing dependencies...
echo Note: This may take 2-5 minutes...
echo.

call conda run -n finrobot pip install --pre -r requirements.txt
call conda run -n finrobot pip install -e .

echo.
echo ======================================
echo Installation completed successfully!
echo ======================================
echo.
echo To activate the environment, run:
echo   conda activate finrobot
echo.
echo To verify installation, run:
echo   python -c "import finrobot; print('FinRobot installed successfully!')"
echo.
pause
