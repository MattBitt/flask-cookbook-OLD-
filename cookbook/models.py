
from cookbook import db, ma
from utils.serializer import serialize 
from marshmallow import fields, ValidationError, validate


class CRUDModel(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_from(self, new_obj):
        raise NotImplementedError
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

        
class RecipeIngredient(db.Model, CRUDModel):
    __tablename__ = 'recipeingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    qty = db.Column(db.Float)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    preparation = db.Column(db.String)
    # put a column for the ingredient heading here?
    # in this example, oil and flour would have ingredient grouping "roux" and 
    # bell pepper... would have ingredient_grouping "gumbo"
    # if no groupings field would be blank
    # allow for links to subrecipes on our site?
    # Roux
    # 1 cup oil
    # 1 cup of flour
    # Gumbo
    # 1 bell pepper
    # 
    
    
    # try to emulate Modernist Cuisine Style Recipes?
    # give each recipeingredient and step and group number
    # subrecipe wouldn't be important anymore
    #
    # 1 cup oil                                 Stir Together
    # 1 cup flour                           Cook until desired color
    # _____________________________________________________________
    # 1 Onion                                   Chop vegetables
    # 1 bell pepper    

    
    @property
    def ingredient_name(self):
        return Ingredient.query.get(self.ingredient_id).name
    
    @property
    def recipe_name(self):
        return Recipe.query.get(self.recipe_id).name
    
    @property
    def unit_name(self):
        return Unit.query.get(self.unit_id).name
    
    def __repr__(self):
        return '<RecipeIngredient {} {} {}, {} >'.format(self.qty, self.unit_name, self.ingredient_name, self.preparation)

    def __str__(self):
        return '<RecipeIngredient {} {} {}, {} >'.format(self.qty, self.unit_name, self.ingredient_name, self.preparation)

        
class Step(db.Model, CRUDModel):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    step = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))


    def __repr__(self):
        return '<Step {:d} {} (Recipe {})>'.format(self.order, self.step, self.recipe_id)

    def __str__(self):
        return self.step
        
    def update_from(self, new_obj):
        self.step = new_obj.step
        self.order = new_obj.order
        self.recipe_id = new_obj.recipe_id
        self.save()

class StepSchema(ma.ModelSchema):
    step = fields.Str()
    order = fields.Int()
    recipe = fields.Nested('RecipeSchema')
    class Meta:
        # Fields to expose
        
        model = Step
        #fields = ('step', 'order')
            
class Note(db.Model, CRUDModel):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    def __repr__(self):
        return '<Note {:d} {}>'.format(self.id, self.note)

    def __str__(self):
        return self.note
        
    def update_from(self, new_obj):
        self.note = new_obj.note
        self.recipe_id = new_obj.recipe_id
        
        self.save()

class NoteSchema(ma.ModelSchema):
    note = fields.Str()
    recipe = fields.Nested('RecipeSchema')
    class Meta:
        model = Note

        
class Ingredient(db.Model, CRUDModel):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    recipeingredients = db.relationship('RecipeIngredient', backref='ingredient',
                                lazy='dynamic')
    
    @property
    def as_dict(self):
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {'name' : self.name, 'department' : self.department_name}
    
    @property
    def department_name(self):
        return Department.query.get(self.department_id).name
    
    
    def __repr__(self):
        return '<Ingredient id {:d}: {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

    def update_from(self, new_obj):
        self.name = new_obj.name
        self.department_id = new_obj.department_id
        self.save()
        
class Department(db.Model, CRUDModel):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.relationship('Ingredient', backref='department',
                                lazy='dynamic')


    @property
    def ingredients_list(self):
        return [i.serialize() for i in self.ingredients.all()]
    
    def __repr__(self):
        return '<Department {} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name
        
    def update_from(self, new_obj):
        self.name = new_obj.name
        self.save()


class IngredientSchema(ma.ModelSchema):
    name = fields.Str()
    department = fields.Nested('DepartmentSchema', exclude=('ingredients',))
     #Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_ingredient', id='<id>'),
        'collection': ma.URLFor('get_ingredients')
    })
    class Meta:
        model = Ingredient



        
class DepartmentSchema(ma.ModelSchema):
    ingredients = fields.Nested(IngredientSchema, many=True, exclude=('department',))
    name = fields.Str()
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_department', id='<id>'),
        'collection': ma.URLFor('get_departments')
    })    
    class Meta:
        model = Department
        



class Unit(db.Model, CRUDModel):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Unit {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name
        
    def update_from(self, new_obj):
        self.name = new_obj.name
        self.save()
        
class UnitSchema(ma.ModelSchema):
    
    name = fields.String()
    class Meta:
        model = Unit    

class Recipe(db.Model, CRUDModel):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rating = db.Column(db.Integer)
    date_added = db.Column(db.String)
    steps = db.relationship('Step', backref='recipe',
                                lazy='dynamic')
    notes = db.relationship('Note', backref='recipe',
                                lazy='dynamic')
    recipeingredients = db.relationship('RecipeIngredient', backref='recipe',
                                lazy='dynamic')                                
                                
    def __repr__(self):
        return '<Recipe {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name
        
    def update_from(self, new_obj):
        self.name = new_obj.name
        self.rating = new_obj.rating
        self.date_added = new_obj.date_added
        self.save()

class RecipeSchema(ma.ModelSchema):
    steps = fields.Nested(StepSchema, many=True, exclude=('recipe',))
    notes = fields.Nested(NoteSchema, many=True, exclude=('recipe',))
    name = fields.Str()
    _links = ma.Hyperlinks({
        'self': ma.URLFor('get_recipe', id='<id>'),
        'collection': ma.URLFor('get_recipes')
    })
    class Meta:
        # Fields to expose
        model = Recipe
