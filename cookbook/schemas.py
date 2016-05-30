from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, pre_load, post_load, post_dump

from cookbook import db
from cookbook.models import Department, Ingredient

class BaseSchema(ModelSchema):
    class Meta:
        sqla_session = db.session
   
        
class DepartmentSchema(BaseSchema):
    
    __model__ = Department
    ingredients = fields.Nested('IngredientSchema', many=True, exclude=('department', 'recipeingredients' ))
    class Meta(BaseSchema.Meta):
        model = Department
        
class IngredientSchema(BaseSchema):
    
    __model__ = Ingredient
    department = fields.Nested('DepartmentSchema', exclude=('ingredients', ), required=True)
    class Meta(BaseSchema.Meta):
        model = Ingredient