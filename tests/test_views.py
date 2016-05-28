from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from flask.ext.testing import TestCase
from cookbook import db, app
from flask.ext.fixtures import FixturesMixin
import json
import pprint


FixturesMixin.init_app(app, db)

class ViewTest(TestCase, FixturesMixin):
    pp = pprint.PrettyPrinter(indent=2)
    
    
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        #app.config.from_object('config.TestingLocalDBConfig')
        return app
    
    
class IngredientsViewTest(ViewTest):
    fixtures = ['ingredients.json', 
                'departments.json']
    
    def test_ingredients(self):
        #result = app.test_client().get('/ingredients')
        pass

        
class DepartmentsViewTest(ViewTest):
    fixtures = ['departments.json',
                'ingredients.json']
    
    def test_department(self):
        result = app.test_client().get('/departments/1')
        departments = json.loads(result.data)['departments']
        
        assert departments['name'] == 'Produce'
        assert departments['id'] == 1
        

        
    