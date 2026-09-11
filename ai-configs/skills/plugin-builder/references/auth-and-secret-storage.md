# Authentication and secret storage

## End-user login

Use a user-driven browser flow:

1. The binary starts a short-lived loopback callback server.
2. It opens a login page containing a single-use opaque state token.
3. The user enters credentials directly into that page.
4. The server exchanges the credentials for a session.
5. The binary stores the session in the OS keyring and closes the temporary flow.

The agent must never type credentials, ask the user to paste a password into chat, infer a password, or reuse a token from a URL or previous conversation.

The completion page should say what the user needs to know, for example “Your account is connected. You can close this page and return to the request.” Do not expose implementation details such as “your token was saved in the OS keyring”.

## Storage rules

| Secret | Location | Rule |
|---|---|---|
| User session/refresh token | OS keyring | Namespace by plugin and account; never log it |
| One-time login state | Memory or short-lived secure store | Expire and consume it once |
| API base URL | Compiled product default | Allow a developer override only when explicitly useful |
| Server credentials | Deployment secret manager | Never ship them in the plugin or CLI |
| Release credentials | GitHub Actions secrets/token | Never put them in workflow files |

Logout must delete local credentials even if the remote logout call fails. On invalid or expired sessions, clear the keyring entry promptly and send the user through login again.

