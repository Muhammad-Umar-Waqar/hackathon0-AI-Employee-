@echo off
echo.
echo ============================================================
echo QUICK SILVER TIER TEST
echo ============================================================
echo.

REM Test 1: Check dependencies
echo [Test 1] Checking dependencies...
cd AI_Employee_Vault
python -c "import watchdog; import googleapiclient; import playwright" 2>nul
if %errorlevel% equ 0 (
    echo   ✓ Dependencies OK
) else (
    echo   ✗ Install: pip install -r requirements.txt
    goto :end
)

REM Test 2: Check credentials
echo.
echo [Test 2] Checking Gmail credentials...
if exist ..\credentials\gmail-token.json (
    echo   ✓ Gmail OAuth configured
) else (
    echo   ✗ Run: python generate_oauth_url.py
    goto :end
)

REM Test 3: Check skills
echo.
echo [Test 3] Checking Claude Skills...
set skills=0
if exist ..\.claude\skills\process-tasks\SKILL.md set /a skills+=1
if exist ..\.claude\skills\create-plans\SKILL.md set /a skills+=1
if exist ..\.claude\skills\approval-workflow\SKILL.md set /a skills+=1
if exist ..\.claude\skills\linkedin-post\SKILL.md set /a skills+=1
if exist ..\.claude\skills\weekly-briefing\SKILL.md set /a skills+=1
if exist ..\.claude\skills\orchestrator-advanced\SKILL.md set /a skills+=1
echo   ✓ %skills%/6 skills found

REM Test 4: Test file system watcher
echo.
echo [Test 4] Testing File System Watcher...
echo Test file created at %time% > Inbox\quick_test_%random%.txt
echo   ✓ Test file created in Inbox/
echo   → Wait 10 seconds...
timeout /t 10 >nul

dir Needs_Action\FILE_*.md /b >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ File detected by watcher
) else (
    echo   → Start watcher: python filesystem_watcher.py
)

REM Test 5: Quick Claude test
echo.
echo [Test 5] Testing Claude integration...
echo.
echo   Try: claude /process-tasks
echo.

:end
echo.
echo ============================================================
echo TEST COMPLETE
echo ============================================================
echo.
echo Next steps:
echo   1. Run: start_watchers.bat (to start all watchers)
echo   2. Drop a file in: AI_Employee_Vault\Inbox\
echo   3. Run: claude /process-tasks
echo.
echo For full test: python test_silver_tier.py
echo ============================================================
echo.
pause
