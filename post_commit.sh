# To run after a commit to the main branch

# shellcheck disable=SC2164
cd ~/medusa_website
source ~/.virtualenvs/medusa_website/bin/activate
echo

printf 'Fetching changes from Git ...'
git fetch --all
git reset --hard origin/main
echo

printf 'Updating Python dependencies ...'
pip install -r requirements_prod.txt
echo

printf 'Updating Node.js dependencies ...'
npm install
echo

printf 'Collecting static files ...'
python manage.py collectstatic --noinput

printf 'Running migrations ...'
python manage.py migrate

printf 'Restarting application ...'
sudo systemctl restart gunicorn
echo
