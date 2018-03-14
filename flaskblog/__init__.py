from flask import Flask
from flask_blogtheme import BlogTheme
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_babel import Babel
from flask_login import LoginManager
from .md import md


app = Flask(__name__)
app.config.from_pyfile('config.py')
BlogTheme(app, theme_folder='themes')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
babel = Babel(app)
login_manager = LoginManager(app)


from . import cli   # noqa
from . import views  # noqa
from . import templating  # noqa
from .models import Post, Tag, Category, auto_delete_orphans, User    # noqa
from .admin import admin    # noqa
auto_delete_orphans(Tag.posts)
auto_delete_orphans(Category.posts)
admin.init_app(app)


@login_manager.user_loader
def get_user(uid):
    return User.query.get(uid)


@app.shell_context_processor
def shell_context():
    return {'db': db, 'Post': Post, 'md': md}
