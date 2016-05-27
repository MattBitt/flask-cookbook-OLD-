from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

db = SQLAlchemy()

from cookbook import views

db.init_app(app)