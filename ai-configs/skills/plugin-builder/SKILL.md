---
name: plugin-builder
description: Build standalone ChatGPT plugins around verified cross-platform binaries, user-driven browser login, OS keyring storage, GitHub Releases, and marketplace installation.
---

# Plugin Builder

Use this skill when creating or changing a ChatGPT plugin that users should install and operate without npm, PyPI, Go, Python, or shell commands.

This is a binary-first workflow learned from the Redan and Takealot plugins. The generated plugin is its own Git repository. Do not place it inside another repository's `plugins/` directory.

## Non-negotiable product shape

- Put `.codex-plugin/plugin.json` at the plugin repository root.
- Use Go for the companion CLI unless the user explicitly chooses another language.
- Publish static binaries through GitHub Releases for Linux, macOS, and Windows on AMD64 and ARM64.
- Let the agent download, checksum-verify, cache, and execute the matching binary. Do not make end users install a package manager or runtime.
- Default to human-readable output and provide normalized `--json` output for agent use.
- Store user sessions and refresh credentials in the OS keyring. Never put them in source, logs, plain config files, or required environment variables.
- Use a user-controlled browser login page with a short-lived opaque callback token. Never infer, collect, submit, or reuse credentials on the user's behalf.
- Keep server deployment secrets and CI secrets separate from end-user configuration.
- Do not publish, push, create releases, or change marketplace configuration unless the user explicitly requests that action.

## Build workflow

1. Inspect the target product, API, existing reference implementation, and repository state. Extract concrete lessons from Redan and Takealot instead of copying their historical nesting or accidental behavior.
2. Create a standalone plugin repository with the root layout in [repo-layout.md](references/repo-layout.md).
3. Define the user-facing skill and CLI contract before implementation. Keep the plugin name broad enough for its actual roadmap; do not name a general management plugin after its first feature.
4. Implement the binary, keyring-backed authentication, browser callback, API client, normalized errors, and links. Read [auth-and-secret-storage.md](references/auth-and-secret-storage.md) and [binary-distribution.md](references/binary-distribution.md) when those parts apply.
5. Add focused tests for command parsing, JSON output, platform selection, authentication state, secret redaction, API errors, and destructive-operation confirmation.
6. Add pull-request CI and tag-based release automation from [github-actions.md](references/github-actions.md).
7. Validate the manifest, run the complete test/build checks, inspect the generated release assets, and test installation from the remote repository when publishing is in scope.

## Marketplace and installation

The plugin manifest, agent instructions, binary distribution, login page, and marketplace entry are one product workflow. Keep them aligned and test the installed plugin from the actual remote repository.

Use a separate marketplace repository when multiple plugins must be listed together. Each plugin entry should reference its standalone repository directly; avoid a `git-subdir` source for a plugin that is meant to be independently installable. Read [marketplace-and-installation.md](references/marketplace-and-installation.md) for the failure modes seen with the Redan and Takealot layouts.

## Security and UX review

Before reporting completion, confirm that:

- no token, password, API key, OTP, cookie, or authorization header appears in logs, test output, error messages, screenshots, or committed files;
- browser copy speaks to the person completing login and does not expose internal terms such as “OS keyring”;
- the agent does not perform an external mutation without the user's confirmation when the operation is destructive or consequential;
- links come from API responses or verified canonical data, not guessed URL patterns;
- branding uses supplied assets and explicit brand guidance, not assumptions from a logo or external research;
- CI actually runs for the event it claims to cover, and release automation is not confused with pull-request validation.
