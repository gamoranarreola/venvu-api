import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")
    MAIL_SUPPRESS_SEND = False
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.environ.get("REDIS_URL")
    RESULT_BACKEND = os.environ.get("REDIS_URL")


class DevelopmentConfig(Config):
    DEBUG = True
    uri = os.environ.get("DATABASE_URL")

    if uri.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = uri.replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = uri


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://venvu_db_test:venvu_db_test@localhost:5432/venvu_db_test"
    )
