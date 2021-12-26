MeDUSA Website
==============

Website for MeDUSA, Deakin University's medical student society, [hosted here](https://www.medusa.org.au)

License
:   MIT

Installation
------------

### Pre-prerequisites

* [Python 3.9](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/)
* [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* [sass](https://sass-lang.com/install)
* [postgresql](https://www.postgresql.org/download/)
*

### Install

Install python requirements:

```shell
poetry install
```

Install node requirements

```shell
npm install
```

Create database, where `db_user` is the name of your user account:

```shell
sudo -u postgres psql
# Inside of psql shell
postgres=# create database medusa_website;
postgres=# create user db_user with encrypted password 'db_pass';
postgres=# grant all privileges on database mydb to db_user;
```

After creating, in the top level `.env` file, set the values to what you just used:

```shell
DATABASE_URL="postgres://localhost/medusa_website"
DATABASE_USER="db_user"
DATABASE_PASSWORD="db_pass"
```

Run migrations:

```shell
python shell # To activate virtualenv
python manage.py migrate
```

### Check install worked

```shell
python start_console.py
```

Settings
--------

Moved to
[settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "
  Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into
  your browser. Now the user's email should be verified and ready to go.
- To create an **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar),
so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy medusa_website

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with py.test

    $ pytest

### Live reloading and Sass CSS compilation

Moved
to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html)
.
