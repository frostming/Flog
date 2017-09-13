"""Flask blog app config"""
import os.path as op
import os

here = op.dirname(__file__)


BLOG_THEME_NAME = 'footstrap'
BLOG_THEME_PROCESSOR = 'site'
SECRET_KEY = 'flask blog'

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                    'sqlite:///' + op.join(here, 'db.sqlite3'))

SQLALCHEMY_TRACK_MODIFICATIONS = False

BLOG_PER_PAGE = 10
