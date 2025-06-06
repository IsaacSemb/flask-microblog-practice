import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # our apps secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"
    
    # database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATATBASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        
    # Setting up pagination
    POSTS_PER_PAGE = 10
    
    # configuring email for errors
    
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_SERVER = 'localhost'
    
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25 )
    MAIL_PORT = 8025
    
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_TLS = False
    
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_USERNAME = None
    
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PASSWORD = None
    
    ADMINS = ['isaacsemb1996@gmail.com']