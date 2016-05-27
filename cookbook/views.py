from cookbook import app
from cookbook.models import Ingredient, Department
from flask import jsonify


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
    


@app.route('/ingredients')    
def get_ingredients():
    ingred_list = []
    depart_list = []
    for i in Ingredient.query.all():
        ingred_list.append(i.as_dict)
    for d in Department.query.all():
        depart_list.append({'name' : d.name, 'id' : d.id})
    
    
    ingred_dict = {'ingredients' : ingred_list, 'departments' : depart_list}
    return jsonify(**ingred_dict)