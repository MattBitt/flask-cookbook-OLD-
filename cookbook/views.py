from cookbook import app
from cookbook.models import Ingredient, Department
from flask import jsonify
from cookbook.schemas import IngredientSchema, DepartmentSchema
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
    
@app.route('/ingredients')
def get_ingredients():

    ingreds = Ingredient.query.all()
    result = IngredientSchema(many=True).dump(ingreds)
    #return jsonify({'ingredients' : result.data})
    return jsonify({'ingredients' :result.data})

@app.route('/departments')
def get_departments():
    departments = Department.query.all()
    result = DepartmentSchema(many=True).dump(departments)
    return jsonify({'departments' :result.data})
    