from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hmac, hashlib
from flask import current_app

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(20), primary_key= True)
    name = db.Column(db.String(80), nullable = False)
    password  = db.Column(db.String(128), nullable = False)
    dob = db.Column(db.DateTime, nullable = False)
    email_id = db.Column(db.String(30), nullable = False)

    #relationship: one user can have multiple todos one to many
    todos = db.relationship('Todo', backref = 'user', lazy = True)

    def set_password(self, password):
        secret_key = current_app.config['SECRET_KEY'].encode('utf-8')
        self.password = hmac.new(secret_key, password.encode('utf-8'), hashlib.sha256).hexdigest()

    def check_password(self, password):
        secret_key = current_app.config['SECRET_KEY'].encode('utf-8')
        hashed = hmac.new(secret_key,password.encode('utf-8'),hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.password, hashed)

    def __repr__(self):
        return f'<User_id {self.user_id}>\nname {self.name}\npassword {self.password}'


class Todo(db.Model):
    __tablename__ = 'todos'

    t_id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(500))
    priority = db.Column(db.String(20), nullable = False)
    action = db.Column(db.Boolean, default = False)
    completed_at = db.Column(db.DateTime, nullable = True)

    # connect each todo to a user via foreign key
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.title}>'
