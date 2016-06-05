from cookbook.models import Recipe, Step, Note, Ingredient, Department, Unit, RecipeIngredient
from cookbook.schemas import DepartmentSchema, IngredientSchema, UnitSchema, StepSchema
from cookbook.schemas import NoteSchema, RecipeSchema
from flask_testing import TestCase
from cookbook import app
from flask_fixtures import FixturesMixin
from flask_sqlalchemy import SQLAlchemy
import json
import pprint
import unittest 
import csv
import requests

#FixturesMixin.init_app(app, db)


class TestClient(object):
    def post(self, url, json_data):
        url = 'http://127.0.0.1:5000' + url
        json_data = json.loads(json_data)
        return requests.post(url, json=json_data)
        #return app.test_client().post(url, data=json_data,
        #               content_type = 'application/json')

    def put(self, url, json_data):
        url = 'http://127.0.0.1:5000' + url
        json_data = json.loads(json_data)
        return requests.put(url, json=json_data)
        #return app.test_client().put(url, data=json_data,
        #               content_type = 'application/json')
    
    def delete(self, url):
        url = 'http://127.0.0.1:5000' + url
        return requests.delete(url)
        #return app.test_client().delete(url)
    
    def get(self, url):
        url = 'http://127.0.0.1:5000' + url
        return requests.get(url)
        #return app.test_client().get(url)

db = SQLAlchemy()

class DepartmentsViewTest(TestCase):
    fixtures = ['recipes.json',
                'steps.json',
                'notes.json',
                'units.json',
                'ingredients.json',
                'departments.json',
                'recipeingredients.json']
    
   
    def create_app(self):
        app.logger.debug('Create_app method')
        app.config.from_object('config.TestingConfig')
        db.init_app(app)
        return app
        
    @classmethod
    def setUpClass(cls):
        app.logger.debug('SetUp Class Method')
        db.create_all(app=app)


    @classmethod
    def tearDownClass(cls):
        app.logger.debug('TearDown Class Method')
        db.drop_all(app=app)

    def setUp(self):
        app.logger.debug('SetUp Method')
        db.session.rollback()
        self.trans = db.session.begin(subtransactions=True)
        

    def tearDown(self):
        app.logger.debug('TearDown Method')
        self.trans.rollback()
        db.session.begin(subtransactions=True)

    
    def test_get_item(self):
        app.logger.debug('In test_get_item')
        dep = Department(name='Bakery')
        self.trans.session.add(dep)
        
        
        new_dep = Department.query.all()
        app.logger.debug('Created dep:  {}'.format(dep))
        app.logger.debug('Queried dep: {}'.format(new_dep))
        assert len(new_dep) == 1
        assert new_dep[0].name == 'Bakery'
        
    
    @unittest.skip('skipping')
    def test_get_one(self):
        
        app.logger.debug('Starting test_get_one Departments')
        app.logger.debug('Using DB:  {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
        result = TestClient().get('/departments/1')
        app.logger.debug('GET result:  {}'.format(result.content))
        assert result.status_code == 200
        data, errors = DepartmentSchema().loads(result.content)
        assert errors == {}
        assert isinstance(data, Department) == True
        assert data.name == 'Produce'
        assert data.id == 1
    
    @unittest.skip('skipping')  
    def test_get_not_existing(self):
        url_endpoint = self.url_base + str(self.test_data['bad_id'])
        result = TestClient().get('/departments/15')
        assert result.status_code == 404
        assert isinstance(result.data, str) 
    @unittest.skip('skipping')     
    def test_get_all(self):
        url_endpoint = self.url_base
        result = TestClient().get(url_endpoint)
        assert result.status_code == 200
        data, errors = self.schema(many=True).loads(result.content)
        assert len(data) == self.test_data['total_num']
        assert data[0].name == self.test_data['name']
    @unittest.skip('skipping')
    def test_create_item(self):
        new_item_string = r"""{"name" : "hba"}"""
        
        app.logger.debug('Starting create_item test for {}'.format(repr(self)))
        app.logger.debug('Existing Departments:  {}')
        url_endpoint = self.url_base
        result = TestClient().post(url_endpoint, self.new_item_string)
        assert result.status_code == 200
        app.logger.debug('Post result = {}'.format(result.content))
        result = TestClient().get(url_endpoint)
        assert result.status_code == 200
        assert self.test_data['new_item'] in result.contents
        
    @unittest.skip('skipping')     
    def test_delete_item(self):
        url_endpoint = self.url_base + str(self.test_data['id'])
        result = TestClient().delete(url_endpoint)
        assert result.status_code == 200
        result = TestClient().get(url_endpoint)
        assert result.status_code == 404
    @unittest.skip('skipping')  
    def test_update_item(self):
        update_item_string = r"""{"name" : "floral"}"""
        url_endpoint = self.url_base + str(self.test_data['id'])
        result = TestClient().put(url_endpoint, self.update_item_string)
        assert self.component.query.get(1).name == self.test_data['updated_item']