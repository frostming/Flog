from flask import Blueprint, Flask
from flask.helpers import get_env
from flask_cors import CORS

api = Blueprint('api', __name__)   # type: Blueprint


def init_app(app: Flask) -> None:
    from . import views

    app.register_blueprint(api, url_prefix='/api')
    if get_env() == 'development':
        CORS(app, resources={r"/api/*": {"origins": "http://localhost:9527"}}, supports_credentials=True)
