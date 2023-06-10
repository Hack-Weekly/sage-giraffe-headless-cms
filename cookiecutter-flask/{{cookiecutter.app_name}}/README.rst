===============================
{{ cookiecutter.project_name }}
===============================

{{ cookiecutter.project_short_description}}


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.  This is only needed in Production, for DEV an TEST you can use the defaults

.. code-block:: bash

    export {{cookiecutter.app_name|upper}}_SECRET='something-really-secret'

You will also need to set the environment variable to configure if this is dev, test or prod

Windows
.. code-block:: bash
    setx {{cookiecutter.app_name|upper}}_ENV "dev" -m

Linux
.. code-block:: bash
    export {{cookiecutter.app_name|upper}}_ENV='dev'

Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.app_name}}
    cd {{cookiecutter.app_name}}
    pip install -r requirements/dev.txt

if running windows install one of these from https://www.lfd.uci.edu/~gohlke/pythonlibs/:

        MySQL_python-1.2.5-cp27-none-win32.whl
        MySQL_python-1.2.5-cp27-none-win_amd64.whl

    bower install
    python manage.py server

You will see a pretty welcome screen.

To install the DBMS, run the sql commands in the scripts\db_create.sql file

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration:

::

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``{{cookiecutter.app_name|upper}}_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
