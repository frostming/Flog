from flask import Flask
from flask_moment import Moment
from flask_babel import Babel
from flask_login import LoginManager
from .md import markdown
from . import cli, views, templating, models, admin


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    Moment(app)
    Babel(app)
    models.init_app(app)
    cli.init_app(app)
    views.init_app(app)
    templating.init_app(app)
    admin.init_app(app)

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def get_user(uid):
        return models.User.query.get(uid)

    @app.shell_context_processor
    def shell_context():
        return {'db': models.db, 'Post': models.Post, 'markdown': markdown}

    return app
