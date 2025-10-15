@echo off
REM DL_Assistant Dashboard Launcher
REM Quick launcher to open the configuration dashboard

echo Opening DL_Assistant Dashboard...
echo Dashboard will be available at http://127.0.0.1:5000
echo.
echo Press Ctrl+C to close the dashboard.
echo.

REM Wait a bit before opening browser
timeout /t 2 /nobreak >nul

REM Open browser
start "" http://127.0.0.1:5000

REM Start the dashboard
dl-assistant --mode dashboard
