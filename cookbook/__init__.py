from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
api = Api(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)

from cookbook import views


db.init_app(app)