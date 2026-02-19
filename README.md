# AI Employee - Bronze Tier Implementation

A local-first AI Employee system using Claude Code and Obsidian for autonomous task processing.

## Overview

This is a Bronze Tier implementation of the Personal AI Employee Hackathon. It provides:
- Obsidian vault for knowledge management and task tracking
- File system watcher that monitors the Inbox folder
- Claude Code integration via Agent Skills
- Automated task processing workflow

## Architecture

```
AI_Employee_Vault/
├── Inbox/              # Drop files here for processing
├── Needs_Action/       # Tasks waiting to be processed
├── Done/               # Completed tasks
├── Plans/              # Task execution plans
├── Logs/               # System logs
├── Pending_Approval/   # Tasks requiring human approval
├── Approved/           # Approved tasks
├── Rejected/           # Rejected tasks
├── Dashboard.md        # Real-time status dashboard
└── Company_Handbook.md # Rules and guidelines
```

## Prerequisites

- Python 3.13 or higher
- Claude Code CLI installed
- Obsidian (optional, for GUI viewing)

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd AI_Employee_Vault
pip install -r requirements.txt
```

### 2. Start the File System Watcher

The watcher monitors the Inbox folder for new files:

```bash
python filesystem_watcher.py
```

This will run continuously and create task files in `Needs_Action/` whenever you drop files in `Inbox/`.

### 3. Process Tasks with Claude Code

Use the Claude Code skill to process tasks:

```bash
claude /process-tasks
```

Or manually invoke Claude Code to process tasks:

```bash
claude "Process all tasks in AI_Employee_Vault/Needs_Action folder according to Company_Handbook.md rules"
```

## How It Works

### Workflow

1. **File Detection**: Drop a file in `Inbox/` folder
2. **Task Creation**: File system watcher detects the file and creates a task in `Needs_Action/`
3. **Task Processing**: Run `/process-tasks` skill in Claude Code
4. **Execution**: Claude reads the task, follows Company_Handbook rules, and executes
5. **Completion**: Task moved to `Done/`, Dashboard updated, action logged

### Example Usage

```bash
# Terminal 1: Start the watcher
python filesystem_watcher.py

# Terminal 2: Drop a test file
echo "Test document" > Inbox/test.txt

# Terminal 3: Process with Claude Code
claude /process-tasks
```

## Bronze Tier Requirements ✓

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (file system monitoring)
- ✅ Claude Code successfully reading from and writing to the vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ All AI functionality implemented as Agent Skills

## Features

### File System Watcher
- Monitors `Inbox/` folder continuously
- Creates detailed task files for each new file
- Logs all activity
- Handles errors gracefully

### Claude Code Integration
- Custom `/process-tasks` skill
- Reads Company_Handbook.md for rules
- Updates Dashboard.md automatically
- Moves completed tasks to Done/
- Creates logs for all actions

### Safety Features
- Human-in-the-loop for sensitive actions
- Approval workflow via Pending_Approval folder
- Comprehensive logging
- No automatic file deletion

## Configuration

### Company_Handbook.md

Edit this file to customize AI Employee behavior:
- Communication style
- Task processing rules
- Approval requirements
- Error handling

### Dashboard.md

Automatically updated by the AI Employee with:
- System status
- Recent activity
- Task statistics
- Quick links

## Logs

All activity is logged to `Logs/` folder:
- `filesystem_watcher.log` - File detection events
- Task-specific logs created by Claude Code

## Troubleshooting

### Watcher not detecting files
- Ensure you're dropping files in the `Inbox/` folder
- Check `Logs/filesystem_watcher.log` for errors
- Verify Python dependencies are installed

### Claude Code not processing tasks
- Ensure you're running Claude Code from the project root
- Check that task files exist in `Needs_Action/`
- Verify the `/process-tasks` skill is properly installed

### Permission errors
- Ensure the vault folders have write permissions
- Check that log files can be created

## Next Steps (Silver/Gold Tier)

To upgrade to Silver or Gold tier:
- Add Gmail watcher for email monitoring
- Add WhatsApp watcher for message monitoring
- Implement MCP servers for external actions
- Add scheduling via cron/Task Scheduler
- Implement Ralph Wiggum loop for autonomous operation
- Add business audit and CEO briefing features

## Security Notes

- All data stays local (local-first architecture)
- No external API calls in Bronze tier
- Sensitive actions require approval
- Comprehensive audit logging

## License

This is a hackathon project for educational purposes.

---

**Built for**: Personal AI Employee Hackathon 0
**Tier**: Bronze
**Date**: 2026-02-19
