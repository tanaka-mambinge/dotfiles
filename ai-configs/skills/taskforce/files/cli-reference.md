# taskforce CLI reference

Full command and flag reference. See `SKILL.md` for the output schemas and
chaining patterns — this file is for command details only.

## Auth

### `taskforce login [--email <email>] [--password <password>] [--api-url <url>]`

Authenticates and stores a bearer token in the global config
(`~/.config/taskforce/config.json`, or `taskforce-dev` for the dev binary).

- `--email` / `--password` can also be supplied via `TASKFORCE_EMAIL` /
  `TASKFORCE_PASSWORD` env vars.
- `--api-url` overrides the API base URL and is saved for future commands.
- Output: the authenticated user object (`{id, name, email}`).

### `taskforce logout`

Revokes the token server-side (best-effort) and clears it locally.
Output: `{"ok": true}`.

### `taskforce whoami`

Output: the authenticated user object. Errors with "Not authenticated" if no
token is stored.

## Project linking

### `taskforce init [--project-id <id>] [--create] [--name <name>] [--description <d>] [--product <p>]`

Links the current directory to a Task Force project by writing
`.taskforce.json` (`{ projectId, projectName }`). Once linked, `task create`
and `task list` default to this project unless `--project`/`--all` is given.

- `--project-id <id>`: link to an existing project.
- `--create --name <name> [--description] [--product]`: create a new project
  and link to it.
- One of `--project-id` or `--create` is required.
- Output: the linked project object.

## Projects

### `taskforce project list`

Output: array of project objects (`{id, name, description, status,
tasks_count}`).

### `taskforce project create --name <name> [--description <d>] [--product <p>]`

Output: the created project object.

## Tasks

### `taskforce task create --title <title> [--description <d>] [--status <s>] [--project <id>] [--done]`

- `--project <id>`: defaults to the project linked via `taskforce init`
  (`.taskforce.json`). Tasks can be created without a project.
- `--status <s>`: initial status (e.g. `"In Progress"`). Defaults to the
  Task Force default ("Not Started") if omitted.
- `--done`: after creating the task, immediately calls `task complete` on
  it. Use this to log already-finished work in one step.
- Output: the created (and possibly completed) task object.

### `taskforce task update <id|-> [--title <t>] [--description <d>] [--status <s>] [--project <id>]`

Updates only the fields provided. Output: the updated task object.

### `taskforce task complete <id|->`

Marks the task complete (sets `is_completed`, `completed_at`, `progress:
100`, status → `Completed`). Output: the updated task object.

### `taskforce task show <id|->`

Output: the task object.

### `taskforce task list [--project <id>] [--status <s>] [--mine] [--all]`

- `--project <id>`: filter by project. Defaults to the linked project
  (`.taskforce.json`) if present.
- `--all`: ignore the linked project and list across all projects.
- `--status <s>`: filter by status string.
- `--mine`: only tasks assigned to the authenticated user.
- Output: array of task objects. The CLI follows the API's pagination
  internally and returns the **complete** result set, not just the first
  page.

### `taskforce task statuses`

Output: array of `{value, label}` objects — the valid `--status` values for
`task create`/`task update`/`task list` (currently `Not Started`, `In
Progress`, `Completed`, `Closed`, `Blocked`, `Carried over`, `Overdue`,
`Forfeited`, but this command is the source of truth).

## `<id|->` argument

Wherever a command takes `<id>`, you may pass `-` instead to read a JSON
object from stdin and use its `.id` field. Errors if stdin isn't valid JSON
with a numeric `id`.

## Config & environment

| Setting | Source (highest priority first) |
| --- | --- |
| API base URL | `--api-url` flag (login only) > `TASKFORCE_API_URL` env > saved config > build-time default |
| Auth token | `TASKFORCE_TOKEN` env > saved config (set by `login`) |
| Linked project | `--project <id>` flag > `.taskforce.json` in cwd |

- `taskforce` (prod build): default API URL `https://tasks.mugonat.dev/api`,
  config in `~/.config/taskforce/config.json`.
- `taskforce-dev` (dev build): default API URL `http://127.0.0.1:8047/api`,
  config in `~/.config/taskforce-dev/config.json`.
- `.taskforce.json` lives in the project repo root and is shared between
  `taskforce` and `taskforce-dev`.

## Errors

Any command that fails prints `{"error": "<message>"}` to **stderr** and
exits with a non-zero status. Stdout is left empty — never parse stdout as
JSON without first checking the exit code.

- No token stored at all: `"Not authenticated. Run \`taskforce login\` first."`
- Token rejected by the API (expired/revoked/invalid — HTTP 401):
  `"Authentication failed (401). Your token is missing, invalid, or has been
  revoked — run \`taskforce login\` again."` Re-run `taskforce login` to fix
  either case.
