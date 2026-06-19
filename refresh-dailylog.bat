@echo off
REM Refreshes dailylog.js from the published Daily Log CSV, then opens the dashboard.
cd /d "%~dp0"
echo Refreshing Daily Log data...
node build-dailylog.mjs
if errorlevel 1 (
  echo.
  echo Could not refresh. Check your internet connection.
  pause
  exit /b 1
)
echo.
echo Done. Opening dashboard...
start "" "index.html"
