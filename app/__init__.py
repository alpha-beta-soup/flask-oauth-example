import os

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

from config import BASEDIR

app = Flask(__name__)
app.config.from_object('config') # load config.py at project root
db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = 'index'

from app import views, models # NOTE app package != app variable
