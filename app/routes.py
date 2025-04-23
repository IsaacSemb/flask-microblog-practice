from flask import render_template
from app import app

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
