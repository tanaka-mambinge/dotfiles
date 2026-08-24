# Execution Rules

* Do exactly what is asked. If told to replace something, replace it—do not keep the old version alongside the new one.
* Do not add fallbacks, legacy support, or backward compatibility unless explicitly instructed.
* When given a direct instruction to implement something, do it—no clarifying questions, alternative approaches, or deviations.
* Questions and back-and-forth are only appropriate when I am explicitly brainstorming or asking for recommendations. If I am telling you to do something, just do it.

# Parallel Workstreams

* Apply this only when I explicitly ask you to create parallel threads, child threads, or subagents. Do not force it on every task.
* Always use `5.6 luna` for spawned work, at medium or high reasoning depending on the task's complexity.
* I am on the $20 plan. Higher reasoning levels can burn through my quota, lock me out for hours, and stop me from working, so default to medium reasoning and only go high when the task genuinely warrants it.
* Never switch models on your own. Choosing between medium and high reasoning per task is expected; do not infer, assume, or decide that a different model is warranted.
* The main thread acts as coordinator. Child threads and subagents handle isolated, well-scoped units of work.
* Child threads and subagents must report back with a clear final status. Do not assume they are done until they explicitly say so.
* If I ask you to monitor multiple workstreams, only split the parts that actually benefit from separation.

# Diagrams in Plans & Responses

* When a plan or response involves structure, flow, architecture, or relationships (e.g. system design, call flow, state machines, file/module layout), prefer a proper diagram over hand-drawn ASCII art.
* Use Mermaid syntax (flowchart, sequenceDiagram, classDiagram, stateDiagram, etc.) as the default diagram format.
* Do not build ASCII box-and-arrow diagrams by hand; they are harder to read and maintain than a Mermaid diagram.
* Plain text is still fine for anything that isn't inherently structural or visual—don't force a diagram where a short explanation is clearer.

# Screenshot & Temp File Conventions

* Save all screenshots and temporary files to `./tmp/` in the current working directory.
* `./tmp/` must be added to `.gitignore` if it is not already present. Check first and append it only when missing.
* For browser screenshots taken through Chrome DevTools or `agent-browser`, always capture the full page, not just the visible viewport.
* For mobile screenshots taken through Android CLI, save them as-is to `./tmp/`.
* Use descriptive filenames following this format: `tmp/screenshot-<context>-<timestamp>.png`.
