"""
File System Watcher - Monitors Inbox folder for new files
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from datetime import datetime
import shutil
import logging

class DropFolderHandler(FileSystemEventHandler):
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.processed_files = set()

        # Setup logging
        self.logger = logging.getLogger('FileSystemWatcher')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.vault_path / 'Logs' / 'filesystem_watcher.log'),
                logging.StreamHandler()
            ]
        )

    def on_created(self, event):
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Avoid processing the same file multiple times
        if source in self.processed_files:
            return

        # Skip temporary files and hidden files
        if source.name.startswith('.') or source.name.startswith('~'):
            return

        self.logger.info(f'New file detected: {source.name}')

        try:
            # Wait a moment to ensure file is fully written
            import time
            time.sleep(1)

            # Create action file in Needs_Action
            self.create_action_file(source)
            self.processed_files.add(source)

        except Exception as e:
            self.logger.error(f'Error processing {source.name}: {e}')

    def create_action_file(self, source: Path):
        """Create a markdown file in Needs_Action describing the new file"""
        timestamp = datetime.now().isoformat()

        # Get file info
        file_size = source.stat().st_size
        file_ext = source.suffix

        content = f"""---
type: file_drop
original_name: {source.name}
size: {file_size} bytes
extension: {file_ext}
detected: {timestamp}
status: pending
priority: normal
---

## New File Detected

A new file has been dropped in the Inbox folder and needs processing.

### File Details
- **Name**: {source.name}
- **Size**: {file_size} bytes
- **Type**: {file_ext}
- **Location**: {source}

### Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or categorize the file
- [ ] Move to Done when complete

### Notes
Add any processing notes here.
"""

        # Create action file
        action_filename = f'FILE_{timestamp.replace(":", "-")}_{source.stem}.md'
        action_path = self.needs_action / action_filename
        action_path.write_text(content, encoding='utf-8')

        self.logger.info(f'Created action file: {action_filename}')
        return action_path

def run_watcher(vault_path: str):
    """Start the file system watcher"""
    vault = Path(vault_path)
    inbox = vault / 'Inbox'

    # Ensure inbox exists
    inbox.mkdir(exist_ok=True)

    event_handler = DropFolderHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, str(inbox), recursive=False)
    observer.start()

    print(f"File System Watcher started. Monitoring: {inbox}")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nWatcher stopped.")

    observer.join()

if __name__ == '__main__':
    import sys

    # Get vault path from command line or use default
    vault_path = sys.argv[1] if len(sys.argv) > 1 else './AI_Employee_Vault'
    run_watcher(vault_path)
