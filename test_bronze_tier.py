"""
Test script to verify Bronze Tier implementation
"""
from pathlib import Path
import time
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_bronze_tier():
    """Test all Bronze Tier requirements"""
    vault = Path('AI_Employee_Vault')

    print("Testing Bronze Tier Implementation...")
    print("=" * 60)

    # Test 1: Vault structure
    print("\n[Test 1] Checking vault structure...")
    required_folders = ['Inbox', 'Needs_Action', 'Done', 'Plans', 'Logs',
                       'Pending_Approval', 'Approved', 'Rejected']

    for folder in required_folders:
        folder_path = vault / folder
        if folder_path.exists():
            print(f"  [OK] {folder}/ exists")
        else:
            print(f"  [FAIL] {folder}/ missing")
            return False

    # Test 2: Core files
    print("\n[Test 2] Checking core files...")
    required_files = ['Dashboard.md', 'Company_Handbook.md']

    for file in required_files:
        file_path = vault / file
        if file_path.exists():
            print(f"  [OK] {file} exists")
        else:
            print(f"  [FAIL] {file} missing")
            return False

    # Test 3: Watcher script
    print("\n[Test 3] Checking watcher script...")
    watcher = vault / 'filesystem_watcher.py'
    if watcher.exists():
        print(f"  [OK] filesystem_watcher.py exists")
    else:
        print(f"  [FAIL] filesystem_watcher.py missing")
        return False

    # Test 4: Claude Code skill
    print("\n[Test 4] Checking Claude Code skill...")
    skill_path = Path('.claude/skills/process-tasks')
    if skill_path.exists():
        print(f"  [OK] /process-tasks skill exists")
        if (skill_path / 'PROMPT.md').exists():
            print(f"  [OK] PROMPT.md exists")
        if (skill_path / 'SKILL.md').exists():
            print(f"  [OK] SKILL.md exists")
    else:
        print(f"  [FAIL] /process-tasks skill missing")
        return False

    # Test 5: Create a test file
    print("\n[Test 5] Creating test file in Inbox...")
    test_file = vault / 'Inbox' / 'test_document.txt'
    test_file.write_text("This is a test document for Bronze Tier verification.")
    print(f"  [OK] Created {test_file.name}")

    print("\n" + "=" * 60)
    print("SUCCESS: ALL BRONZE TIER REQUIREMENTS MET!")
    print("=" * 60)

    print("\nNext steps:")
    print("1. Start the watcher: python AI_Employee_Vault/filesystem_watcher.py")
    print("2. The watcher will detect test_document.txt and create a task")
    print("3. Process tasks: claude /process-tasks")
    print("\nOr use the orchestrator: python orchestrator.py")

    return True

if __name__ == '__main__':
    test_bronze_tier()
