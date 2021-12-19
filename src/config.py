import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class BaseConfig:
    TESTING = False
    DEVELOPMENT = True
    PRODUCTION = False
    SECRET_KEY = 'ddf3eead1244664fe42d0ae458364095'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class TestingConfig(BaseConfig):
    TESTING = True
    DEVELOPMENT = False


class ProductionConfig(BaseConfig):
    DEVELOPMENT = False
    PRODUCTION = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = 'fb6103f3c29371784f9fab2257c8f090'
