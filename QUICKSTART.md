# Quick Start Guide - Bronze Tier AI Employee

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd AI_Employee_Vault
pip install -r requirements.txt
```

### Step 2: Start the System

**Option A: Using the Orchestrator (Recommended)**
```bash
python orchestrator.py
```
Then select option 1 to start the watcher.

**Option B: Manual Start**
```bash
# Terminal 1: Start the watcher
python AI_Employee_Vault/filesystem_watcher.py

# Terminal 2: Process tasks when ready
claude /process-tasks
```

### Step 3: Test the System

1. Drop a file in `AI_Employee_Vault/Inbox/`
2. The watcher will automatically detect it and create a task in `Needs_Action/`
3. Run `claude /process-tasks` to process the task
4. Check `Dashboard.md` for updates
5. Find completed task in `Done/` folder

## Example Workflow

```bash
# Create a test file
echo "Meeting notes for Q1 planning" > AI_Employee_Vault/Inbox/meeting_notes.txt

# The watcher detects it automatically (if running)
# A task file appears in Needs_Action/

# Process with Claude Code
claude /process-tasks

# Check results
cat AI_Employee_Vault/Dashboard.md
```

## What Happens Behind the Scenes

1. **File Drop**: You drop `meeting_notes.txt` in Inbox
2. **Detection**: Watcher creates `FILE_2026-02-19_meeting_notes.md` in Needs_Action
3. **Processing**: Claude reads the task, analyzes the file
4. **Action**: Claude processes according to Company_Handbook.md rules
5. **Completion**: Task moved to Done/, Dashboard updated, action logged

## Customization

### Modify AI Behavior
Edit `AI_Employee_Vault/Company_Handbook.md` to change:
- Task processing rules
- Approval requirements
- Communication style
- Error handling

### View Dashboard
Open `AI_Employee_Vault/Dashboard.md` in:
- Obsidian (for rich GUI experience)
- Any text editor
- VS Code with Markdown preview

## Troubleshooting

**Watcher not starting?**
```bash
# Check if watchdog is installed
pip list | grep watchdog

# Reinstall if needed
pip install watchdog
```

**Claude Code not finding tasks?**
```bash
# Make sure you're in the project root
cd /d/giaic/hackathon-0

# Check if tasks exist
ls AI_Employee_Vault/Needs_Action/
```

**Want to stop the watcher?**
Press `Ctrl+C` in the terminal running the watcher.

## Next Steps

Once comfortable with Bronze Tier:
- Add Gmail watcher (Silver Tier)
- Add WhatsApp watcher (Silver Tier)
- Implement MCP servers for external actions (Silver/Gold)
- Add business audit features (Gold)
- Deploy to cloud for 24/7 operation (Platinum)

## Support

- Check `AI_Employee_Vault/Logs/` for error messages
- Review the main README.md for detailed documentation
- Join the Wednesday Research Meetings for help
