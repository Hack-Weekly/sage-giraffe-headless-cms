# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from marshmallow import Schema, fields, ValidationError


from flask import request
from   flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

from {{cookiecutter.app_name}}.extensions import bcrypt
from {{cookiecutter.app_name}}.extensions import security
from {{cookiecutter.app_name}}.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(SurrogatePK, Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    # id = Column(db.Integer, primary_key=True)
    # email = Column(db.String(80), unique=True, nullable=False)
    # #: The hashed password
    # password = Column(db.String(128), nullable=True)
    # locked = Column(db.Boolean, nullable=True, default=False)
    # lastlogin = Column(db.DateTime, index=True, default=dt.datetime.utcnow)
    # created_at = Column(db.DateTime, default=dt.datetime.utcnow, index=True)
    # modified_at = Column(db.DateTime, default=dt.datetime.utcnow, index=True)
    # confirmed_at = Column(db.DateTime, default=dt.datetime.utcnow, index=True)
    # first_name = Column(db.String(30), nullable=True)
    # last_name = Column(db.String(30), nullable=True)
    # active = Column(db.Boolean(), default=False)
    # is_admin = Column(db.Boolean(), default=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # def __init__(self, email, password=None, **kwargs):
    #     db.Model.__init__(self, email=email, **kwargs)
    #     if password:
    #         self.set_password(password)
    #     else:
    #         self.password = None

    # def set_password(self, password):
    #     self.password = bcrypt.generate_password_hash(password)

    # def check_password(self, value):
    #     result = bcrypt.check_password_hash(self.password, value)
    #     audit = LoginAudit()
    #     audit.user_id = self.id
    #     audit.ip = request.remote_addr
    #     audit.success = result
    #     now = dt.datetime.utcnow()
    #     audit.created_at = now
    #     if result:
    #         self.lastlogin = now
    #         db.session.add(self)
    #     db.session.add(audit)
    #     db.session.commit()
    #     return result

    @property
    def full_name(self):
        return "{0}".format(self.email)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.id)

    def __str__(self):
        return '{0}'.format(self.email)


class LoginAudit(Model):

    __tablename__ = 'loginaudit'
    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, index=True)
    ip = Column(db.String(45), index=True, nullable=False)
    success = Column(db.Boolean(), default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, index=True)
    
    
    def __repr__(self):
        return '<LoginAudit({id!r})>'.format(id=self.id)




class {{cookiecutter.detail_table_title}}(Model):

    __tablename__ = '{{cookiecutter.detail_table_title|lower}}'
    id = Column(db.String(128), primary_key=True)
    hashtag = Column(db.String(128), index=True)
    {{cookiecutter.core_table_title|lower}}_id = Column(db.Integer, index=True)
    body = Column(db.Text(), default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, index=True)
    modified_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, index=True)
    
    def __repr__(self):
        return '<{{cookiecutter.detail_table_title}}({id!r})>'.format(id=self.id)

class {{cookiecutter.detail_table_title}}Schema(Schema):
    id = fields.Str()
    hashtag = fields.Str()
    {{cookiecutter.core_table_title|lower}}_id = fields.Int(dump_only=True)
    body = fields.Str()
    created_at = fields.DateTime()
    modified_at = fields.DateTime()