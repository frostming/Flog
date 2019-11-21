
from .views import bp


def init_app(app):
    # from . import models    # noqa

    app.register_blueprint(bp, url_prefix='/auth')
