#!/bin/bash -i

# Add path
# echo 'export PATH=$PATH:$HOME/.pyenv/versions/$(ls $HOME/.pyenv/versions/)/bin/' >> ~/.bashrc

# Fail on errors.
set -e

# Make sure .bashrc is sourced
. /root/.bashrc

# Allow the workdir to be set using an env var.
# Useful for CI pipiles which use docker for their build steps
# and don't allow that much flexibility to mount volumes
WORKDIR=${SRCDIR:-/app}
# Allow the user to specify the spec file
# Sometimes there are 2 executables to be built from one
# folder, this allows the user to specify which one
# should we build.
# In case it's not defind, find the first match for `*.spec`
# In case the user specified a custom URL for PYPI, then use
# that one, instead of the default one.

cd $WORKDIR

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
fi # [ -f requirements.txt ]

echo "$@"

# Run build.py if no arguments are passed to the entrypoint script
if [[ "$@" == "" ]]; then
    python /app/build.py
else
    sh -c "$@"
fi
