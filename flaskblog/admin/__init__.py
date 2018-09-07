from flask import Blueprint

bp = Blueprint('admin', __name__)


def init_app(app):
    from . import views
    views.init_blueprint(bp)
    app.register_blueprint(bp, url_prefix='/admin')
