from datetime import datetime

from application import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    _idx1 = db.Index('users_username', 'username', unique=True)
    _idx2 = db.Index('users_email', 'email', unique=True)


class AdvertisingModel(db.Model):
    __tablename__ = 'advertisings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        
    _idx1 = db.Index('advertisings_title', 'title')
    _idx2 = db.Index('advertisings_created_at', 'created_at')
