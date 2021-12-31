#!/bin/bash
set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "$SCRIPT_DIR/env_config.sh" # Sets MEDUSA_WEBSITE_VENV and MEDUSA_WEBSITE_ROOT vars

cd "$MEDUSA_WEBSITE_ROOT"

DB_BACKUPS_DIR="$MEDUSA_WEBSITE_ROOT/backups/db"
MEDIA_BACKUP_DIR="$MEDUSA_WEBSITE_ROOT/backups/media"

mkdir -p "$DB_BACKUPS_DIR"
cd "$DB_BACKUPS_DIR"
CURRENT_DATE="$(date +'%Y-%m-%d')"
echo "Backing up db to $DB_BACKUPS_DIR/$CURRENT_DATE.sql"
export PGPASSWORD="$DATABASE_PASSWORD"
pg_dump medusa_website -U "$DATABASE_USER" -h localhost > "$CURRENT_DATE.sql"


echo "Backing up media files to $MEDIA_BACKUP_DIR"
mkdir -p "$MEDIA_BACKUP_DIR"
cd "$MEDUSA_WEBSITE_ROOT"
# https://devhints.io/rsync
rsync -rtvh "$MEDUSA_WEBSITE_ROOT/medusa_website/media" "$MEDIA_BACKUP_DIR" --delete --delete-excluded

echo "Backup complete!"
