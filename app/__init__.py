from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import os
app.config.from_object('app.setting')
if not os.environ.get('FLASKR_SETTINGS'):
    os.environ["FLASKR_SETTINGS"] = os.path.join(os.path.dirname(__file__), 'setting.py')
app.config.from_envvar('FLASKR_SETTINGS')

db = SQLAlchemy(app)

from app.model import Popularity
from app.controller import router