# FILE: app/models/user.py
from ..extensions import db
from datetime import datetime, timezone

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    public_key = db.Column(db.Text, nullable=False)  
    private_key = db.Column(db.Text, nullable=False) 
    
    role = db.relationship('Role', backref=db.backref('users', lazy=True))