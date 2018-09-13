from flask import Flask, g, request
from flask_moment import Moment
from flask_babel import Babel
from flask_login import LoginManager
from flask_babel import lazy_gettext
from flask_bootstrap import Bootstrap
from flask_static_compress import FlaskStaticCompress
from .md import markdown
from . import cli, views, templating, models, admin


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    Moment(app)
    Bootstrap(app)
    FlaskStaticCompress(app)
    babel = Babel(app)
    models.init_app(app)
    cli.init_app(app)
    views.init_app(app)
    templating.init_app(app)
    admin.init_app(app)

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
