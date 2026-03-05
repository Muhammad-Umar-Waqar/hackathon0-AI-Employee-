# Silver Tier Watchers - Setup Guide

## Quick Setup

### Step 1: Install Python Dependencies

```bash
cd AI_Employee_Vault
pip install -r requirements.txt
```

### Step 2: Setup Gmail Credentials

1. **Place your credentials.json file:**
   ```
   Copy your credentials.json to: AI_Employee_Vault/credentials/credentials.json
   ```

2. **Verify Gmail API is enabled:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Select your project
   - Navigate to APIs & Services > Library
   - Search for "Gmail API" and ensure it's enabled

3. **Configure OAuth consent screen:**
   - Go to APIs & Services > OAuth consent screen
   - Fill in required fields (app name, user support email)
   - Add scopes: `gmail.readonly`
   - Add test users (include your Gmail address)

4. **First run authentication:**
   ```bash
   python gmail_watcher.py
   ```
   - Browser will open for OAuth authorization
   - Sign in and grant permissions
   - Token will be saved for future runs

### Step 3: Setup LinkedIn (Optional)

LinkedIn uses Playwright for browser automation:

```bash
# Install Playwright
pip install playwright

# Install browser binaries
playwright install chromium
```

**First time LinkedIn login:**
- Run the watcher once with headless=False
- Login to LinkedIn manually
- Session will be saved for future runs

### Step 4: Start Watchers

#### Start Gmail Watcher
```bash
cd AI_Employee_Vault
python gmail_watcher.py
```

#### Start LinkedIn Watcher
```bash
cd AI_Employee_Vault
python linkedin_watcher.py
```

#### Start File System Watcher
```bash
cd AI_Employee_Vault
python filesystem_watcher.py
```

### Step 5: Run Multiple Watchers

Open multiple terminal windows:

**Terminal 1:**
```bash
python filesystem_watcher.py
```

**Terminal 2:**
```bash
python gmail_watcher.py
```

**Terminal 3:**
```bash
python linkedin_watcher.py
```

Or use the orchestrator:
```bash
python orchestrator.py
```

## Configuration

### Gmail Watcher Settings

Edit `gmail_watcher.py` to customize:

```python
# Check interval (default: 2 minutes)
check_interval = 120

# Keywords to detect
keywords = [
    'urgent', 'asap', 'invoice', 'payment', 'help',
    'deadline', 'important', 'action required', 'reply needed'
]

# Credentials file location
credentials_file = "credentials.json"
```

### LinkedIn Watcher Settings

Edit `linkedin_watcher.py` to customize:

```python
# Check interval (default: 5 minutes)
check_interval = 300

# Keywords to detect
keywords = [
    'message', 'connection request', 'comment', 'mention',
    'job opportunity', 'hiring', 'partnership', 'collaboration'
]
```

## Troubleshooting

### Gmail Watcher Issues

**Error: "Credentials file not found"**
```
Solution: Place credentials.json in AI_Employee_Vault/credentials/
```

**Error: "Token expired"**
```
Solution: Delete token.json and re-authenticate
  rm AI_Employee_Vault/credentials/token.json
  python gmail_watcher.py
```

**Error: "Gmail API not enabled"**
```
Solution: Enable Gmail API in Google Cloud Console
```

### LinkedIn Watcher Issues

**Error: "Playwright not installed"**
```
Solution: 
  pip install playwright
  playwright install chromium
```

**Error: "Login failed"**
```
Solution: 
1. Run with headless=False first time
2. Login manually in browser
3. Session will be saved
```

## Testing

### Test Gmail Watcher

1. Send yourself an email with subject "URGENT: Test"
2. Watcher should detect it within 2 minutes
3. Check `Needs_Action/` folder for new EMAIL_*.md file

### Test LinkedIn Watcher

1. Wait for a LinkedIn notification or message
2. Watcher should detect it within 5 minutes
3. Check `Needs_Action/` folder for new LINKEDIN_*.md file

### Test File System Watcher

1. Drop a file in `Inbox/` folder
2. Watcher should detect it within 10 seconds
3. Check `Needs_Action/` folder for new FILE_*.md file

## Logs

All watchers log to `Logs/` folder:

- `gmail_watcher.log` - Gmail activity
- `linkedin_watcher.log` - LinkedIn activity
- `filesystem_watcher.log` - File system activity

View logs:
```bash
# View latest Gmail logs
tail -f AI_Employee_Vault/Logs/gmail_watcher.log

# View all logs
ls AI_Employee_Vault/Logs/
```

## Security Notes

- **Never commit credentials**: credentials.json and token.json are in .gitignore
- **Keep session files private**: LinkedIn session contains login cookies
- **Rotate credentials regularly**: Update Gmail credentials every 3-6 months
- **Use test users**: Only add trusted emails to OAuth test users

## Next Steps

After watchers are running:

1. **Process tasks with Claude:**
   ```bash
   claude /process-tasks
   ```

2. **Check created action files:**
   ```bash
   ls AI_Employee_Vault/Needs_Action/
   ```

3. **Generate weekly briefing:**
   ```bash
   claude /weekly-briefing
   ```

4. **Post to LinkedIn:**
   ```bash
   claude /linkedin-post "Your content here"
   ```

---

**Silver Tier Watchers Complete** ✅

For more information, see:
- SILVER_TIER_README.md - Full implementation guide
- Company_Handbook.md - AI behavior rules
- README.md - Project overview
