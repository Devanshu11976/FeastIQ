@echo off
echo Stopping FeastIQ Servers...
echo.

taskkill /FI "WINDOWTITLE eq FeastIQ Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq FeastIQ Frontend*" /T /F >nul 2>&1

echo.
echo ========================================
echo Servers Stopped Successfully!
echo ========================================
echo.
pause
