# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User, Content, Log, db
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

#Create Flask blueprint object
api = Blueprint('api', __name__)


#Simple default route for the index that pulls from the templates folder by default index.html
@api.route('/api/allcontent')
def apiTest():
    allContent = Content.query.all()
    data ={}
    for content in allContent:
        key = content.id
        value = {"title": content.title,
                 "body": content.body,
                 "createdAt": content.createdAt}
        data[key]=value
    return jsonify(data)

@api.route('/api/content/limit/<int:limit>', methods=['GET'])
def get_content_by_limit(limit):
    all_content = Content.query.limit(limit).all()
    data = {}
    for content in all_content:
        key = content.id
        value = {
            "title": content.title,
            "body": content.body,
            "createdAt": content.createdAt
        }
        data[key] = value
    return jsonify(data)


@api.route('/api/content/id/<int:content_id>', methods=['GET'])
def get_content_by_id(content_id):
    content = Content.query.get(content_id)
    if content:
        data = {
            "title": content.title,
            "body": content.body,
            "createdAt": content.createdAt
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Content not found"})