from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm

from flask_login import current_user, login_user
from app.models import User
import sqlalchemy as sa



@app.route('/')
@app.route('/index')
def index():
    context1 = {
        "username":"Isaac Ssembuusi",
        "title": "Home Page"
        }
    
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    
    return render_template( 'index.html', **context1, posts=posts )

@app.route('/login', methods=[ 'GET', 'POST' ])
def login():
    
    # checked if the user is authenticated already
    # An already logged in user should not go to the login page
    if current_user.is_authenticated:
        return  redirect(url_for('index'))
    
    # pass the login form to the view
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        
        # check for user details from submitted form in the database
        user = db.session.scalar(
            sa
            .select(User)
            .where(User.username==login_form.username.data)
        )
        
        # check password if the user exists
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        # if sucessfull if statement wont run
        login_user(user, remember=login_form.remember_me.data)
        
        # send the user to the homepage
        return redirect(url_for('index'))
    
    return render_template('login.html', title="Sign In", form=login_form )
    