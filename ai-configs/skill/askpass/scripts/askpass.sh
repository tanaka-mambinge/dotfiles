#!/bin/bash
# SUDO_ASKPASS helper - reads password from environment or file

# Option 1: Read from environment variable
if [ -n "$SUDO_PASSWORD" ]; then
    echo "$SUDO_PASSWORD"
    exit 0
fi

# Option 2: Read from file
if [ -f "$HOME/.sudo_password" ]; then
    cat "$HOME/.sudo_password"
    exit 0
fi

# Option 3: Use a default password (not recommended for security)
# echo "yourpassword"

exit 1
