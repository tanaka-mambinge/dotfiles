---
name: taskforce
description: "Logs completed development work (features, bug fixes, refactors, chores) as tasks in Task Force via the `taskforce` CLI, and manages task lifecycle (create, update, complete, list, show). Activates when the user asks to log/save/record/create a task for work just completed, says things like 'create a task for that', 'log this as done', 'add this to task force', 'save that as a task', 'mark that task complete', or asks to list/check/update tasks or projects in Task Force."
metadata:
  domain: project-management
  triggers: task force, taskforce, log task, create task, mark complete
---

# Task Force CLI

`taskforce` is a CLI client for Task Force (project/task management). Use it
to record completed work as a task, and to create/update/complete/list/show
tasks and projects.

## When to apply

- The user just finished a piece of work with you (a feature, bug fix,
  refactor, chore) and asks you to log/save/record it as a task.
- The user asks you to create, update, complete, list, or show tasks or
  projects in Task Force.

## Refer to tasks and projects by name, not ID

When talking to the user, identify tasks and projects by their **name/title**
(and status, plus project name when it adds clarity) — never by numeric id.
People don't track IDs.

- `id` and `project_id` are **internal handles for you**, not for the user. Use
  them to chain commands: resolve the user's named task to its id (via
  `task list` / `task show`), then `update`/`complete` by that id. Don't surface
  the id in what you say.
- **Listing**: render titles + status (and the project name when results span
  multiple projects), not ids.
- **Disambiguation**: if a name matches several tasks, distinguish them by
  status, project, or description and ask the user which they mean — never ask
  them to pick an id.

## Preconditions

1. Check the CLI is installed and authenticated:
   ```sh
   taskforce whoami
   ```
   If this errors with "Not authenticated", tell the user to run
   `taskforce login --email <email> --password <password>` (or set
   `TASKFORCE_EMAIL` / `TASKFORCE_PASSWORD`) and stop.

2. Check the repo is linked to a Task Force project — look for a
   `.taskforce.json` file in the repo root. If it's missing, tell the user to
   run `taskforce init --project-id <id>` (or `taskforce init --create --name
   "<project name>"` to create a new project) and stop. Once linked, every
   `task` command defaults to that project automatically.

> A separate `taskforce-dev` binary exists for testing against a local Task
> Force instance — it has its own config and `.taskforce.json` is shared, so
> it behaves the same way. Use whichever the user has set up; don't switch
> between them without being asked.

## Core workflow: log completed work

Once preconditions are met, summarize the work into a short title and a
description (what changed and why — this is what teammates will see in Task
Force), then run:

```sh
taskforce task create --title "<concise summary>" --description "<what changed and why>" --done
```

`--done` creates the task **and** marks it complete in one call. Confirm back
to the user by **title and status** — not the id (e.g. "Logged 'Fix auth token
refresh race' — Completed."). Keep the returned `id` for your own follow-up
commands; don't show it.

If the user wants to log work as still in-progress (e.g. a WIP checkpoint),
omit `--done` and optionally pass `--status "In Progress"`.

Valid `--status` values: `Not Started`, `In Progress`, `Completed`, `Closed`,
`Blocked`, `Carried over`, `Overdue`, `Forfeited` (also shown in `--help`, and
available live via `taskforce task statuses`).

## Output contract

**Every command prints exactly one JSON value to stdout on success and
nothing else.** On failure, nothing is printed to stdout — instead
`{"error": "<message>"}` is printed to stderr and the process exits non-zero.
Always check the exit code / stderr before parsing stdout as JSON.

### Task object (`task create`, `update`, `complete`, `show`, items in `task list`)

```json
{
  "id": 123,
  "title": "Fix auth token refresh race",
  "description": "Token refresh could fire twice under load, causing 401s. Added a mutex.",
  "status": "Completed",
  "is_completed": true,
  "progress": 100,
  "project_id": 5,
  "completed_at": "2026-06-10T10:05:00Z",
  "updated_at": "2026-06-10T10:05:00Z"
}
```

### Project object (`project create`, `init`, items in `project list`)

```json
{
  "id": 5,
  "name": "Task Force",
  "description": "...",
  "status": "planning",
  "tasks_count": 12
}
```

### User object (`whoami`, `login`)

```json
{ "id": 1, "name": "Dev User", "email": "dev@mugonat.com" }
```

`task list` and `project list` print a JSON **array** of the objects above.
`task list` always returns the full result set across all pages, regardless
of how many tasks exist.

### Task status object (`task statuses`)

```json
{ "value": "In Progress", "label": "In Progress" }
```

`task statuses` prints a JSON array of these — the authoritative list of
valid `--status` values for `task create`/`task update`/`task list`.

## Chaining commands

Because every command emits exactly one JSON value on stdout (and errors go
to stderr instead), commands compose cleanly without temp files:

- **Read-then-call** (preferred for agents): run a command, read the `id`
  field from its JSON output, and pass it as a literal argument to the next
  command. E.g. create a task, note `id: 123`, then later run
  `taskforce task complete 123`.
- **Shell piping**: `task create`, `task update`, `task complete`, and `task
  show` accept `-` in place of `<id>` to read a JSON object from stdin and
  use its `.id`. This lets you write a single pipeline, e.g.:
  ```sh
  taskforce task create --title "Add export" --description "..." \
    | taskforce task complete -
  ```
  This is efficient — one process per step, no intermediate files, and the
  full filtered task object flows straight through to the final output.

Both patterns are valid; use shell piping for fixed multi-step sequences in a
single command, and read-then-call when a decision (e.g. whether to mark
`--done`) depends on intermediate output.

## Full command reference

For the complete list of commands, flags, and config (`.taskforce.json`,
env vars, `taskforce-dev` vs `taskforce`), see
[`files/cli-reference.md`](files/cli-reference.md).
