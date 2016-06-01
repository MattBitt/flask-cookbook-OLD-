from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from flask_testing import TestCase
from cookbook import db, app
from flask_fixtures import FixturesMixin
import json

import unittest 
from cookbook.schemas import DepartmentSchema, IngredientSchema, UnitSchema, RecipeSchema
from cookbook.schemas import StepSchema, NoteSchema, RecipeIngredientSchema


FixturesMixin.init_app(app, db)




class SchemaTest(TestCase, FixturesMixin):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)

    fixtures = ['recipes.json',
                'steps.json',
                'notes.json',
                'units.json',
                'ingredients.json',
                'departments.json',
                'recipeingredients.json']
    
    __test__ = False
    
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        #app.config.from_object('config.TestingLocalDBConfig')
        return app
    
    ### dump object to dict
    def test_dump_one(self):
        dep = self.component.query.get(1)
        data, errors = self.schema().dump(dep)
        assert errors == {}
        assert type(data) == dict
        assert data[self.test_data['field1']] == self.test_data[self.test_data['field1']]
        assert data[self.test_data['field2']] == self.test_data[self.test_data['field2']]
    
    ### dump object to dict
    def test_dump_many(self):
        deps = self.component.query.all()
        data, errors = self.schema(many=True).dump(deps)
        assert errors == {}
        assert type(data) == list
        assert data[0][self.test_data['field1']] == self.test_data[self.test_data['field1']]
        assert data[0][self.test_data['field2']] == self.test_data[self.test_data['field2']]
        #assert data[0]['ingredients'][2]['name'] == 'honey kiss melon'
    
    ### load string to object
    def test_load_one_existing(self):
        data, errors = self.schema().loads(self.existing_json)
        assert isinstance(data, self.component) == True
        assert data.__dict__[self.test_data['field1']] == self.test_data[self.test_data['field1']]
        assert data.__dict__[self.test_data['field2']] == self.test_data[self.test_data['field2']]
        #assert len(data.ingredients.all()) == 3
    
    ### load a "new" string to a new Department object
    def test_load_one_new(self):
        data, errors = self.schema().loads(self.new_json)
        assert errors == {}
        assert isinstance(data, self.component)
        assert data.name == self.test_data['new_name']
        data.save()
        assert data.id == self.test_data['new_id']
        #assert data.ingredients.all() == []

    ### load string to list of objects    
    def test_load_many(self):
        data, errors = self.schema(many=True).loads(self.many_json)
        assert errors == {}
        assert type(data) == list
        assert isinstance(data[0], self.component) == True
        
class DepartmentSchemaTest(SchemaTest):
    __test__ = True
    
    def __init__(self, *args, **kwargs):
        SchemaTest.__init__(self, *args, **kwargs)
        self.test_data = {'id' : 1,
                          'name' : 'Produce',
                          'new_id' : 5,
                          'new_name' : 'hba',
                          'field1' : 'name',
                          'field2' : 'id'}
        self.component = Department
        self.schema = DepartmentSchema
        self.new_json = r"""{  
                              "name":"hba"
                            }"""
        self.existing_json = r"""{  
                                  "id":1,
                                  "name":"Produce",
                                  "ingredients":[  
                                    {  
                                      "id":1,
                                      "name":"cauliflower"
                                    },
                                    {  
                                      "id":2,
                                      "name":"broccoli"
                                    },
                                    {  
                                      "id":5,
                                      "name":"honey kiss melon"
                                    }
                                  ]
                                }"""
        self.many_json = r"""[  
                              {  
                                "id":1,
                                "name":"Produce",
                                "ingredients":[  
                                  {  
                                    "id":1,
                                    "name":"cauliflower"
                                  },
                                  {  
                                    "id":2,
                                    "name":"broccoli"
                                  },
                                  {  
                                    "id":5,
                                    "name":"honey kiss melon"
                                  }
                                ]
                              },
                              {  
                                "id":2,
                                "name":"Grocery",
                                "ingredients":[  
                                  {  
                                    "id":3,
                                    "name":"spaghetti"
                                  }
                                ]
                              },
                              {  
                                "id":3,
                                "name":"Meat",
                                "ingredients":[  

                                ]
                              },
                              {  
                                "id":4,
                                "name":"Dairy",
                                "ingredients":[  
                                  {  
                                    "id":4,
                                    "name":"milk"
                                  }
                                ]
                              }
                            ]"""
        
class IngredientSchemaTest(SchemaTest):
    __test__ = True
    
    def __init__(self, *args, **kwargs):
        SchemaTest.__init__(self, *args, **kwargs)
        self.test_data = {'id' : 1,
                          'name' : 'cauliflower',
                          'new_id' : 6,
                          'new_name' : 'mustard',
                          'field1' : 'name',
                          'field2' : 'id'}
        self.component = Ingredient
        self.schema = IngredientSchema
        self.new_json = r"""{  
                              "name":"mustard",
                              "department":{  
                                "id":2,
                                "name":"Grocery"
                              }
                            }"""
        self.existing_json = r"""{  
                                  "department":{  
                                    "id":1,
                                    "name":"Produce"
                                  },
                                  "id":1,
                                  "name":"cauliflower",
                                  "recipeingredients":[  

                                  ]
                                }"""
        self.many_json = r"""[  
                              {  
                                "department":{  
                                  "id":1,
                                  "name":"Produce"
                                },
                                "id":1,
                                "name":"cauliflower",
                                "recipeingredients":[  

                                ]
                              },
                              {  
                                "department":{  
                                  "id":1,
                                  "name":"Produce"
                                },
                                "id":2,
                                "name":"broccoli",
                                "recipeingredients":[  

                                ]
                              },
                              {  
                                "department":{  
                                  "id":2,
                                  "name":"Grocery"
                                },
                                "id":3,
                                "name":"spaghetti",
                                "recipeingredients":[  

                                ]
                              },
                              {  
                                "department":{  
                                  "id":4,
                                  "name":"Dairy"
                                },
                                "id":4,
                                "name":"milk",
                                "recipeingredients":[  

                                ]
                              },
                              {  
                                "department":{  
                                  "id":1,
                                  "name":"Produce"
                                },
                                "id":5,
                                "name":"honey kiss melon",
                                "recipeingredients":[  

                                ]
                              }
                            ]"""
        #assert data['department']['name'] == 'Produce'
        #assert data[0]['department']['name'] == 'Produce'
        #assert data.department.id == 1 

class RecipeIngredientSchemaTest(SchemaTest):
    __test__ = True
    
    def __init__(self, *args, **kwargs):
        SchemaTest.__init__(self, *args, **kwargs)
        self.test_data = {'id' : 1,
                          'name' : 'cauliflower',
                          'new_id' : 6,
                          'new_name' : 'mustard',
                          'field1' : 'name',
                          'field2' : 'id'}
        self.component = RecipeIngredient
        self.schema = RecipeIngredientSchema
        self.new_json = r"""{
                              "recipe":{
                                "id": 1
                              },
                              "ingredient":{
                                "id": 5,
                                "department": {
                                  "id": 1
                                }
                              },  
                              "qty" : 12,
                              "unit":{ 
                              "id": 4
                              },
                              "preparation" : "chopped"
                            }"""
        self.existing_json = r""""""
        self.many_json = r"""""" 

    def test_dump_one(self):
        dep = self.component.query.get(1)
        data, errors = self.schema().dump(dep)
        assert errors == {}
        assert type(data) == dict
        assert data['ingredient']['name'] == 'cauliflower'
        assert data['recipe']['name'] == 'Spaghetti and Meatballs'
        assert data['id'] == 1
    
    def test_dump_many(self):
        pass
        
    def test_load_one_existing(self):
        pass
        
    def test_load_one_new(self):
        data, errors = self.schema().loads(self.new_json, partial=True)
        assert errors == {}
        assert isinstance(data, self.component)
        assert data.ingredient.name == 'honey kiss melon'
        data.save()
        assert data.id == self.test_data['new_id']
        
    def test_load_many(self):
        pass
class UnitSchemaTest(SchemaTest):
    __test__ = True
    
    def __init__(self, *args, **kwargs):
        SchemaTest.__init__(self, *args, **kwargs)
        self.test_data = {'id' : 1,
                          'name' : 'tablespoon',
                          'new_id' : 5,
                          'new_name' : 'liter',
                          'field1' : 'name',
                          'field2' : 'id'}
        self.component = Unit
        self.schema = UnitSchema
        self.new_json = r"""{  
                              "name":"liter"
                            }"""
        self.existing_json = r"""{  
                                  "id":1,
                                  "name":"tablespoon"
                                 }"""
        self.many_json = r""""""
    
    @unittest.skip('skipping')
    def test_load_many(self):
        pass
          
    
class StepSchemaTest(SchemaTest):
    __test__ = True
    
    def __init__(self, *args, **kwargs):
        SchemaTest.__init__(self, *args, **kwargs)
        self.test_data = {'id' : 1,
                          'step' : 'Bring water to a boil',
                          'new_id' : 5,
                          'new_name' : 'Simmer for 10',
                          'field1' : 'step',
                          'field2' : 'id'}
        self.component = Step
        self.schema = StepSchema
        self.new_json = r"""{  
                              "step":"Simmer for 10",
                              "order":4,
                              "recipe":{  
                                "name":"Tacos"
                              }
                            }"""
        self.existing_json = r"""{  
                                   "id":1,
                                   "step":"Bring water to a boil",
                                   "order":1,
                                   "recipe":{  
                                     "id":1
                                   }
                                 }"""
        self.many_json = r""""""
    
    @unittest.skip('skipping')
    def test_load_many(self):
        pass

    @unittest.skip('skipping')
    def test_load_one_new(self):
        pass
    ### load a "new" step string to a new Step object
    # sending a recipe dict without an id will create a new recipe
    # need to check in view whether that recipe exists or not
    @unittest.skip('skipping')       
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
