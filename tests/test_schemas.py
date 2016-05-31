from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from flask_testing import TestCase
from cookbook import db, app
from flask_fixtures import FixturesMixin
import json

import unittest 
from cookbook.schemas import DepartmentSchema, IngredientSchema, UnitSchema
from cookbook.schemas import StepSchema, NoteSchema
FixturesMixin.init_app(app, db)

class SchemaTest(TestCase, FixturesMixin):
    
    fixtures = ['ingredients.json', 
                'departments.json',
                'units.json',
                'steps.json',
                'notes.json', 
                'recipes.json']
    
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        #app.config.from_object('config.TestingLocalDBConfig')
        return app
        
class DepartmentSchemaTest(SchemaTest):
    ### dump object to dict
    def test_dump_one_existing(self):
        dep = Department.query.get(1)
        data, errors = DepartmentSchema().dump(dep)
        assert errors == {}
        assert type(data) == dict
        assert data['name'] == 'Produce'
        assert data['id'] == 1
        assert len(data['ingredients']) == 3
    
    ### dump object to dict
    def test_dump_many(self):
        deps = Department.query.all()
        data, errors = DepartmentSchema(many=True).dump(deps)
        assert errors == {}
        assert type(data) == list
        assert data[0]['name'] == 'Produce'
        assert data[0]['id'] == 1
        assert data[0]['ingredients'][2]['name'] == 'honey kiss melon'
    
    def test_load_one_existing(self):
    ### load string to object
        json_string = r"""{"id": 1, "name": "Produce", "ingredients": [{"id": 1, "name": "cauliflower"}, {
                           "id": 2, "name": "broccoli"}, {"id": 5, "name": "honey kiss melon"}]}"""
        data, errors = DepartmentSchema().loads(json_string)
        assert isinstance(data, Department) == True
        assert data.name == 'Produce'
        assert data.id == 1
        assert len(data.ingredients.all()) == 3
    
    ### load a "new" department string to a new Department object
    def test_load_one_new(self):
        json_string = r"""{"name": "hba"}"""
        data, errors = DepartmentSchema().loads(json_string)
        assert errors == {}
        assert isinstance(data, Department)
        assert data.name == 'hba'
        data.save()
        assert data.id == 5
        assert data.ingredients.all() == []
    
    def test_load_many(self):
    ### load string to list of objects
        json_string = r"""[{"id": 1, "name": "Produce", "ingredients": [{"id": 1, "name": "cauliflower"},
                           {"id": 2, "name": "broccoli"}, {"id": 5, "name": "honey kiss melon"}]}, {"id": 2,
                            "name": "Grocery", "ingredients": [{"id": 3, "name": "spaghetti"}]}, {"id": 3,
                            "name": "Meat", "ingredients": []}, {"id": 4, "name": "Dairy", "ingredients": 
                           [{"id": 4, "name": "milk"}]}]"""

        data, errors = DepartmentSchema(many=True).loads(json_string)
        assert errors == {}
        assert type(data) == list
        assert isinstance(data[0], Department) == True
        
    

        
class IngredientSchemaTest(SchemaTest):
    ### load object from string
    def test_dump_one(self):
        ing = Ingredient.query.get(1)
        data, errors = IngredientSchema().dump(ing)
        assert errors == {}
        assert type(data) == dict
        assert data['name'] == 'cauliflower'
        assert data['id'] == 1
        assert data['department']['name'] == 'Produce'
        
    def test_dump_many(self):
        ings = Ingredient.query.all()
        data, errors = IngredientSchema(many=True).dump(ings)
        assert errors == {}
        assert type(data) == list
        assert data[0]['name'] == 'cauliflower'
        assert data[0]['id'] == 1
        assert data[0]['department']['name'] == 'Produce'

    ### load string to object        
    def test_load_one_existing(self):
        json_string = r"""{"department": {"id": 1, "name": "Produce"}, "id": 1, "name": "cauliflower",
                           "recipeingredients": []}"""
        data, errors = IngredientSchema().loads(json_string)
        assert isinstance(data, Ingredient) == True
        assert data.name == 'cauliflower'
        assert data.id == 1
        assert data.department.id == 1
    
    ### load a "new" ingredient string to a new Ingredient object
    def test_load_one_new(self):
        json_string = r"""{"name": "mustard", "department": {"id": 2, "name": "Grocery"}}"""
        data, errors = IngredientSchema().loads(json_string)
        assert errors == {}
        assert isinstance(data, Ingredient)
        assert data.name == 'mustard'
        assert data.department.id == 2
        data.save()
        assert data.id == 6
    
    ### load a "new" ingredient string to a new Ingredient object
    def test_load_one_new_missing_department(self):
        json_string = r"""{"name": "mustard"}"""
        data, errors = IngredientSchema().loads(json_string)
        assert errors['department'][0] == u'Missing data for required field.'
        
    def test_load_many(self):
    ### load string to list of objects
        json_string = r"""[{"department": {"id": 1, "name": "Produce"}, "id": 1, "name": "cauliflower", 
                            "recipeingredients": []}, {"department": {"id": 1, "name": "Produce"}, "id": 2, 
                            "name": "broccoli", "recipeingredients": []}, {"department": {"id": 2, "name": 
                            "Grocery"}, "id": 3, "name": "spaghetti", "recipeingredients": []}, {"department":
                            {"id": 4, "name": "Dairy"}, "id": 4, "name": "milk", "recipeingredients": []}, 
                            {"department": {"id": 1, "name": "Produce"}, "id": 5, "name": "honey kiss melon",
                            "recipeingredients": []}]"""
        data, errors = IngredientSchema(many=True).loads(json_string)
        assert errors == {}
        assert type(data) == list
        assert isinstance(data[0], Ingredient) == True
        
class UnitSchemaTest(SchemaTest):
    ### load object from string
    def test_dump_one(self):
        uni = Unit.query.get(1)
        data, errors = UnitSchema().dump(uni)
        assert errors == {}
        assert type(data) == dict
        assert data['name'] == 'tablespoon'
        assert data['id'] == 1
         
    def test_dump_many(self):
        units = Unit.query.all()
        data, errors = UnitSchema(many=True).dump(units)
        assert errors == {}
        assert type(data) == list
        assert data[0]['name'] == 'tablespoon'
        assert data[0]['id'] == 1

    ### load string to object        
    def test_load_one_existing(self):
        json_string = r"""{"id": 1, "name": "tablespoon",
                           "recipeunits": []}"""
        data, errors = UnitSchema().loads(json_string)
        assert isinstance(data, Unit) == True
        assert data.name == 'tablespoon'
        assert data.id == 1
    
    ### load a "new" unit string to a new Unit object
    def test_load_one_new(self):
        json_string = r"""{"name": "liter"}"""
        data, errors = UnitSchema().loads(json_string)
        assert errors == {}
        assert isinstance(data, Unit)
        assert data.name == 'liter'
        data.save()
        assert data.id == 5

class StepSchemaTest(SchemaTest):
    ### load object from string
    def test_dump_one(self):
        step = Step.query.get(1)
        data, errors = StepSchema().dump(step)
        assert errors == {}
        assert type(data) == dict
        assert data['step'] == 'Bring water to a boil'
        assert data['id'] == 1
        assert data['recipe']['name'] == 'Spaghetti and Meatballs'
        
    def test_dump_many(self):
        steps = Step.query.all()
        data, errors = StepSchema(many=True).dump(steps)
        assert errors == {}
        assert type(data) == list
        assert data[0]['step'] == 'Bring water to a boil'
        assert data[0]['id'] == 1
        assert data[0]['recipe']['name'] == 'Spaghetti and Meatballs'

    ### load string to object        
    def test_load_one_existing(self):
        json_string = r"""{"id": 1, "step": "Bring water to a boil", "order" : 1, 
                           "recipe" : {"id" : 1}}"""
        data, errors = StepSchema().loads(json_string)
        assert isinstance(data, Step) == True
        assert data.step == u'Bring water to a boil'
        assert data.id == 1
        assert data.order == 1
        assert data.recipe.id == 1
    
    ### load a "new" step string to a new Step object
    # sending a recipe dict without an id will create a new recipe
    # need to check in view whether that recipe exists or not
    def test_load_one_new(self):
        json_string = r"""{"step": "Simmer for 10", "order" : 4, 
                           "recipe" : {"name" : "Tacos"}}"""
        data, errors = StepSchema().loads(json_string)
        assert errors == {}
        assert isinstance(data, Step)
        assert data.step == 'Simmer for 10'
        assert data.order == 4
        assert data.recipe.name == 'Tacos'
        data.save()
        assert data.recipe.id == 4
        assert data.id == 5
        
    def test_load_one_new_missing_recipe(self):
        json_string = r"""{"step": "chop herbs", "order" : 12}"""
        data, errors = StepSchema().loads(json_string)
        assert errors['recipe'][0] == u'Missing data for required field.'
    
class NoteSchemaTest(SchemaTest):
    ### load object from string
    def test_dump_one(self):
        note = Note.query.get(1)
        data, errors = NoteSchema().dump(note)
        assert errors == {}
        assert type(data) == dict
        assert data['note'] == 'Eat with asparagus'
        assert data['id'] == 1
        assert data['recipe']['name'] == 'Spaghetti and Meatballs'
        
    def test_dump_many(self):
        notes = Note.query.all()
        data, errors = NoteSchema(many=True).dump(notes)
        assert errors == {}
        assert type(data) == list
        assert data[0]['note'] == 'Eat with asparagus'
        assert data[0]['id'] == 1
        assert data[0]['recipe']['name'] == 'Spaghetti and Meatballs'
        
    ### load string to object        
    def test_load_one_existing(self):
        json_string = r"""{"id": 1, "note": "Eat with asparagus", 
                           "recipe" : {"id" : 1}}"""
        data, errors = NoteSchema().loads(json_string)
        assert isinstance(data, Note) == True
        assert data.note == 'Eat with asparagus'
        assert data.id == 1
        assert data.recipe.id == 1
    
    ### load a "new" note string to a new Note object
    def test_load_one_new(self):
        json_string = r"""{"note": "dont burn it", "recipe": {"id": 3}}"""
        data, errors = NoteSchema().loads(json_string)
        assert errors == {}
        assert isinstance(data, Note)
        assert data.note == 'dont burn it'
        assert data.recipe.id == 3
        data.save()
        assert data.id == 2
    
    def test_load_one_new_missing_recipe(self):
        json_string = r"""{"note": "chop herbs"}"""
        data, errors = NoteSchema().loads(json_string)
        assert errors['recipe'][0] == u'Missing data for required field.'
