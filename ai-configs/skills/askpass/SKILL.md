---
name: askpass
description: Use this skill whenever you need to execute commands requiring elevated sudo privileges. Automatically handles non-interactive sudo operations via SUDO_ASKPASS—no manual command composition needed. Apply for automated tasks, CI/CD pipelines, headless environments, and any scenario where interactive password prompts aren't feasible.
---

# SUDO_ASKPASS Helper

Execute sudo commands non-interactively using the pre-configured SUDO_ASKPASS helper script.

## Overview

SUDO_ASKPASS enables sudo operations without interactive password prompts by reading credentials from a helper script. Use this skill when:

- Executing commands that require elevated privileges in a script
- Running tasks in CI/CD pipelines
- Working in headless/automated environments
- Avoiding interactive TTY prompts

## Usage

### Single Command

```bash
SUDO_ASKPASS="$HOME/.config/opencode/skill/askpass/scripts/askpass.sh" sudo -A command
```

### In Scripts

When executing multiple sudo commands, set the environment variable once:

```bash
#!/bin/bash
set -e

export SUDO_ASKPASS="$HOME/.config/opencode/skill/askpass/scripts/askpass.sh"

sudo -A apt-get update
sudo -A apt-get install -y package
sudo -A systemctl restart service
```

### Conditional sudo in Scripts

Use only when necessary (already root vs. needs elevation):

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

## Reference

The askpass helper reads credentials from:

- `SUDO_PASSWORD` environment variable (preferred for immediate execution)
- `~/.sudo_password` file (if environment variable not set)
