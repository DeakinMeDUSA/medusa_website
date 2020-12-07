# shellcheck disable=SC1090
yarn install --ignore-engines
source ~/.virtualenvs/affinda/bin/activate
yarn build
../manage.py collectstatic
sudo supervisorctl restart resumes:
