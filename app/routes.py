from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    context = {
        "username":"Isaac Ssembuusi",
        "title": "Home Page"
        }
    return render_template( 'index.html', **context )
