#!/bin/bash
# To run after a commit to the main branch
set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var

cd "$HOME"/medusa_website || exit

printf '\nRunning backup script'
printf '\n%80s\n' | tr ' ' -
./scripts/backup_db.sh
echo

printf '\nFetching changes from Git'
printf '\n%80s\n' | tr ' ' -
git fetch --all
git reset --hard origin/main
echo

printf '\nUpdating Python dependencies'
printf '\n%80s\n' | tr ' ' -
poetry install
echo

printf '\nUpdating Node.js dependencies'
printf '\n%80s\n' | tr ' ' -
npm install
echo

printf '\nCollecting static files'
printf '\n%80s\n' | tr ' ' -
poetry run python ./manage.py collectstatic --noinput

printf '\nRunning migrations'
printf '\n%80s\n' | tr ' ' -
poetry run python ./manage.py migrate

printf '\nRestarting application and flushing cache'
printf '\n%80s\n' | tr ' ' -
# sudo systemctl restart gunicorn.socket gunicorn.service
# sudo systemctl daemon-reload
redis-cli FLUSHDB

# Restart web and celery services
sudo systemctl restart gunicorn
sudo systemctl restart celery.service
sudo systemctl restart celerybeat.service
# sudo systemctl reload nginx

echo "Post commit script complete!"
