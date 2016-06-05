
from cookbook import db, app
import json

app.logger.debug('loading models.py')


class CRUDModel(object):
    def save(self):
        app.logger.debug('Saving object {}'.format(repr(self)))
        db.session.add(self)
        db.session.commit()
        app.logger.debug('Object Saved: {}'.format(repr(self)))
        
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

    
    def __repr__(self):
        return '<RecipeIngredient {} {} {}>'.format(self.qty, self.unit, self.ingredient)

    def __str__(self):
        return '<RecipeIngredient {} {} {}>'.format(self.qty, self.unit, self.ingredient)

        
class Step(db.Model, CRUDModel):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    step = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))


    def __repr__(self):
        return '<Step {} {}>'.format(self.id, self.step)

    def __str__(self):
        return self.step
        
    def update_from(self, new_obj):
        self.step = new_obj.step
        self.order = new_obj.order
        self.recipe_id = new_obj.recipe_id
        self.save()

            
class Note(db.Model, CRUDModel):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    def __repr__(self):
        return '<Note {} {}>'.format(self.id, self.note)

    def __str__(self):
        return self.note
        
    def update_from(self, new_obj):
        self.note = new_obj.note
        self.recipe_id = new_obj.recipe_id
        
        self.save()

        
class Ingredient(db.Model, CRUDModel):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    recipeingredients = db.relationship('RecipeIngredient', backref='ingredient',
                                lazy='dynamic')
    
   
    def __repr__(self):
        return '<Ingredient {} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

    def update_from(self, new_obj):
        if new_obj.name:
            self.name = new_obj.name
        if new_obj.department:
            self.department = new_obj.department
        self.save()
        
class Department(db.Model, CRUDModel):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.relationship('Ingredient', backref='department',
                                lazy='dynamic')
    
    def __repr__(self):
        return '<Department {} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name
        
    def update_from(self, new_obj):
        app.logger.debug('Updating {} from {}'.format(self, new_obj))
        self.name = new_obj.name
        self.save()
    
 

class Unit(db.Model, CRUDModel):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    recipeingredients = db.relationship('RecipeIngredient', backref='unit',
                                lazy='dynamic')    
    def __repr__(self):
        return '<Unit {} {}>'.format(self.id, self.name)


    def __str__(self):
        return self.name
        
    def update_from(self, new_obj):
        if new_obj.name:
            self.name = new_obj.name
        self.save()
          

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
        if new_obj.name:
            self.name = new_obj.name
        if new_obj.rating:
            self.rating = new_obj.rating
        if new_obj.date_added:
            self.date_added = new_obj.date_added
        self.save()
        
        
