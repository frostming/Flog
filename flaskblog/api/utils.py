# -*- coding: utf-8 -*-
from flask import g
from ..models import User


def verify_auth(username_or_token, password=None):
    if password:
        user = User.query.filter_by(username=username_or_token).get_one_or_none()
        if not user or not user.check_password(password):
            return False
    else:
        user = User.verify_auth_token(username_or_token)
        if not user:
            return False
    g.user = user
    return True
