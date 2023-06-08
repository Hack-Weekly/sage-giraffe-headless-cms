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

#Main function initilization
if __name__ == "__main__":
    app.run(debug=True)