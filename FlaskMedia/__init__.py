from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

from FlaskMedia import views, models
