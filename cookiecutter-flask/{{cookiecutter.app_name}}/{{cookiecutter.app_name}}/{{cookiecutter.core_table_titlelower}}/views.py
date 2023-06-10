# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask import jsonify
from flask_login import login_required, current_user
from .models import {{cookiecutter.core_table_title}}, {{cookiecutter.core_table_title}}Schema
from .forms import {{cookiecutter.core_table_title}}Form
from flask.globals import current_app
from {{cookiecutter.app_name}}.utils import flash_errors
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
from itertools import cycle, izip
import time
import hashlib
import uuid
import {{cookiecutter.app_name}}.constants as CONST
from {{cookiecutter.app_name}}.database import db
from sqlalchemy.sql import text

from ..user.models import {{cookiecutter.detail_table_title}}, {{cookiecutter.detail_table_title}}Schema

blueprint = Blueprint("{{cookiecutter.core_table_title|lower}}", __name__, url_prefix='/{{cookiecutter.core_table_title|lower}}s',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def {{cookiecutter.core_table_title|lower}}():
    
    return render_template("private/{{cookiecutter.core_table_title|lower}}s.html", tweetwallboard=current_app.config['TWEETWALLBOARD_DOMAIN'])

@blueprint.route("/detail/<int:{{cookiecutter.core_table_title|lower}}_id>")
@login_required
def {{cookiecutter.core_table_title|lower}}_detail({{cookiecutter.core_table_title|lower}}_id):
    view_type = request.args.get('view_type')
    if view_type not in ['all', 'pending', 'censored', 'approved']:
        view_type = 'all'
    return render_template("private/{{cookiecutter.core_table_title|lower}}-detail.html", {{cookiecutter.core_table_title|lower}}_id={{cookiecutter.core_table_title|lower}}_id, view_type=view_type)    

@blueprint.route("/create/", methods=['GET', 'POST'])
@login_required
def create():
    form = {{cookiecutter.core_table_title}}Form(request.form, csrf_enabled=True)
    
    if form.validate_on_submit():

        new_{{cookiecutter.core_table_title|lower}} = {{cookiecutter.core_table_title}}(hashtag=form.hashtag.data,
                        user_id=current_user.id,
                        start=form.start.data.strftime("%Y-%m-%d %H:%M:%S"),
                        end=form.end.data.strftime("%Y-%m-%d %H:%M:%S"),
                        created_at=datetime.utcnow(),
                        modified_at=datetime.utcnow(),
                        body='{"template":"' + form.body.data + '"}'
                        )
        db.session.add(new_{{cookiecutter.core_table_title|lower}})
        db.session.flush()
        db.session.refresh(new_{{cookiecutter.core_table_title|lower}})
        new_{{cookiecutter.core_table_title|lower}}.uuid = uuid.uuid5(current_app.config['{{cookiecutter.core_table_title|upper}}_ID_UUID_NAMESPACE'], str(new_{{cookiecutter.core_table_title|lower}}.id))
        db.session.commit()
        flash("{{cookiecutter.core_table_title}} is now saved.", 'success')
        return redirect(url_for('{{cookiecutter.core_table_title|lower}}.{{cookiecutter.core_table_title|lower}}'))
    else:
        flash_errors(form)
    return render_template("private/{{cookiecutter.core_table_title|lower}}-create.html", form=form)


# AJAX calls below ###############

@blueprint.route("/data")
@login_required
def data():
    current_{{cookiecutter.core_table_title|lower}}s = {{cookiecutter.core_table_title}}.query.filter_by(user_id=current_user.id).all()
    {{cookiecutter.core_table_title|lower}}s_schema = {{cookiecutter.core_table_title}}Schema(many=True)
    result = {{cookiecutter.core_table_title|lower}}s_schema.dump(current_{{cookiecutter.core_table_title|lower}}s)
    return jsonify({'data': result.data})


@blueprint.route("/datadetail/<int:{{cookiecutter.core_table_title|lower}}_id>")
@login_required
def detail({{cookiecutter.core_table_title|lower}}_id):
    current_{{cookiecutter.core_table_title|lower}}s = {{cookiecutter.core_table_title}}.query.filter_by(user_id=current_user.id,id={{cookiecutter.core_table_title|lower}}_id).all()
    if len(current_{{cookiecutter.core_table_title|lower}}s) != 0:
        details = {{cookiecutter.detail_table_title}}.query.filter_by({{cookiecutter.core_table_title|lower}}_id={{cookiecutter.core_table_title|lower}}_id).all()
        detail_schema = {{cookiecutter.detail_table_title}}Schema(many=True)
        result = detail_schema.dump(details)
        return jsonify({'data': result.data})
    else:
        flash(u'Invalid {{cookiecutter.core_table_title|lower}}', 'error')
        return redirect(url_for('{{cookiecutter.core_table_title|lower}}.{{cookiecutter.core_table_title|lower}}'))


@blueprint.route("/all/<int:{{cookiecutter.core_table_title|lower}}_id>")
@login_required
def allposts({{cookiecutter.core_table_title|lower}}_id):
    current_{{cookiecutter.core_table_title|lower}}s = {{cookiecutter.core_table_title}}.query.filter_by(user_id=current_user.id,id={{cookiecutter.core_table_title|lower}}_id).all()
    if len(current_{{cookiecutter.core_table_title|lower}}s) != 0:
        details = {{cookiecutter.detail_table_title}}.query.filter(text("{{cookiecutter.core_table_title|lower}}.{{cookiecutter.core_table_title|lower}}_id=:{{cookiecutter.core_table_title|lower}}_id")).params({{cookiecutter.core_table_title|lower}}_id={{cookiecutter.core_table_title|lower}}_id).all()
        detail_schema = {{cookiecutter.detail_table_title}}Schema(many=True)
        result = detail_schema.dump(details)
        return jsonify({'data': result.data})
    else:
        flash(u'Invalid {{cookiecutter.core_table_title|lower}}', 'error')
        return redirect(url_for('{{cookiecutter.core_table_title|lower}}.{{cookiecutter.core_table_title|lower}}'))
