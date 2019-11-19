# -*- coding: utf-8 -*-
from flask_login import login_user, current_user
from ..models import User


def verify_auth(username_or_token, password=None):
    if password:
        user = User.query.filter_by(username=username_or_token, is_admin=True).first()
        if not user or not user.check_password(password):
            return False
    else:
        user = User.verify_auth_token(username_or_token)
        if not user or not user.is_admin:
            return False
    if not current_user or current_user.get_id() != user.get_id():
        login_user(user)
    return True
