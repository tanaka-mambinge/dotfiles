---
name: dev-servers
description: Choose development-server ports for Laravel, React, FastAPI, and messaging-channel chatbot projects, and expose a local MCP server through Cloudflare Tunnel when remote agent testing is requested. Use the shared port convention only when the user has not specified a port; leave unclear and other application types on their framework default.
---

# Dev Servers

Use this skill when starting or running a development server and the request does not already specify a port. Also use the Cloudflare Tunnel guidance when the user asks to make a local MCP server reachable to a remote agent.

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

## Expose a local MCP server with Cloudflare Tunnel

Use this only when remote access to a local MCP server is requested. Identify the MCP HTTP port from the project, and route only that service through the tunnel. Do not expose the website or API as a side effect. Reuse a healthy named tunnel already connected to the machine before creating another. Use a persistent hostname for ongoing agent use; use a Quick Tunnel only when the user explicitly wants a temporary test.

In the Cloudflare dashboard:

1. Open **Networking → Tunnels** and check for an existing healthy tunnel connected to the MCP machine. Add the published application route to that tunnel when possible.
2. Create a named tunnel only if no suitable existing tunnel is available. Choose the server environment, run Cloudflare's connector setup on the MCP machine, and keep tunnel tokens out of chat and source files.
3. Add a **Published application** route with a hostname in a domain managed by Cloudflare and a service URL of `http://127.0.0.1:<MCP_PORT>`.
4. Keep the connector running and configure the MCP server's allowed host, resource URL, OAuth audience, and client connection URL for that hostname.

### Persistent routes on this workstation

| Project | Tunnel | Public MCP URL | Local service |
| --- | --- | --- | --- |
| YouTube Planner | `Dev tunnels` | `https://dev-mcp.iamt12e.co.zw/mcp` | `http://127.0.0.1:8277` |

For YouTube Planner, use the existing route and hostname above. Its OAuth issuer is `https://dev-mcp.iamt12e.co.zw`, and its audience and resource URL are `https://dev-mcp.iamt12e.co.zw/mcp`. Keep the route limited to the MCP service; the website and API stay local.

If the dashboard requires authentication, let the user sign in through the normal browser flow. A named public hostname also requires a domain managed by the Cloudflare account. Do not ask the user to share credentials or tokens in chat.

For an explicitly requested temporary test, a Cloudflare Quick Tunnel can be started with:

```sh
cloudflared tunnel --no-autoupdate --url http://127.0.0.1:<MCP_PORT> --http-host-header 127.0.0.1:<MCP_PORT>
```

Keep the command running while the agent uses the printed HTTPS `trycloudflare.com` URL. The URL is temporary and changes when the process restarts; stop the process to close the tunnel. Cloudflare documents that Quick Tunnels do not support SSE, so they are not the default for full MCP use.

Cloudflare Tunnel provides network routing only. Keep the MCP server's own authentication and scopes enabled; do not disable authentication to make remote calls work. A tunnel does not configure OAuth or make a private development token usable by a remote client.
