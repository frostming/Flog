# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from datetime import datetime

from flask import abort, g, json, jsonify, request
from flask.views import MethodView
from flask_login import current_user, logout_user
from urllib.parse import urlparse

from ..models import (Category, Comment, Integration, Page, Post, Tag, db,
                      generate_password_hash, User)
from ..templating import get_integrations
from . import api
from .utils import verify_auth

TOKEN_HEADER = "X-Token"
SUCCESS_RESPONSE = {"code": 20000, "data": "success"}


@api.before_request
def authenticate_view():
    if request.method == "OPTIONS":
        return
    if request.path == "/api/user/login":
        return
    token = request.headers.get(TOKEN_HEADER)
    return
    if not token or not verify_auth(token):
        return jsonify({"code": 50008, "data": {"error": "Invalid token"}})


@api.route("/user/login", methods=["POST"])
def login():
    data = request.get_json()
    if not verify_auth(data.get("username"), data.get("password")):
        return jsonify(
            {"code": 60204, "message": "Account and password are incorrect."}
        )
    return jsonify(
        {"code": 20000, "data": {"token": current_user.generate_token().decode()}}
    )


@api.route("/user/info")
def get_info():
    return jsonify(
        {
            "code": 20000,
            "data": {
                "roles": ["admin"],
                "introduction": "I am a super administrator",
                "avatar": g.site["avatar"],
                "name": "Site Admin",
            },
        }
    )


@api.route("/user/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify(SUCCESS_RESPONSE)


@api.route("/user/password", methods=["POST"])
def change_password():
    data = request.get_json()
    if not current_user.check_password(data["old"]):
        abort(401)
    if data["new"] != data["confirm"]:
        return (
            jsonify({"code": 51123, "message": "New and confirm are not the same!"}),
            400,
        )
    current_user.password = generate_password_hash(data["new"])
    db.session.add(current_user)
    db.session.commit()
    return jsonify(SUCCESS_RESPONSE)


@api.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "GET":
        return jsonify({"code": 20000, "data": g.site})
    else:
        g.site.update(request.get_json())
        current_user.write_settings(g.site)
        return jsonify(SUCCESS_RESPONSE)


@api.route("/settings/theme", methods=["GET", "POST"])
def theme():
    if request.method == "POST":
        g.site["primary_color"] = request.get_json().get("value")
        current_user.write_settings(g.site)
        return jsonify(SUCCESS_RESPONSE)
    else:
        return jsonify(
            {"code": 20000, "data": {"value": g.site.get("primary_color", "#000000")}}
        )


@api.route("/settings/language", methods=["GET", "POST"])
def language():
    if request.method == "POST":
        locale_in_request = request.get_json().get("value")
        g.site["locale"] = (
            "zh_Hans_CN" if locale_in_request == "zh" else locale_in_request
        )
        current_user.write_settings(g.site)
        return jsonify(SUCCESS_RESPONSE)
    else:
        locale_in_g = g.site.get("locale")
        return jsonify(
            {
                "code": 20000,
                "data": {
                    "value": "zh" if str(locale_in_g).startswith("zh") else locale_in_g
                },
            }
        )


@api.route("/categories")
def categories():
    result = Category.query.all()
    return jsonify(
        {
            "code": 20000,
            "data": {
                "total": len(result),
                "items": [{"id": cat.id, "name": cat.text} for cat in result],
            },
        }
    )


@api.route("/tags")
def tags():
    name = request.args.get("name")
    result = Tag.query.filter(Tag.text.ilike(f"%{name}%")).all()
    return jsonify(
        {
            "code": 20000,
            "data": {
                "total": len(result),
                "items": [{"id": tag.id, "name": tag.text} for tag in result],
            },
        }
    )


@api.route("/token/cos")
def cos_token():
    from sts.sts import Sts

    cos = get_integrations().get("integration", {}).get("cos")
    if not cos:
        abort(401)
    print(cos)

    config = {
        "duration_seconds": 1800,
        "secret_id": cos["secret_id"],
        "secret_key": cos["secret_key"],
        "bucket": cos["bucket"],
        "region": cos["region"],
        "allow_prefix": "*",
        "allow_actions": [
            "name/cos:PutObject",
            "name/cos:PostObject",
            "name/cos:InitiateMultipartUpload",
            "name/cos:ListMultipartUploads",
            "name/cos:ListParts",
            "name/cos:UploadPart",
            "name/cos:CompleteMultipartUpload",
        ],
    }

    sts = Sts(config)
    response = sts.get_credential()
    return jsonify({"code": 20000, "data": response})


class PostView(MethodView):
    def get(self):
        is_draft = request.args.get("type", "published") == "draft"
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
        items = (
            Post.query.filter_by(is_draft=is_draft)
            .order_by(Post.date.desc())
            .paginate(page=page, per_page=limit)
            .items
        )
        return jsonify(
            {
                "code": 20000,
                "data": {
                    "total": Post.query.filter_by(is_draft=is_draft).count(),
                    "items": [post.to_dict(True) for post in items],
                },
            }
        )

    def post(self):
        post_data = request.get_json()
        post = Post(**post_data)
        db.session.add(post)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


class PostItemView(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)
        return jsonify({"code": 20000, "data": post.to_dict(True)})

    def put(self, id):
        post = Post.query.get_or_404(id)
        data = request.get_json()
        for k, v in data.items():
            if k in ("date", "last_modified"):
                continue
            if k == "tags" and v:
                v = [Tag.get_one_or_new(o) for o in v]
            elif k == "category" and v:
                v = Category.get_one_or_new(v)
            setattr(post, k, v)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)

    def delete(self, id):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


class PageView(MethodView):
    def get(self):
        items = Page.query
        return jsonify(
            {
                "code": 20000,
                "data": {
                    "total": items.count(),
                    "items": [post.to_dict() for post in items],
                },
            }
        )

    def post(self):
        post_data = request.get_json()
        page = Page(**post_data)
        db.session.add(page)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


class PageItemView(MethodView):
    def get(self, id):
        page = Page.query.get_or_404(id)
        return jsonify({"code": 20000, "data": page.to_dict()})

    def put(self, id):
        data = request.get_json()
        data.pop("id", None)
        page = Page.query.get_or_404(id)
        for k, v in data.items():
            setattr(page, k, v)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)

    def delete(self, id):
        page = Page.query.get_or_404(id)
        db.session.delete(page)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


class IntegrationView(MethodView):
    def get(self):
        return jsonify({"code": 20000, "data": get_integrations()["integration"]})

    def post(self):
        data = request.get_json()
        tool = Integration.query.filter_by(name=data["name"]).first()
        if not tool:
            tool = Integration(name=data.pop("name"))
            db.session.add(tool)
        tool.enabled = data.pop("enabled", False)
        tool.settings = json.dumps(data)
        db.session.commit()
        return jsonify(SUCCESS_RESPONSE)


def comment_list():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    queryset = Comment.query.order_by(Comment.create_at.desc())
    return jsonify(
        {
            "code": 20000,
            "data": {
                "total": queryset.count(),
                "items": [
                    comment.to_dict()
                    for comment in queryset.paginate(page=page, per_page=limit).items
                ],
            },
        }
    )


def delete_comment(id):
    Comment.query.filter_by(id=id).delete()
    db.session.commit()


def import_disqus_comment():
    xml = ET.parse(request.files["file"])
    ns = {
        "base": "http://disqus.com",
        "dsq": "http://disqus.com/disqus-internals",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }
    threads = {}
    for th in xml.findall('base:thread', ns):
        id_ = th.attrib['{http://disqus.com/disqus-internals}id']
        link = th.find('base:link', ns).text
        threads[id_] = link
    comments = {}
    for comment in xml.findall('base:post', ns):
        is_delete = comment.find('base:isDeleted', ns).text
        is_spam = comment.find('base:isSpam', ns).text
        if is_delete == 'true' or is_spam == 'true':
            continue
        id_ = comment.attrib['{http://disqus.com/disqus-internals}id']
        message = comment.find('base:message', ns).text
        create_at = datetime.strptime(comment.find('base:createdAt', ns).text, '%Y-%m-%dT%H:%M:%SZ')
        thread = threads[comment.find('base:thread', ns).attrib['{http://disqus.com/disqus-internals}id']]
        post = Post.query.filter_by(url=urlparse(thread).path).first()
        if not post:
            continue
        parent = comment.find('base:parent', ns)
        if parent:
            parent = comments.get(parent.attrib['{http://disqus.com/disqus-internals}id'])
        author_name = comment.find('base:author/base:name', ns).text
        author_username = getattr(comment.find('base:author/base:username', ns), 'text', None)
        if author_name == 'Frost Ming':
            author_username = 'admin'
        author = User.query.filter_by(username=author_username).first()
        if not author:
            author = User(username=author_username, name=author_name)
            db.session.add(author)
            db.session.commit()
        instance = Comment(
            author=author,
            post=post,
            parent=parent,
            message=message,
            create_at=create_at
        )
        db.session.add(instance)
        comments[id_] = instance
    db.session.commit()
    return jsonify(SUCCESS_RESPONSE)


api.add_url_rule("/post", view_func=PostView.as_view("post"))
api.add_url_rule("/post/<int:id>", view_func=PostItemView.as_view("post_item"))
api.add_url_rule("/page", view_func=PageView.as_view("page"))
api.add_url_rule("/page/<int:id>", view_func=PageItemView.as_view("page_item"))
api.add_url_rule("/integration", view_func=IntegrationView.as_view("integration"))
api.add_url_rule("/comment/import", view_func=import_disqus_comment, methods=["POST"])
api.add_url_rule(
    "/comment/<int:id>", "delete_comment", view_func=delete_comment, methods=["DELETE"]
)
api.add_url_rule("/comment", "comment_list", view_func=comment_list)
