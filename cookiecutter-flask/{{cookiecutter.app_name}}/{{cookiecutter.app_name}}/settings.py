# -*- coding: utf-8 -*-
import os
import uuid

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env.get('{{cookiecutter.app_name|upper}}_SECRET', '66ts8yrQAW7wAhX9de')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_PASSWORD_SALT = 'BYNqjRtVKc7dRTVdi3'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_RESET_PASSWORD_WITHIN = '26 hours'
    SECURITY_CONFIRM_EMAIL_WITHIN = '26 hours'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_RECYCLE = 280

class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://{{cookiecutter.db_user}}:{{cookiecutter.db_password}}@{{cookiecutter.db_server}}:3306/{{cookiecutter.app_name}}'  # TODO: Change me
    DEBUG_TB_ENABLED = False
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    {{cookiecutter.app_name|upper}}_ID_UUID_NAMESPACE = uuid.UUID('8f0e61f4-9f04-313e-b83e-1586d0e395ae')
    TWEETWALLBOARD_DOMAIN = 'tweetwallboard.com'
    

class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://{{cookiecutter.db_user}}:{{cookiecutter.db_password}}@localhost:3306/{{cookiecutter.app_name}}'
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    {{cookiecutter.app_name|upper}}_ID_UUID_NAMESPACE = uuid.UUID('afd0b036-625a-3aa8-b639-9dc8c8fff0ff')
    TWEETWALLBOARD_DOMAIN = 'localhost'
    

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    TWEETWALLBOARD_DOMAIN = 'localhost'
    {{cookiecutter.app_name|upper}}_ID_UUID_NAMESPACE = uuid.UUID('eed0b036-725a-4aa8-4639-ccc8c8fff0ff')
    