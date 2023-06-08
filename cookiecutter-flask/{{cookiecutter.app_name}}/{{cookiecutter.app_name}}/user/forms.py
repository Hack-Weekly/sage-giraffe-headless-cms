# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Required
from flask_security.forms import ResetPasswordForm
from .models import User


class RegisterForm(Form):
    """Register form."""
    username = TextField('Username',
                    validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                    validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                                validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True

class ExtendedResetPasswordForm(ResetPasswordForm):
    """The default reset password form"""
    password = PasswordField('New Password', validators=[Required(message='PASSWORD_NOT_PROVIDED'), Length(min=6, max=128, message='PASSWORD_INVALID_LENGTH')])