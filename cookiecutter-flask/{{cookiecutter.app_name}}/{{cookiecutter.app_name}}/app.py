# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from {{cookiecutter.app_name}}.settings import ProdConfig
from {{cookiecutter.app_name}}.assets import assets
from {{cookiecutter.app_name}}.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
    security,
    csrf,
    mail
)
from {{cookiecutter.app_name}} import public, user, {{cookiecutter.core_table_title|lower}}
from flask_security import SQLAlchemyUserDatastore
from {{cookiecutter.app_name}}.user.models import User, Role
from {{cookiecutter.app_name}}.user.forms import ExtendedResetPasswordForm
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, Personalization
import urllib2

def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)      

    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)
    security_ctx = security.init_app(app, SQLAlchemyUserDatastore(db, user.models.User, user.models.Role), reset_password_form=ExtendedResetPasswordForm)

@security_ctx.send_mail_task
    def send_email_override(msg):

        sg = sendgrid.SendGridAPIClient(apikey='SG.xxxxxxxxxx')

        #example data
        # data = {
        #   "personalizations": [
        #     {
        #       "to": [
        #         {
        #           "email": "test@example.com"
        #         }
        #       ],
        #       "subject": msg.subject
        #     }
        #   ],
        #   "from": {
        #     "email": "Acronis SCS<noreply@acronisscs.com>"
        #   },
        #   "content": [
        #     {
        #       "type": "text/plain",
        #       "value": msg.body
        #     },
        #                 {
        #       "type": "text/html",
        #       "value": msg.html
        #     }
        #   ]
        # }



        data = {
          "personalizations": [
            {
               "to": [],
              "subject": msg.subject
            }
          ],
          "from": {
            "email": "Acronis SCS<noreply@acronisscs.com>"
          },
          "content": [
            {
              "type": "text/plain",
              "value": msg.body
            },
                        {
              "type": "text/html",
              "value": msg.html
            }
          ]
        }

        for to in msg.recipients:
            #personalization.add_to(Email(to))
            if 'to' in data['personalizations'][0]:
                data['personalizations'][0]['to'].append( { "email": to })
                print data['personalizations'][0]['to']
            else:
                data['personalizations'][0]['to'] = [ { "email": to } ]

        try:
            response = sg.client.mail.send.post(request_body=data)
        except urllib2.HTTPError as e:
            error_message = e.read()
            print error_message

    return None



def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint({{cookiecutter.core_table_title|lower}}.views.blueprint)
    
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

