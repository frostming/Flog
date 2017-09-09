from flask import Flask
from flask_blogtheme import BlogTheme
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import os
import os.path as op
from .md import md
import io
import re
import yaml


app = Flask(__name__)
app.config.from_pyfile('config.py')
BlogTheme(app, theme_folder='themes')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
blog_folder = os.path.join(app.root_path, '_posts')


from . import cli   # noqa
from . import views  # noqa
from . import templating  # noqa
from .models import Post    # noqa
from .admin import admin    # noqa
admin.init_app(app)


@app.shell_context_processor
def shell_context():
    return {'db': db, 'Post': Post, 'md': md}
