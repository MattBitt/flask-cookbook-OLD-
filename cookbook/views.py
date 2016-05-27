from cookbook import app
from cookbook.models import Ingredient, Department
from flask import jsonify


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
    
@app.route('/ingredients')
def get_ingredients():

    ingreds = Ingredient.query.all()
    
  

@app.route('/departments')
def get_departments():
    departments = Department.query.all()
    
    