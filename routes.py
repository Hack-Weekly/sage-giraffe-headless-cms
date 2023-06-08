# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

#Create Flask blueprint object
api = Blueprint('api', __name__)

#Simple default route for the index that pulls from the templates folder by default index.html
@api.route('/')
def index():
    return render_template('index.html')

#Route for admin dashboard
@api.route('/admin')
def admin():
    return render_template('admin.html')

#Route for content dashboard
@api.route('/content')
def content():
    return render_template('content.html')

#Route for Login page
@api.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        # im going to comment these out just because we do not have any set variables for username and password
        username = request.form['username']
        password = request.form['password']
        # (PSEUDOCODE) if username and password match inside DB, route to dashboard/index page (waiting for DB set up to proceed)
        if username == "rob" and password == "rob":
            return redirect(url_for('index'))
        # if not make the user login again
        else:
            return render_template('login.html', error="Invalid username/password")
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
            return redirect(url_for('index'))
        # if not make the user register again
        else:
            return render_template('login.html', error="Invalid username/password")
    return render_template('login.html')

#Missing Page 404 route
@api.app_errorhandler(404)
def invalid_route(e):
    return render_template('404.html')


#Route for Create(?)

