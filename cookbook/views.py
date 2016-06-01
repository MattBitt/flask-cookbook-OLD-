from cookbook import app, api
from cookbook.models import Ingredient, Department, Unit, Step, Note, Recipe
from cookbook.schemas import DepartmentSchema, IngredientSchema, UnitSchema, StepSchema
from cookbook.schemas import NoteSchema, RecipeSchema
from flask import jsonify, request
from flask_classy import FlaskView, route

import json
import jsonpickle


def get_object(obj, obj_schema, id, envelope):
    ## retrieve item from db and dump it to a json string
    try:
        new_obj = obj.query.get(id)
    except:# IntegrityError:
        return jsonify({"message": "No {} found with id {}.".format(envelope, id)}), 404
    if new_obj:
        obj_dict, errors = obj_schema(many=False).dump(new_obj)
        return jsonify(obj_dict)
    else:
        return jsonify({"message": "{} could not be found.".format(envelope)}), 404
        
def get_objects(obj, obj_schema, envelope):
    ## retrieve all items from db and dump it them to a list of json strings
    objs = obj.query.all()
    if objs:
        obj_dict_list, errors = obj_schema(many=True).dump(objs)
        if errors:
            return jsonify(errors), 500
        return jsonify(obj_dict_list)
    else:
        return jsonify({'message' : 'No {}s found'.format(envelope)})

def create_object(obj, obj_schema, envelope):
    ## if this is always a POST request, should return 201
    
    ## takes in new data and converts that to a new object
    ## this new object is then saved in the database
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    obj_dict, errors = obj_schema().load(json_data)
    if errors:
        return jsonify(errors), 422
    obj_dict.save()
    
    result, errors = obj_schema().dump(obj_dict)
    return jsonify({"message": "Created new envelope.",
                    envelope : result})       


        
def update_object(obj, obj_schema, id, envelope):
    ## takes in new data and converts that to a new object
    ## the existing (id) object is updated with the fields from the newly created one
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    
    new_obj, errors = obj_schema().load(json_data, partial=True)
    if errors:
        return jsonify(errors), 422
    existing_obj = obj.query.get(id)
    existing_obj.update_from(new_obj)
        
    result, errors = obj_schema().dump(existing_obj)
    if errors:
        return jsonify(errors), 422
    return jsonify({"message": "Updated envelope.",
                    envelope : result})


def delete_object(obj, id, envelope):
    try:
        new_obj = obj.query.get(id)
    except IntegrityError:
        return jsonify({"message": "{} could not be found.".format(envelope)}), 400
    new_obj.delete()
    return jsonify({"message": "Deleted item."})      
                    
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


class CRUDView(FlaskView):
    def index(self):
        return get_objects(self.obj, self.schema, self.desc)

    def get(self, id):
        return get_object(self.obj, self.schema, id, self.desc)

    def post(self):
        return create_object(self.obj, self.schema, self.desc)
    
    def put(self, id):
        return update_object(self.obj, self.schema, id, self.desc)

    def delete(self, id):
        return delete_object(self.obj, id, self.desc)

        
class DepartmentsView(CRUDView):
    def __init__(self):
        self.obj = Department
        self.schema = DepartmentSchema
        self.desc = 'departments'
    
    def index(self):
        print "Only departmentss index"
        return super(DepartmentsView, self).index()
        
        
class IngredientsView(CRUDView):
    def __init__(self):
        self.obj = Ingredient
        self.schema = IngredientSchema
        self.desc = 'ingredients'

class UnitsView(CRUDView):
    def __init__(self):
        self.obj = Unit
        self.schema = UnitSchema
        self.desc = 'units'        

class NotesView(CRUDView):
    def __init__(self):
        self.obj = Note
        self.schema = NoteSchema
        self.desc = 'notes'        

class StepsView(CRUDView):
    def __init__(self):
        self.obj = Step
        self.schema = StepSchema
        self.desc = 'recipes'
        
class RecipesView(CRUDView):
    def __init__(self):
        self.obj = Recipe
        self.schema = RecipeSchema
        self.desc = 'recipes'
    
    @route('/recipes/<int:id>/steps/', methods=['POST'])
    def add_new_step_to_recipe(self, id):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        # Validate and deserialize input
        data, errors = (None, {'message': 'marshmallow gone'})
        if errors:
            return jsonify(errors), 422
        data.save()

        recipe = Recipe.query.get(id)
        recipe.steps.append(data)
        recipe.save()
        data, errors = (None, {'message': 'marshmallow gone'})
        #recipe_result = recipe_schema.dump(Recipe.query.get(id))
        #step_result = steps_schema.dump(recipe.steps.all())
        #return jsonify({"message": "Created new step in Recipe.",
        #                'recipes' : recipe_result.data, 'steps' : step_result.data})    
        return jsonify(errors)
       
DepartmentsView.register(app)
IngredientsView.register(app)
UnitsView.register(app)
StepsView.register(app)
NotesView.register(app)   
RecipesView.register(app)



                    
                    
###############  Do i ever need this?? ###################    
@app.route('/departments/<int:id>/ingredients/', methods=['GET'])
def get_department_ingredients(id):
    try:
        department = Department.query.get(id)
    except IntegrityError:
        return jsonify({"message": "Department could not be found."}), 400
    department_result = department_schema.dump(department)
    ingredients_result = ingredients_schema.dump(department.ingredients.all())
    return jsonify({'department': department_result.data, 'ingredients': ingredients_result.data})
    