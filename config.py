import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # our apps secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    
    # database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATATBASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # configuring email for errors
    MAILSERVER = os.environ.get('MAILSERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25 )
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['isaacsemb1996@gmail.com']