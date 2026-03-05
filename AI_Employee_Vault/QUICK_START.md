# 🚀 Quick Start - Silver Tier Watchers

## ✅ What's Ready

All watcher scripts and skills are created and ready to use!

## ⚠️ What You Need to Do

### 1. Install Python Dependencies

```bash
cd AI_Employee_Vault
pip install -r requirements.txt
```

This will install:
- `watchdog` - File system monitoring (✅ Already installed)
- `google-api-python-client` - Gmail API (❌ Need to install)
- `google-auth-httplib2` - Google authentication (❌ Need to install)
- `google-auth-oauthlib` - Google OAuth (❌ Need to install)
- `playwright` - Browser automation (❌ Need to install)

### 2. Install Playwright Browsers

After installing playwright:

```bash
playwright install chromium
```

### 3. Place Your Gmail Credentials

You mentioned you already have `credentials.json`. Place it here:

```
credentials/credentials.json
```

**Full Path:** `D:\giaic\hackathon-0\credentials\credentials.json`

**Note:** The `credentials/` folder is at the **project root**, not inside `AI_Employee_Vault/`. This keeps credentials separate from vault data and is properly ignored by git.

### 4. First Time Gmail Authentication

```bash
cd AI_Employee_Vault
python gmail_watcher.py
```

- Browser will open
- Sign in with your Google account
- Grant Gmail API permissions
- Token will be saved automatically

### 5. First Time LinkedIn Setup

```bash
cd AI_Employee_Vault
python linkedin_watcher.py
```

First run may require manual login. Session will be saved.

---

## Start Using

### Start All Watchers (3 terminals)

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

### Process Tasks with Claude

```bash
claude /process-tasks
```

### Generate Weekly Briefing

```bash
claude /weekly-briefing
```

### Post to LinkedIn

```bash
claude /linkedin-post "Your business update here"
```

---

## Test Everything

```bash
python test_silver_tier.py
```

All tests should pass after installing dependencies.

---

## Installation Commands Summary

```bash
# Navigate to vault
cd D:\giaic\hackathon-0\AI_Employee_Vault

# Install all dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Test setup
python test_silver_tier.py

# Start watchers
python gmail_watcher.py
python linkedin_watcher.py
python filesystem_watcher.py
```

---

## Troubleshooting

### "credentials.json NOT found"
```
Solution: Place your credentials.json file in:
D:\giaic\hackathon-0\credentials\credentials.json
```

### "google-api-python-client NOT installed"
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### "playwright NOT installed"
```bash
pip install playwright
playwright install chromium
```

---

## Documentation

- `SILVER_TIER_WATCHERS_COMPLETE.md` - Complete guide
- `WATCHERS_SETUP.md` - Detailed setup instructions
- `SILVER_TIER_README.md` - Full implementation guide
- `Company_Handbook.md` - AI behavior rules (v2.0)

---

**Ready to start! 🎉**
