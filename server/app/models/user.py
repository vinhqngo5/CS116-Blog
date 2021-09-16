from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=True)
    middleName = db.Column(db.String(50), nullable=True)
    lastName = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True)
    registeredAt = db.Column(db.DateTime)
    lastLogin = db.Column(db.DateTime, nullable=True)