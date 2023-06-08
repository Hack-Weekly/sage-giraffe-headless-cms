# -*- coding: utf-8 -*-
import datetime as dt
from marshmallow import Schema, fields, ValidationError


from {{cookiecutter.app_name}}.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)



class {{cookiecutter.core_table_title}}(Model):

    __tablename__ = '{{cookiecutter.core_table_title|lower}}'
    id = Column(db.Integer, primary_key=True)
    hashtag = Column(db.String(128), index=True)
    uuid = Column(db.String(40), index=True)
    user_id = ReferenceCol('user', nullable=True)
    user = relationship('User', backref='{{cookiecutter.core_table_title|lower}}')
    start = Column(db.DateTime, nullable=False, index=True)
    end = Column(db.DateTime, nullable=False, index=True)
    body = Column(db.Text(), default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, index=True)
    modified_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow, index=True)

    
    def __repr__(self):
        return '<{{cookiecutter.core_table_title}}({id!r})>'.format(id=self.id)

class {{cookiecutter.core_table_title}}Schema(Schema):
    id = fields.Int(dump_only=True)
    hashtag = fields.Str()
    uuid = fields.Str()
    user_id = fields.Int(dump_only=True)
    start = fields.DateTime()
    end = fields.DateTime()
    body = fields.Str()
    created_at = fields.DateTime()
    modified_at = fields.DateTime()
