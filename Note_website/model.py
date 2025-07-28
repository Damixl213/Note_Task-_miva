# Database models for users, notes, and tasks
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
  # User account model
  id=db.Column(db.Integer,primary_key =True)        # Unique user ID
  email=db.Column(db.String(150),unique=True)       # Login email (unique)
  password=db.Column(db.String(150))                # Hashed password
  Name = db.Column(db.String(150))                  # Display name
  note =db.relationship('Note')                     # Link to user's notes
  
class Note(db.Model):
    # Note storage model
    id = db.Column(db.Integer, primary_key=True)                           # Note ID
    subject = db.Column(db.String(200), nullable=False)                    # Note title
    data = db.Column(db.String(10000000))                                 # Note content
    date = db.Column(db.DateTime(timezone=True), default=func.now())      # Created date
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))             # Owner reference

class Task(db.Model):
    # Task/todo model
    id = db.Column(db.Integer, primary_key=True)                           # Task ID
    description = db.Column(db.String(500), nullable=False)               # Task description
    completed = db.Column(db.Boolean, default=False)                      # Completion status
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # Created date
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Owner reference