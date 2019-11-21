"""Flask blog app config"""
import os
import os.path as op

here = op.dirname(__file__)


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "flask blog")
    DEFAULT_ADMIN_PASSWORD = "admin"
    BLOG_PER_PAGE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WHOOSHEE_MIN_STRING_LEN = 2
    ADMIN_EMAIL = 'mianghong@gmail.com'
    MAIL_DEFAULT_SENDER = os.getenv('FLASK_MAIL_SENDER')
    MAIL_SERVER = os.getenv('FLASK_MAIL_SERVER', 'localhost')
    MAIL_USERNAME = os.getenv('FLASK_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('FLASK_MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + op.join(here, "db.sqlite3")
    )


class ProductionConfig(BaseConfig):

    if "DATABASE_URL" in os.environ:  # Heroku environment
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + op.join(here, "db.sqlite3")

    SERVER_NAME = "frostming.com"


class DevelopConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    TESTING = True


config_dict = {
    "production": ProductionConfig,
    "development": DevelopConfig,
    "testing": TestingConfig,
}
