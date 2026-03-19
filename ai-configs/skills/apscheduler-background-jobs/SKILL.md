---
name: apscheduler-background-jobs
description: Provide a standalone guide for wiring APScheduler into FastAPI projects so agents can add reliable background jobs without per-repo assumptions.
license: MIT
compatibility: opencode
metadata:
  audience: developers
---

## Overview

Use APScheduler whenever an API needs recurring or deferred jobs (reminders, cleanup tasks, notifications) without relying on external cron infrastructure. The skill assumes FastAPI as the host app and keeps examples framework-agnostic by focusing on scheduler setup, job registration, and lifecycle hooks rather than business rules.

## Setup

1. Activate the virtual environment before installing dependencies.
2. Install APScheduler via `pip install APScheduler` (or add it to your lockfile if the repo uses one).
3. Decide on job stores/executors:
   - Use `BackgroundScheduler` for simple deployments.
   - Add `jobstores` (e.g., `SQLAlchemyJobStore`) if persistence across restarts matters.
   - Configure `executors` when jobs are CPU-bound (`processpool`) or I/O-bound (`threadpool`).
4. Always set `timezone="UTC"` to keep datetimes consistent, matching FastAPI apps that treat timestamps as UTC.

## Scheduler configuration

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

scheduler = BackgroundScheduler(
    jobstores={"default": SQLAlchemyJobStore(url="sqlite:///jobs.db")},
    timezone="UTC",
)

def start_scheduler():
    if not scheduler.running:
        scheduler.start(paused=True)

def attach_to_app(app: FastAPI):
    app.add_event_handler("startup", lambda: start_scheduler())
    app.add_event_handler("shutdown", lambda: scheduler.shutdown(wait=False))
```

Call `start_scheduler` before scheduling any jobs and resume the scheduler once the app fully boots (e.g., after dependency injection is ready). Tie the handlers to `FastAPI` using `app.add_event_handler` or the decorator helpers so jobs are not started twice in testing environments.

## Job definition pattern

Jobs should be plain callables that accept all context they need via arguments (e.g., request identifiers, serialized payloads). Avoid referencing global state; inject dependencies explicitly:

```python
from uuid import uuid4

def create_reminder_job(user_id: str, payload: dict):
    job_id = uuid4().hex
    scheduler.add_job(
        func=send_reminder,
        trigger="cron",
        id=job_id,
        replace_existing=True,
        kwargs={"user_id": user_id, "payload": payload},
    )
    return job_id

def send_reminder(user_id: str, payload: dict):
    with get_session() as session:
        # perform DB work via session
        pass
```

Use deterministic job IDs when you may update the trigger later (`job_id=f"user-{user_id}-daily"`). Always persist a reference to the APScheduler job id if you plan to cancel or reschedule it from another request.

## Lifecycle management

- Start the scheduler during FastAPI startup, and consciously shut it down with `scheduler.shutdown(wait=True)` on shutdown events.
- Pause jobs during deployment maintenance by calling `scheduler.pause_job(job_id)` and resume with `scheduler.resume_job(job_id)`.
- Remove obsolete jobs using `scheduler.remove_job(job_id)`; wrap these operations in try/except for `JobLookupError` because the job may already be gone.
- Schedule long-running jobs with `max_instances` and `misfire_grace_time` so overlapping run attempts are handled gracefully.

## Observability & error handling

- Attach a listener to log job events:

```python
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

def job_listener(event):
    if event.exception:
        logger.error("job failed", job_id=event.job_id, exception=event.exception)
    else:
        logger.debug("job succeeded", job_id=event.job_id)

scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
```

- Use structured logging (e.g., Loguru or Stdlib) so you can correlate job IDs with request traces.
- If a job mutates the database, wrap it in a transaction (`with get_session() as session:`) and log errors before rethrowing or retrying.

## References

- Use the APScheduler docs for advanced triggers: https://apscheduler.readthedocs.io/en/stable/
- Keep job payloads serializable (JSON-friendly) so functions can be retried safely.
