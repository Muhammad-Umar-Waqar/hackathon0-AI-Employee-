"""
Simple Orchestrator - Coordinates the AI Employee system
"""
import subprocess
import sys
from pathlib import Path
import time

class Orchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'

    def check_for_tasks(self):
        """Check if there are tasks in Needs_Action folder"""
        tasks = list(self.needs_action.glob('*.md'))
        return len(tasks)

    def run_watcher(self):
        """Start the file system watcher"""
        print("Starting File System Watcher...")
        watcher_script = self.vault_path / 'filesystem_watcher.py'
        subprocess.Popen([sys.executable, str(watcher_script), str(self.vault_path)])
        print("✓ Watcher started")

    def display_status(self):
        """Display current system status"""
        task_count = self.check_for_tasks()
        print("\n" + "="*50)
        print("AI EMPLOYEE - BRONZE TIER")
        print("="*50)
        print(f"Vault Location: {self.vault_path}")
        print(f"Tasks Pending: {task_count}")
        print("\nFolders:")
        print(f"  - Inbox: {self.vault_path / 'Inbox'}")
        print(f"  - Needs_Action: {self.needs_action}")
        print(f"  - Done: {self.vault_path / 'Done'}")
        print("\nTo process tasks, run:")
        print("  claude /process-tasks")
        print("\nOr manually:")
        print('  claude "Process all tasks in AI_Employee_Vault/Needs_Action"')
        print("="*50 + "\n")

def main():
    vault_path = Path(__file__).parent / 'AI_Employee_Vault'

    if not vault_path.exists():
        print(f"Error: Vault not found at {vault_path}")
        sys.exit(1)

    orchestrator = Orchestrator(str(vault_path))
    orchestrator.display_status()

    print("Options:")
    print("1. Start watcher only")
    print("2. Check status")
    print("3. Exit")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == '1':
        orchestrator.run_watcher()
        print("\nWatcher is running in the background.")
        print("Drop files in Inbox/ folder to create tasks.")
        print("Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping...")
    elif choice == '2':
        orchestrator.display_status()
    else:
        print("Goodbye!")

if __name__ == '__main__':
    main()
