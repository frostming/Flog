from flask import Blueprint, Flask

bp = Blueprint('admin', __name__)   # type: Blueprint


def init_app(app: Flask) -> None:
    from . import views
    views.init_blueprint(bp)
    app.register_blueprint(bp, url_prefix='/admin')
