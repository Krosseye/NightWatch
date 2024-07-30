#!/bin/bash

# Fail on errors.
set -e

# Source .bashrc if it exists
if [ -f /root/.bashrc ]; then
    . /root/.bashrc
fi

# Set working directory to /app/src unless SRCDIR env var is defined
WORKDIR=${SRCDIR:-/app}

# Navigate to the working directory
cd $WORKDIR

# Install requirements if requirements.txt exists
if [ -f /app/requirements.txt ]; then
    pip install -r /app/requirements.txt
fi

# Run build.py if no arguments are passed to the entrypoint script
if [[ "$@" == "" ]]; then
    python /app/build.py
else
    sh -c "$@"
fi
