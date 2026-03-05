# Approval Workflow Skill

Manage human-in-the-loop approval workflow for sensitive actions.

## Usage

```
/approval-workflow
```

Or automatically invoked when sensitive actions are detected.

## What this skill does

1. Identifies actions requiring human approval per Company_Handbook.md
2. Creates approval request files in Pending_Approval folder
3. Tracks approval status and expiration
4. Processes approved actions
5. Archives decisions (approved/rejected)
6. Sends reminders for pending approvals

## Approval Categories

| Category | Auto-Approve | Requires Approval |
|----------|--------------|-------------------|
| Email replies | Known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs, sensitive topics |
| File operations | Create, read | Delete, move outside vault |
| External API calls | Read-only | Write actions, payments |

## Approval Request Structure

```markdown
---
type: approval_request
action: {{action_type}}
created: {{timestamp}}
expires: {{timestamp + 24 hours}}
priority: {{normal|high|urgent}}
amount: {{if payment}}
recipient: {{if applicable}}
status: pending
---

## Action Required
{{Clear description of what needs approval}}

## Details
- **Action**: {{Specific action}}
- **Target**: {{Recipient/destination}}
- **Amount**: {{If payment}}
- **Reason**: {{Why this action is needed}}

## Context
{{Background information from original task}}

## Risk Assessment
{{Low|Medium|High}} - {{Explanation}}

## To Approve
Move this file to: /Approved/

## To Reject
Move this file to: /Rejected/

## To Request Changes
Add comments to this file and keep in /Pending_Approval/
```

## Workflow

### 1. Create Approval Request
When a sensitive action is detected:
- Create file in Pending_Approval/
- Use descriptive filename: ACTION_Type_Description_YYYY-MM-DD.md
- Include all relevant details
- Set expiration (24 hours from creation)

### 2. Wait for Human Decision
Human reviews and moves file to:
- /Approved/ → Execute the action
- /Rejected/ → Log rejection, notify if needed
- Stays in /Pending_Approval/ → Awaiting decision

### 3. Process Decision
**If Approved:**
- Execute the action
- Log to Logs/
- Move to Done/
- Update Dashboard

**If Rejected:**
- Log rejection
- Move to Rejected/
- Update Dashboard
- Notify if required

### 4. Handle Expiration
- Check for expired approvals daily
- Move expired to Rejected/
- Log expiration
- Notify human if action still needed

## Integration

Works with:
- `/process-tasks` - Detects when approval is needed
- `/create-plans` - Identifies approval steps in plans
- `/linkedin-post` - Submits posts for approval
- `/weekly-briefing` - Reports on approval statistics

## Example Approval Requests

### Email Approval
```markdown
---
type: approval_request
action: send_email
to: client@example.com
subject: Invoice #1234 - $1500
created: 2026-01-07T10:30:00Z
expires: 2026-01-08T10:30:00Z
status: pending
---

## Action Required
Send invoice email to Client A

## Details
- **To**: client@example.com
- **Subject**: Invoice #1234 - January Services
- **Amount**: $1,500.00
- **Attachment**: Invoice_1234.pdf

## Context
Client A requested invoice for January services. 
Invoice generated and ready to send.

## Risk Assessment
Low - Known client, standard invoice amount

## To Approve
Move to /Approved/
```

### Payment Approval
```markdown
---
type: approval_request
action: payment
amount: 500.00
recipient: Vendor XYZ
created: 2026-01-07T10:30:00Z
expires: 2026-01-08T10:30:00Z
status: pending
---

## Action Required
Process payment to Vendor XYZ

## Details
- **Amount**: $500.00
- **Recipient**: Vendor XYZ (Bank: XXXX1234)
- **Reference**: Invoice #5678
- **Due Date**: 2026-01-10

## Context
Monthly software subscription payment.
Recurring vendor, always paid on time.

## Risk Assessment
Low - Recurring payment, known vendor

## To Approve
Move to /Approved/
```

### Social Media Post Approval
```markdown
---
type: approval_request
action: social_post
platform: LinkedIn
created: 2026-01-07T10:30:00Z
expires: 2026-01-08T10:30:00Z
status: pending
---

## Action Required
Post business update on LinkedIn

## Details
- **Platform**: LinkedIn
- **Type**: Business announcement
- **Scheduled**: 2026-01-07 12:00 PM

## Post Content
"We're excited to announce our new AI Employee 
consulting services! Helping businesses automate 
their workflows with cutting-edge AI solutions.

#AI #Automation #Business"

## Context
Weekly business promotion post.
Part of marketing strategy.

## Risk Assessment
Low - Standard business content

## To Approve
Move to /Approved/
```

## Security Notes

- Never execute actions without approval file in /Approved/
- Always log approval decisions
- Expired approvals must be refreshed
- High-risk actions may require additional verification
