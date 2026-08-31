---
name: dev-servers
description: Choose the development-server port for chatbot, API, and web applications when starting, running, serving, or hosting them locally. Use the shared port convention only when the user has not specified a port; leave unclear and other application types on their framework default.
---

# Dev Servers

Use this skill when starting or running a development server and the request does not already specify a port. It is provider-neutral and does not configure Cloudflare APIs, DNS, tunnels, or deployments.

## Port convention

Choose the port from the service's primary role:

| Primary role | Port |
| --- | ---: |
| Chatbot application | `8205` |
| API-only application | `8206` |
| Web application | `8207` |

Unclear app types and all other applications have no assigned port; use the framework or tool's normal default.

An explicit user-provided port always takes precedence over this convention. Pass the selected port using the project's framework-native command-line flag or environment variable, without changing project configuration unless the user asks for that change.

Before starting a mapped server, check whether its port is already occupied when practical. If it is occupied, report the conflict and ask whether to stop the existing process or use another port; do not silently select a nearby port or fall back to the framework default.
