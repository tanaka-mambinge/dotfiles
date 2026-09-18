# Execution Rules

* Do exactly what is asked. If told to replace something, replace it—do not keep the old version alongside the new one.
* Do not add fallbacks, legacy support, backward compatibility, alternate implementations, or secondary code paths unless explicitly instructed by the user.
* Treat direct, command-style instructions as execution requests. If I tell you to implement, change, remove, replace, fix, create, or update something, do it without asking clarifying questions, offering alternatives, or asking for confirmation.
* Only switch into discussion, recommendation, or suggestion mode when I explicitly ask a question, ask for help, ask for suggestions, ask what you think, or otherwise clearly request input.
* A question mark or explicit question means you may explain, recommend, compare options, or suggest improvements where useful.
* Do not ask questions whose answers are already present in my prompt, the conversation, attached files, screenshots, code, or existing project context.
* If a command has minor ambiguity, make the most reasonable interpretation and proceed. Only ask a clarifying question when the missing information genuinely prevents execution or would materially change the result.
* Do not turn clear implementation instructions into back-and-forth discussion.

# User-Facing Language & UX

* Build things for normal users, not developers, unless the product is explicitly intended for a technical audience.
* Do not expose users to technical jargon, implementation details, developer terminology, infrastructure concepts, or internal system language they do not need to understand.
* Specialist terminology is fine when it is normal language for the actual field or profession the product serves.
* Use plain, familiar language for buttons, labels, errors, instructions, onboarding, settings, and other user-facing copy.
* Do not tell normal users to use a CLI, terminal, source code, package manager, compiler, environment variable, config file, build process, or other developer tooling.
* Do not suggest compiling from source, cloning repositories, running commands, or editing code as a normal-user solution.
* Technical setup instructions are only appropriate when the intended user is explicitly a developer, administrator, engineer, or other relevant technical specialist.
* Do not leak internal implementation details into the UI just because they are useful to developers.
* Prefer a simple user-facing workflow over exposing technical complexity.

# UI Layout, Navigation & Separation of Concerns

* Prefer vertical layouts and vertical scrolling over horizontal scrolling.
* Avoid interfaces that require users to scroll horizontally to reach important content, controls, columns, cards, or actions.
* Do not make wide layouts just because more information can fit side by side.
* On narrow screens, stack content vertically instead of forcing it into a wide row.
* Do not cram everything into a single page, screen, modal, panel, dashboard, or view.
* Use separate pages, screens, tabs, sections, drawers, detail views, or drill-down flows when the content has distinct purposes.
* A page should have a clear primary purpose. If unrelated or secondary content makes the page crowded, move it elsewhere.
* Apply separation of concerns to UI design. Listing, viewing, creating, editing, and deleting are distinct concerns and should not all compete for space on the same page by default.
* Do not place full create forms, edit forms, detail views, delete controls, and the complete list view on the same screen unless there is a clear UX reason.
* A list page should primarily focus on browsing, searching, filtering, and selecting records.
* A detail page should primarily focus on viewing one record and the actions relevant to that record.
* Create and edit workflows should normally use their own page, modal, drawer, sheet, or focused form flow.
* Destructive actions such as delete should normally live behind an action menu, contextual menu, detail view, or confirmation modal rather than being permanently prominent everywhere.
* Secondary actions should be hidden behind menus, modals, drawers, or other contextual UI when keeping them visible would clutter the main interface.
* "View all" content should not be dumped onto the current page when a dedicated list or detail view would be clearer.
* Do not optimize for showing the maximum amount of information or every possible action at once. Optimize for clarity, hierarchy, and ease of use.
* Progressive disclosure is preferred: show the important information and primary actions first, then reveal secondary actions or deeper details when needed.
* Dense dashboards are acceptable only when the product genuinely requires them and the user explicitly benefits from seeing those items together.
* Do not hide poor information architecture behind tiny text, excessive columns, compressed cards, or tightly packed controls.
* Horizontal scrolling should only be used when it is genuinely appropriate for the content itself, such as timelines, media carousels, or very large data tables that cannot reasonably be represented another way.

# Git Safety

* Do not perform Git mutations unless I explicitly instruct you to do so.
* Do not commit, push, force-push, merge, rebase, reset, create or delete branches or tags, modify remotes, or perform other Git operations that change repository history or remote state unless explicitly instructed.
* Do not perform operations that require my Git credentials, SSH keys, access tokens, signing keys, or other Git authentication unless I explicitly instruct you to do so.
* Never assume permission to push changes because you were asked to modify code.
* Local code changes are allowed when requested. Git history and remote repositories should remain untouched unless explicitly requested.
* Read-only Git inspection such as `git status`, `git diff`, `git log`, and `git show` is allowed when useful.

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

# Image Capture and Reading

* Before reading or sending an image, create and use an optimized local derivative whenever the capture path allows it. Preserve the original capture in `./tmp/` for escalation, but do not send or read it by default, especially when the original is multi-megabyte PNG data.
* Use a maximum-edge resize rather than forcing a square image. A geometry such as `1280x1280>` means: fit within a 1280-by-1280 box, preserve aspect ratio, and never enlarge a smaller image.
* For `agent-browser`, configure the capture itself as JPEG quality 70 where possible so multi-megabyte PNGs are not produced for transmission. Prefer a WebP quality-70 derivative when the receiving tool accepts WebP, use `--if-changed` for repeated captures, and keep browser captures around a 1280-pixel maximum edge by default.
* For Android CLI and hybrid CLI/device capture paths, capture the required native PNG, then create an optimized WebP quality-70 derivative before reading or sending it. The native PNG remains local for escalation only. Use a 1280-pixel maximum edge for general UI inspection and 1600 pixels when mobile text needs more detail.
* For other images, use WebP quality 70 by default. Use PNG or lossless WebP for diagrams, line art, screenshots with tiny text, or pixel-accurate comparisons where lossy compression could obscure detail.
* For full-page browser evidence, capture the full page as required, then read an optimized derivative or targeted crops instead of repeatedly sending the largest original image.
* If the optimized image is unclear, do not upscale the entire image by default. Re-read only the relevant crop at higher resolution, using the preserved native/original capture when necessary. This override is permitted without additional confirmation for dense grids, small repeated items, tiny text, or any localized region that cannot be interpreted confidently.
* Treat higher-resolution rereads as an exception. In normal cases, remain at the standard optimized resolutions because most UI state and layout information is sufficiently visible there.

# Text-First UI Interaction and CLI Preferences

* Prefer structured text and accessibility data over screenshots whenever it is available. Transmitting and reasoning over text is usually faster and less data-intensive than capturing, uploading, and reading images.
* For Android CLI workflows, use `android layout`, UI text, element metadata, and other device inspection commands before taking a screenshot. Use screenshots for visual-only information, layout verification, rendering issues, or when structured inspection cannot answer the question.
* For `agent-browser`, use accessibility snapshots, text extraction, semantic locators, DOM attributes, and page evaluation for navigation and interaction whenever they provide the needed information. Do not take a screenshot merely to locate or click ordinary text or controls.
* Use screenshots when visual appearance matters, the accessibility/DOM representation is incomplete, an image or canvas is the subject, or text-first inspection is ambiguous. Apply the image-optimization rules before reading or sending those screenshots.
* For Cloudflare tasks, prefer the Cloudflare CLI and structured command output over browser navigation. If authentication is required, pause and ask the user to authenticate through the CLI or its normal login flow; never request or expose credentials, tokens, or secrets in chat or command output.
