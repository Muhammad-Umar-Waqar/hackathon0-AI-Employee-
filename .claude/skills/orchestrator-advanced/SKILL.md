# Orchestrator Advanced Skill

Advanced orchestration with scheduling, multi-skill coordination, and automated workflows.

## Usage

```
/orchestrator-advanced
```

Or with options:
```
/orchestrator-advanced --status
/orchestrator-advanced --run-scheduled
/orchestrator-advanced --trigger "linkedin-weekly"
```

## What this skill does

1. Coordinates multiple skills in sequence
2. Manages scheduled tasks (daily, weekly, monthly)
3. Triggers automated workflows
4. Monitors system health across all watchers
5. Handles task routing to appropriate skills
6. Maintains orchestration logs and history

## Scheduled Tasks

| Task | Schedule | Skill Triggered |
|------|----------|-----------------|
| Daily Briefing | Mon-Fri 8:00 AM | Process tasks + Dashboard update |
| LinkedIn Post | Tue, Thu 10:00 AM | linkedin-post |
| Weekly Briefing | Monday 7:00 AM | weekly-briefing |
| Approval Check | Daily 5:00 PM | approval-workflow |
| System Health | Daily 6:00 PM | Health check all watchers |
| Monthly Review | 1st of month 9:00 AM | weekly-briefing (monthly) |

## Orchestration Patterns

### Pattern 1: Sequential Skill Execution
```
1. /create-plans → Analyze tasks, create plans
2. /approval-workflow → Process pending approvals
3. /process-tasks → Execute approved tasks
4. /linkedin-post → Post scheduled content
5. Update Dashboard → Final status update
```

### Pattern 2: Conditional Execution
```
IF task requires plan → /create-plans
IF approval pending → /approval-workflow
IF approved → Execute action
ELSE → Wait for approval
```

### Pattern 3: Scheduled Workflow
```
Monday 7:00 AM:
1. /weekly-briefing → Generate CEO briefing
2. Create tasks from briefing actions
3. /process-tasks → Process urgent items
4. Update Dashboard with briefing summary
```

## Workflow Definitions

### Daily Processing Workflow
```yaml
name: daily-processing
schedule: "0 8 * * 1-5"  # Mon-Fri 8 AM
steps:
  - skill: process-tasks
    description: Process overnight tasks
  - skill: approval-workflow
    description: Check and process approvals
  - action: update-dashboard
    description: Refresh status dashboard
```

### Weekly Content Workflow
```yaml
name: weekly-content
schedule: "0 10 * * 2,4"  # Tue, Thu 10 AM
steps:
  - skill: linkedin-post
    topic: from Business_Goals.md
  - action: log-post
    description: Record post metrics
```

### Weekly Briefing Workflow
```yaml
name: weekly-briefing
schedule: "0 7 * * 1"  # Monday 7 AM
steps:
  - skill: weekly-briefing
    period: previous week
  - action: create-tasks
    description: Create tasks from briefing actions
  - skill: process-tasks
    filter: urgent only
```

## System Health Monitoring

### Watcher Health Check
Monitor all active watchers:
- File System Watcher ✅/❌
- Gmail Watcher ✅/❌
- WhatsApp Watcher ✅/❌
- LinkedIn Watcher ✅/❌

### Health Status Structure
```markdown
---
check_time: {{timestamp}}
overall_status: {{healthy|degraded|down}}
---

## Watcher Status
| Watcher | Status | Last Activity | Issues |
|---------|--------|---------------|--------|
| File System | ✅ Active | 5 min ago | None |
| Gmail | ✅ Active | 2 min ago | None |

## Task Queues
| Queue | Count | Oldest | Status |
|-------|-------|--------|--------|
| Needs_Action | 3 | 1 hour | Normal |
| Pending_Approval | 1 | 2 hours | Normal |

## Recent Errors
- None in last 24 hours

## Recommendations
- All systems operational
```

## Task Routing Logic

Route tasks to appropriate skills:

| Task Type | Route To |
|-----------|----------|
| Complex multi-step | /create-plans first |
| Email/Payment | /approval-workflow |
| Social media | /linkedin-post |
| Report generation | /weekly-briefing |
| Simple file processing | /process-tasks direct |

## Integration

Works with all skills:
- `/process-tasks` - Coordinates task execution
- `/create-plans` - Triggers for complex tasks
- `/approval-workflow` - Manages approval flow
- `/linkedin-post` - Schedules and posts
- `/weekly-briefing` - Generates reports

## Commands

### Status Check
```
/orchestrator-advanced --status
```
Returns: System health, queue sizes, recent activity

### Run Scheduled
```
/orchestrator-advanced --run-scheduled
```
Executes all due scheduled tasks

### Trigger Workflow
```
/orchestrator-advanced --trigger "workflow-name"
```
Manually trigger a specific workflow

### Health Check
```
/orchestrator-advanced --health
```
Full system health report

## Scheduling Setup

### Windows Task Scheduler
Create tasks for each scheduled item:

```xml
<!-- Weekly Briefing - Monday 7 AM -->
<Task>
  <Trigger>
    <CalendarTrigger>
      <StartBoundary>2026-01-06T07:00:00</StartBoundary>
      <ScheduleByWeek>
        <DaysOfWeek><Monday /></DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Trigger>
  <Actions>
    <Exec>
      <Command>claude</Command>
      <Arguments>/orchestrator-advanced --run-scheduled</Arguments>
    </Exec>
  </Actions>
</Task>
```

### macOS/Linux cron
```bash
# Daily processing - Mon-Fri 8 AM
0 8 * * 1-5 claude /orchestrator-advanced --run-scheduled

# Weekly briefing - Monday 7 AM
0 7 * * 1 claude /weekly-briefing

# LinkedIn posts - Tue, Thu 10 AM
0 10 * * 2,4 claude /linkedin-post
```

## Error Handling

### Retry Logic
- Transient errors: Retry up to 3 times with exponential backoff
- Permanent errors: Log and create manual task
- Critical errors: Alert via Dashboard immediately

### Degraded Mode
If a skill fails:
1. Log the failure
2. Continue with remaining skills
3. Create task for manual intervention
4. Update Dashboard with issue

## Logging

All orchestration activity logged to:
`Logs/orchestration.log`

Format:
```json
{
  "timestamp": "2026-01-07T08:00:00Z",
  "workflow": "daily-processing",
  "step": "process-tasks",
  "status": "success",
  "duration_seconds": 45,
  "tasks_processed": 5
}
```

## Example Orchestration Run

```
[2026-01-07 08:00:00] Starting daily-processing workflow
[2026-01-07 08:00:01] → Running /process-tasks
[2026-01-07 08:00:45] ✓ Processed 5 tasks
[2026-01-07 08:00:46] → Running /approval-workflow
[2026-01-07 08:01:15] ✓ Processed 2 approvals
[2026-01-07 08:01:16] → Updating Dashboard
[2026-01-07 08:01:20] ✓ Dashboard updated
[2026-01-07 08:01:20] Daily processing complete
```

## Security Notes

- Never bypass approval workflows
- Log all automated actions
- Rate limit external API calls
- Validate all inputs before execution
