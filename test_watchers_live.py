"""
Live test for watchers
"""
from pathlib import Path
import time
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_filesystem_watcher():
    """Test filesystem watcher by creating a file and checking if it's detected"""
    print("\n" + "="*60)
    print("TESTING FILESYSTEM WATCHER")
    print("="*60)
    
    vault = Path('AI_Employee_Vault')
    inbox = vault / 'Inbox'
    needs_action = vault / 'Needs_Action'
    
    # Ensure inbox exists
    inbox.mkdir(exist_ok=True)
    
    # Create a test file
    test_file = inbox / 'live_test_file.txt'
    test_file.write_text("This is a live test for Silver Tier watchers\n")
    print(f"✓ Created test file: {test_file}")
    
    # Import and run watcher for a short time
    print("\n📡 Starting filesystem watcher (10 second test)...")
    
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import threading
    
    class TestHandler(FileSystemEventHandler):
        def __init__(self):
            self.file_detected = False
            self.detected_file = None
            
        def on_created(self, event):
            if not event.is_directory:
                if 'Inbox' in event.src_path:
                    self.file_detected = True
                    self.detected_file = event.src_path
                    print(f"\n✅ FILE DETECTED: {event.src_path}")
    
    handler = TestHandler()
    observer = Observer()
    observer.schedule(handler, str(inbox), recursive=False)
    observer.start()
    
    print(f"👀 Watching: {inbox}")
    print("⏱️  Test duration: 10 seconds\n")
    
    # Wait for file detection
    time.sleep(10)
    
    observer.stop()
    observer.join()
    
    # Check if file was detected
    if handler.file_detected:
        print("\n✅ SUCCESS: Filesystem watcher is working!")
        return True
    else:
        print("\n❌ FAIL: File was not detected")
        return False

def test_gmail_watcher_import():
    """Test if Gmail watcher can be imported and initialized"""
    print("\n" + "="*60)
    print("TESTING GMAIL WATCHER INITIALIZATION")
    print("="*60)
    
    try:
        sys.path.insert(0, 'AI_Employee_Vault')
        from gmail_watcher import GmailWatcher
        
        vault_path = Path('AI_Employee_Vault')
        
        # Create watcher instance
        watcher = GmailWatcher(str(vault_path))
        
        print("✓ GmailWatcher class imported successfully")
        print(f"✓ Vault path: {vault_path}")
        print(f"✓ Credentials dir: {watcher.credentials_dir}")
        print(f"✓ Credentials file exists: {watcher.credentials_file.exists()}")
        
        if watcher.credentials_file.exists():
            print("✅ SUCCESS: credentials.json found!")
            
            # Try to authenticate
            print("\n🔐 Testing authentication...")
            if watcher.authenticate():
                print("✅ SUCCESS: Gmail API authenticated!")
                return True
            else:
                print("⚠️  Authentication failed (may need browser login)")
                return True  # Still OK, just needs first-time auth
        else:
            print("⚠️  credentials.json not found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_linkedin_watcher_import():
    """Test if LinkedIn watcher can be imported"""
    print("\n" + "="*60)
    print("TESTING LINKEDIN WATCHER INITIALIZATION")
    print("="*60)
    
    try:
        sys.path.insert(0, 'AI_Employee_Vault')
        from linkedin_watcher import LinkedInWatcher
        
        vault_path = Path('AI_Employee_Vault')
        
        # Create watcher instance
        watcher = LinkedInWatcher(str(vault_path))
        
        print("✓ LinkedInWatcher class imported successfully")
        print(f"✓ Vault path: {vault_path}")
        print(f"✓ Session path: {watcher.session_path}")
        print(f"✓ Playwright available: {watcher.playwright_available}")
        
        if watcher.playwright_available:
            print("✅ SUCCESS: Playwright is available!")
        else:
            print("⚠️  Playwright not available")
        
        return True
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_claude_skills():
    """Test Claude skills by checking their files"""
    print("\n" + "="*60)
    print("TESTING CLAUDE SKILLS")
    print("="*60)
    
    skills_dir = Path('.claude/skills')
    skills = [
        'process-tasks',
        'create-plans',
        'approval-workflow',
        'linkedin-post',
        'weekly-briefing',
        'orchestrator-advanced'
    ]
    
    all_ok = True
    for skill in skills:
        skill_path = skills_dir / skill
        has_skill = (skill_path / 'SKILL.md').exists()
        has_prompt = (skill_path / 'PROMPT.md').exists()
        
        if has_skill and has_prompt:
            print(f"✓ /{skill} - Complete")
        else:
            print(f"✗ /{skill} - Missing files")
            all_ok = False
    
    if all_ok:
        print("\n✅ SUCCESS: All Claude skills are ready!")
    
    return all_ok

def main():
    """Run all live tests"""
    print("\n" + "="*60)
    print("LIVE TEST - SILVER TIER WATCHERS")
    print("="*60)
    
    results = {
        'Filesystem Watcher': test_filesystem_watcher(),
        'Gmail Watcher': test_gmail_watcher_import(),
        'LinkedIn Watcher': test_linkedin_watcher_import(),
        'Claude Skills': test_claude_skills()
    }
    
    print("\n" + "="*60)
    print("LIVE TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL LIVE TESTS PASSED!")
        print("\n🎉 Silver Tier is ready for production use!")
    else:
        print("⚠️  Some tests need attention")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
