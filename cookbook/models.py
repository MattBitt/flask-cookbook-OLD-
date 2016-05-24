from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    steps = db.relationship('Step', backref='recipe',
                                lazy='dynamic')
    notes = db.relationship('Note', backref='recipe',
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
    department = db.Column(db.String)
    # recipe link goes here

    def __repr__(self):
        return '<Ingredient {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Department {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

class RecipeIngredient(db.Model):
    __tablename__ = 'recipeingredients'

    id = db.Column(db.Integer, primary_key=True)
    #recipe.id
    #ingredient.id
    qty = db.Column(db.Numeric)
    #unit.id
    preparation = db.Column(db.String)

    def __repr__(self):
        return '<Department {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name

class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Unit {:d} {}>'.format(self.id, self.name)

    def __str__(self):
        return self.name