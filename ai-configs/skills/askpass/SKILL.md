---
name: askpass
description: Set up and use SUDO_ASKPASS helpers for non-interactive sudo operations. Use when automating commands that require sudo privileges, setting up passwordless sudo alternatives, or configuring sudo to work in CI/CD or headless environments.
---

# SUDO_ASKPASS Helper

This skill provides a script and guidance for using SUDO_ASKPASS to enable sudo operations without interactive password prompts.

## Overview

SUDO_ASKPASS allows sudo to read passwords from a helper script instead of prompting interactively. This is essential for:
- CI/CD pipelines requiring sudo
- Automated scripts that need elevated privileges
- Docker/container environments where TTY isn't available
- Headless/automated server management

## Setup

The askpass script is bundled with this skill at `scripts/askpass.sh`.

### Step 1: Set the password

Option 1 - Environment variable:
```bash
export SUDO_PASSWORD="your_password_here"
```

Option 2 - Password file:
```bash
echo "your_password_here" > "$HOME/.sudo_password"
chmod 600 "$HOME/.sudo_password"
```

### Step 2: Use sudo with -A flag

```bash
export SUDO_ASKPASS="$HOME/.config/opencode/skill/askpass/scripts/askpass.sh"
sudo -A apt-get update
```

## Quick Usage

```bash
# One-time command
SUDO_PASSWORD="mypass" SUDO_ASKPASS="$HOME/.config/opencode/skill/askpass/scripts/askpass.sh" sudo -A command

# Session-wide
export SUDO_ASKPASS="$HOME/.config/opencode/skill/askpass/scripts/askpass.sh"
export SUDO_PASSWORD="mypass"
sudo -A apt-get update
sudo -A apt-get install package
```

## In Scripts

```bash
#!/bin/bash
set -e

ASKPASS_SCRIPT="$HOME/.config/opencode/skill/askpass/scripts/askpass.sh"

if [ "$EUID" -ne 0 ]; then
    export SUDO_ASKPASS="$ASKPASS_SCRIPT"
    SUDO="sudo -A"
else
    SUDO=""
fi

$SUDO apt-get update
$SUDO apt-get install -y package
```

## Install TeX for PDF Export

To export Jupyter notebooks to PDF:

```bash
export SUDO_ASKPASS="$HOME/.config/opencode/skill/askpass/scripts/askpass.sh"
export SUDO_PASSWORD="your_password"
sudo -A apt-get update
sudo -A apt-get install -y texlive-xetex texlive-fonts-recommended texlive-plain-generic
```

## Security Considerations

1. **Environment variables**: May be visible in process lists (`ps aux`) or logged
2. **Password files**: Should have restricted permissions (`chmod 600`)
3. **Scripts**: Avoid hardcoding passwords directly in scripts
4. **CI/CD**: Use secrets management (GitHub Actions secrets, etc.)

## Troubleshooting

- **"sudo: no askpass program specified"**: Ensure `SUDO_ASKPASS` is exported
- **"sudo: 3 incorrect password attempts"**: Check `SUDO_PASSWORD` or `~/.sudo_password` contents
- **Permission denied**: Ensure script is executable (`chmod +x`)

## Reference

The askpass script supports:
- `SUDO_PASSWORD` environment variable
- `~/.sudo_password` file
- Falls back to exit 1 if neither is set
