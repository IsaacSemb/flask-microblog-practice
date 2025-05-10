from flask import Flask
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

from app import routes, models, errors