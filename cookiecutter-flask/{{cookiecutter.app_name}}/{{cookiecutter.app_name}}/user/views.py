# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User
from ..{{cookiecutter.core_table_title|lower}}.models import {{cookiecutter.core_table_title}}

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    current_{{cookiecutter.core_table_title|lower}}s = {{cookiecutter.core_table_title}}.query.filter_by(user_id=current_user.id)
    #TODO: show list of login events
    return render_template("users/members.html", current_{{cookiecutter.core_table_title|lower}}s=current_{{cookiecutter.core_table_title|lower}}s)
