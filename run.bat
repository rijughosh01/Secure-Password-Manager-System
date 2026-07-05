@echo off
setlocal EnableExtensions
title SecureVault - Running

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
  echo Virtual environment not found. Please run setup.bat first.
  echo.
  pause
  exit /b 1
)

call venv\Scripts\activate.bat
echo.
echo  SecureVault is starting...
echo  Open http://127.0.0.1:5000 in your browser
echo  Press Ctrl+C to stop the server
echo.
python run.py
