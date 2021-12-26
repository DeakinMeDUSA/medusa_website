#!/bin/bash
# To run after a commit to the main branch
set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var

cd ~/medusa_website || exit
poetry shell
echo

printf 'Fetching changes from Git ...'
git fetch --all
git reset --hard origin/main
echo

printf 'Updating Python dependencies ...'
poetry install
echo

printf 'Updating Node.js dependencies ...'
npm install
echo

printf 'Collecting static files ...'
python manage.py collectstatic --noinput

printf 'Running migrations ...'
python manage.py migrate

printf 'Restarting application and flushing cache...'
redis-cli FLUSHDB
sudo systemctl restart gunicorn
echo
