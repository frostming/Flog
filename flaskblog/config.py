"""Flask blog app config"""
import os.path as op
import os

here = op.dirname(__file__)


BLOG_THEME_NAME = 'footstrap'
BLOG_THEME_PROCESSOR = 'site'
SECRET_KEY = 'flask blog'

# aws environment
if 'RDS_HOSTNAME' in os.environ:
    db_name = os.environ['RDS_DB_NAME']
    db_user = os.environ['RDS_USERNAME']
    db_password = os.environ['RDS_PASSWORD']
    db_host = os.environ['RDS_HOSTNAME']
    db_port = os.environ['RDS_PORT']
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                               .format(db_user, db_password, db_host, db_port,
                                       db_name))
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + op.join(here, 'db.sqlite3')

SQLALCHEMY_TRACK_MODIFICATIONS = False

BLOG_PER_PAGE = 10
