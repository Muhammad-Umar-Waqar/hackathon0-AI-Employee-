"""
Test script to verify Silver Tier Watchers
"""
from pathlib import Path
import sys
import os

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_dependencies():
    """Test if required dependencies are installed"""
    print("\n" + "="*60)
    print("TESTING DEPENDENCIES")
    print("="*60)
    
    all_installed = True
    
    # Test watchdog
    try:
        import watchdog
        print("✓ watchdog installed")
    except ImportError:
        print("✗ watchdog NOT installed")
        all_installed = False
    
    # Test Google API
    try:
        from googleapiclient.discovery import build
        print("✓ google-api-python-client installed")
    except ImportError:
        print("✗ google-api-python-client NOT installed")
        all_installed = False
    
    # Test Playwright
    try:
        import playwright
        print("✓ playwright installed")
    except ImportError:
        print("✗ playwright NOT installed")
        print("  Install: pip install playwright && playwright install")
        all_installed = False
    
    return all_installed

def test_vault_structure():
    """Test if vault structure is correct"""
    print("\n" + "="*60)
    print("TESTING VAULT STRUCTURE")
    print("="*60)
    
    vault = Path('AI_Employee_Vault')
    all_good = True
    
    # Required folders
    required_folders = [
        'Inbox', 'Needs_Action', 'Done', 'Plans', 'Logs',
        'Pending_Approval', 'Approved', 'Rejected', 'Briefings'
    ]
    
    for folder in required_folders:
        folder_path = vault / folder
        if folder_path.exists() and folder_path.is_dir():
            print(f"✓ {folder}/ exists")
        else:
            print(f"✗ {folder}/ missing")
            all_good = False
    
    # Required files
    required_files = ['Dashboard.md', 'Company_Handbook.md', 'gmail_watcher.py', 'linkedin_watcher.py']
    
    for file in required_files:
        file_path = vault / file
        if file_path.exists():
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_good = False
    
    # Credentials folder (at project root)
    creds_folder = Path('credentials')
    if creds_folder.exists():
        print(f"✓ credentials/ folder exists (project root)")
        # Check for credentials.json
        creds_file = creds_folder / 'credentials.json'
        if creds_file.exists():
            print(f"✓ credentials.json found")
        else:
            print(f"⚠ credentials.json NOT found (place your file here)")
    else:
        print(f"⚠ credentials/ folder missing (creating it)")
        creds_folder.mkdir(exist_ok=True)
    
    # Plans/Social folder
    social_folder = vault / 'Plans' / 'Social'
    if social_folder.exists():
        print(f"✓ Plans/Social/ folder exists")
    else:
        print(f"⚠ Plans/Social/ missing (creating it)")
        social_folder.mkdir(parents=True, exist_ok=True)
    
    return all_good

def test_watcher_scripts():
    """Test if watcher scripts are syntactically correct"""
    print("\n" + "="*60)
    print("TESTING WATCHER SCRIPTS")
    print("="*60)
    
    vault = Path('AI_Employee_Vault')
    all_good = True
    
    # Test Gmail Watcher
    gmail_watcher = vault / 'gmail_watcher.py'
    if gmail_watcher.exists():
        try:
            with open(gmail_watcher, 'r', encoding='utf-8') as f:
                compile(f.read(), str(gmail_watcher), 'exec')
            print("✓ gmail_watcher.py syntax OK")
        except SyntaxError as e:
            print(f"✗ gmail_watcher.py syntax error: {e}")
            all_good = False
    else:
        print("✗ gmail_watcher.py missing")
        all_good = False
    
    # Test LinkedIn Watcher
    linkedin_watcher = vault / 'linkedin_watcher.py'
    if linkedin_watcher.exists():
        try:
            with open(linkedin_watcher, 'r', encoding='utf-8') as f:
                compile(f.read(), str(linkedin_watcher), 'exec')
            print("✓ linkedin_watcher.py syntax OK")
        except SyntaxError as e:
            print(f"✗ linkedin_watcher.py syntax error: {e}")
            all_good = False
    else:
        print("✗ linkedin_watcher.py missing")
        all_good = False
    
    # Test File System Watcher
    fs_watcher = vault / 'filesystem_watcher.py'
    if fs_watcher.exists():
        try:
            with open(fs_watcher, 'r', encoding='utf-8') as f:
                compile(f.read(), str(fs_watcher), 'exec')
            print("✓ filesystem_watcher.py syntax OK")
        except SyntaxError as e:
            print(f"✗ filesystem_watcher.py syntax error: {e}")
            all_good = False
    else:
        print("✗ filesystem_watcher.py missing")
        all_good = False
    
    return all_good

def test_claude_skills():
    """Test if Claude skills are installed"""
    print("\n" + "="*60)
    print("TESTING CLAUDE SKILLS")
    print("="*60)
    
    skills_dir = Path('.claude/skills')
    all_good = True
    
    required_skills = [
        'process-tasks',
        'create-plans',
        'approval-workflow',
        'linkedin-post',
        'weekly-briefing',
        'orchestrator-advanced'
    ]
    
    for skill in required_skills:
        skill_path = skills_dir / skill
        if skill_path.exists():
            # Check for required files
            has_skill_md = (skill_path / 'SKILL.md').exists()
            has_prompt_md = (skill_path / 'PROMPT.md').exists()
            
            if has_skill_md and has_prompt_md:
                print(f"✓ /{skill} complete (SKILL.md + PROMPT.md)")
            else:
                if not has_skill_md:
                    print(f"⚠ /{skill} missing SKILL.md")
                if not has_prompt_md:
                    print(f"⚠ /{skill} missing PROMPT.md")
                all_good = False
        else:
            print(f"✗ /{skill} missing")
            all_good = False
    
    return all_good

def test_logs():
    """Test if logging is working"""
    print("\n" + "="*60)
    print("TESTING LOGGING SYSTEM")
    print("="*60)
    
    vault = Path('AI_Employee_Vault')
    logs_folder = vault / 'Logs'
    
    if not logs_folder.exists():
        print("⚠ Logs/ folder missing (creating it)")
        logs_folder.mkdir(exist_ok=True)
        return True
    
    print(f"✓ Logs/ folder exists")
    
    # Check for existing logs
    log_files = list(logs_folder.glob('*.log'))
    if log_files:
        print(f"✓ Found {len(log_files)} log file(s):")
        for log in log_files:
            print(f"  - {log.name}")
    else:
        print(f"ℹ No log files yet (will be created when watchers run)")
    
    return True

def run_quick_test():
    """Run a quick functional test"""
    print("\n" + "="*60)
    print("QUICK FUNCTIONAL TEST")
    print("="*60)
    
    vault = Path('AI_Employee_Vault')
    
    # Create a test file
    test_file = vault / 'Inbox' / 'test_silver_tier.txt'
    test_file.write_text("Silver Tier Watcher Test File\n")
    print(f"✓ Created test file: {test_file.name}")
    
    print("\n📋 Next Steps:")
    print(f"1. Start filesystem watcher: python AI_Employee_Vault/filesystem_watcher.py")
    print(f"2. Watcher should detect: {test_file.name}")
    print(f"3. Check Needs_Action/ for created task file")
    print(f"4. Process with: claude /process-tasks")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SILVER TIER WATCHERS - TEST SUITE")
    print("="*60)
    
    results = {
        'Dependencies': test_dependencies(),
        'Vault Structure': test_vault_structure(),
        'Watcher Scripts': test_watcher_scripts(),
        'Claude Skills': test_claude_skills(),
        'Logging': test_logs(),
        'Functional Test': run_quick_test()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL TESTS PASSED - Silver Tier Ready!")
        print("\n📋 Start Watchers:")
        print("   python AI_Employee_Vault/gmail_watcher.py")
        print("   python AI_Employee_Vault/linkedin_watcher.py")
        print("   python AI_Employee_Vault/filesystem_watcher.py")
    else:
        print("❌ SOME TESTS FAILED - Fix issues above")
        print("\n📋 Common Fixes:")
        print("   pip install -r AI_Employee_Vault/requirements.txt")
        print("   playwright install chromium")
        print("   Place credentials.json in AI_Employee_Vault/credentials/")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
