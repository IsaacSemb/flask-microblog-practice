from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


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
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        flash( message=f"Login requested for user: {login_form.username.data}, remember_me={login_form.remember_me.data}" )
        
        print(login_form.username)
        print(login_form.password)
        print(login_form.remember_me)
        
        return redirect('/index')
    
    return render_template('login.html', title="Sign In", form=login_form )
    