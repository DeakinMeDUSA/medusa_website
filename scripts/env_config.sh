#!/usr/bin/env bash
# Load .env file
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
echo "Using SCRIPT_DIR = $SCRIPT_DIR"
BASH_ERR_HANDLER="$HOME/tools/shell-core/base/trap.bash"
if test -f "$BASH_ERR_HANDLER"; then
  echo "Loading bash error handler from $BASH_ERR_HANDLER"
  source "$BASH_ERR_HANDLER"
else
  echo "Setting set -euo pipefail to exit on any non-zero exit code"
  set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var
fi

PARENT_PARENT_DIR="$(dirname "$SCRIPT_DIR")"

export PATH="$HOME/.poetry/bin:$PATH"

if test -f "$PARENT_PARENT_DIR/.env"; then
  set -o allexport
  source "$PARENT_PARENT_DIR/.env"
  set +o allexport
else
  echo "NO .env FILE FOUND at $PARENT_PARENT_DIR/.env"
fi

if [ -z "${MEDUSA_WEBSITE_ROOT-}" ]; then
  MEDUSA_WEBSITE_ROOT="/home/$USER/medusa_website"
fi

cd "$MEDUSA_WEBSITE_ROOT" # So that poetry env works
# Set VENV and REPO variables if not defined previously
if [ -z "${MEDUSA_WEBSITE_VENV-}" ]; then
  MEDUSA_WEBSITE_VENV="$(poetry env info -p)"
fi
cd "$SCRIPT_DIR"

echo "Using MEDUSA_WEBSITE_VENV = $MEDUSA_WEBSITE_VENV"
echo "Using MEDUSA_WEBSITE_ROOT = $MEDUSA_WEBSITE_ROOT"
export MEDUSA_WEBSITE_VENV="$MEDUSA_WEBSITE_VENV"
export MEDUSA_WEBSITE_ROOT="$MEDUSA_WEBSITE_ROOT"

if test -f "$HOME/.ssh/id_rsa"; then
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_rsa
fi
