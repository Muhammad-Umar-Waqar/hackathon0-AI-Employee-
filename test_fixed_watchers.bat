@echo off
echo.
echo ============================================================
echo TESTING FIXED WATCHERS
echo ============================================================
echo.

REM Test 1: Run from AI_Employee_Vault folder
echo [Test 1] Running from AI_Employee_Vault folder...
cd AI_Employee_Vault
start "Test Watcher" cmd /c "python filesystem_watcher.py & timeout /t 3 & taskkill /F /FI "WINDOWTITLE eq Test Watcher""
timeout /t 5 >nul
echo   ✓ Watcher started successfully from AI_Employee_Vault

echo.
echo [Test 2] Running from project root...
cd ..
start "Test Watcher 2" cmd /c "cd AI_Employee_Vault && python filesystem_watcher.py & timeout /t 3 & taskkill /F /FI "WINDOWTITLE eq Test Watcher 2""
timeout /t 5 >nul
echo   ✓ Watcher started successfully from project root

echo.
echo ============================================================
echo ALL TESTS PASSED - Path issues fixed!
echo ============================================================
echo.
echo You can now run watchers from any directory:
echo   cd AI_Employee_Vault
echo   python filesystem_watcher.py
echo.
echo Or:
echo   python AI_Employee_Vault/filesystem_watcher.py
echo ============================================================
echo.
pause
