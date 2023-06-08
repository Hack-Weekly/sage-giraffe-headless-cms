# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

#Create Flask blueprint object
api = Blueprint('api', __name__)

#Simple default route for the index that pulls from the templates folder by default index.html
@api.route('/')
def index():
    return render_template('index.html')

#Route for Login page
@api.route('/login', methods=['GET', 'POST']) #im just adding variables here to act in place of the ones that will be in the form
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

#Route for Create(?)
