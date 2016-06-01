from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, pre_load, post_load, post_dump

from cookbook import db
from cookbook.models import Department, Ingredient, Unit, Step, Note, Recipe, RecipeIngredient

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
        
class UnitSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Unit
        
class StepSchema(BaseSchema):
    recipe = fields.Nested('RecipeSchema', exclude=('steps', ), required=True)
    class Meta(BaseSchema.Meta):
        model = Step
        
class NoteSchema(BaseSchema):
    recipe = fields.Nested('RecipeSchema', exclude=('notes', ), required=True)
    class Meta(BaseSchema.Meta):
        model = Note
        
class RecipeSchema(BaseSchema):
    steps = fields.Nested('StepSchema', many=True, exclude=('recipe', ))
    notes = fields.Nested('NoteSchema', many = True, exclude=('recipe',))
    recipeingredients = fields.Nested('RecipeIngredientSchema', many = True, exclude=('recipe',))
    class Meta(BaseSchema.Meta):
        model = Recipe
        
class RecipeIngredientSchema(BaseSchema):
    recipe = fields.Nested('RecipeSchema', exclude=('recipeingredients', ), required=True)
    ingredient = fields.Nested('IngredientSchema', exclude=('recipeingredients', ), required=True)
    unit = fields.Nested('UnitSchema', exclude=('recipeingredients', ), required=True)
    
    class Meta(BaseSchema.Meta):
        model = RecipeIngredient