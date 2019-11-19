from flask import Blueprint

bp = Blueprint('auth', __name__)   # type: Blueprint


def init_app(app):
    from . import views

    app.register_blueprint(bp, url_prefix='/auth')
