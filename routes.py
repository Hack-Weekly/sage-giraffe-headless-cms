# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User, Content, Log, db
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from flask_login import login_required, current_user, login_user, logout_user

#Create Flask blueprint object
cms = Blueprint('cms', __name__)
# db = SQLAlchemy()
bcrypt = Bcrypt()

#Simple default route for the index that pulls from the templates folder by default index.html
@cms.route('/')
def index():
    return render_template('index.html')

#Route for Login page
@cms.route('/login', methods=['GET', 'POST']) 
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
                return redirect(url_for('cms.content'))
            # if not make the user login again
            else:
                return render_template('login.html', error="Invalid username/password")
        except Exception as e:
            return render_template('login.html', error=e)
    return render_template('login.html')

# Route for Logout
@cms.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('cms.index'))

# Route for Register
@cms.route('/register', methods=['GET', 'POST'])
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
            new_user = User(username=username, password=hash_password, role=role)
            db.session.add(new_user)

            try:
                db.session.commit()

                log_entry = Log(user_id=new_user.id, action=f'Registered new user: {username}')
                db.session.add(log_entry)
                db.session.commit()

                if current_user.role == 'admin' or (not current_user and role == 'admin'):
                    return redirect(url_for('cms.admin'))
                else:
                    return redirect(url_for('cms.index'))
            except:
                return "There was an error adding your user"

        except IntegrityError:
            # If any database integrity error occurs handle it here
            print("Error in registration")
            error = "Error in registraton, please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

#Route for admin dashboard
@cms.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role == 'admin':
        users = User.query.order_by(User.lastLogin.desc()).all()
        return render_template('admin.html', users=users)
    else:
        return render_template('index.html', error="You are not authorized to view this page")

#Route for content dashboard
@cms.route('/content', methods=['GET', 'POST'])
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
        return redirect(url_for('cms.content'))
    if current_user.is_authenticated:
        contents = Content.query.order_by(Content.createdAt.desc()).all()
        return render_template('content.html', contents=contents)
    else:
        return render_template('login.html', error="You are not authorized to view this page")

#Route to add content
@cms.route('/content/add', methods=['GET','POST'])
@login_required
def add_content():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        userId = current_user.id

        new_content = Content(title=title, body=body, userId=userId)
        db.session.add(new_content)
        try:
            db.session.commit()

            log_entry = Log(user_id=current_user.id, action=f'Added content: {title}')
            db.session.add(log_entry)
            db.session.commit()
            return redirect(url_for('cms.content'))
        except:
            return "There was an error adding your content"

    if request.method == 'GET':
        return render_template('add_content.html')

#Route to update content
@cms.route('/content/update/<int:post_id>', methods=['GET','POST'])
@login_required
def update_content(post_id):
    content = Content.query.get_or_404(post_id)
    if request.method == 'POST':
        content.title = request.form['title']
        content.body = request.form['body']
        try:
            db.session.commit()

            log_entry = Log(user_id=current_user.id, action=f'Updated content: {content.title}')
            db.session.add(log_entry)
            db.session.commit()
            return redirect(url_for('cms.content'))
        except:
            return "There was an error updating your content"
    else:
        return render_template('edit_content.html', content=content)

#Route to delete content
@cms.route('/content/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_content(post_id):
    content = Content.query.get_or_404(post_id)
    db.session.delete(content)
    try:
        db.session.commit()

        log_entry = Log(user_id=current_user.id, action=f'Deleted content: {content.title}')
        db.session.add(log_entry)
        db.session.commit()
        return redirect(url_for('cms.content'))
    except:
        return "There was an error deleting your content"

#Route to confirm delete content
@cms.route('/content/confirm_delete/<int:post_id>', methods=['GET'])
@login_required
def confirm_delete_content(post_id):
    content = Content.query.get_or_404(post_id)
    return render_template('confirm_delete_content.html', content=content)

#Route for add user from admin dashboard
@cms.route('/admin/add_user', methods=['GET'])
@login_required
def add_user():
    return render_template('add_user.html')

#Route to update user
@cms.route('/admin/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user.role = request.form['role']
        try:
            db.session.commit()

            log_entry = Log(user_id=current_user.id, action=f'Updated user: {user.username}')
            db.session.add(log_entry)
            db.session.commit()
            return redirect(url_for('cms.admin'))
        except:
            return "There was an error updating your content"
    else:
        return render_template('edit_user.html', user=user)

#Route to delete user
@cms.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Delete all content associated with user
    if user.contents:
        for content in user.contents:
            db.session.delete(content)

    # Delete all activity logs associated with the user
    if user.user_logs:
        for log in user.user_logs:
            db.session.delete(log)

    db.session.delete(user)

    try:
        db.session.commit()

        log_entry = Log(user_id=current_user.id, action=f'Deleted user: {user.username}')
        db.session.add(log_entry)
        db.session.commit()
        return redirect(url_for('cms.admin'))
    except Exception as e:
        return "There was an error deleting the user: " + str(e)

#Route to confirm delete user
@cms.route('/admin/confirm_delete/<int:user_id>', methods=['GET'])
@login_required
def confirm_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('confirm_delete_user.html', user=user)


#Missing Page 404 route
@cms.app_errorhandler(404)
def invalid_route(e):
    return render_template('404.html')

#Route for Create(?)