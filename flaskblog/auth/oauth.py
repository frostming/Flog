from authlib.integrations.flask_client import OAuth
from flask_login import current_user
from .models import OAuth2Token
from ..models import db


def fetch_token(name):
    token = OAuth2Token.query.filter_by(name=name, user=current_user).first()
    return token.to_token()


def update_token(name, token, refresh_token=None, access_token=None):
    if refresh_token:
        item = OAuth2Token.filter_by(name=name, refresh_token=refresh_token).first()
    elif access_token:
        item = OAuth2Token.filter_by(name=name, access_token=access_token).first()
    else:
        return
    if not item:
        return
    # update old token
    item.access_token = token['access_token']
    item.refresh_token = token.get('refresh_token')
    item.expires_at = token['expires_at']
    db.session.commit()


oauth = OAuth(fetch_token=fetch_token, update_token=update_token)
github = oauth.register(
    name='github',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)
google = oauth.register(
    name='google',
    access_token_url='https://www.googleapis.com/oauth2/v4/token',
    access_token_params={'grant_type': 'authorization_code'},
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth?access_type=offline',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/',
    client_kwargs={'scope': 'email profile'}
)
