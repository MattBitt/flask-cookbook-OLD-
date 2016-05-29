from cookbook import app, api
from cookbook.models import Ingredient, Department, Unit, Step, Note, Recipe
from cookbook.models import DepartmentSchema, IngredientSchema, UnitSchema
from cookbook.models import StepSchema, NoteSchema, RecipeSchema
from flask import jsonify, request

import json

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)
unit_schema = UnitSchema()
units_schema = UnitSchema(many=True)
step_schema = StepSchema()
steps_schema = StepSchema(many=True)
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

def get_object(obj, obj_schema, id, envelope):
    try:
        new_obj = obj.query.get(id)
    except IntegrityError:
        return jsonify({"message": "{} could not be found.".format(envelope)}), 400
    if new_obj:
        result = obj_schema.dump(new_obj)
        return jsonify({envelope : result.data})
    else:
        return jsonify({'message' : 404})
        
def get_objects(obj, obj_schema, envelope):
    objs = obj.query.all()
    if objs:
        result = obj_schema.dump(objs)
        return jsonify({envelope : result.data})
    else:
        return jsonify({'message' : 'No {}s found'.format(envelope)})

        
def update_object(obj, obj_schema, id, envelope):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    data, errors = obj_schema.load(json_data[envelope])
    if errors:
        return jsonify(errors), 422
    new_obj = obj.query.get(id)
    new_obj.update_from(data)
        
    result = obj_schema.dump(obj.query.get(new_obj.id))
    return jsonify({"message": "Updated envelope.",
                    envelope : result.data})

def create_object(obj, obj_schema, envelope):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    data, errors = obj_schema.load(json_data[envelope])
    if errors:
        return jsonify(errors), 422
    data.save()
    
    result = obj_schema.dump(obj.query.get(data.id))
    return jsonify({"message": "Created new envelope.",
                    envelope : result.data})       

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
@app.route('/departments/', methods=['GET'])
def get_departments():   
    return get_objects(Department, departments_schema, 'departments')

@app.route('/departments/', methods=['POST'])
def create_department():
    return create_object(Department, department_schema, 'departments')

@app.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    return update_object(Department, department_schema,
                         id, 'departments')
                    
@app.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    return get_object(Department, department_schema, id, 'departments')

@app.route('/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    return delete_object(Department, id, 'department')


    
    
    
############## Ingredient Routes ####################    
@app.route('/ingredients/', methods=['GET'])
def get_ingredients():   
    return get_objects(Ingredient, ingredients_schema, 'ingredients')

@app.route('/ingredients/', methods=['POST'])
def create_ingredient():
    return create_object(Ingredient, ingredient_schema, 'ingredients')

@app.route('/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id):
    return update_object(Ingredient, ingredient_schema,
                         id, 'ingredients')
                    
@app.route('/ingredients/<int:id>', methods=['GET'])
def get_ingredient(id):
    return get_object(Ingredient, ingredient_schema, id, 
                      'ingredients')

@app.route('/ingredients/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
    return delete_object(Ingredient, id, 'ingredient')


############## Unit Routes ####################    
@app.route('/units/', methods=['GET'])
def get_units():   
    return get_objects(Unit, units_schema, 'units')
                    
@app.route('/units/<int:id>', methods=['GET'])
def get_unit(id):
    return get_object(Unit, unit_schema, id, 'units')

@app.route('/units/', methods=['POST'])
def create_unit():
    return create_object(Unit, unit_schema, 'units')

@app.route('/units/<int:id>', methods=['PUT'])
def update_unit(id):
    return update_object(Unit, unit_schema, id, 'units')

@app.route('/units/<int:id>', methods=['DELETE'])
def delete_unit(id):
    return delete_object(Unit, id, 'unit')


############## Step Routes ####################    
@app.route('/steps/', methods=['GET'])
def get_steps():   
    return get_objects(Step, steps_schema, 'steps')
                    
@app.route('/steps/<int:id>', methods=['GET'])
def get_step(id):
    return get_object(Step, step_schema, id, 'steps')

@app.route('/steps/', methods=['POST'])
def create_step():
    return create_object(Step, step_schema, 'steps')

@app.route('/steps/<int:id>', methods=['PUT'])
def update_step(id):
    return update_object(Step, step_schema, id, 'steps')

@app.route('/steps/<int:id>', methods=['DELETE'])
def delete_step(id):
    return delete_object(Step, id, 'step')

    
############## Note Routes ####################    
@app.route('/notes/', methods=['GET'])
def get_notes():   
    return get_objects(Note, notes_schema, 'notes')
                    
@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    return get_object(Note, note_schema, id, 'notes')

@app.route('/notes/', methods=['POST'])
def create_note():
    return create_object(Note, note_schema, 'notes')

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    return update_object(Note, note_schema, id, 'notes')

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    return delete_object(Note, id, 'note')
 
############## Recipe Routes ####################    
@app.route('/recipes/', methods=['GET'])
def get_recipes():   
    return get_objects(Recipe, recipes_schema, 'recipes')
                    
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    return get_object(Recipe, recipe_schema, id, 'recipes')

@app.route('/recipes/', methods=['POST'])
def create_recipe():
    return create_object(Recipe, recipe_schema, 'recipes')

@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    return update_object(Recipe, recipe_schema, id, 'recipes')

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    return delete_object(Recipe, id, 'recipe') 


@app.route('/recipes/<int:id>/steps/', methods=['POST'])
def add_new_step_to_recipe(id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    data, errors = step_schema.load(json_data['steps'])
    if errors:
        return jsonify(errors), 422
    data.save()

    recipe = Recipe.query.get(id)
    recipe.steps.append(data)
    recipe.save()
    recipe_result = recipe_schema.dump(Recipe.query.get(id))
    step_result = steps_schema.dump(recipe.steps.all())
    return jsonify({"message": "Created new step in Recipe.",
                    'recipes' : recipe_result.data, 'steps' : step_result.data})    
                    
                    
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
    