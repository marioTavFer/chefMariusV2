@echo off
setlocal
cd /d "%~dp0"

REM Build the standalone executable
python build_exe.py

if %ERRORLEVEL% NEQ 0 (
  echo Build failed.
  exit /b %ERRORLEVEL%
)

echo.
echo Build complete. Find chefMariusV2.exe in .\dist
endlocal
