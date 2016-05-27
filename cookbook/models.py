
from cookbook import db



class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
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


class Step(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    step = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))


    def __repr__(self):
        return '<Step {:d} {} (Recipe {})>'.format(self.order, self.step, self.recipe_id)

    def __str__(self):
        return self.step


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    def __repr__(self):
        return '<Note {:d} {}>'.format(self.id, self.note)

    def __str__(self):
        return self.note

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    recipeingredients = db.relationship('RecipeIngredient', backref='ingredient',
                                lazy='dynamic')
    
    @property
    def as_dict(self):
        #return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {'name' : self.name, 'department' : Department.query.get(self.department_id).name}
    
    def __repr__(self):
        return '<Ingredient id {:d}: {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.relationship('Ingredient', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name


class RecipeIngredient(db.Model):
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


class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Unit {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

