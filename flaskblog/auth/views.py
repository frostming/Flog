from flask import Blueprint, abort, current_app, jsonify, redirect, request, session, url_for
from flask_login import login_user

from ..models import User, db
from .models import OAuth2Token
from .oauth import github, google

bp = Blueprint('auth', __name__)   # type: Blueprint


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


@bp.route('/github/login')
def github_login():
    origin_url = request.headers['Referer']
    session['oauth_origin'] = origin_url
    redirect_uri = url_for('.github_auth', _external=True)
    if not current_app.debug:
        redirect_uri = redirect_uri.replace('http://', 'https://')
    return github.authorize_redirect(redirect_uri)


@bp.route('/github/auth')
def github_auth():
    token = github.authorize_access_token()
    resp = github.get('user')
    resp.raise_for_status()
    profile = resp.json()
    if profile.get("email") is None:
        resp = github.get("user/emails")
        resp.raise_for_status()
        data = resp.json()
        profile["email"] = next(email["email"] for email in data if email["primary"])
    user = User.query.filter_by(email=profile['email']).first()
    if user:
        user.name = profile['name']
        user.link = profile['html_url']
        user.picture = profile['avatar_url']
    else:
        user = User(
            username=profile['login'],
            name=profile['name'],
            email=profile['email'],
            link=profile['html_url'],
            picture=profile['avatar_url'],
            type='github'
        )
        db.session.add(user)

    oauth_token = OAuth2Token.query.filter_by(user=user, name='github').first()
    if oauth_token:
        oauth_token.access_token = token['access_token']
        oauth_token.token_type = token['token_type']
    else:
        oauth_token = OAuth2Token(
            user=user,
            name='github',
            access_token=token['access_token'],
            token_type=token['token_type']
        )
        db.session.add(oauth_token)
        db.session.commit()
    login_user(user)
    next_url = session.pop('oauth_origin', None)
    return redirect(next_url or url_for('home'))


@bp.route('/google/login')
def google_login():
    origin_url = request.headers['Referer']
    session['oauth_origin'] = origin_url
    redirect_uri = url_for('.google_auth', _external=True)
    if not current_app.debug:
        redirect_uri = redirect_uri.replace('http://', 'https://')
    return google.authorize_redirect(redirect_uri)


@bp.route('/google/auth')
def google_auth():
    token = google.authorize_access_token()
    resp = google.get('oauth2/v3/userinfo')
    resp.raise_for_status()
    profile = resp.json()
    user = User.query.filter_by(email=profile['email']).first()
    if user:
        user.name = profile['name']
        user.picture = profile['picture']
    else:
        user = User(
            username=profile['login'],
            name=profile['name'],
            email=profile['email'],
            picture=profile['picture'],
            type='google'
        )
        db.session.add(user)

    oauth_token = OAuth2Token.query.filter_by(user=user, name='google').first()
    if oauth_token:
        oauth_token.access_token = token['access_token']
        oauth_token.token_type = token['token_type']
        oauth_token.expires_at = token['expires_at']
    else:
        oauth_token = OAuth2Token(
            user=user,
            name='google',
            access_token=token['access_token'],
            token_type=token['token_type'],
            expires_at=token['expires_at']
        )
        db.session.add(oauth_token)
        db.session.commit()
    login_user(user)
    next_url = session.pop('oauth_origin', None)
    return redirect(next_url or url_for('home'))
