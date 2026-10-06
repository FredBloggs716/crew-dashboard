@echo off
REM Opens a counsel session in Claude Code from this repo, on your existing subscription.
REM Usage: double-click for a morning brief, or run:  start-counsel.bat debrief
cd /d "%~dp0.."
where claude >nul 2>&1
if errorlevel 1 (
  echo Claude Code CLI not found. Install it from https://claude.com/claude-code and sign in with your Claude account,
  echo or open this folder in the Claude Code desktop app and type /counsel
  pause
  exit /b 1
)
if "%~1"=="" (
  claude "/counsel brief"
) else (
  claude "/counsel %*"
)
