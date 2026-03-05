@echo off
echo.
echo ============================================================
echo AI EMPLOYEE - SILVER TIER WATCHER STARTER
echo ============================================================
echo.
echo This will start all 3 watchers in separate windows
echo.
pause

REM Start File System Watcher
start "File System Watcher" cmd /k "cd AI_Employee_Vault && python filesystem_watcher.py"
timeout /t 2 >nul

REM Start Gmail Watcher
start "Gmail Watcher" cmd /k "cd AI_Employee_Vault && python gmail_watcher.py"
timeout /t 2 >nul

REM Start LinkedIn Watcher
start "LinkedIn Watcher" cmd /k "cd AI_Employee_Vault && python linkedin_watcher.py"
timeout /t 2 >nul

echo.
echo ============================================================
echo All watchers started!
echo ============================================================
echo.
echo Running watchers:
echo   - File System Watcher (monitoring Inbox/)
echo   - Gmail Watcher (checking every 2 minutes)
echo   - LinkedIn Watcher (checking every 5 minutes)
echo.
echo To process tasks, open a new terminal and run:
echo   cd AI_Employee_Vault
echo   claude /process-tasks
echo.
echo To stop watchers, close the terminal windows or press Ctrl+C
echo ============================================================
echo.
pause
