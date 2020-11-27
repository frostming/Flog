# -*- coding: utf-8 -*-
import hashlib
import io
import re
from datetime import datetime
from random import choice
from typing import Type, Union

import sqlalchemy as sa
import yaml
from flask import Flask, current_app, json, url_for
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from slugify import slugify
from werkzeug.security import check_password_hash, generate_password_hash

from .md import markdown, strict_markdown
from .utils import strip_tags

db: SQLAlchemy = SQLAlchemy()
whooshee: Whooshee = Whooshee()

tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
)  # type: sa.Table

DEFAULT_SETTINGS = {
    "locale": "en",
    "name": "Flog",
    "cover_url": "/static/images/cover.jpg",
    "avatar": "/static/images/avatar.jpeg",
    "description": "A simple blog powered by Flask",
}


def auto_delete_orphans(cls: sa.Column, attr: str) -> None:
    @sa.event.listens_for(sa.orm.Session, "after_flush")
    def delete_orphan_listener(session, ctx):
        session.query(cls).filter(~getattr(cls, attr).any()).delete(
            synchronize_session=False
        )


@whooshee.register_model("title", "description", "content")
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    image = db.Column(db.String(400))
    image_caption = db.Column(db.String(400))
    lang = db.Column(db.String(20))
    content = db.Column(db.Text)
    html = db.Column(db.Text)
    toc = db.Column(db.Text)
    url = db.Column(db.String(80))
    comment = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(400))
    author = db.Column(db.String(50))
    tags = db.relationship("Tag", secondary=tags, backref="posts")
    slug = db.Column(db.String(100))
    is_draft = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    comments = db.relationship(
        "Comment", cascade="all, delete-orphan", backref="post", lazy="dynamic"
    )

    def __init__(self, **kwargs):
        if isinstance(kwargs.get("category"), str):
            kwargs["category"] = Category.get_one_or_new(kwargs["category"])
        tags = kwargs.get("tags")
        if tags and isinstance(tags[0], str):
            kwargs["tags"] = [Tag.get_one_or_new(tag) for tag in tags]
        kwargs.pop("date", None)
        kwargs.pop("last_modified", None)
        super().__init__(**kwargs)

    def to_dict(self, ensure_text=False) -> dict:
        return dict(
            id=self.id,
            title=self.title,
            date=self.date,
            image=self.image,
            image_caption=self.image_caption,
            category=self.category if not ensure_text else str(self.category),
            lang=self.lang,
            comment=self.comment,
            description=self.description,
            author=self.author,
            tags=self.tags if not ensure_text else [str(tag) for tag in self.tags],
            slug=self.slug,
            content=self.content,
            last_modified=self.last_modified,
            is_draft=self.is_draft,
        )

    def __repr__(self) -> str:
        return "<Post: %s>" % self.title

    @property
    def previous(self) -> "Post":
        return Post.query.order_by(Post.id.desc()).filter(
            Post.is_draft == False, Post.id < self.id   # noqa
        ).first()

    @property
    def next(self) -> "Post":
        return Post.query.order_by(Post.id.asc()).filter(
            Post.is_draft == False, Post.id > self.id   # noqa
        ).first()

    @property
    def excerpt(self) -> str:
        """The excerpt of the post, detect <!--more--> tag as delimiter, or the first
        200 characters.
        """
        match = re.match(r"^(.+?)<!--more-->", self.content, flags=re.DOTALL)
        if match:
            content = match.group(1)
            return markdown(content)
        else:
            content = self.content
            return strip_tags(markdown(content))[:200]

    def related_post(self) -> Union["Post", None]:
        posts = Post.query.join(Post.tags).filter(
            Tag.id.in_([tag.id for tag in self.tags]),
            Post.id != self.id,
            ~Post.is_draft,
        )
        if posts.count() > 0:
            return choice(posts.all())
        return None

    def dump_md(self) -> str:
        meta = {
            "title": self.title,
            "template": "post",
            "date": self.date,
            "description": self.description,
            "image": self.image,
            "tags": [tag.text for tag in self.tags],
            "category": self.category.text,
        }
        meta_buffer = io.StringIO()
        yaml.safe_dump(meta, meta_buffer, allow_unicode=True)
        return "---\n{}---\n\n{}".format(meta_buffer.getvalue(), self.content)


@sa.event.listens_for(Post, "before_insert")
@sa.event.listens_for(Post, "before_update")
def render_markdown(
    mapper: Type[sa.orm.Mapper], connection: sa.engine.Connection, target: sa.orm.Mapper
) -> None:
    if not target.slug:
        target.slug = slugify(target.title)
    if not target.date:
        target.date = datetime.utcnow()
    target.html = markdown(target.content)
    target.toc = markdown.renderer.render_toc()
    target.url = "/{}/{}".format(target.date.strftime("%Y/%m-%d"), target.slug)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    settings = db.Column(db.Text())
    is_admin = db.Column(db.Boolean(), default=False)
    link = db.Column(db.String(128))
    picture = db.Column(db.String(512))
    type = db.Column(db.String(16))
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("username", "email", name="_username_email"),)

    def __init__(self, **kwargs) -> None:
        password = kwargs.pop("password", None)
        if password:
            password = generate_password_hash(password)
            kwargs["password"] = password
        if not kwargs.get('username') and kwargs.get('name'):
            kwargs['username'] = slugify(kwargs['name'])
        super(User, self).__init__(**kwargs)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def display_name(self):
        return self.name or self.username

    @classmethod
    def get_admin(cls) -> "User":
        """Get the admin user. The only one will be returned."""
        rv: Union[None, User] = cls.query.filter_by(is_admin=True).first()
        if not rv:
            rv = cls(
                username="admin",
                email=current_app.config["ADMIN_EMAIL"],
                password=current_app.config["DEFAULT_ADMIN_PASSWORD"],
                is_admin=True,
            )
            db.session.add(rv)
            db.session.commit()
        return rv

    @property
    def avatar(self) -> str:
        """Get the gravatar image"""
        if self.picture:
            return self.picture
        email_hash = hashlib.md5(
            (self.email or self.username).strip().lower().encode()
        ).hexdigest()
        return f'https://www.gravatar.com/avatar/{email_hash}?d=identicon'

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return None
        user = cls.query.get(data["id"])
        return user

    def generate_token(self, expiration=24 * 60 * 60):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id})

    def read_settings(self) -> dict:
        return json.loads(self.settings or json.dumps(DEFAULT_SETTINGS))

    def write_settings(self, data: dict) -> None:
        self.settings = json.dumps(data)
        db.session.commit()

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'avatar': self.avatar,
            'display_name': self.display_name
        }


class GetOrNewMixin:
    @classmethod
    def get_one_or_new(cls, text):
        record = cls.query.filter_by(text=text).first()
        if not record:
            record = cls(text=text)
        return record


class Tag(db.Model, GetOrNewMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), unique=True)
    url = db.Column(db.String(100))

    def __init__(self, **kwargs) -> None:
        with current_app.test_request_context():
            kwargs["url"] = url_for("tag", text=slugify(kwargs["text"]))
        super(Tag, self).__init__(**kwargs)

    def __repr__(self) -> str:
        return "<Tag: {}>".format(self.text)

    @property
    def heat(self) -> int:
        return self.posts.count()

    def __str__(self) -> str:
        return self.text


class Category(db.Model, GetOrNewMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), unique=True)
    posts = db.relationship("Post", backref="category", lazy="dynamic")

    def __repr__(self) -> str:
        return "<Category: {}>".format(self.text)

    def __str__(self) -> str:
        return self.text


class Integration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    settings = db.Column(db.Text())
    enabled = db.Column(db.Boolean())


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    display = db.Column(db.Boolean(), default=False)
    ptype = db.Column(db.String(20), default="markdown")
    content = db.Column(db.Text)
    html = db.Column(db.Text)

    def to_dict(self):
        return {
            k: getattr(self, k)
            for k in ("id", "slug", "title", "display", "ptype", "content")
        }


@sa.event.listens_for(Page, "before_insert")
@sa.event.listens_for(Page, "before_update")
def get_html(
    mapper: Type[sa.orm.Mapper], connection: sa.engine.Connection, target: sa.orm.Mapper
) -> None:
    if target.ptype == "html":
        target.html = target.content
    else:
        target.html = markdown(target.content)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    floor = db.Column(db.Integer)
    content = db.Column(db.Text())
    html = db.Column(db.Text())
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    replies = db.relationship(
        "Comment", cascade="all, delete-orphan",
        backref=db.backref("parent", remote_side=[id]), lazy="dynamic"
    )

    __table_args__ = (db.UniqueConstraint("post_id", "floor", name="_post_floor"),)

    @property
    def children(self):
        queue = self.replies.all()
        rv = []
        while queue:
            node = queue.pop(0)
            rv.append(node)
            queue.extend(node.replies or [])
        return sorted(rv, key=lambda x: x.create_at)

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author.to_dict(),
            'post': {'title': self.post.title, 'url': self.post.url},
            'floor': self.floor,
            'content': self.content,
            'html': self.html,
            'create_at': self.create_at,
        }


@sa.event.listens_for(Comment, "before_insert")
@sa.event.listens_for(Comment, "before_update")
def comment_html(
    mapper: Type[sa.orm.Mapper], connection: sa.engine.Connection, target: sa.orm.Mapper
) -> None:
    # Use a more strict version of markdown parser for untrusted source.
    target.html = strict_markdown(target.content)


def init_app(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)
    whooshee.init_app(app)
    auto_delete_orphans(Tag, "posts")
    auto_delete_orphans(Category, "posts")
