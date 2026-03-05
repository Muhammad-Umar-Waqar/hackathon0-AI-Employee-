# Silver Tier Implementation Guide

Complete guide for implementing and running the Silver Tier AI Employee system.

## Overview

Silver Tier builds upon Bronze Tier with:
- ✅ Two or more Watcher scripts (File System + Gmail)
- ✅ Automated LinkedIn posting for business promotion
- ✅ Claude reasoning loop that creates Plan.md files
- ✅ Human-in-the-loop approval workflow
- ✅ Weekly CEO Briefing generation
- ✅ Advanced orchestration with scheduling
- ✅ All AI functionality as Agent Skills

**Estimated Setup Time:** 20-30 hours

## Architecture

```
AI_Employee_Vault/
├── Inbox/                    # File drops
├── Needs_Action/             # Tasks to process
├── Done/                     # Completed tasks
├── Plans/                    # Execution plans
│   └── Social/               # Social media plans
├── Logs/                     # System logs
├── Pending_Approval/         # Awaiting human decision
├── Approved/                 # Approved actions
├── Rejected/                 # Rejected actions
├── Briefings/                # CEO briefings
│   └── YYYY-MM-DD_Briefing.md
├── Dashboard.md              # Real-time status
├── Company_Handbook.md       # AI behavior rules (v2.0)
├── Business_Goals.md         # Business objectives
│
├── base_watcher.py           # Base watcher class
├── filesystem_watcher.py     # File monitoring
├── gmail_watcher.py          # Gmail monitoring ⭐ NEW
└── requirements.txt          # Python dependencies

.claude/skills/
├── process-tasks/            # Bronze: Task processing
├── create-plans/             # Silver: Plan creation ⭐ NEW
├── approval-workflow/        # Silver: Approvals ⭐ NEW
├── linkedin-post/            # Silver: LinkedIn posting ⭐ NEW
├── weekly-briefing/          # Silver: CEO briefings ⭐ NEW
└── orchestrator-advanced/    # Silver: Orchestration ⭐ NEW
```

## Prerequisites

### Software Requirements
- Python 3.13 or higher
- Claude Code CLI installed
- Node.js v24+ (for MCP servers)
- Git (for version control)

### API Setup
- Google Gmail API credentials (for Gmail watcher)
- LinkedIn account (for posting)

### Python Dependencies
```bash
cd AI_Employee_Vault
pip install -r requirements.txt
```

Update `requirements.txt` to include:
```
watchdog>=2.3.0
google-api-python-client>=2.100.0
google-auth-httplib2>=0.1.0
google-auth-oauthlib>=1.1.0
```

## Setup Instructions

### Step 1: Verify Bronze Tier
Ensure Bronze Tier is complete:
- ✅ Vault structure exists
- ✅ Dashboard.md present
- ✅ Company_Handbook.md present
- ✅ filesystem_watcher.py working
- ✅ /process-tasks skill functional

### Step 2: Install Silver Tier Skills
Copy the following skills to `.claude/skills/`:
```
create-plans/
approval-workflow/
linkedin-post/
weekly-briefing/
orchestrator-advanced/
```

### Step 3: Update Company Handbook
Replace `Company_Handbook.md` with version 2.0 (Silver Tier).

### Step 4: Setup Gmail Watcher

#### 4.1 Enable Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials as `gmail-credentials.json`

#### 4.2 Configure Credentials
```bash
# Create credentials directory
mkdir -p ~/.credentials

# Move credentials file
mv ~/Downloads/gmail-credentials.json ~/.credentials/
```

#### 4.3 Test Gmail Watcher
```bash
cd AI_Employee_Vault
python gmail_watcher.py
```

First run will open browser for OAuth authorization.

### Step 5: Create Business Goals File
Create `Business_Goals.md` in vault:

```markdown
# Business Goals

---
last_updated: 2026-03-02
review_frequency: weekly
---

## Q1 2026 Objectives

### Revenue Target
- Monthly goal: $10,000
- Current MTD: $4,500

### Key Metrics to Track
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Client response time | < 24 hours | > 48 hours |
| Invoice payment rate | > 90% | < 80% |
| Software costs | < $500/month | > $600/month |
| LinkedIn posts/week | 3 | < 2 |

### Active Projects
1. Project Alpha - Due Jan 15 - Budget $2,000
2. Project Beta - Due Jan 30 - Budget $3,500

### Subscription Audit Rules
Flag for review if:
- No login in 30 days
- Cost increased > 20%
- Duplicate functionality with another tool
```

### Step 6: Create Required Folders
```bash
cd AI_Employee_Vault
mkdir -p Briefings Plans/Social
```

### Step 7: Update Dashboard
Update `Dashboard.md` to include Silver Tier features:

```markdown
# AI Employee Dashboard

---
last_updated: 2026-03-02
status: active
tier: Silver
---

## System Status
- **AI Employee**: ✅ Active (Silver Tier)
- **Watchers Running**: File System, Gmail
- **Pending Tasks**: 0
- **Pending Approvals**: 0

## Quick Stats
- **Tasks Completed Today**: 0
- **Tasks Pending**: 0
- **Posts This Week**: 0/3
- **Success Rate**: 100%

## Scheduled Tasks
- **Daily Processing**: Mon-Fri 8:00 AM
- **LinkedIn Posts**: Tue, Thu 10:00 AM
- **Weekly Briefing**: Monday 7:00 AM

## Recent Activity
- [2026-03-02] 🚀 Silver Tier initialized
- [2026-03-02] 📧 Gmail watcher configured
- [2026-03-02] 📝 New skills installed

## Folders
- `/Inbox` - Drop files here
- `/Needs_Action` - Tasks to process
- `/Done` - Completed tasks
- `/Briefings` - CEO briefings

---
*Silver Tier Complete*
```

## Usage Guide

### Starting Watchers

#### File System Watcher
```bash
python AI_Employee_Vault/filesystem_watcher.py
```

#### Gmail Watcher
```bash
python AI_Employee_Vault/gmail_watcher.py
```

#### Run Both (separate terminals)
```bash
# Terminal 1
python AI_Employee_Vault/filesystem_watcher.py

# Terminal 2
python AI_Employee_Vault/gmail_watcher.py
```

### Using Skills

#### Process Tasks
```bash
claude /process-tasks
```

#### Create Plans for Complex Tasks
```bash
claude /create-plans
```

#### Manage Approvals
```bash
claude /approval-workflow
```

#### Post to LinkedIn
```bash
claude /linkedin-post
# Or with topic
claude /linkedin-post "New AI service launch"
```

#### Generate Weekly Briefing
```bash
claude /weekly-briefing
```

#### Advanced Orchestration
```bash
claude /orchestrator-advanced
# Check status
claude /orchestrator-advanced --status
# Run scheduled tasks
claude /orchestrator-advanced --run-scheduled
# Health check
claude /orchestrator-advanced --health
```

### Scheduling Setup

#### Windows Task Scheduler

Create tasks for automated scheduling:

**Daily Processing (Mon-Fri 8 AM):**
1. Open Task Scheduler
2. Create Basic Task: "AI Employee Daily Processing"
3. Trigger: Weekly, Mon-Fri, 8:00 AM
4. Action: Start a program
   - Program: `claude`
   - Arguments: `/orchestrator-advanced --run-scheduled`
   - Start in: `D:\giaic\hackathon-0`

**Weekly Briefing (Monday 7 AM):**
1. Create Basic Task: "AI Employee Weekly Briefing"
2. Trigger: Weekly, Monday, 7:00 AM
3. Action: Start a program
   - Program: `claude`
   - Arguments: `/weekly-briefing`
   - Start in: `D:\giaic\hackathon-0`

#### macOS/Linux cron

Add to crontab (`crontab -e`):

```bash
# Daily processing - Mon-Fri 8 AM
0 8 * * 1-5 cd /path/to/hackathon-0 && claude /orchestrator-advanced --run-scheduled

# Weekly briefing - Monday 7 AM
0 7 * * 1 cd /path/to/hackathon-0 && claude /weekly-briefing

# LinkedIn posts - Tue, Thu 10 AM
0 10 * * 2,4 cd /path/to/hackathon-0 && claude /linkedin-post
```

## Workflow Examples

### Example 1: Email Processing Flow

1. **Gmail Watcher** detects urgent email from client
2. Creates action file in `Needs_Action/`
3. **Claude** processes via `/process-tasks`
4. Determines reply needed
5. Drafts response
6. Creates approval request in `Pending_Approval/`
7. Human reviews and moves to `Approved/`
8. **Claude** sends email via MCP
9. Logs action and moves to `Done/`

### Example 2: LinkedIn Post Flow

1. **Scheduled** for Tuesday 10 AM
2. **Orchestrator** triggers `/linkedin-post`
3. Claude reads `Business_Goals.md` for topics
4. Generates engaging post content
5. Creates post record in `Plans/Social/`
6. Auto-posts (routine business content)
7. Logs post details
8. Updates Dashboard

### Example 3: Weekly Briefing Flow

1. **Scheduled** for Monday 7 AM
2. **Orchestrator** triggers `/weekly-briefing`
3. Claude scans `Done/` folder for completed tasks
4. Analyzes revenue and expenses
5. Identifies bottlenecks
6. Reviews subscriptions
7. Generates CEO Briefing in `Briefings/`
8. Creates action items in `Needs_Action/`
9. Updates Dashboard with summary

## Approval Workflow

### Creating Approval Requests

When Claude detects action requiring approval:

```markdown
---
type: approval_request
action: send_email
to: client@example.com
subject: Invoice #1234
created: 2026-03-02T10:30:00Z
expires: 2026-03-03T10:30:00Z
status: pending
---

## Action Required
Send invoice email to Client A

## Details
- **To**: client@example.com
- **Subject**: Invoice #1234 - January Services
- **Amount**: $1,500.00

## Risk Assessment
Low - Known client, standard invoice

## To Approve
Move to /Approved/

## To Reject
Move to /Rejected/
```

### Human Review Process

1. Check `Pending_Approval/` folder regularly
2. Review approval request details
3. **To Approve**: Move file to `Approved/`
4. **To Reject**: Move file to `Rejected/`
5. **To Modify**: Add comments, keep in `Pending_Approval/`

### Claude Monitors Approved Folder

- Checks `Approved/` for files ready to execute
- Executes approved actions
- Logs with approval reference
- Moves to `Done/`

## Testing Silver Tier

### Test Plan Creation
1. Drop complex task in `Inbox/`
2. Run: `claude /create-plans`
3. Verify `Plans/` folder contains new plan
4. Check plan has checkboxes and steps

### Test Approval Workflow
1. Create task requiring approval
2. Run: `claude /approval-workflow`
3. Verify file created in `Pending_Approval/`
4. Move to `Approved/`
5. Run: `claude /approval-workflow`
6. Verify action executed and logged

### Test LinkedIn Posting
1. Run: `claude /linkedin-post "Test post"`
2. Verify post content generated
3. Check `Plans/Social/` for post record
4. Verify post published (or approval created)

### Test Weekly Briefing
1. Run: `claude /weekly-briefing`
2. Verify `Briefings/` folder contains briefing
3. Check all sections populated
4. Verify Dashboard updated

## Troubleshooting

### Gmail Watcher Not Working

**Problem:** Authentication fails

**Solution:**
```bash
# Reinstall Google libraries
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Delete token and re-authenticate
rm ~/.credentials/gmail-token.json
python gmail_watcher.py
```

### Skills Not Found

**Problem:** Claude says "skill not found"

**Solution:**
```bash
# Verify skill structure
ls .claude/skills/

# Each skill needs:
# - SKILL.md (documentation)
# - PROMPT.md (instructions)
```

### Approval Not Processing

**Problem:** Approved files not being processed

**Solution:**
1. Run: `claude /approval-workflow`
2. Check `Approved/` folder is being monitored
3. Verify Company_Handbook.md allows action type

### LinkedIn Post Fails

**Problem:** Post not publishing

**Solution:**
1. Check if MCP server configured (if using)
2. Verify browser automation setup (if using Playwright)
3. Use manual posting instructions in post file

## Silver Tier Checklist

### Core Requirements
- [ ] Two or more watchers (File System + Gmail)
- [ ] LinkedIn auto-posting functional
- [ ] Plan.md creation for complex tasks
- [ ] Approval workflow implemented
- [ ] Weekly briefing generation
- [ ] Scheduling configured
- [ ] All functionality as Agent Skills

### Skills Installed
- [ ] `/process-tasks`
- [ ] `/create-plans`
- [ ] `/approval-workflow`
- [ ] `/linkedin-post`
- [ ] `/weekly-briefing`
- [ ] `/orchestrator-advanced`

### Documentation
- [ ] Company_Handbook.md v2.0
- [ ] Business_Goals.md created
- [ ] Dashboard.md updated
- [ ] This README in place

### Testing
- [ ] File drop → task creation works
- [ ] Gmail → task creation works
- [ ] Plan creation works
- [ ] Approval workflow works
- [ ] LinkedIn posting works
- [ ] Weekly briefing generates
- [ ] Scheduling configured

## Next Steps: Gold Tier

To upgrade to Gold Tier, add:
- WhatsApp watcher
- Facebook/Instagram integration
- Twitter (X) integration
- Odoo accounting integration
- Multiple MCP servers
- Ralph Wiggum loop for autonomy
- Error recovery systems
- Comprehensive audit logging

## Support

For issues or questions:
- Check logs in `Logs/` folder
- Review Company_Handbook.md for rules
- Run health check: `claude /orchestrator-advanced --health`

---

**Silver Tier Complete** 🎉

Built for: Personal AI Employee Hackathon 0
Tier: Silver
Date: 2026-03-02
