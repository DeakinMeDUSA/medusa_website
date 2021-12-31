#!/bin/bash
#set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var

# Load .env file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "Using SCRIPT_DIR = $SCRIPT_DIR"
export enable_trap_debug=1
source "$SCRIPT_DIR/lib.trap.sh"
PARENT_PARENT_DIR="$(dirname "$SCRIPT_DIR")"

export PATH="$HOME/.poetry/bin:$PATH"

if test -f "$PARENT_PARENT_DIR/.env"; then
  set -o allexport; source "$PARENT_PARENT_DIR/.env"; set +o allexport
else
  echo "NO .env FILE FOUND at $PARENT_PARENT_DIR/.env"
fi

if [ -z "${MEDUSA_WEBSITE_ROOT-}" ]; then
  MEDUSA_WEBSITE_ROOT="/home/$USER/medusa_website"
fi

cd "$MEDUSA_WEBSITE_ROOT"  # So that poetry env works
# Set VENV and REPO variables if not defined previously
if [ -z "${MEDUSA_WEBSITE_VENV-}" ]; then
  MEDUSA_WEBSITE_VENV="$(poetry env info -p)"
fi

echo "Using MEDUSA_WEBSITE_VENV = $MEDUSA_WEBSITE_VENV"
echo "Using MEDUSA_WEBSITE_ROOT = $MEDUSA_WEBSITE_ROOT"
export MEDUSA_WEBSITE_VENV="$MEDUSA_WEBSITE_VENV"
export MEDUSA_WEBSITE_ROOT="$MEDUSA_WEBSITE_ROOT"


eval "$(ssh-agent -s)"

if test -f "$HOME/.ssh/id_rsa"; then
    ssh-add ~/.ssh/id_rsa
fi
