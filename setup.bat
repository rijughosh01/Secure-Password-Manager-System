@echo off
setlocal EnableExtensions
title SecureVault - Setup

echo.
echo  ========================================
echo   SecureVault Password Manager - Setup
echo  ========================================
echo.

cd /d "%~dp0"

:: Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python is not installed or not in PATH.
  echo         Please install Python 3.10+ from https://www.python.org/downloads/
  echo         Make sure to check "Add Python to PATH" during installation.
  echo.
  pause
  exit /b 1
)

echo [1/3] Checking Python version...
python --version
echo.

:: Create virtual environment
if exist "venv\Scripts\python.exe" (
  echo [2/3] Virtual environment already exists - skipping creation.
) else (
  echo [2/3] Creating virtual environment...
  python -m venv venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
  )
  echo       Virtual environment created successfully.
)
echo.

:: Install dependencies
echo [3/3] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Failed to install dependencies.
  pause
  exit /b 1
)
echo.

echo  ========================================
echo   Setup completed successfully!
echo  ========================================
echo.
echo  To start the application, run:
echo    run.bat
echo.
echo  Or manually:
echo    venv\Scripts\activate
echo    python run.py
echo.
echo  Then open: http://127.0.0.1:5000
echo.
pause
