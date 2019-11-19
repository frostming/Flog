from flask import abort, request, jsonify
from flask_login import login_user

from . import bp
from ..models import User, db


@bp.route('/login', methods=['POST'])
def login():
    form = request.form
    user = User.query.filter_by(**form).first()
    if not user:
        user = User(**form)
        db.session.add(user)
        db.session.commit()
    elif user.is_admin:
        abort(403)
    login_user(user)
    return jsonify({'message': 'success', 'username': user.username})
