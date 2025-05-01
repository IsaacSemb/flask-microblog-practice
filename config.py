import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # our apps secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    
    # database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATATBASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    