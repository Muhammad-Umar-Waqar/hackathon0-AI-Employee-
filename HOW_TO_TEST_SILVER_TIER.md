# 🚀 How to Use & Test Your Silver Tier AI Employee

**Quick Start Guide** - Get your AI Employee running in 5 minutes!

---

## 📋 Prerequisites Check

Before starting, verify everything is ready:

```bash
cd D:\giaic\hackathon-0
python test_silver_tier.py
```

**Expected Output:**
```
✅ ALL TESTS PASSED - Silver Tier Ready!
```

---

## 🎯 STEP 1: Start the Watchers

You need to start 3 watchers in separate terminal windows.

### **Terminal 1 - File System Watcher**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
python filesystem_watcher.py
```

**Expected Output:**
```
File System Watcher started. Monitoring: AI_Employee_Vault\Inbox
Press Ctrl+C to stop...
```

**What it does:** Watches for files dropped in `Inbox/` folder

---

### **Terminal 2 - Gmail Watcher**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
python gmail_watcher.py
```

**Expected Output:**
```
✅ Gmail Watcher started successfully!
📬 Monitoring for urgent messages...
⏱️  Check interval: 120 seconds
```

**What it does:** Checks your Gmail every 2 minutes for important emails

---

### **Terminal 3 - LinkedIn Watcher**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
python linkedin_watcher.py
```

**Expected Output:**
```
✅ LinkedIn Watcher started!
📬 Monitoring for important notifications...
⏱️  Check interval: 300 seconds
```

**What it does:** Monitors LinkedIn for messages and notifications

---

## 🧪 STEP 2: Test Each Watcher

### **Test 1: File System Watcher**

1. **Create a test file:**
   ```bash
   echo "This is a test document for AI Employee processing" > AI_Employee_Vault/Inbox/test_file.txt
   ```

2. **Wait 10 seconds**

3. **Check Needs_Action folder:**
   ```bash
   dir AI_Employee_Vault\Needs_Action
   ```

4. **You should see:** A new file like `FILE_2026-03-03_test_file.md`

5. **Read the task file:**
   ```bash
   type AI_Employee_Vault\Needs_Action\FILE_*.md
   ```

✅ **SUCCESS:** File System Watcher is working!

---

### **Test 2: Gmail Watcher**

1. **Send yourself an email** with:
   - **Subject:** `URGENT: Test Email`
   - **Body:** `This is a test for my AI Employee`

2. **Wait up to 2 minutes**

3. **Check Needs_Action folder:**
   ```bash
   dir AI_Employee_Vault\Needs_Action
   ```

4. **You should see:** A new file like `EMAIL_2026-03-03_URGENT_Test_Email.md`

5. **Read the email task:**
   ```bash
   type AI_Employee_Vault\Needs_Action\EMAIL_*.md
   ```

✅ **SUCCESS:** Gmail Watcher is working!

---

### **Test 3: LinkedIn Watcher** (Optional)

LinkedIn testing requires actual LinkedIn activity. The watcher will automatically detect:
- New messages
- Connection requests
- Comments on your posts
- Mentions

**Just leave it running** and it will create task files when activity occurs.

---

## 🤖 STEP 3: Process Tasks with Claude

Now that you have tasks in `Needs_Action/`, let's process them!

### **Open a 4th Terminal:**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
claude /process-tasks
```

**What Claude will do:**
1. Read all task files in `Needs_Action/`
2. Analyze each task
3. Create plans for complex tasks
4. Execute simple tasks
5. Create approval requests for sensitive actions
6. Move completed tasks to `Done/`
7. Update `Dashboard.md`

---

## 📝 STEP 4: Test Specific Skills

### **Test: Create Plans**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
claude /create-plans
```

**What it does:** Analyzes tasks and creates detailed `Plan.md` files in `Plans/` folder

---

### **Test: Approval Workflow**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
claude /approval-workflow
```

**What it does:** 
- Checks for actions needing approval
- Creates approval requests in `Pending_Approval/`
- Processes approved actions from `Approved/`

---

### **Test: LinkedIn Post**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
claude /linkedin-post "Excited to share my AI Employee project! Building autonomous automation with Claude Code and Obsidian. #AI #Automation"
```

**What it does:** 
- Creates a post record in `Plans/Social/`
- Posts to LinkedIn (or creates approval request)
- Logs the post

---

### **Test: Weekly Briefing**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
claude /weekly-briefing
```

**What it does:**
- Analyzes completed tasks
- Generates CEO Briefing in `Briefings/`
- Includes revenue, bottlenecks, suggestions
- Updates Dashboard

---

### **Test: Orchestrator**

```bash
cd D:\giaic\hackathon-0\AI_Employee_Vault
claude /orchestrator-advanced --status
```

**What it does:** Shows system status, scheduled tasks, health check

---

## 🎬 COMPLETE DEMO WORKFLOW

Here's a complete end-to-end demo:

### **Scenario: Client Email → Invoice → Send**

1. **Start all watchers** (3 terminals)

2. **Send email to yourself:**
   - Subject: `URGENT: Need Invoice`
   - Body: `Please send me the invoice for January services, $1500`

3. **Wait for Gmail Watcher** (2 minutes)
   - Check: `Needs_Action/` should have new email task

4. **Process with Claude:**
   ```bash
   claude /process-tasks
   ```

5. **Claude will:**
   - Read the email
   - Create a plan in `Plans/`
   - Create approval request in `Pending_Approval/`

6. **Approve the action:**
   ```bash
   # Move the approval file from Pending_Approval/ to Approved/
   move AI_Employee_Vault\Pending_Approval\*.md AI_Employee_Vault\Approved\
   ```

7. **Process the approval:**
   ```bash
   claude /approval-workflow
   ```

8. **Claude will:**
   - Execute the approved action
   - Log it
   - Move to `Done/`

9. **Check Dashboard:**
   ```bash
   type AI_Employee_Vault\Dashboard.md
   ```

✅ **DEMO COMPLETE!**

---

## 📊 Monitor Activity

### **View Logs:**

```bash
# Gmail activity
type AI_Employee_Vault\Logs\gmail_watcher.log

# File system activity
type AI_Employee_Vault\Logs\filesystem_watcher.log

# All logs
dir AI_Employee_Vault\Logs\
```

### **Check Task Queues:**

```bash
# Pending tasks
dir AI_Employee_Vault\Needs_Action\

# Completed tasks
dir AI_Employee_Vault\Done\

# Awaiting approval
dir AI_Employee_Vault\Pending_Approval\
```

### **View Dashboard:**

```bash
type AI_Employee_Vault\Dashboard.md
```

---

## 🛑 Stop Watchers

When done testing:

**Press `Ctrl+C`** in each terminal running watchers

---

## 🎯 Quick Test Commands

### **1-Minute Test:**

```bash
# Drop a file
echo "Test" > AI_Employee_Vault\Inbox\quick_test.txt

# Wait 10 seconds

# Check if detected
dir AI_Employee_Vault\Needs_Action\

# Process with Claude
claude /process-tasks

# Check result
dir AI_Employee_Vault\Done\
```

---

## ✅ Success Indicators

You'll know everything is working when:

1. ✅ Dropping a file creates a task in `Needs_Action/`
2. ✅ Gmail emails create tasks (within 2 minutes)
3. ✅ Claude processes tasks when you run `/process-tasks`
4. ✅ Completed tasks move to `Done/`
5. ✅ Dashboard.md gets updated
6. ✅ Logs show activity

---

## 🐛 Troubleshooting

### **Watcher not detecting files?**

```bash
# Check if watcher is running
# Look for the Python process in Task Manager

# Restart watcher
python filesystem_watcher.py
```

### **Gmail not working?**

```bash
# Check if token exists
dir credentials\gmail-token.json

# If missing, re-authenticate
python generate_oauth_url.py
```

### **Claude skills not found?**

```bash
# Make sure you're in the right directory
cd D:\giaic\hackathon-0\AI_Employee_Vault

# Verify skills exist
dir ..\.claude\skills\
```

---

## 📚 Next Steps

After basic testing:

1. **Set up scheduling** (Task Scheduler / cron)
2. **Customize Company_Handbook.md** rules
3. **Add your business goals** to `Business_Goals.md`
4. **Test the weekly briefing** with real data
5. **Configure LinkedIn posting** for your business

---

## 🎉 You're Ready!

Your Silver Tier AI Employee is fully functional and ready for:
- ✅ Live demonstrations
- ✅ Real email processing
- ✅ Task automation
- ✅ LinkedIn posting
- ✅ Approval workflows
- ✅ Weekly business briefings

**Happy automating!** 🚀

---

**For detailed documentation, see:**
- `SILVER_TIER_VERIFICATION.md` - Complete verification report
- `WATCHERS_SETUP.md` - Detailed setup guide
- `SILVER_TIER_README.md` - Full implementation guide
