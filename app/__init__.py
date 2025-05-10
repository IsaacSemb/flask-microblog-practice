from flask import Flask 


import logging
from logging.handlers import SMTPHandler

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

app = Flask(__name__)

# pull in configuration settings
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialise flask login
login_manager = LoginManager(app)

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



from app import routes, models, errors