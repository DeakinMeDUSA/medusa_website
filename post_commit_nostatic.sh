#!/bin/bash
# To run after a commit to the main branch

set -euo pipefail # Exit on any non-zero exit code, and error on use of undefined var
source "$HOME"/.poetry/env

cd "$HOME"/medusa_website || exit
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

printf 'Running migrations ...'
python manage.py migrate

printf 'Restarting application and flushing cache...'
# sudo systemctl restart gunicorn.socket gunicorn.service
# sudo systemctl daemon-reload
redis-cli FLUSHDB
sudo systemctl restart gunicorn
# sudo systemctl reload nginx
echo
