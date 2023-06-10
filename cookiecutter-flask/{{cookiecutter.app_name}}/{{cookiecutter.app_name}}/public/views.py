# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask_login import login_user, login_required, logout_user

from {{cookiecutter.app_name}}.extensions import login_manager
from {{cookiecutter.app_name}}.user.models import User
from {{cookiecutter.app_name}}.public.forms import LoginForm
from {{cookiecutter.app_name}}.user.forms import RegisterForm
from {{cookiecutter.app_name}}.utils import flash_errors
from {{cookiecutter.app_name}}.database import db

from datetime import datetime


blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    return render_template("public/home.html")

@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")


