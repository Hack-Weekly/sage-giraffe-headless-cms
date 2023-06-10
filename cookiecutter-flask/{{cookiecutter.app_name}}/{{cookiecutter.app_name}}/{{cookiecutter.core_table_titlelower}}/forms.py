# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField, SelectField, SelectMultipleField
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import time
from itertools import cycle, izip
import hashlib

from .models import {{cookiecutter.core_table_title}}


class {{cookiecutter.core_table_title}}Form(Form):
    hashtag = StringField('Hashtag',
                    validators=[DataRequired(), Length(min=1, max=128)])
    start = DateTimeField('Start Time',
                    validators=[DataRequired()], id='starttime' )
    end = DateTimeField('End Time', id='endtime')
    body = SelectField(u'Display Template', choices=[('horizontalrow', 'Horizontal 2-Row'), ('single', 'Rotating Single')])


    def __init__(self, *args, **kwargs):
        super({{cookiecutter.core_table_title}}Form, self).__init__(*args, **kwargs)
        #self.user = None

    def validate(self):
        initial_validation = super({{cookiecutter.core_table_title}}Form, self).validate()
        if not initial_validation:
            return False
        return True
