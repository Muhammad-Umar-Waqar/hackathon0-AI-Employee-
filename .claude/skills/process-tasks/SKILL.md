# Process Tasks Skill

Process tasks from the Needs_Action folder and move them to Done when complete.

## Usage

```
/process-tasks
```

## What this skill does

1. Reads all task files from the AI_Employee_Vault/Needs_Action folder
2. Analyzes each task and determines appropriate action
3. Creates a plan in the Plans folder if needed
4. Executes the task according to Company_Handbook.md rules
5. Updates Dashboard.md with progress
6. Moves completed tasks to Done folder
7. Logs all actions to Logs folder

## Task Processing Rules

- Follow guidelines in Company_Handbook.md
- For sensitive actions, create approval requests in Pending_Approval folder
- Always log actions taken
- Update Dashboard.md after processing

## Example

When a file is dropped in Inbox:
1. File system watcher creates a task file in Needs_Action
2. Run `/process-tasks` to process it
3. Task is analyzed and appropriate action taken
4. Task file moved to Done folder
5. Dashboard updated with results
