from cookbook import app
from cookbook.models import Ingredient, Department, Unit, Step, Note, Recipe
from cookbook.schemas import DepartmentSchema, IngredientSchema, UnitSchema, StepSchema
from cookbook.schemas import NoteSchema, RecipeSchema
from flask import jsonify, request, abort
from flask_classy import FlaskView, route
import json
from webargs.flaskparser import parser
from webargs import fields

app.logger.debug('loading views.py')

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('custom 404 error function')
    return jsonify({'message' : 'custom not found'}), 404
                  
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
index_args = {'q' : fields.Str(),
        'sort' : fields.Str()
       }

class CRUDView(FlaskView):
    
    def index(self):
        ## retrieve all items from db and dump it them to a list of json strings
        args = parser.parse(index_args, request)
        app.logger.debug('GET request for all {}'.format(self.desc))
        app.logger.debug('Arguments passed in:  {}'.format(args))
        objs = self.obj.query.all()
        if objs:
            obj_dict_list, errors = self.schema(many=True).dump(objs)
            if errors:
                return jsonify(errors), 500
            return jsonify(obj_dict_list)
        else:
            return jsonify({'message' : 'No {}s found'.format(self.desc)})

    def get(self, id):
        app.logger.debug('GET request for {}: id: {}'.format(self.desc, id))
        try:
            obj = self.obj.query.get(id)
        except:
            return jsonify({"message": "Error processing {} query: {}.".format(self.desc, self.obj.query)}), 400
        if obj:
            app.logger.debug('{} id:{} found.'.format(self.desc, id))
            obj_dict, errors = self.schema(many=False).dump(obj)
            if errors:
                app.logger.debug("Error dumping schema {}: {}".format(self.desc, errors))
                return jsonify({"message": "Error dumping {}: {}.".format(self.desc, errors)}), 400
            return jsonify(obj_dict)
        else:
            #abort(404)
            app.logger.debug("404 Error.  No {} found with id {}.".format(self.desc, id))
            return jsonify({"message": "{} could not be found.".format(self.desc)}), 404
    
    def post(self):
        ## if this is always a POST request, should return 201
        ## takes in a new data and dumps that to a new object
        ## this new object is then saved in the database
        app.logger.debug("POST request for {}:".format(self.desc))
        json_data = request.get_json()
        if not json_data:
            app.logger.error("No json_data for POST request")
            return jsonify({'message': 'No input data provided'}), 400
        app.logger.debug("Incoming data: {}".format(json_data))
        obj_dict, errors = self.schema().load(json_data)
        if errors:
            app.logger.debug("Error loading schema {}: {}".format(self.desc, errors))
            return jsonify({"message": "Error dumping {}: {}.".format(self.desc, errors)}), 400
        obj_dict.save()
        result, errors = self.schema().dump(obj_dict)
        return jsonify(result)       

    def put(self, id):
        ## takes in new data and converts that to a new object
        ## the existing (id) object is updated with the fields from the newly created one
        app.logger.debug("PUT request for {}:".format(self.desc))
        json_data = request.get_json()
        if not json_data:
            app.logger.error("No json_data for PUT request")
            return jsonify({'message': 'No input data provided'}), 400
        app.logger.debug("Incoming data: {}".format(json_data))
        new_obj, errors = self.schema().load(json_data, partial=True)
        if errors:
            app.logger.debug("Error loading schema {}: {}".format(self.desc, errors))
            return jsonify({"message": "Error dumping {}: {}.".format(self.desc, errors)}), 400
        existing_obj = self.obj.query.get(id)
        existing_obj.update_from(new_obj)
            
        result, errors = self.schema().dump(existing_obj)
        if errors:
            app.logger.debug("Error dumping schema {}: {}".format(self.desc, errors))
            return jsonify({"message": "Error dumping {}: {}.".format(self.desc, errors)}), 400
        return jsonify(result)
        
    def delete(self, id):
        app.logger.debug("DELETE request for {} {}:".format(self.desc, id))
        try:
            new_obj = self.obj.query.get(id)
        except IntegrityError:
            return jsonify({"message": "{} could not be found.".format(self.desc)}), 400
        new_obj.delete()
        return jsonify({"message": "Deleted item."})    
        
class DepartmentsView(CRUDView):
    def __init__(self):
        self.obj = Department
        self.schema = DepartmentSchema
        self.desc = 'departments'
        
    # this is how to add individual stuff to the views
    def index(self):
        #add specific stuff here before calling super
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

class RecipesView(CRUDView):
    def __init__(self):
        self.obj = Recipe
        self.schema = RecipeSchema
        self.desc = 'recipes'
    
      
DepartmentsView.register(app)
IngredientsView.register(app)
UnitsView.register(app)
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
    