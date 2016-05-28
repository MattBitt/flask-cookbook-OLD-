from cookbook import app, api
from cookbook.models import Ingredient, Department
from flask import jsonify

import json


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
  

@app.route('/departments')
def get_departments_list():
    return get_objects(Department.query)
    

@app.route('/departments/<int:department_id>')
def get_department(department_id):
    return get_individual_object(Department, department_id)

@app.route('/departments/<int:department_id>/ingredients')
def get_department_ingredients(department_id):
    d = Department.query.get(department_id)
    return get_objects(d.ingredients)

    
@app.route('/ingredients')            
def get_ingredients_list():
    return get_objects(Ingredient.query)
 
@app.route('/ingredients/<int:ingredient_id>')       
def get_ingredient(ingredient_id):
    return get_individual_object(Ingredient, ingredient_id)

        