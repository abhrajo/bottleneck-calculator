@echo off
REM ─────────────────────────────────────────────────────────────────
REM  Bottleneck Calculator — Build Script
REM  Requirements: Python 3.10+, pip
REM  Run this script on Windows to produce BottleneckCalculator.exe
REM ─────────────────────────────────────────────────────────────────

echo [1/4] Installing dependencies...
pip install pyinstaller --upgrade --quiet
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python is in PATH.
    pause & exit /b 1
)

echo [2/4] Cleaning previous build...
if exist build  rmdir /s /q build
if exist dist   rmdir /s /q dist

echo [3/4] Building executable...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name "BottleneckCalculator" ^
  --icon NONE ^
  --add-data "bottleneck_calculator.py;." ^
  bottleneck_calculator.py

if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause & exit /b 1
)

echo [4/4] Done!
echo ──────────────────────────────────────────
echo  Executable: dist\BottleneckCalculator.exe
echo ──────────────────────────────────────────
explorer dist
pause
