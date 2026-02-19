#!/bin/bash
# Demo script to show Bronze Tier AI Employee in action

echo "=========================================="
echo "  BRONZE TIER AI EMPLOYEE - DEMO"
echo "=========================================="
echo ""

# Check structure
echo "✓ Checking vault structure..."
if [ -d "AI_Employee_Vault" ]; then
    echo "  [OK] Vault exists"
    echo "  [OK] Folders: $(ls -d AI_Employee_Vault/*/ | wc -l) directories"
fi

# Check core files
echo ""
echo "✓ Checking core files..."
[ -f "AI_Employee_Vault/Dashboard.md" ] && echo "  [OK] Dashboard.md"
[ -f "AI_Employee_Vault/Company_Handbook.md" ] && echo "  [OK] Company_Handbook.md"
[ -f "AI_Employee_Vault/filesystem_watcher.py" ] && echo "  [OK] filesystem_watcher.py"

# Check Claude skill
echo ""
echo "✓ Checking Claude Code skill..."
[ -d ".claude/skills/process-tasks" ] && echo "  [OK] /process-tasks skill installed"

# Check dependencies
echo ""
echo "✓ Checking dependencies..."
python -c "import watchdog" 2>/dev/null && echo "  [OK] watchdog installed" || echo "  [!] Run: pip install -r AI_Employee_Vault/requirements.txt"

# Show inbox files
echo ""
echo "✓ Files in Inbox (ready for processing):"
ls -1 AI_Employee_Vault/Inbox/ 2>/dev/null | sed 's/^/  - /'

echo ""
echo "=========================================="
echo "  SYSTEM READY!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start watcher: python AI_Employee_Vault/filesystem_watcher.py"
echo "  2. Process tasks: claude /process-tasks"
echo "  3. View dashboard: cat AI_Employee_Vault/Dashboard.md"
echo ""
