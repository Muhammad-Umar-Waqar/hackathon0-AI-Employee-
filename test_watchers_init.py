"""Quick test of fixed watchers"""
import sys
from pathlib import Path

# Add vault to path
sys.path.insert(0, str(Path('AI_Employee_Vault').absolute()))

# Test filesystem watcher
import filesystem_watcher
vault_path = Path('AI_Employee_Vault').absolute()
print(f"Testing filesystem watcher...")
print(f"Vault path: {vault_path}")
print(f"Inbox exists: {(vault_path / 'Inbox').exists()}")

# Test creating handler
handler = filesystem_watcher.DropFolderHandler(str(vault_path))
print("Filesystem watcher: OK")

# Test gmail watcher
import gmail_watcher
gmail = gmail_watcher.GmailWatcher(str(vault_path))
print(f"Gmail credentials: {gmail.credentials_file}")
print(f"Gmail token exists: {gmail.token_file.exists()}")
print("Gmail watcher: OK")

# Test linkedin watcher
import linkedin_watcher
linkedin = linkedin_watcher.LinkedInWatcher(str(vault_path))
print(f"LinkedIn session: {linkedin.session_path}")
print(f"Playwright available: {linkedin.playwright_available}")
print("LinkedIn watcher: OK")

print("\nAll watchers initialized successfully!")
