from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api


app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
api = Api(app)
db = SQLAlchemy()

from cookbook import views


db.init_app(app)