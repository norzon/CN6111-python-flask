# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskblog import config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri

# General files
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'

from flaskblog import routes
