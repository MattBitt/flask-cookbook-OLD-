
from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from flask.ext.testing import TestCase
from cookbook import db, app
from flask.ext.fixtures import FixturesMixin
import json
from cookbook.schemas import department_schema, ingredient_schema

FixturesMixin.init_app(app, db)

class SchemasTest(TestCase, FixturesMixin):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        #app.config.from_object('config.TestingLocalDBConfig')
        return app


    def setUp(self):
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

class DepartmentSchemaTest(SchemasTest):
    fixtures = ['ingredients.json',
                'departments.json']

    def first_test(self):
        ingred = Ingredient.query.get(1)
        department = Department.query.get(1)
        print department_schema.dump(department).data
        print ingredient_schema.dump(ingred).data['name']

