---
name: dev-servers
description: Choose the development-server port for Laravel monoliths, React web applications, FastAPI APIs, and messaging-channel chatbot integrations when starting, running, serving, or hosting them locally. Use the shared port convention only when the user has not specified a port; leave unclear and other application types on their framework default.
---

# Dev Servers

Use this skill when starting or running a development server and the request does not already specify a port. It is provider-neutral and does not configure Cloudflare APIs, DNS, tunnels, or deployments.

## Port convention

For this convention, a chatbot means an application or integration for a messaging channel such as WhatsApp, Telegram, Messenger, or a similar platform. An AI agent used only through a web UI or API does not count as a chatbot.

Choose the port from the framework and service shape:

| Project type | Messaging chatbot present | No messaging chatbot |
| --- | ---: | ---: |
| Laravel monolith | `8205` | `8207` |
| React web application | `8207` | `8207` |
| FastAPI API | `8205` | `8206` |

For a React and FastAPI project, run the React web application on `8207`. Run the FastAPI service on `8205` when it handles a messaging-channel chatbot and on `8206` otherwise.

Unclear app types and all other applications have no assigned port; use the framework or tool's normal default.

An explicit user-provided port always takes precedence over this convention. Pass the selected port using the project's framework-native command-line flag or environment variable, without changing project configuration unless the user asks for that change.

Before starting a mapped server, check whether its port is already occupied when practical. If it is occupied, report the conflict and ask whether to stop the existing process or use another port; do not silently select a nearby port or fall back to the framework default.
