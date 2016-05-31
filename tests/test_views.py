from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from cookbook.schemas import DepartmentSchema, IngredientSchema, UnitSchema, StepSchema
from cookbook.schemas import NoteSchema, RecipeSchema
from flask_testing import TestCase
from cookbook import db, app
from flask_fixtures import FixturesMixin
import json
import pprint
import unittest 
import jsonpickle

FixturesMixin.init_app(app, db)

class ViewTest(TestCase, FixturesMixin):
    pp = pprint.PrettyPrinter(indent=2)
    
    
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        #app.config.from_object('config.TestingLocalDBConfig')
        return app
    
    def t_client_post(self, url, json_data):
        
        
        result = app.test_client().post(url, data=json_data,
                       content_type = 'application/json')
        
        return result
    def t_client_put(self, url, json_data):

        return app.test_client().put(url, data=json_data,
                       content_type = 'application/json')
    def t_client_delete(self, url):
        return app.test_client().delete(url)


class IngredientsViewTest(ViewTest):
    fixtures = ['ingredients.json', 
                'departments.json']
    
    def test_ingredient(self):
        result = app.test_client().get('/ingredients/1')
        assert result.status_code == 200
        obj_dict = json.loads(result.data)#['ingredients']
        data, errors = IngredientSchema().load(obj_dict)
        assert errors == {}
        assert isinstance(data, Ingredient) == True
        assert data.name == 'cauliflower'
        assert data.id == 1
        assert data.department.id == 1
        
    
    def test_bad_ingredient_id(self):
        result = app.test_client().get('/ingredients/15')
        assert result.status_code == 404
    
 
    def test_all_ingredients(self):
        result = app.test_client().get('/ingredients/')
        assert result.status_code == 200
        obj_dict_list = json.loads(result.data)#['ingredients']
        data, errors = IngredientSchema(many=True).load(obj_dict_list)
        assert len(data) == 5
        assert data[0].name == 'cauliflower'
        
    def test_create_ingredient(self):
        ing = r"""{"name" : "ground pork", "department" : { "id" : 2, "name" : "Meat"}}"""
        result = self.t_client_post('/ingredients/', ing)
        assert result.status_code == 200
        result = app.test_client().get('/ingredients/')
        assert result.status_code == 200
        assert 'ground pork' in result.data
    
    def test_create_ingredient_missing_department(self):
        ing = r"""{"name" : "ground pork"}"""
        result = self.t_client_post('/ingredients/', ing)
        assert 'Missing data' in result.data
    
    
    def test_update_ingredient_name(self):
        assert Ingredient.query.get(1).name == 'cauliflower'
        ing = r"""{"name" : "watermelon"}"""
        result = self.t_client_put('/ingredients/1', ing)
        assert result.status_code == 200
        assert Ingredient.query.get(1).name == 'watermelon'
        assert Ingredient.query.get(1).department_id == 1
    
    def test_update_ingredient_department(self):
        assert Ingredient.query.get(1).name == 'cauliflower'
        ing = r"""{"department" : {"name" : "Meat", "id" : 3}}"""
        result = self.t_client_put('/ingredients/1', ing)
        assert result.status_code == 200
        assert Ingredient.query.get(1).name == 'cauliflower'
        assert Ingredient.query.get(1).department.id == 3
        assert Department.query.get(3).name == 'Meat'
        
    def test_delete_ingredient(self):
        assert Ingredient.query.get(1).name == 'cauliflower'
        result = self.t_client_delete('/ingredients/1')
        assert Ingredient.query.get(1) is None
       
class DepartmentsViewTest(ViewTest):
    fixtures = ['departments.json',
                'ingredients.json']
    
    def test_department(self):
        result = app.test_client().get('/departments/1')
        assert result.status_code == 200
        obj_dict = json.loads(result.data)#['department']
        data, errors = DepartmentSchema().load(obj_dict)
        assert errors == {}
        assert isinstance(data, Department) == True
        assert data.name == 'Produce'
        assert data.id == 1
        assert len(data.ingredients.all()) == 3

    def test_bad_department_id(self):
        result = app.test_client().get('/departments/15')
        assert result.status_code == 404

    def test_all_departments(self):
        result = app.test_client().get('/departments/')
        assert result.status_code == 200
        obj_dict_list = json.loads(result.data)#['departments']
        data, errors = DepartmentSchema(many=True).load(obj_dict_list)
        assert data[0].name == 'Produce'
        assert len(data) == 4
        
    def test_create_department(self):
        dep = r"""{"name" : "hba"}"""
        result = self.t_client_post('/departments/', dep)
        assert result.status_code == 200
        result = app.test_client().get('/departments/')
        assert result.status_code == 200
        assert 'hba' in result.data
        
    def test_update_department(self):
        dep = r"""{"name" : "hba"}"""
        assert Department.query.get(1).name == 'Produce'
        result = self.t_client_put('/departments/1', dep)
        assert Department.query.get(1).name == 'hba'

    def test_delete_department(self):
        assert Department.query.get(1).name == 'Produce'
        result = self.t_client_delete('/departments/1')
        assert Department.query.get(1) is None

        
@unittest.skip('skipping')
class UnitsViewTest(ViewTest):
    fixtures = ['units.json']
    
    def test_unit(self):
        result = app.test_client().get('/units/1')
        units = json.loads(result.data)['units']

        assert units['name'] == 'tablespoon'
        assert units['id'] == 1
        
    def test_bad_unit_id(self):
        result = app.test_client().get('/units/15')
        assert result.status_code == 404
        
    def test_all_units(self):
        result = app.test_client().get('/units/')
        units = json.loads(result.data)['units']
        assert len(units) == 4
    
    def test_create_unit(self):
        j = json.dumps({'units' : {'name' : 'pound'}})
        result = self.t_client_post('/units/', j)
        result = app.test_client().get('/units/')
        
    def test_update_unit(self):
        assert Unit.query.get(1).name == 'tablespoon'
        j = json.dumps({'units' : {'name' : 'TBSP'}})
        result = self.t_client_put('/units/1', j)
        assert Unit.query.get(1).name == 'TBSP'
    
    def test_delete_unit(self):
        assert Unit.query.get(1).name == 'tablespoon'
        result = self.t_client_delete('/units/1')
        assert Unit.query.get(1) is None 
@unittest.skip("classing skipping")       
class StepsViewTest(ViewTest):
    fixtures = ['steps.json',
                'recipes.json']
    
    def test_step(self):
        result = app.test_client().get('/steps/1')
        steps = json.loads(result.data)['steps']

        assert steps['step'] == 'Bring water to a boil'
        assert steps['order'] == 1
        
    def test_bad_step_id(self):
        result = app.test_client().get('/steps/15')
        error = json.loads(result.data)['message']
        assert error == 404
        
    def test_all_steps(self):
        result = app.test_client().get('/steps/')
        steps = json.loads(result.data)['steps']
        assert len(steps) == 4
    
    def test_create_step(self):
        j = json.dumps({'steps' : {'step' : 'Chop onions.'}})
        result = self.t_client_post('/steps/', j)
        result = app.test_client().get('/steps/')
        
    def test_update_step(self):
        assert Step.query.get(1).step == 'Bring water to a boil'
        j = json.dumps({'steps' : {'step' : 'asdfjk;'}})
        result = self.t_client_put('/steps/1', j)
        assert Step.query.get(1).step == 'asdfjk;'
    
    def test_delete_step(self):
        assert Step.query.get(1).step == 'Bring water to a boil'
        result = self.t_client_delete('/steps/1')
        assert Step.query.get(1) is None
@unittest.skip("classing skipping")        
class NotesViewTest(ViewTest):
    fixtures = ['notes.json',
                'recipes.json']
    
    def test_note(self):
        result = app.test_client().get('/notes/1')
        notes = json.loads(result.data)['notes']

        assert notes['note'] == 'Eat with asparagus'
        assert notes['id'] == 1
        
    def test_bad_note_id(self):
        result = app.test_client().get('/notes/15')
        error = json.loads(result.data)['message']
        assert error == 404
        
    def test_all_notes(self):
        result = app.test_client().get('/notes/')
        notes = json.loads(result.data)['notes']
        assert len(notes) == 1
    
    def test_create_note(self):
        j = json.dumps({'notes' : {'note' : 'bakery'}})
        result = self.t_client_post('/notes/', j)
        result = app.test_client().get('/notes/')
        
    def test_update_note(self):
        assert Note.query.get(1).note == 'Eat with asparagus'
        j = json.dumps({'notes' : {'note' : 'Serve with bread'}})
        result = self.t_client_put('/notes/1', j)
        assert Note.query.get(1).note == 'Serve with bread'
    
    def test_delete_note(self):
        assert Note.query.get(1).note == 'Eat with asparagus'
        result = self.t_client_delete('/notes/1')
        assert Note.query.get(1) is None

@unittest.skip("classing skipping")
class RecipesViewTest(ViewTest):
    fixtures = ['recipes.json',
                'steps.json',
                'notes.json']
    
    def test_recipe(self):
        result = app.test_client().get('/recipes/1')
        recipes = json.loads(result.data)['recipes']

        assert recipes['name'] == 'Spaghetti and Meatballs'
        assert recipes['id'] == 1
        
    def test_bad_recipe_id(self):
        result = app.test_client().get('/recipes/15')
        error = json.loads(result.data)['message']
        assert error == 404
        
    def test_all_recipes(self):
        result = app.test_client().get('/recipes/')
        recipes = json.loads(result.data)['recipes']
        assert len(recipes) == 3
    
    def test_create_recipe(self):
        j = json.dumps({'recipes' : {'name' : 'roast beef'}})
        result = self.t_client_post('/recipes/', j)
        result = app.test_client().get('/recipes/')
        
    def test_update_recipe(self):
        assert Recipe.query.get(1).name == 'Spaghetti and Meatballs'
        j = json.dumps({'recipes' : {'name' : 'boyardee'}})
        result = self.t_client_put('/recipes/1', j)
        assert Recipe.query.get(1).name == 'boyardee'
    
    def test_delete_recipe(self):
        assert Recipe.query.get(1).name == 'Spaghetti and Meatballs'
        result = self.t_client_delete('/recipes/1')
        assert Recipe.query.get(1) is None

    def test_add_step_to_recipe(self):
        j = json.dumps({'steps' : {'step' : 'add pasta to water', 'order' : 4}})
        result = self.t_client_post('/recipes/1/steps/', j)
        result = app.test_client().get('/recipes/1')
        
