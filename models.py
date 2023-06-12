from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model, UserMixin):
    # Define the table name
    __tablename__ = 'users'
    
    # Define columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    lastLogin = db.Column(db.DateTime, default=datetime.utcnow) # -5 hours for EST

    # Define the relationship to Content model
    logs = relationship('Log', backref='user_logs')

    def __repr__(self):
        return '<User %r>' % self.username


class Content(db.Model, UserMixin):
    __tablename__ = 'contents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # -5 hours for EST
    
    # Define the relationship to User model
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('contents', lazy=True))

    def __repr__(self):
        return '<Content %r>' % self.title
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'createdAt': self.createdAt,
            'userId': self.userId
        }
    

class Log(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user_logs', lazy=True))
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # -5 hours for EST


    def __repr__(self):
        return '<Log %r>' % self.id
