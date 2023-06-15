import argparse
from flask import Flask
from models import db, User, Log
import bcrypt

# Create Flask app object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize db with Flask app
db.init_app(app)

# Function to create a new admin user
def create_admin(username, password):
    with app.app_context():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print("Username is already taken, please choose a different one.")
                return

            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create the User and add to the database
            new_user = User(username=username, password=password_hash, role='admin')
            db.session.add(new_user)
            db.session.commit()

            log_entry = Log(user_id=new_user.id, action=f'Registered new user with script: {username}')
            db.session.add(log_entry)
            db.session.commit()

            print("Admin user created successfully!")
        except Exception as e:
            print("Error creating admin user:", str(e))

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Create a new admin user')
parser.add_argument('username', help='Username for the new admin user')
parser.add_argument('password', help='Password for the new admin user')

# Parse command-line arguments
args = parser.parse_args()

# Call the create_admin function with parsed arguments
create_admin(args.username, args.password)
