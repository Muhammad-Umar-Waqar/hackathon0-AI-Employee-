# LinkedIn Post Skill

Automatically create and post business content on LinkedIn to generate sales.

## Usage

```
/linkedin-post
```

Or provide a topic:
```
/linkedin-post "New AI Employee service launch"
```

## What this skill does

1. Generates LinkedIn post content based on business goals
2. Creates engaging posts with appropriate hashtags
3. Submits posts for approval (initial) or auto-posts (Silver tier+)
4. Tracks post performance and engagement
5. Maintains posting schedule
6. Archives all posts for reference

## Post Categories

| Category | Purpose | Approval |
|----------|---------|----------|
| Business Updates | Company news, milestones | Auto (Silver+) |
| Service Announcements | New offerings, promotions | Auto (Silver+) |
| Thought Leadership | Industry insights, tips | Auto (Silver+) |
| Client Success | Testimonials, case studies | Required |
| Engagement | Replies, comments | Required |

## Post Structure

### Standard Business Post
```
{{Hook - attention-grabbing first line}}

{{Body - 2-3 sentences of value/content}}

{{Call-to-action - optional}}

{{Hashtags - 3-5 relevant hashtags}}
```

### Example Posts

**Service Announcement:**
```
🚀 Exciting News!

We're launching our new AI Employee consulting service! 
Helping businesses automate workflows and reduce costs by 85%.

Ready to transform your business? Let's talk.

#AI #Automation #Business #Innovation #DigitalTransformation
```

**Thought Leadership:**
```
💡 The future of business is autonomous.

Companies using AI agents are seeing:
• 90% cost reduction per task
• 24/7 operations without burnout
• Instant scaling capabilities

Are you ready for the AI revolution?

#FutureOfWork #AI #BusinessStrategy #Innovation
```

**Business Update:**
```
📈 Milestone Alert!

Just completed our 100th automated workflow for clients.
The results? Average 40 hours saved per week per business.

Small changes, massive impact.

#Milestone #Automation #Results #BusinessGrowth
```

## Posting Workflow

### Step 1: Determine Post Topic
Sources for post content:
- Business_Goals.md objectives
- Recent company milestones
- Industry news and trends
- Client successes (with permission)
- Scheduled content calendar

### Step 2: Generate Post Content
Create engaging content following:
- Professional tone
- Clear value proposition
- Appropriate length (150-300 characters ideal)
- Relevant hashtags (3-5)
- Emoji usage (sparingly, for emphasis)

### Step 3: Create Post Record
Create file in Plans/Social/ folder:

```markdown
---
type: linkedin_post
category: {{category}}
created: {{timestamp}}
scheduled: {{timestamp}}
status: draft
approval_required: {{true|false}}
---

## Post Content
{{Full post text}}

## Context
{{Why this post is being created}}

## Target Audience
{{Who should see this post}}

## Expected Outcome
{{What we hope to achieve}}

## Approval Status
{{Pending|Approved|Rejected}}
```

### Step 4: Submit for Approval (if required)
For posts requiring approval:
- Create approval request in Pending_Approval/
- Include full post content
- Wait for human decision

### Step 5: Execute Post
**Auto-post (Silver tier+):**
- Use LinkedIn MCP server or
- Use Playwright browser automation or
- Generate instructions for manual posting

**Manual posting instructions:**
```markdown
## How to Post

1. Go to: https://www.linkedin.com/feed/
2. Click "Start a post"
3. Paste this content:
   {{post content}}
4. Add image if specified: {{image details}}
5. Click "Post"
6. Screenshot for records
```

### Step 6: Log and Archive
- Move post record to Done/Social/
- Log post details with timestamp
- Update Dashboard with post count
- Track in Social_Media_Log.md

## Content Guidelines

### Do's
✅ Keep it professional and positive
✅ Focus on value to audience
✅ Use relevant hashtags
✅ Include clear call-to-action when appropriate
✅ Proofread for errors

### Don'ts
❌ Controversial topics (politics, religion)
❌ Overly promotional without value
❌ Too many hashtags (>5)
❌ Long paragraphs (>3 lines)
❌ Spelling/grammar errors

## Posting Schedule

| Frequency | Type | Best Time |
|-----------|------|-----------|
| Daily | Engagement, quick tips | 9-10 AM |
| 3x/week | Standard posts | 8-9 AM, 12 PM, 5-6 PM |
| Weekly | Long-form, announcements | Tuesday-Thursday 10 AM |

## Integration

Works with:
- `/create-plans` - Plans social media campaigns
- `/approval-workflow` - Submits posts for approval
- `/weekly-briefing` - Reports on social media performance

## Silver Tier Behavior

In Silver tier:
- ✅ Auto-posts business updates and announcements
- ✅ Auto-posts scheduled content
- ⚠️ Requires approval for client-specific content
- ⚠️ Requires approval for sensitive topics

## Example Workflow

**Task:** "Post about our new AI Employee service"

1. Read Business_Goals.md for service details
2. Generate 2-3 post variations
3. Select best option
4. Create post record in Plans/Social/
5. Submit for approval (first time) or auto-post
6. Execute post via MCP/browser/manual
7. Log and archive

## Metrics to Track

- Posts published (count)
- Engagement rate (if API available)
- Click-through rate (if tracking)
- Lead generation (inbound inquiries)
- Follower growth (weekly)

## Security Notes

- Never post confidential information
- Never post client details without permission
- Always maintain professional tone
- Keep credentials secure (use MCP, not stored)
