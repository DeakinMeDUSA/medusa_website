#!/bin/bash
set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "$SCRIPT_DIR/env_config.sh" # Sets MEDUSA_WEBSITE_VENV and MEDUSA_WEBSITE_ROOT vars

psql medusa_website < "$DATABASE_BACKUP_FILE"
