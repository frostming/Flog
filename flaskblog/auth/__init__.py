
from .views import bp
from .oauth import oauth


def init_app(app):
    from . import models    # noqa

    oauth.init_app(app)
    app.register_blueprint(bp, url_prefix='/auth')
