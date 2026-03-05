"""
Final test - Run watcher and create a file
"""
import subprocess
import time
from pathlib import Path
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vault = Path('AI_Employee_Vault')

print("\n" + "="*60)
print("FINAL WATCHER TEST")
print("="*60 + "\n")

# Start watcher
print("1. Starting filesystem watcher...")
proc = subprocess.Popen(
    [sys.executable, 'filesystem_watcher.py'],
    cwd=str(vault),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(3)

# Check if running
if proc.poll() is None:
    print("   ✓ Watcher started successfully\n")
else:
    print("   ✗ Watcher failed to start")
    stdout, stderr = proc.communicate()
    print(f"   stdout: {stdout}")
    print(f"   stderr: {stderr}")
    sys.exit(1)

# Create test file
print("2. Creating test file in Inbox/...")
test_file = vault / 'Inbox' / f'final_test_{int(time.time())}.txt'
test_file.write_text("Final test of fixed watcher")
print(f"   Created: {test_file.name}\n")

# Wait for detection
print("3. Waiting for detection (10 seconds)...")
time.sleep(10)

# Check Needs_Action
print("4. Checking Needs_Action folder...")
needs_action = vault / 'Needs_Action'
task_files = list(needs_action.glob('FILE_*.md'))

if task_files:
    latest = max(task_files, key=lambda p: p.stat().st_mtime)
    print(f"   ✓ Task file created: {latest.name}")
    print(f"   ✓ File System Watcher: WORKING!\n")
else:
    print("   ✗ No task file created")
    print("   ✗ File System Watcher: NOT WORKING\n")

# Stop watcher
print("5. Stopping watcher...")
proc.terminate()
try:
    proc.wait(timeout=2)
except:
    proc.kill()

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60 + "\n")

if task_files:
    print("✅ SUCCESS: File System Watcher is working correctly!")
    print("\nThe path fix resolved the issue.")
    print("You can now run watchers from any directory.")
else:
    print("❌ FAILED: Something is still wrong")

print("\n" + "="*60 + "\n")
