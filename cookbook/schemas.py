#from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields, pprint
from models import Ingredient, Department
from cookbook import db



class IngredientSchema(Schema):
    name = fields.Str()
    department = fields.Str()

    class Meta:
        model = Ingredient
        sqla_session = db.session


class DepartmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()

    class Meta:
        model = Department
    

ingredient_schema = IngredientSchema()
department_schema = DepartmentSchema()
ingredients_schema = IngredientSchema(many=True)
departments_schema = DepartmentSchema(many=True)