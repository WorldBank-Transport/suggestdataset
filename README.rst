=============================================================
A simple app for collecting suggestions for datasets release
=============================================================

Writen using `Python <https://www.python.org/>`_/`Django <https://www.djangoproject.com/>`_

Demo Instance: https://suggestdataset.herokuapp.com/


This is a typical Django app and since there are a lot of Python/Django
resources online therefore you can always find more information on how
Django works and how develop and to deploy projects by using it.

    Note: The default database for this project is `PostgresSQL`.

The source code also include sample helper script for starting Gunicorn (`bin/start_gunicorn`)
and sample cofiguration files for `Gunicorn`, `Nginx` and `Supervisor` in `conf/` folder.


=========
Features
=========

- Dataset suggestion form
- Datasets suggestions list with status filter
- Upvoting/Downvoting approved suggestions
- Comment thread for dataset suggestion with an indicator for staff comments
- Admin/Management interface, accessible via ``/admin``
- General feedback/contact form
- Email notifications for feedback
- Multilingual support (default: English and Swahili)
- Bulk data export


============================================================
Sample installation on Ubuntu or other debian based systems
============================================================

Install the database engine
----------------------------

To install PostgreSQL and its client API run :-

::

    sudo apt-get install postgresql postgresql-contrib libpq-dev

Make sure the Postgresql server is running

::

    sudo service postgresql start

Configuring the database
------------------------

Login as `postgres` (Postgresql admin user)

::

    sudo su - postgres

While logged in as `postgres` create the database 

::

    createdb suggestdataset

Connect to the database shell

::

    psql suggestdataset

While you are in the database shell create the database user and grant appropriate privillages to the user.

::

    CREATE USER suggestdataset WITH PASSWORD '<your_dbuser_password>';
    GRANT ALL PRIVILEGES ON DATABASE suggestdataset TO suggestdataset;
    exit;

Logout as `postgres` user

::

    exit

Remember the database details especially the database user
password used in this stage because they are going to be
used in configuring your project later

You can also use other database engines including `SQLite`, `MySql` and `Oracle`.
However the default project dependancies includes the python database driver for PostgresSQL (`psycopg2`) only, therefore
if you want to use another database engine apart from PostgreSQL and SQLite you will have to install its respective python client library.
( probably replace `psycopg2` with the required database driver in `requirements.txt` ).


`SQLite` is the altenative database which is the easiest to use, suitable for development but not for production use.

To install SQLite you can run

::

    sudo apt-get install sqlite3 libsqlite3-dev


With SQLite you don't need to create a *database* or a *database user* in advance.


Setting the python environment
------------------------------
Install `pip`, `virtualenv` and `virtualenvwrapper` into your system

::

    sudo apt-get update
    sudo apt-get install python-dev python-pip

If you already had an old version of pip installed  you may need to upgrade to a newer version.

::
    sudo pip install -U pip

Then using pip

::

    sudo pip install virtualenv virtualenvwrapper


Virtualenvwrapper is an optional but very convenient when working
with python virtual enviroments especially during development.
To use virtualenvwrapper you may need to make some few configurations to
your system according to its documentation http://virtualenvwrapper.readthedocs.io/en/latest/install.html#shell-startup-file/ .

For example on ubuntu you may need to create or edit ``~/.bashrc`` or ``~/.profile`` and add the following lines

::

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh


You may need to start a new terminal session for the above changes to take effect.

Create virtualenv for your project
__________________________________
Assuming you have virtualenvwrapper properly installed and you want to call your
virtual enviroment `suggestdataset` you can run

::

    mkvirtualenv suggestdatset

Getting the source code
_______________________
Download the source code archive and extract its content to your working directory

**OR**

Move to the directory where you want to your source code to live
then clone the github repository

::

    git clone https://github.com/WorldBank-Transport/suggestdataset.git

Go to project root

::

    cd suggestdataset

use pip to install project requirements

::

    pip install -r requirements.txt


Preparing the Project
______________________

Add file named `.env` within the project root for configuring your local settings

::

    touch .env


Traditionally in Django project settings are configured in `settings.py` file
within the project module but for convenience `"suggestdataset"` allows passing
settings through enviroment variables or by configuring enviroment variables
in a file named .env in your project root directory. Project .env file is not
tracked by Git.


Add local environment settigs to `.env` , example

::

    DEBUG=True

    DATABASE_ENGINE='django.db.backends.postgresql_psycopg2'

    DATABASE_NAME=suggestdataset

    DATABASE_USER=suggestdataset

    DATABASE_PASSWORD='<your_dbuser_password>'


You can also add other configuratiuons, example

::

    SECRET_KEY='Xxxxxxx-your-s3cr3t-xxxxxxxxxxxxxxxxxx'

    ALLOWED_HOSTS='localhost suggestdataset.example.com'

    DATABASE_ENGINE='django.db.backends.postgresql_psycopg2'

    DATABASE_NAME=suggestdataset

    DATABASE_USER=suggestdataset

    DATABASE_PASSWORD='<your_dbuser_password>'

    DATABASE_HOST='localhost'

    DATABASE_PORT='5432'

    DATABASE_CONN_MAX_AGE=10

    STATIC_ROOT='/var/www/suggestdataset/static'

    STATIC_URL='http://suggestdataset.example.com/static/'

    MEDIA_ROOT='/var/www/suggestdataset/media'

    MEDIA_URL='http://suggestdataset.example.com/media/'

    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'

    EMAIL_USE_TLS='true'

    EMAIL_HOST='smtp.example.com'

    EMAIL_HOST_USER='mailboxuser'

    EMAIL_HOST_PASSWORD='XXXXXXXX'

    DEFAULT_FROM_EMAIL='mail@example.com'

    SERVER_EMAIL='server@example.com'

    ADMINS='Admin:admin@example.com, Other Admin:admin2@example.com'


Check if things are ok

::

    python manage.py check

Create database tables

::

    python manage.py migrate

Create project admin/superuser

::

    python manage.py createsuperuser



Starting the development server
________________________________

Django comes with an inbuilt server which can be user during testing or development. You shouldn't be using this server on production sites.
To start the deveopment server you can run

::

    python manage.py runserver 8000

Now you will be able to access local site via http://127.0.0.1:8000


Deployment (Gunicorn, Nginx, Supervisor and PostgreSQL)
--------------------------------------------------------

Since this is a typical Django application any standard Django deployment stack can be used

One of the most common Django deployment stacks is

:Web/Proxy server: Nginx
:Application server: Gunicorn or uWSGI
:Process manager: supervisor (Especially when using Gunicorn)
:Database engine: Postgresql

The basic steps for deploymnent could be

- Installing system wide packages
- Configuring the database
- Creating python virtualenv
- Getting the source code
- Configure project settings
- Install project Python requirements within virtualenv
- Create database tables
- Collect static files
- Configure application server
- Configure web server
- Configure process manager
- Restart services

Some of the steps for deployment as similar as in development setup but some are a bit different.

To install system wide packages you can run

::

    sudo apt-get install postgresql postgresql-contrib libpq-dev python-dev python-pip python-virtualenv python-virtualenvwrapper supervisor  nginx

You can put your source code and virtualenv wherever you feels better for you and in this case we will put our virtualenv and our suggest dataset within a directory called `/opt/`.

Create an `/opt/` directory if it doesn't exist

::

    mkdir /opt/
    cd /opt/

Create Virtualenv

::

    mkdir virtualenv
    cd /opt/virtualenv
    mkvirtualenv suggestdataset

Clone the sorce code

::

    cd /opt/
    git clone https://github.com/WorldBank-Transport/suggestdataset.git

Create deployment configurations in `/opt/suggestdataset/.env` file


Within the virtual enviroment

::

    cd /opt/suggestdataset
    pip install requirements-gunicorn.txt 
    python manage.py migrate
    python manage.py collectstatic --no-input

Use the included helper script to test the application server

::

    ./bin/start_gunicorn

If things are ok you will see Gunicorn running without an error and you can stop it by pressing `Ctr-C`

Configure Nginx as a proxy server, copy `conf/nginx/suggestdataset.conf` to `/etc/nginx/sites-available/` and modify it as necessary to reflect your current setup.

::

    cp /opt/suggestdataset/conf/nginx/suggestdataset.conf /etc/nginx/sites-available/

Enable the site on Nginx

::

    ln -s /etc/nginx/sites-available/suggestdataset.conf /etc/nginx/sites-enabled/suggestdataset.conf

Copy supervisor configurations to `/etc/supervisor/conf.d/` folder and
update it as necessary to reflect your actual deployment setup

::

    cp /opt/suggestdataset/conf/supervisor/suggestdataset_gunicorn.conf /etc/supervisor/conf.d

Restart services

::

    sudo service supervisor restart
    sudo service nginx restart

