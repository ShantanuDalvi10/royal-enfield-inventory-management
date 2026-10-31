from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)

    username = db.Column(db.String(100),unique=True,nullable=False)

    password = db.Column(db.String(100),nullable=False)

class Parts(db.Model):
    __tablename__ = "parts"

    id = db.Column(db.Integer,primary_key=True)

    part_id = db.Column(db.String(50),unique=True,nullable=False)

    part_name = db.Column(db.String(100),nullable=False)

    price = db.Column(db.Float,nullable=False,default=0.00)

    stock = db.Column(db.Integer,nullable=False,default=0)

