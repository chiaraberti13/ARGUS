@echo off
REM Quick launcher for Windows: uses the local venv if present.
set "DIR=%~dp0.."
if exist "%DIR%\.venv\Scripts\python.exe" (
  "%DIR%\.venv\Scripts\python.exe" -m ghosttrack %*
) else (
  python -m ghosttrack %*
)
