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

from app import routes, models