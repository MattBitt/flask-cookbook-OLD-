from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))
class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'flask-session-insecure-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mattscott@192.168.0.201/cookbook'

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mattscott@192.168.0.201/test_cookbook'
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mattscott@192.168.0.201/test_cookbook'
    