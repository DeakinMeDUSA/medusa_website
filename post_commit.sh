# To run after a commit to the main branch
function tc_progress() {
    printf "%%steamcity[progressMessage '%%s']" '##' "$1"
}

# shellcheck disable=SC2164
cd ~/medusa_website
source ~/.virtualenvs/medusa_website/bin/activate
echo

tc_progress 'Fetching changes from Git ...'
git pull && git checkout main
echo

tc_progress 'Updating Python dependencies ...'
pip install -r requirements.txt
echo

#tc_progress 'Updating Node.js dependencies ...'
#npm install
#echo

tc_progress 'Collecting static files ...'
python manage.py collectstatic --noinput

tc_progress 'Running migrations ...'
python manage.py migrate

tc_progress 'Restarting application ...'
sudo systemctl restart gunicorn
echo
