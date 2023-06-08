# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Flask
from models import db
from routes import api

#Create Flask base app object
app = Flask(__name__)

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