#!/bin/bash
set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
source "$SCRIPT_DIR/env_config.sh" # Sets MEDUSA_WEBSITE_VENV and MEDUSA_WEBSITE_ROOT vars
if [[ $# -eq 0 ]]; then
  DB_BACKUPS_DIR="$MEDUSA_WEBSITE_ROOT/backups/db"
  DB_TO_IMPORT="$(find "$DB_BACKUPS_DIR" -type f -printf "%T@ %p\n" | sort -n | cut -d' ' -f 2- | tail -n 1)"
  echo "No path to .sql file given, using latest file : $DB_TO_IMPORT"
else
  DB_TO_IMPORT="$1"
fi
echo "Attempting import of file $DB_TO_IMPORT"
pg_restore --dbname medusa_website --no-owner --clean "$DB_TO_IMPORT"
