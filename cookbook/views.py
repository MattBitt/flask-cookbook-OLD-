from cookbook import app, api
from cookbook.models import Ingredient, Department, DepartmentSchema, IngredientSchema
from flask import jsonify

import json

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)

def get_individual_object(obj, id):
    q = obj.query.get(id)
    if q:
        return jsonify(departments=q.serialize())
    else:
        return jsonify({'error' : 404})    

        
def get_objects(obj):
    q_list = obj.all()
    if q_list:
        return jsonify(ingredients=[q.serialize() for q in q_list])
    else:
        return jsonify({'error' : 404})    

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
  

@app.route('/departments/', methods=['GET'])
def get_departments():   
    all_departments = Department.query.all()
    result = departments_schema.dump(all_departments)
    print result.data
    return jsonify(departments=result.data)
    
    
@app.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    department = Department.query.get(id)
    result = department_schema.dump(department)
    return jsonify(department=result.data)


@app.route('/ingredients/', methods=['GET'])
def get_ingredients():   
    all_ingredients = Ingredient.query.all()
    if all_ingredients:
        result = ingredients_schema.dump(all_ingredients)
        return jsonify(ingredient=result.data)
    else:
        return jsonify({'message' : 'No ingredients found'})

        
@app.route('/ingredients/<int:id>', methods=['GET'])
def get_ingredient(id):
    try:
        ingredient = Ingredient.query.get(id)
    except IntegrityError:
        return jsonify({"message": "Ingredient could not be found."}), 400
    return ingredient_schema.jsonify(ingredient)    
    
@app.route('/departments/<int:id>/ingredients/', methods=['GET'])
def get_department_ingredients(id):
    try:
        department = Department.query.get(id)
    except IntegrityError:
        return jsonify({"message": "Department could not be found."}), 400
    department_result = department_schema.dump(department)
    ingredients_result = ingredients_schema.dump(department.ingredients.all())
    return jsonify({'department': department_result.data, 'ingredients': ingredients_result.data})
    