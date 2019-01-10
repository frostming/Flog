from typing import Union

from flask import Flask, g, request
from flask.helpers import get_env
from flask_assets import Environment
from flask_babel import Babel, lazy_gettext
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment

from . import admin, cli, config, models, templating, views
from .md import markdown


def create_app(env: Union[str, None] = None) -> Flask:
    env = env or get_env()
    app = Flask(__name__)  # type: Flask
    app.config.from_object(config.config_dict[env])
    Moment(app)
    Bootstrap(app)
    babel = Babel(app)
    models.init_app(app)
    cli.init_app(app)
    views.init_app(app)
    templating.init_app(app)
    admin.init_app(app)
    Environment(app)

    @babel.localeselector
    def get_locale():
        if 'site' in g:
            return g.site['locale']
        return request.accept_languages.best_match(['zh', 'en'])

    login_manager = LoginManager(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = lazy_gettext('Please login')
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def get_user(uid):
        return models.User.query.get(uid)

    @app.shell_context_processor
    def shell_context():
        return {'db': models.db, 'Post': models.Post, 'markdown': markdown}

    return app
