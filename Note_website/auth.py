# Authentication routes - login, logout, signup
from flask import Blueprint,render_template, request , flash,redirect,url_for
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db
from flask_login import login_user, login_required, logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route("/login", methods=['GET','POST'] )
def login():
  if request.method== 'POST':
     # Get form data
     email= request.form.get('email')
     password=request.form.get('password')
     
     # Find user in database
     user=User.query.filter_by(email=email).first()
     
     if user:
       # Check password hash
       if check_password_hash(user.password,password):
         flash('Logged in successfully!',category='success')
         login_user(user, remember=True)  # Create session
         return redirect(url_for('views.home'))
       else:
        flash('Incorrect password, try again.', category= 'error')
     else:
        flash('Email does not exist🤔', category ='error' ) 
          
  return render_template("login.html", user= current_user)

@auth.route("/logout")
@login_required
def logout():
  # End user session
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET','POST'] )
def sign_up():
 if  request.method == 'POST':
      # Get registration form data
      email = request.form.get('email')
      Name=request.form.get('Name')
      password=request.form.get('password')
      confirmpassword=request.form.get('conpass')
      
      # Check if email already exists
      user=User.query.filter_by(email=email).first()
      
      # Validation checks
      if user:
        flash('Email already exists.', category='error')
      elif len(email)<4:
          flash('Your email most be greater than 3 characters.', category='error')
      elif len(Name)<2:
        flash('Your name most be greater than 1 characters.', category='error')
      elif password != confirmpassword:
        flash('Oops your password doesn\'t match 😥.', category='error')
      elif len(password)<7:
        flash('password is not strong make sure it least 7 characters', category='error')
      else:
       # Create new user with hashed password
       new_user= User(email=email, Name=Name, password=generate_password_hash(confirmpassword, method='pbkdf2:sha256'))
       db.session.add(new_user)
       db.session.commit()
       login_user(new_user, remember=True)  # Auto-login
       flash('Account successful created ', category='success')
       return redirect(url_for('views.home'))
       
 return render_template("sign_up.html", user= current_user)
