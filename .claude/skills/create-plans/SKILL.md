# Create Plans Skill

Create detailed execution plans for complex tasks in the Plans folder.

## Usage

```
/create-plans
```

Or automatically invoked by `/process-tasks` for complex tasks.

## What this skill does

1. Analyzes tasks in Needs_Action folder to identify complex multi-step tasks
2. Creates detailed Plan.md files in the Plans folder
3. Breaks down tasks into actionable checkbox items
4. Identifies dependencies and required approvals
5. Estimates effort and priority
6. Links related tasks and resources

## Plan Structure

Each plan follows this structure:

```markdown
---
created: 2026-01-07T10:30:00Z
status: pending
priority: normal
estimated_effort: 30 minutes
requires_approval: false
related_tasks: []
---

## Objective
Clear statement of what needs to be accomplished

## Context
Background information and relevant details

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Resources
Links to relevant files or information

## Notes
Additional information for execution

## Approval Required
If approval is needed, details here
```

## When Plans Are Created

Plans are automatically created for:
- Tasks requiring 3+ steps
- Tasks involving external communications
- Tasks that modify multiple files
- Tasks requiring research or analysis
- Tasks with dependencies on other tasks

## Example

When processing a client invoice request:

1. Skill analyzes the task
2. Creates: Plans/PLAN_invoice_client_a_2026-01-07.md
3. Breaks down into:
   - [ ] Identify client details
   - [ ] Calculate amount owed
   - [ ] Generate invoice document
   - [ ] Send via email (requires approval)
   - [ ] Log transaction
   - [ ] Update dashboard

## Integration

Works with:
- `/process-tasks` - Automatically creates plans for complex tasks
- `/approval-workflow` - Identifies approval requirements
- `/weekly-briefing` - Reports on plan completion status
