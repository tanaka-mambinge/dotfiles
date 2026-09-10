# Execution Rules

* Do exactly what is asked. If told to replace something, replace it—do not keep the old version alongside the new one.
* Do not add fallbacks, legacy support, or backward compatibility unless explicitly instructed.
* Treat direct, command-style instructions as execution requests. If I tell you to implement, change, remove, replace, fix, create, or update something, do it without asking clarifying questions, offering alternatives, or asking for confirmation.
* Only switch into discussion, recommendation, or suggestion mode when I explicitly ask a question, ask for help, ask for suggestions, ask what you think, or otherwise clearly request input.
* A question mark or explicit question means you may explain, recommend, compare options, or suggest improvements where useful.
* Do not ask questions whose answers are already present in my prompt, the conversation, attached files, screenshots, code, or existing project context.
* If a command has minor ambiguity, make the most reasonable interpretation and proceed. Only ask a clarifying question when the missing information genuinely prevents execution or would materially change the result.
* Do not turn clear implementation instructions into back-and-forth discussion.

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

# UI Icons

* Never use Unicode characters, glyphs, emoji, text symbols, or characters such as `✓`, `✕`, `→`, `←`, `⋮`, `⚙`, `★`, `●`, or similar as substitutes for UI icons.
* Always use a proper icon library/package for interface icons.
* If the project already has an icon library, use that library consistently.
* If no icon library exists, add an appropriate established icon package for the project's stack rather than using text or Unicode characters as icons.
* Keep icon style, stroke weight, sizing, and alignment consistent across the interface.

# Screenshot & Temp File Conventions

* Save all screenshots and temporary files to `./tmp/` in the current working directory.
* `./tmp/` must be added to `.gitignore` if it is not already present. Check first and append it only when missing.
* For browser screenshots taken through Chrome DevTools or `agent-browser`, always capture the full page, not just the visible viewport.
* For mobile screenshots taken through Android CLI, save them as-is to `./tmp/`.
* Use descriptive filenames following this format: `tmp/screenshot-<context>-<timestamp>.png`.
