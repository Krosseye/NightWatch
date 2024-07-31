#!/bin/bash

# Fail on errors.
set -e

# Source .bashrc to ensure environment variables are loaded
. ~/.bashrc

# Set working directory to /app unless SRCDIR env var is defined
WORKDIR=${SRCDIR:-/app}

# Change to the working directory
cd $WORKDIR

# Install dependencies if requirements.txt is present
[ -f requirements.txt ] && pip3 install -r requirements.txt

# Run build.py if no arguments are passed to the entrypoint script
if [ -z "$@" ]; then
    python build.py
else
    exec "$@"
fi
