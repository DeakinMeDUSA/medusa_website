MeDUSA Website
==============

Website for MeDUSA, Deakin University's medical student society, [hosted here](https://www.medusa.org.au)

License
:   MIT


Installation
------------
With `python` ≥ 3.8 installed:
```shell
poetry install
```
Setting up database, run `psql` then:
```postgresql
CREATE ROLE medusa_it LOGIN SUPERUSER
```
Open psql with new user:
```shell
psql postgres -U medusa_it
```
And create a new database:
```postgresql
CREATE DATABASE medusa_website;
GRANT ALL PRIVILEGES ON DATABASE medusa_website TO medusa_it;
```
Then run migrations
```shell
python manage.py migrate
```




Usage
-----

To activate the virtualenv
```shell
poetry shell
```

To get a django console
```shell
poetry shell
python start_console.py
```


Settings
--------

Moved to
[settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you'll see a "Verify Your E-mail
    Address" page. Go to your console to see a simulated email
    verification message. Copy the link into your browser. Now the
    user's email should be verified and ready to go.
-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy medusa_website

### Test coverage

To run the tests, check your test coverage, and generate an HTML
coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with py.test

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS
compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).
