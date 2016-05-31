from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import orm

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
api = Api(app)
db = SQLAlchemy(app)
from cookbook import views


db.init_app(app)