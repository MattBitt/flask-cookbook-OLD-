from cookbook import app, api
from cookbook.models import Ingredient, Department, Unit, Step, Note, Recipe
from cookbook.schemas import DepartmentSchema, IngredientSchema, UnitSchema, StepSchema
from cookbook.schemas import NoteSchema, RecipeSchema
from flask import jsonify, request

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
  
############## Department Routes ####################
@app.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    return get_object(Department, DepartmentSchema, id, 'department')
    
@app.route('/departments/', methods=['GET'])
def get_departments():   
    return get_objects(Department, DepartmentSchema, 'departments')

@app.route('/departments/', methods=['POST'])
def create_department():
    return create_object(Department, DepartmentSchema, 'departments')

@app.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    return update_object(Department, DepartmentSchema, id, 'departments')
                    
@app.route('/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    return delete_object(Department, id, 'department')


    
    
    
############## Ingredient Routes ####################    
@app.route('/ingredients/', methods=['GET'])
def get_ingredients():   
    return get_objects(Ingredient, IngredientSchema, 'ingredients')

@app.route('/ingredients/', methods=['POST'])
def create_ingredient():
    return create_object(Ingredient, IngredientSchema,'ingredients')

@app.route('/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id):
    return update_object(Ingredient, IngredientSchema,id, 'ingredients')
                    
@app.route('/ingredients/<int:id>', methods=['GET'])
def get_ingredient(id):
    return get_object(Ingredient, IngredientSchema,id, 'ingredients')

@app.route('/ingredients/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
    return delete_object(Ingredient, id, 'ingredient')


############## Unit Routes ####################    
@app.route('/units/', methods=['GET'])
def get_units():   
    return get_objects(Unit, UnitSchema,'units')
                    
@app.route('/units/<int:id>', methods=['GET'])
def get_unit(id):
    return get_object(Unit, id, UnitSchema,'units')

@app.route('/units/', methods=['POST'])
def create_unit():
    return create_object(Unit, UnitSchema,'units')

@app.route('/units/<int:id>', methods=['PUT'])
def update_unit(id):
    return update_object(Unit, UnitSchema, id,'units')

@app.route('/units/<int:id>', methods=['DELETE'])
def delete_unit(id):
    return delete_object(Unit, id, 'unit')


############## Step Routes ####################    
@app.route('/steps/', methods=['GET'])
def get_steps():   
    return get_objects(Step, StepSchema,'steps')
                    
@app.route('/steps/<int:id>', methods=['GET'])
def get_step(id):
    return get_object(Step, id, StepSchema,'steps')

@app.route('/steps/', methods=['POST'])
def create_step():
    return create_object(Step, StepSchema,'steps')

@app.route('/steps/<int:id>', methods=['PUT'])
def update_step(id):
    return update_object(Step, StepSchema,id, 'steps')

@app.route('/steps/<int:id>', methods=['DELETE'])
def delete_step(id):
    return delete_object(Step, id, 'step')

    
############## Note Routes ####################    
@app.route('/notes/', methods=['GET'])
def get_notes():   
    return get_objects(Note, NoteSchema,'notes')
                    
@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    return get_object(Note, NoteSchema,id, 'notes')

@app.route('/notes/', methods=['POST'])
def create_note():
    return create_object(Note, NoteSchema,'notes')

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    return update_object(Note, NoteSchema,id, 'notes')

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    return delete_object(Note, id, 'note')
 
############## Recipe Routes ####################    
@app.route('/recipes/', methods=['GET'])
def get_recipes():   
    return get_objects(Recipe, RecipeSchema,'recipes')
                    
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    return get_object(Recipe, RecipeSchema,id, 'recipes')

@app.route('/recipes/', methods=['POST'])
def create_recipe():
    return create_object(Recipe, RecipeSchema,'recipes')

@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    return update_object(Recipe, RecipeSchema,id, 'recipes')

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    return delete_object(Recipe, id, 'recipe') 


@app.route('/recipes/<int:id>/steps/', methods=['POST'])
def add_new_step_to_recipe(id):
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
    