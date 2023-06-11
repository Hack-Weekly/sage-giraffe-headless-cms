# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User, Content, db
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from flask_login import login_required, current_user, login_user, logout_user

#Create Flask blueprint object
api = Blueprint('api', __name__)
# db = SQLAlchemy()
bcrypt = Bcrypt()

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
            # If username's password and inputted password match (hashed), log user in and route to content page
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('api.content'))
            # if not make the user login again
            else:
                return render_template('login.html', error="Invalid username/password")
        except Exception as e:
            return render_template('login.html', error=e)
    return render_template('login.html')

# Route for Logout
@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('api.index'))

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
            print("User already exists")
            error = 'Username is already taken, please choose a different one.'
            return render_template('login.html', error=error)
        
        try:
            # Create the User and add to database
            print("Creating new user")
            new_user = User(username=username, password=hash_password, role=role)
            db.session.add(new_user)
            db.session.commit()

            # This is some code to see if user is making it into db :)
            all_users = db.session.query(User).all()

            for user in all_users:
                print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}, Role: {user.role}")

            return redirect(url_for('api.admin'))
        except IntegrityError:
            # If any database integrity error occurs handle it here
            print("Error in registration")
            error = "Error in registraton, please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

#Route for admin dashboard
@api.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role == 'admin':
        users = User.query.order_by(User.lastLogin.desc()).all()
        return render_template('admin.html', users=users)
    else:
        return render_template('login.html', error="You are not authorized to view this page")

#Route for add user from admin dashboard
@api.route('/admin/add_user', methods=['GET'])
@login_required
def add_user():
    return render_template('add_user.html')

#Route for content dashboard
@api.route('/content', methods=['GET', 'POST'])
@login_required
def content():
    if request.method == 'POST':
        print(request.form)
        title = request.form['title']
        body = request.form['body']
        userId = current_user.id

        new_content = Content(title=title, body=body, userId=userId)
        db.session.add(new_content)
        db.session.commit()

        print("New content added")
        return redirect(url_for('api.content'))
    if current_user.is_authenticated:
        contents = Content.query.order_by(Content.createdAt.desc()).all()
        return render_template('content.html', contents=contents)
    else:
        return render_template('login.html', error="You are not authorized to view this page")

#Route to add content
@api.route('/content/add', methods=['GET','POST'])
@login_required
def add_content():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        userId = current_user.id

        new_content = Content(title=title, body=body, userId=userId)
        db.session.add(new_content)
        db.session.commit()

        return redirect(url_for('api.content'))
    if request.method == 'GET':
        return render_template('add_content.html')

#Route to update content
@api.route('/content/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_content(post_id):
    content = Content.query.get_or_404(post_id)
    if request.method == 'POST':
        content.title = request.form['title']
        content.body = request.form['body']
        try:
            db.session.commit()
            return redirect(url_for('api.content'))
        except:
            return "There was an error updating your content"
    else:
        return render_template('edit_content.html', content=content)


#Missing Page 404 route
@api.app_errorhandler(404)
def invalid_route(e):
    return render_template('404.html')

#Route for Create(?)