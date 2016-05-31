from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from flask_testing import TestCase
from cookbook import db, app
from flask_fixtures import FixturesMixin

FixturesMixin.init_app(app, db)

class ModelTest(TestCase, FixturesMixin):
    

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        #app.config.from_object('config.TestingLocalDBConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class RecipeTest(ModelTest):
    fixtures = ['recipes.json',
                'steps.json',
                'ingredients.json',
                'units.json',
                'notes.json',
                'departments.json',
                'recipeingredients.json']

    def test_recipe(self):
        r = Recipe.query.get(1)
        assert r.name == 'Spaghetti and Meatballs'


    def test_create(self):
        before = len(Recipe.query.all())
        r = Recipe(name='Meatballs')
        assert r.name == 'Meatballs'
        db.session.add(r)
        db.session.commit()
        assert len(Recipe.query.all()) == before + 1

    def test_recipe_add_step(self):
        r = Recipe.query.get(1)
        before = len(r.steps.all())
        s = Step(order = 5, step = "Have a beer")
        r.steps.append(s)
        db.session.add(r)
        db.session.add(s)
        db.session.commit()
        r2 = Recipe.query.get(1)
        assert len(r2.steps.all()) == before + 1
        
    def test_recipe_remove_step(self):
        r = Recipe.query.get(1)
        before = len(r.steps.all())
        r.steps.filter_by(order = 1).delete()

        db.session.add(r)
        db.session.commit()

        r2 = Recipe.query.get(1)
        assert len(r2.steps.all()) == before - 1

    def test_recipe_add_note(self):
        r = Recipe.query.get(1)
        before = len(r.notes.all())
        n = Note(note = "Have a beer")
        r.notes.append(n)
                
        db.session.add(r)
        db.session.add(n)
        db.session.commit()

        r2 = Recipe.query.get(1)
        assert len(r2.notes.all()) == before + 1
        
    def test_recipe_remove_note(self):
        r = Recipe.query.get(1)
        before = len(r.notes.all())
        db.session.delete(r.notes.first())

        db.session.add(r)
        db.session.commit()

        r2 = Recipe.query.get(1)
        assert len(r2.notes.all()) == before - 1

    def test_recipeingredient(self):
        rec = Recipe.query.get(1)
        before = len(rec.recipeingredients.all())
        
        ri = RecipeIngredient.query.get(5)
        rec.recipeingredients.append(ri)

        db.session.add(rec)
        db.session.add(ri)
        db.session.commit()
        
        r2 = Recipe.query.get(1)
        assert len(r2.recipeingredients.all()) == before + 1
        
                
        
class StepTest(ModelTest):
    fixtures = ['steps.json']

    def test_step(self):
        s = Step.query.get(1)
        assert s.step == 'Bring water to a boil'
        assert s.order == 1

    def test_create(self):
        before = len(Step.query.all())
        s = Step(step='Boil Water', order=1)
        db.session.add(s)
        db.session.commit()
        assert len(Step.query.all()) == before + 1



class NoteTest(ModelTest):
    fixtures = ['notes.json']

    def test_note(self):
        n = Note.query.get(1)
        assert n.note == 'Eat with asparagus'

    def test_create(self):
        before = len(Note.query.all())
        n = Note(note='Make ahead')
        db.session.add(n)
        db.session.commit()
        assert len(Note.query.all()) == before + 1
        
        
class IngredientTest(ModelTest):
    fixtures = ['ingredients.json', 
                'departments.json']
    
    def test_ingredient(self):
        i = Ingredient.query.get(1)
        assert i.name == 'cauliflower'
        
        
    def test_create(self):
        before = len(Ingredient.query.all())
        i = Ingredient(name='carrots')
        
        db.session.add(i)
        db.session.commit()
        
        
class DepartmentTest(ModelTest):
    fixtures = ['departments.json']
    
    def test_department(self):
        d = Department.query.get(1)
        assert d.name == 'Produce'
        
        
    def test_create(self):
        before = len(Department.query.all())
        d = Department(name="Deli")
        
        db.session.add(d)
        db.session.commit()
        
        assert len(Department.query.all()) == before + 1
    
    def test_remove(self):
        before = len(Department.query.all())
        d = Department.query.get(1)

        db.session.delete(d)
        db.session.commit()

        assert len(Department.query.all()) == before - 1
        

class UnitTest(ModelTest):
    fixtures = ['units.json']
    
    def test_uni(self):
        d = Unit.query.get(1)
        assert d.name == 'tablespoon'
        
        
    def test_create(self):
        before = len(Unit.query.all())
        u = Unit(name="ounce")
        
        db.session.add(u)
        db.session.commit()
        
        assert len(Unit.query.all()) == before + 1
    
    def test_remove(self):
        before = len(Unit.query.all())
        u = Unit.query.get(1)

        db.session.delete(u)
        db.session.commit()

        assert len(Unit.query.all()) == before - 1       
        
class RecipeIngredientTest(ModelTest):
    fixtures = ['recipeingredients.json',
                'recipes.json',
                'ingredients.json',
                'units.json']
    
    
    def test_recipeingredient(self):
        ri = RecipeIngredient.query.get(1)
        rec = Recipe.query.get(1)
        assert ri.qty == 4
    
    def test_ingredient_name(self):
        ri = RecipeIngredient.query.get(1)
        assert ri.ingredient_name == 'cauliflower'
        
