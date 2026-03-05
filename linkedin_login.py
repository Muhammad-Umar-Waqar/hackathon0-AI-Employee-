"""
LinkedIn Login - Saves session for LinkedIn Watcher
Run this ONCE to log in, then the watcher will work
"""
from playwright.sync_api import sync_playwright
from pathlib import Path

session_path = Path('credentials') / 'linkedin_session'

print("\n" + "="*70)
print("LINKEDIN LOGIN")
print("="*70 + "\n")

print("This will open a browser window.")
print("Please log in to LinkedIn.")
print("Once logged in, wait 5 seconds, then close the browser.\n")

try:
    with sync_playwright() as p:
        # Open browser with persistent session
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Show browser
            viewport={'width': 1280, 'height': 720}
        )
        
        page = browser.pages[0]
        
        # Go to LinkedIn
        print("Opening LinkedIn...")
        page.goto('https://www.linkedin.com/login', timeout=30000)
        
        print("\n" + "="*70)
        print("BROWSER IS OPEN")
        print("="*70)
        print("\nINSTRUCTIONS:")
        print("1. Log in to LinkedIn in the browser")
        print("2. Wait until you see your HOME feed")
        print("3. Wait 5 more seconds (session saving)")
        print("4. Close the browser window")
        print("5. This script will finish automatically")
        print("\n" + "="*70 + "\n")
        
        # Wait for user to login (max 2 minutes)
        import time
        for i in range(120):
            time.sleep(1)
            # Check if logged in (on feed page)
            if 'feed' in page.url or 'mynetwork' in page.url or 'jobs' in page.url:
                print("\n✓ Login detected!")
                print("✓ Waiting 5 seconds for session to save...")
                time.sleep(5)
                print("✓ Session saved!")
                break
        
        browser.close()
        
except Exception as e:
    print(f"\nError: {e}")
    print("\nMake sure Playwright browsers are installed:")
    print("  playwright install chromium")

print("\n" + "="*70)
print("DONE")
print("="*70 + "\n")

print(f"Session saved to: {session_path}")
print("\nNow run:")
print("  python AI_Employee_Vault/linkedin_watcher.py")
print("\n" + "="*70 + "\n")
