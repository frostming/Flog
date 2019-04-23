import os
from flask import Blueprint, send_from_directory

from . import STATIC_PATH


admin = Blueprint(
    'admin',
    __name__,
    static_folder=os.path.join(STATIC_PATH, 'dist', 'static'),
)


@admin.route('/')
def index():
    return send_from_directory(os.path.join(STATIC_PATH, 'dist'), 'index.html')


def init_app(app):
    app.register_blueprint(admin, url_prefix="/admin")
