#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
import os
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand
from flask_security import SQLAlchemyUserDatastore

from {{cookiecutter.app_name}}.app import create_app
from {{cookiecutter.app_name}}.user.models import User, Role
from {{cookiecutter.app_name}}.settings import DevConfig, ProdConfig, TestConfig
from {{cookiecutter.app_name}}.database import db

if os.environ.get("{{cookiecutter.app_name|upper}}_ENV") == 'dev':
    app = create_app(DevConfig)
elif os.environ.get("{{cookiecutter.app_name|upper}}_ENV") == 'test':
    app = create_app(TestConfig)
else:
    app = create_app(ProdConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.option('-r', '--role', dest='role', default=None)
@manager.option('-u', '--user', dest='user', default=None)
def AddRoleToUser(user, role):
    if user and role:
        user_datastore  = SQLAlchemyUserDatastore(db, User, Role)
        user_datastore.add_role_to_user(user, role)         # accepts these parms as strings, and does the finding. Handy.
        user_datastore.commit()
    else:
        print 'Fail AddRoleToUser with user or role parameters.'

@manager.option('-r', '--role', dest='role', default=None)
@manager.option('-d', '--desc', dest='desc', default=None)
def CreateRole(role, desc):
    if role and desc:
        user_datastore  = SQLAlchemyUserDatastore(db, User, Role)
        user_datastore.create_role(name=role, description=desc)
        user_datastore.commit()
    else:
        print 'Fail CreateRole with role or desc parameters'

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
