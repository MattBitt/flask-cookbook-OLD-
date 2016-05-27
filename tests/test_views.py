from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from flask.ext.testing import TestCase
from cookbook import db, app
from flask.ext.fixtures import FixturesMixin
from cookbook.schemas import IngredientSchema, DepartmentSchema
import json


FixturesMixin.init_app(app, db)

class ViewTest(TestCase, FixturesMixin):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        #app.config.from_object('config.TestingLocalDBConfig')
        return app
    
    
class IngredientsViewTest(ViewTest):
    fixtures = ['ingredients.json', 
                'departments.json']
    
    def test_ingredients(self):
        result = app.test_client().get('/ingredients')
        print result.data

        res_schema = IngredientSchema()
        ingredients = res_schema.load(result.data).data
        print ingredients

    def test_departments(self):
        result = app.test_client().get('/departments')
        assert 'Produce' in result.data

        
    