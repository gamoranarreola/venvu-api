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


class DevelopmentConfig(BaseConfig):
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = os.environ['MONGO_PORT']
    MONGO_DB = os.environ['MONGO_DB']
    MONGO_USERNAME = os.environ['MONGO_USERNAME']
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']

class TestingConfig(BaseConfig):
    TESTING = True
    DEVELOPMENT = False


class ProductionConfig(BaseConfig):
    DEVELOPMENT = False
    PRODUCTION = True
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = os.environ['MONGO_PORT']
    MONGO_DB = os.environ['MONGO_DB']
    MONGO_USERNAME = os.environ['MONGO_USERNAME']
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
    SECRET_KEY = 'fb6103f3c29371784f9fab2257c8f090'
