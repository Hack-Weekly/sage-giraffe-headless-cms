# Imports of flask and SQLALCHEMY all done within virtualenv 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#Create Flask base app object
app = Flask(__name__)

#SQLALCHEMY setup with sqlite - change if necessary
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
db = SQLAlchemy(app)

#Simple default route for the index that pulls from the templates folder by default index.html
@app.route('/')
def index():
    return render_template('index.html')

#Route for Login page
@app.route('/login', methods=['GET', 'POST']) #im just adding variables here to act in place of the ones that will be in the form
def login():
    # im going to comment these out just because we do not have any set variables for username and password
    # username =
    # password = 
    # (PSEUDOCODE) if username and password match inside DB, route to dashboard/index page
    # if not make the user login again
    return render_template('login.html')

#Main function initilization
if __name__ == "__main__":
    app.run(debug=True)