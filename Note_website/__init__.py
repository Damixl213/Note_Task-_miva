# Flask app factory - creates and configures the application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize database instance
db= SQLAlchemy()
DB_NAME= "database.db"

def create_app():
  # Create Flask app
  app = Flask(__name__)
  
  # App configuration
  app.config['SECRET_KEY']='aiequhqub1039@02dolap3o'  # For session security
  app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'  # SQLite database
  db.init_app(app)
  
  # Register route blueprints
  from .views import views  # Main app routes
  from .auth  import auth   # Authentication routes
  app.register_blueprint(views,url_prefix='/')
  app.register_blueprint(auth,url_prefix='/')
  
  # Import models and create database
  from .model import User, Note
  create_database(app)
  
  # Setup user session management
  login_manager= LoginManager()
  login_manager.login_view ='auth.login'  # Redirect here if not logged in
  login_manager.init_app(app)
  
  @login_manager.user_loader
  def loaduser(id):
    # Load user from database for session
    return User.query.get(int(id))  
  
  return app

def create_database(app):
    # Create database file if it doesn't exist
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
    print('Created Database!')