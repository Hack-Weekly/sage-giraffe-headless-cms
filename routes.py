# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Blueprint, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import User, Content

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
#Route for Create(?)

# Create route for content page
@api.route('/content')
def content():
    return render_template('content.html')

# Create route to create content
'''
This route accepts the following fields from the database: title, body, and created_at and is used to create a post
We loop where it accepts multiple users and adds it to the database
'''
@api.route('/add_post', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Content(id = data["id"], title = data["title"], body = data["body"], created_at = data["created_at"])
    
    for person in data["user"]:
        curr_user = User.query.filter_by(name=person).first()

        if(curr_user):
            curr_user.contents.append(new_post)
        else: #reroute to login page
            return render_template('login.html')

    db.session.add(new_post)
    db.session.commit()

    post_id = getattr(new_post, "id")
    return jsonify({"id": post_id})

# Fetch route to display posts
@api.route('/posts',methods=["GET"])
def get_posts():
    posts= Content.query.all()
    serialized_data = []
    for post in posts:
        serialized_data.append(post.serialize)

    return jsonify({"all_posts": serialized_data})

@api.route('/post/<int:id>',methods=["GET"])
def get_single_post(id):
    post = Content.query.filter_by(id=id).first()
    serialized_post = post.serialize
    serialized_post["user"] = []

    for person in post.user:
        serialized_post["user"].append(person.serialize)

    return jsonify({"single_post": serialized_post})
