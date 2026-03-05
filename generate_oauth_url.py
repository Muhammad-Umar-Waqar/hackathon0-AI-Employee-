"""
Generate fresh Gmail OAuth URL
"""
from pathlib import Path
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add vault to path
sys.path.insert(0, 'AI_Employee_Vault')

from gmail_watcher import GmailWatcher

print("\n" + "="*60)
print("GMAIL OAUTH URL GENERATOR")
print("="*60)

vault_path = Path('AI_Employee_Vault')
watcher = GmailWatcher(str(vault_path))

print(f"\nCredentials file: {watcher.credentials_file}")
print(f"Credentials exists: {watcher.credentials_file.exists()}")

if not watcher.credentials_file.exists():
    print("\nERROR: credentials.json not found!")
    print(f"Expected at: {watcher.credentials_file}")
    print("\nPlease place your credentials.json file in:")
    print("D:\\giaic\\hackathon-0\\credentials\\credentials.json")
    sys.exit(1)

print("\nStarting OAuth flow...")
print("\nCOPY AND OPEN THIS URL IN YOUR BROWSER:\n")
print("-"*60)

# Authenticate (this will print the OAuth URL)
result = watcher.authenticate()

print("-"*60)

if result:
    print("\nOAuth successful!")
    print("\nNext steps:")
    print("1. The token has been saved automatically")
    print("2. Run: python AI_Employee_Vault/gmail_watcher.py")
else:
    print("\nOAuth needs browser completion")
    print("\nInstructions:")
    print("1. Copy the URL above")
    print("2. Open in your browser")
    print("3. Sign in with Google")
    print("4. Grant permissions")
    print("5. You'll be redirected - the watcher will handle the rest")

print("\n" + "="*60 + "\n")
