from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from cookbook import app, db

app.config.from_object('config.ProductionConfig')

migrate = Migrate(app, db)

from cookbook.models import Ingredient

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()