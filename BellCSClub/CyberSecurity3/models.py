from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
ADMIN_USER = "admin"
ADMIN_KEY = "pGonjQgBWRsstdazVihu4O6WKaXn58tkaCbq9ZywTfqFhbTagLinS001W4WeoPBAlyv9yykl4lWdOcfzNBi4uZa3NmhXgz8mLcjh"

db = SQLAlchemy()
class User(UserMixin, db.Model):
    __tablename__="users"
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(25),unique = True,nullable = False)
    password = db.Column(db.String(10),nullable = False)
