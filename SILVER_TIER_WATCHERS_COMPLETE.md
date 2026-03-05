# Silver Tier Watchers - Complete Implementation

## ✅ Status: COMPLETE

**Date:** 2026-03-02  
**Tier:** Silver  
**Focus:** Gmail + LinkedIn Watchers

---

## What's Been Built

### 1. Gmail Watcher (gmail_watcher.py)

**Features:**
- ✅ Monitors Gmail for urgent/important messages
- ✅ Keyword detection (urgent, invoice, payment, etc.)
- ✅ Uses your existing credentials.json file
- ✅ OAuth 2.0 authentication with token persistence
- ✅ Creates action files in Needs_Action/
- ✅ Configurable check interval (default: 2 minutes)
- ✅ Comprehensive logging to gmail_watcher.log
- ✅ Priority detection (high/normal)
- ✅ Email body extraction (plain text + HTML)

**Location:** `AI_Employee_Vault/gmail_watcher.py`

**Credentials Setup:**
```
Place your credentials.json in:
AI_Employee_Vault/credentials/credentials.json
```

**First Run:**
```bash
cd AI_Employee_Vault
python gmail_watcher.py
```
- Browser opens for OAuth authorization
- Token saved to `credentials/token.json`
- Subsequent runs use saved token

### 2. LinkedIn Watcher (linkedin_watcher.py)

**Features:**
- ✅ Monitors LinkedIn notifications
- ✅ Monitors LinkedIn messages
- ✅ Keyword detection for important updates
- ✅ Playwright-based browser automation
- ✅ Persistent session (login once)
- ✅ Creates action files in Needs_Action/
- ✅ Configurable check interval (default: 5 minutes)
- ✅ Post to LinkedIn capability
- ✅ Creates post records in Plans/Social/

**Location:** `AI_Employee_Vault/linkedin_watcher.py`

**Setup:**
```bash
# Install Playwright
pip install playwright
playwright install chromium

# Run watcher
python linkedin_watcher.py
```

### 3. File System Watcher (filesystem_watcher.py)

**Features:**
- ✅ Monitors Inbox folder for file drops
- ✅ Creates task files automatically
- ✅ Fast detection (<10 seconds)
- ✅ Comprehensive logging

**Already working from Bronze Tier** ✅

---

## Quick Start Guide

### Step 1: Install Dependencies

```bash
cd AI_Employee_Vault
pip install -r requirements.txt
```

### Step 2: Setup Gmail Credentials

1. **Place your credentials.json:**
   ```bash
   # Create credentials directory (if not exists)
   mkdir AI_Employee_Vault\credentials
   
   # Copy your credentials.json
   copy path\to\your\credentials.json AI_Employee_Vault\credentials\
   ```

2. **First authentication:**
   ```bash
   python gmail_watcher.py
   ```
   - Browser opens automatically
   - Sign in with your Google account
   - Grant Gmail API permissions
   - Token saved for future runs

### Step 3: Setup LinkedIn (Optional)

```bash
# Install Playwright
pip install playwright
playwright install chromium

# First run (login manually)
python linkedin_watcher.py
```

### Step 4: Start All Watchers

**Option A: Separate Terminals**

Terminal 1:
```bash
python filesystem_watcher.py
```

Terminal 2:
```bash
python gmail_watcher.py
```

Terminal 3:
```bash
python linkedin_watcher.py
```

**Option B: Use Orchestrator**
```bash
python orchestrator.py
```

---

## Testing

### Run Test Suite

```bash
python test_silver_tier.py
```

This will check:
- ✅ All dependencies installed
- ✅ Vault structure correct
- ✅ Watcher scripts valid
- ✅ Claude skills installed
- ✅ Logging system working
- ✅ Functional test passed

### Test Gmail Watcher

1. Send yourself an email with subject: "URGENT: Test Message"
2. Wait up to 2 minutes
3. Check `Needs_Action/` folder
4. You should see: `EMAIL_*.md` file

### Test LinkedIn Watcher

1. Wait for a LinkedIn notification or message
2. Wait up to 5 minutes
3. Check `Needs_Action/` folder
4. You should see: `LINKEDIN_*.md` file

### Test File System Watcher

1. Drop a file in `Inbox/` folder
2. Wait 10 seconds
3. Check `Needs_Action/` folder
4. You should see: `FILE_*.md` file

---

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     WATCHERS LAYER                       │
├─────────────────────────────────────────────────────────┤
│  Gmail Watcher  │  LinkedIn Watcher  │  File Watcher   │
│  (2 min)        │  (5 min)           │  (10 sec)       │
└────────┬────────┴─────────┬──────────┴────────┬────────┘
         │                  │                   │
         ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│              Needs_Action/ Folder                        │
│  (Action files created by watchers)                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   Claude Code Skills    │
              │   /process-tasks        │
              │   /create-plans         │
              │   /approval-workflow    │
              │   /linkedin-post        │
              │   /weekly-briefing      │
              └─────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │      Actions Taken      │
              │  - Plans created        │
              │  - Approvals requested  │
              │  - Posts published      │
              │  - Dashboard updated    │
              │  - Tasks moved to Done  │
              └─────────────────────────┘
```

### Workflow Example

**Scenario:** Client sends urgent email about invoice

1. **Gmail Watcher** detects email (within 2 min)
   - Subject contains "urgent" keyword
   - Extracts sender, subject, body
   - Creates action file in `Needs_Action/`

2. **Claude** processes via `/process-tasks`
   - Reads email details
   - Determines reply needed
   - Creates plan in `Plans/`

3. **Approval Workflow**
   - Creates approval request in `Pending_Approval/`
   - Waits for human approval

4. **Human approves**
   - Moves file to `Approved/`

5. **Claude** executes
   - Drafts email reply
   - Sends via Gmail MCP
   - Logs action
   - Moves task to `Done/`

---

## Configuration

### Gmail Watcher Settings

Edit `gmail_watcher.py`:

```python
# Check interval (seconds)
check_interval = 120  # 2 minutes

# Keywords to detect
keywords = [
    'urgent', 'asap', 'invoice', 'payment', 'help',
    'deadline', 'important', 'action required', 'reply needed'
]

# Credentials file
credentials_file = "credentials.json"
```

### LinkedIn Watcher Settings

Edit `linkedin_watcher.py`:

```python
# Check interval (seconds)
check_interval = 300  # 5 minutes

# Keywords to detect
keywords = [
    'message', 'connection request', 'comment', 'mention',
    'job opportunity', 'hiring', 'partnership', 'collaboration'
]
```

---

## Files Created

### Watcher Scripts
- ✅ `gmail_watcher.py` - Gmail monitoring
- ✅ `linkedin_watcher.py` - LinkedIn monitoring
- ✅ `filesystem_watcher.py` - File monitoring (Bronze)

### Skills (Silver Tier)
- ✅ `/create-plans` - Plan generation
- ✅ `/approval-workflow` - Approval management
- ✅ `/linkedin-post` - LinkedIn posting
- ✅ `/weekly-briefing` - CEO briefings
- ✅ `/orchestrator-advanced` - Scheduling

### Documentation
- ✅ `WATCHERS_SETUP.md` - Setup guide
- ✅ `SILVER_TIER_README.md` - Implementation guide
- ✅ `SILVER_TIER_COMPLETE.md` - Summary
- ✅ `test_silver_tier.py` - Test suite

### Configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `Company_Handbook.md v2.0` - Silver Tier rules

---

## Logs

All activity logged to `Logs/` folder:

```
AI_Employee_Vault/Logs/
├── gmail_watcher.log      # Gmail activity
├── linkedin_watcher.log   # LinkedIn activity
├── filesystem_watcher.log # File system activity
└── orchestrator.log       # Orchestration activity
```

View logs:
```bash
# Real-time Gmail logs
tail -f AI_Employee_Vault/Logs/gmail_watcher.log

# List all logs
ls AI_Employee_Vault/Logs/
```

---

## Troubleshooting

### Gmail Watcher Not Working

**Problem:** "Credentials file not found"
```
Solution:
1. Place credentials.json in AI_Employee_Vault/credentials/
2. Verify file name is exactly "credentials.json"
3. Run: python gmail_watcher.py
```

**Problem:** "Token expired"
```
Solution:
1. Delete AI_Employee_Vault/credentials/token.json
2. Run: python gmail_watcher.py
3. Re-authenticate in browser
```

**Problem:** "Gmail API not enabled"
```
Solution:
1. Go to Google Cloud Console
2. Select your project
3. APIs & Services > Library
4. Search "Gmail API" and enable
```

### LinkedIn Watcher Not Working

**Problem:** "Playwright not installed"
```
Solution:
pip install playwright
playwright install chromium
```

**Problem:** "Login failed"
```
Solution:
1. First run will fail - that's normal
2. Run with headless=False temporarily
3. Login manually in browser
4. Session saved for future runs
```

### General Issues

**Problem:** Watchers not detecting items
```
Solution:
1. Check watcher is running (look for logs)
2. Verify correct folders being monitored
3. Check keyword detection settings
4. Review log files for errors
```

---

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit credentials:**
   - `credentials.json` and `token.json` are in `.gitignore`
   - Never share these files

2. **Keep sessions private:**
   - LinkedIn session contains login cookies
   - Store securely

3. **Rotate credentials:**
   - Update Gmail credentials every 3-6 months
   - Revoke old tokens in Google Cloud Console

4. **Use test users:**
   - Only add trusted emails to OAuth test users
   - Review OAuth consent screen settings

---

## Next Steps

### Immediate Actions

1. **Run test suite:**
   ```bash
   python test_silver_tier.py
   ```

2. **Setup Gmail:**
   ```bash
   # Place credentials
   # Run watcher
   python gmail_watcher.py
   ```

3. **Process first tasks:**
   ```bash
   claude /process-tasks
   ```

### Optional Enhancements

- **Setup scheduling:** Configure Task Scheduler or cron
- **Add more keywords:** Customize detection lists
- **Create Business_Goals.md:** Define objectives
- **Test weekly briefing:** `claude /weekly-briefing`

### Upgrade to Gold Tier

Add these features:
- WhatsApp watcher
- Facebook/Instagram integration
- Twitter (X) integration
- Odoo accounting integration
- Ralph Wiggum loop for autonomy
- Error recovery systems

---

## Summary

### What You Have Now

| Component | Status | Count |
|-----------|--------|-------|
| Watchers | ✅ Complete | 3 (Gmail, LinkedIn, File) |
| Claude Skills | ✅ Complete | 6 |
| Documentation | ✅ Complete | 5 files |
| Test Suite | ✅ Complete | 1 file |
| Setup Guides | ✅ Complete | 2 files |

### Silver Tier Requirements

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| 2+ Watchers | ✅ | Gmail + LinkedIn + File |
| LinkedIn Posting | ✅ | linkedin-post skill + watcher |
| Plan Creation | ✅ | create-plans skill |
| Approval Workflow | ✅ | approval-workflow skill |
| Scheduling | ✅ | orchestrator-advanced skill |
| All as Skills | ✅ | 6 skills total |

---

**🎉 Silver Tier Watchers Complete!**

**Ready to run:**
```bash
python test_silver_tier.py  # Verify setup
python gmail_watcher.py     # Start Gmail
python linkedin_watcher.py  # Start LinkedIn
```

**For questions or issues, check:**
- `WATCHERS_SETUP.md` - Detailed setup guide
- `SILVER_TIER_README.md` - Full implementation guide
- Log files in `Logs/` folder

---

Built for: Personal AI Employee Hackathon 0  
Tier: Silver - Watchers Complete  
Date: 2026-03-02
