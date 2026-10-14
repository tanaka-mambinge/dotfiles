---
name: gnome-shell-extension
description: Create, edit, and test GNOME Shell extensions using the installed Mutter Development Kit.
---

# GNOME Shell Extension Development

Use this skill when creating, changing, or testing a GNOME Shell extension.

- Inspect the extension's `metadata.json` and follow its supported GNOME Shell versions and existing project commands.
- Run and test the extension in a nested Mutter Devkit session, using `dbus-run-session gnome-shell --wayland --devkit`. See the [upstream Devkit workflow](https://github.com/GNOME/mutter/blob/main/doc/building-and-running.md#running-a-nested-instance) when needed.
- Keep testing isolated from the user's current GNOME session.
- Follow the project's existing structure and keep changes focused on the requested extension work.
