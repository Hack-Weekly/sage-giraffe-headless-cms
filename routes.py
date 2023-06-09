# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, login_user, logout_user
from models import User, Content

#Create Flask blueprint object
api = Blueprint('api', __name__)

#Simple default route for the index that pulls from the templates folder by default index.html
@api.route('/')
def index():
    return render_template('index.html')

#Route for Login page
@api.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            # Query the database for the user
            user = User.query.filter_by(username=username).first()
            # If username's password and inputted password match, route to content page
            if user and user.password == password:
                login_user(user)
                return redirect(url_for('api.content'))
            # if not make the user login again
            else:
                return render_template('login.html', error="Invalid username/password")
        except Exception as e:
            return render_template('login.html', error=e)
    return render_template('login.html')

# Route for Register
@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Perform registration logic here

        # (PSEUDOCODE) if username and password match inside DB, route to dashboard/index page (waiting for DB set up to proceed)
        if username == "someName" and password == "somePassword":
            return redirect(url_for('api.index'))
        # if not make the user register again
        else:
            return render_template('login.html', error="Invalid username/password")
    return render_template('login.html')

#Route for admin dashboard
@api.route('/admin')
@login_required
def admin():
    if current_user.role == 'admin':
        contents = Content.query.order_by(Content.createdAt.desc()).all()
        return render_template('admin.html', contents=contents)
    else:
        return render_template('login.html', error="You are not authorized to view this page")

#Route for content dashboard
@api.route('/content')
@login_required
def content():
    if current_user.is_authenticated:
        return render_template('content.html')
    else:
        return render_template('login.html', error="You are not authorized to view this page")

#Missing Page 404 route
@api.app_errorhandler(404)
def invalid_route(e):
    return render_template('404.html')

#Route for Create(?)