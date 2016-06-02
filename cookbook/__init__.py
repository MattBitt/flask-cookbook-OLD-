from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_restful import Api
from sqlalchemy import orm
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


handler = RotatingFileHandler('log/cookbook.log', maxBytes=1000000, backupCount=1)
formatter = logging.Formatter( "%(asctime)s | %(module)s | %(funcName)s | %(levelname)s | %(message)s ")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG) 
app.logger.addHandler(handler)

app.logger.warning('THE APP IS STARTING')
#api = Api(app)
db = SQLAlchemy(app)

from cookbook import views
db.init_app(app)


