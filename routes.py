# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import User, Content, db
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError


#Create Flask blueprint object
api = Blueprint('api', __name__)
# db = SQLAlchemy()
bcrypt = Bcrypt()

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

# Route for Register
@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        # Perform registration logic here

        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = db.session.query(User).filter_by(username=username).first()

        # If user does exist then return to registration/login page with error
        if(existing_user):
            error_message = 'Username is already taken, please choose a different one.'
            return render_template('login.html', error_message=error_message)
        
        try:
            # Create the User and add to database
            new_user = User(username=username, password=hash_password, role=role)
            db.session.add(new_user)
            db.session.commit()

            # This is some code to see if user is making it into db :)
            all_users = db.session.query(User).all()

            for user in all_users:
                print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}, Role: {user.role}")

            # Go back to home page, you can decide where you want to go next later
            return redirect(url_for('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'))
        except IntegrityError:
            # If any database integrity error occurs handle it here
            error_message = "Error in registraton, please try again."
            return render_template('login.html', error_message=error_message)

        # # (PSEUDOCODE) if username and password match inside DB, route to dashboard/index page (waiting for DB set up to proceed)
        # if username == "someName" and password == "somePassword":
        #     return redirect(url_for('index'))
        # # if not make the user register again
        # else:
        #     return render_template('login.html', error="Invalid username/password")
    return render_template('login.html')
#Route for Create(?)
