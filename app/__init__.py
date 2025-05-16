import os
from typing import Optional
from flask import Flask 


import logging
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

app = Flask(__name__)

# pull in configuration settings
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialise flask login (OVERRIDDEN THE LOGIN MANAGER TO CORRECT THE TYPE)
class MyLoginManager(LoginManager):
    login_view: Optional[str]

login_manager = MyLoginManager(app)

# login_manager = LoginManager(app)

# tell the login manager where the login view is found
# the name is the name of the view function
login_manager.login_view = 'login' 

# setting up the logger 
if not app.debug: # if application is not in debug mode
    
    # if mail server exists
    if app.config['MAIL_SERVER']:
        
        
        
        # setup credentials
        auth = None
        
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        # setup secure transfer    
        secure = None
        
        if app.config['MAIL_USE_TLS']:
            secure = ()
        
        mail_handler = SMTPHandler(
            mailhost = (
                app.config['MAIL_SERVER'], 
                app.config['MAIL_PORT']
                ),
            fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
            toaddrs = app.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # setting file logger

    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/microblog.log',
        maxBytes = 10240,
        backupCount = 10
        )
    
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')



from app import routes, models, errors