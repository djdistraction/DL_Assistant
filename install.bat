@echo off
REM DL_Assistant One-Click Installer for Windows
REM This script installs DL_Assistant and launches the configuration dashboard

echo ======================================
echo DL_Assistant One-Click Installer
echo ======================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detected
echo.

REM Check if pip is installed
echo Checking pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed.
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)

echo [OK] pip detected
echo.

REM Install the package
echo Installing DL_Assistant...
python -m pip install -e . --quiet

if %errorlevel% neq 0 (
    echo Error: Installation failed.
    pause
    exit /b 1
)

echo [OK] DL_Assistant installed successfully!
echo.

echo ======================================
echo Installation Complete!
echo ======================================
echo.
echo Opening the configuration dashboard...
echo.
echo The dashboard will open in your browser at http://127.0.0.1:5000
echo You can:
echo   - Configure folder paths
echo   - Set up naming patterns
echo   - Manage file type classifications
echo   - Configure duplicate detection
echo.
echo After configuring your preferences:
echo   - Close the dashboard (Ctrl+C in terminal)
echo   - Run 'dl-assistant' to start monitoring your downloads folder
echo   - Or run 'dl-assistant --mode dashboard' to open dashboard again
echo.
echo Press Ctrl+C to exit the dashboard when you're done configuring.
echo.

REM Wait a bit before opening browser
timeout /t 2 /nobreak >nul

REM Open browser after a short delay
start "" http://127.0.0.1:5000

REM Start the dashboard
dl-assistant --mode dashboard
