# -*- coding: utf-8 -*-
from . import api
from .utils import verify_auth
from flask import request, jsonify, g, abort, json
from flask.views import MethodView
from ..models import Post, Category, Tag, db, generate_password_hash, Integration
from ..templating import get_integrations

TOKEN_HEADER = 'X-Token'
SUCCESS_RESPONSE = {'code': 20000, 'data': 'success'}


@api.before_request
def authenticate_view():
    if request.method == 'OPTIONS':
        return
    if request.path == "/api/user/login":
        return
    token = request.headers.get(TOKEN_HEADER)
    if not token or not verify_auth(token):
        return jsonify({
            'code': 50008,
            'data': {'error': 'Invalid token'}
        })


@api.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    if not verify_auth(data.get('username'), data.get('password')):
        return jsonify({
            'code': 60204,
            'message': 'Account and password are incorrect.'
        })
    return jsonify({
        'code': 20000,
        'data': {'token': g.user.generate_token().decode()}
    })


@api.route('/user/info')
def get_info():
    return jsonify({
        'code': 20000,
        'data': {
            'roles': ['admin'],
            'introduction': 'I am a super administrator',
            'avatar': g.site['avatar'],
            'name': 'Site Admin'
        }
    })


@api.route('/user/logout', methods=['POST'])
def logout():
    g.user = None
    return jsonify(SUCCESS_RESPONSE)


@api.route('/user/password', methods=['POST'])
def change_password():
    data = request.get_json()
    if not g.user.check_password(data['old']):
        abort(401)
    if data['new'] != data['confirm']:
        return jsonify({'code': 51123, 'message': 'New and confirm are not the same!'}), 400
    g.user.password = generate_password_hash(data['new'])
    db.session.add(g.user)
    db.session.commit()
    return jsonify(SUCCESS_RESPONSE)


@api.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return jsonify({
            'code': 20000,
            'data': g.site
        })
    else:
        g.site.update(request.get_json())
        g.user.write_settings(g.site)
        return jsonify(SUCCESS_RESPONSE)


@api.route('/settings/theme', methods=['GET', 'POST'])
def theme():
    if request.method == "POST":
        g.site['primary_color'] = request.get_json().get('value')
        g.user.write_settings(g.site)
        return jsonify(SUCCESS_RESPONSE)
    else:
        return jsonify({
            'code': 20000,
            'data': {'value': g.site.get('primary_color', '#000000')}
        })


@api.route('/settings/language', methods=['GET', 'POST'])
def language():
    if request.method == "POST":
        locale_in_request = request.get_json().get('value')
        g.site['locale'] = 'zh_Hans_CN' if locale_in_request == 'zh' else locale_in_request
        g.user.write_settings(g.site)
        return jsonify(SUCCESS_RESPONSE)
    else:
        locale_in_g = g.site.get('locale')
        return jsonify({
            'code': 20000,
            'data': {'value': 'zh' if str(locale_in_g).startswith('zh') else locale_in_g}
        })


@api.route('/categories')
def categories():
    result = Category.query.all()
    return jsonify({
        'code': 20000,
        'data': {
            'total': len(result),
            'items': [{'id': cat.id, 'name': cat.text} for cat in result]
        }
    })


@api.route('/tags')
def tags():
    name = request.args.get('name')
    result = Tag.query.filter(Tag.text.ilike(f'%{name}%')).all()
    return jsonify({
        'code': 20000,
        'data': {
            'total': len(result),
            'items': [{'id': tag.id, 'name': tag.text} for tag in result]
        }
    })


@api.route('/token/cos')
def cos_token():
    from sts.sts import Sts

    cos = get_integrations().get('integration', {}).get('cos')
    if not cos:
        abort(401)
    print(cos)

    config = {
        'duration_seconds': 1800,
        'secret_id': cos['secret_id'],
        'secret_key': cos['secret_key'],
        'bucket': cos['bucket'],
        'region': cos['region'],
        'allow_prefix': '*',
        'allow_actions': [
            'name/cos:PutObject',
            'name/cos:PostObject',
            'name/cos:InitiateMultipartUpload',
            "name/cos:ListMultipartUploads",
            "name/cos:ListParts",
            "name/cos:UploadPart",
            "name/cos:CompleteMultipartUpload"
        ]
    }

    sts = Sts(config)
    response = sts.get_credential()
    return jsonify({
        'code': 20000,
        'data': response
    })


class PostView(MethodView):
    def get(self):
        is_draft = request.args.get('type', 'published') == 'draft'
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        items = Post.query.filter_by(is_draft=is_draft).order_by(Post.date.desc()).paginate(page=page, per_page=limit).items
        return jsonify({
            'code': 20000,
            'data': {
                'total': Post.query.filter_by(is_draft=is_draft).count(),
                'items': [post.to_dict(True) for post in items]
            }
        })

    def post(self):
        post_data = request.get_json()
        post = Post(**post_data)
        db.session.add(post)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


class PostItemView(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)
        return jsonify({
            'code': 20000,
            'data': post.to_dict(True)
        })

    def put(self, id):
        post = Post.query.get_or_404(id)
        data = request.get_json()
        for k, v in data.items():
            if k in ('date', 'last_modified'):
                continue
            if k == 'tags' and v:
                v = [Tag.get_one_or_new(o) for o in v]
            elif k == 'category' and v:
                v = Category.get_one_or_new(v)
            elif k == 'lang' and k.startswith('zh'):
                v = 'zh_Hans_CN'
            setattr(post, k, v)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)

    def delete(self, id):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


class IntegrationView(MethodView):
    def get(self):
        return jsonify({
            'code': 20000,
            'data': get_integrations()['integration']
        })

    def post(self):
        data = request.get_json()
        tool = Integration.query.filter_by(name=data['name']).first()
        if not tool:
            tool = Integration(name=data.pop('name'))
            db.session.add(tool)
        tool.enabled = data.pop('enabled', False)
        tool.settings = json.dumps(data)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


api.add_url_rule('/post', view_func=PostView.as_view('post'))
api.add_url_rule('/post/<int:id>', view_func=PostItemView.as_view('post_item'))
api.add_url_rule('/integration', view_func=IntegrationView.as_view('integration'))
