# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Flask
from models import db
from routes import api
from flask_login import LoginManager
from models import User

#Create Flask login manager object
login_manager = LoginManager()

#Create Flask base app object
app = Flask(__name__)

#Initialize login manager with flask app
login_manager.init_app(app)

# Callback used to get user object from user ID stored in session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# set the secret key. KEEP THIS REALLY SECRET!
app.config['SECRET_KEY'] = 'your_secret_key_here'

#SQLALCHEMY setup with sqlite - change if necessary
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#Initialize db with flask app
db.init_app(app)

#Register blueprint
app.register_blueprint(api)

# Used to create the database
with app.app_context():
    db.create_all()

#Main function initilization
if __name__ == "__main__":
    app.run(debug=True)