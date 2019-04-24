# -*- coding: utf-8 -*-
from datetime import datetime
from random import choice
from typing import Union

import sqlalchemy as sa
from flask import Flask, current_app, json, url_for
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from slugify import slugify
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

db: SQLAlchemy = SQLAlchemy()
whooshee: Whooshee = Whooshee()

tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
)  # type: sa.Table

DEFAULT_SETTINGS = {
    'locale': 'en',
    'name': 'Flog',
    'cover_url': '/static/images/cover.jpg',
    'avatar': '/static/images/avatar.jpeg',
    'description': 'A simple blog powered by Flask',
}


def auto_delete_orphans(cls: sa.Column, attr: str) -> None:
    @sa.event.listens_for(sa.orm.Session, 'after_flush')
    def delete_orphan_listener(session, ctx):
        session.query(cls).filter(~getattr(cls, attr).any()).delete(
            synchronize_session=False
        )


@whooshee.register_model('title', 'description', 'content')
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    image = db.Column(db.String(400))
    lang = db.Column(db.String(20))
    content = db.Column(db.Text)
    comment = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(400))
    author = db.Column(db.String(50))
    tags = db.relationship('Tag', secondary=tags, backref='posts')
    slug = db.Column(db.String(100))
    is_draft = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, **kwargs):
        if isinstance(kwargs.get('category'), str):
            kwargs['category'] = Category.get_one_or_new(kwargs['category'])
        tags = kwargs.get('tags')
        if tags and isinstance(tags[0], str):
            kwargs['tags'] = [Tag.get_one_or_new(tag) for tag in tags]
        if kwargs.get('lang', 'en').startswith('zh'):
            kwargs['lang'] = 'zh_Hans_CN'
        kwargs['is_draft'] = kwargs.pop('type', None) == 'draft'
        kwargs.pop('date', None)
        kwargs.pop('last_modified', None)
        super().__init__(**kwargs)

    @property
    def url(self) -> str:
        return '/%d/%02d-%02d/%s' % (
            self.date.year,
            self.date.month,
            self.date.day,
            self.slug,
        )

    def to_dict(self, ensure_text=False) -> dict:
        return dict(
            id=self.id,
            title=self.title,
            date=self.date,
            image=self.image,
            category=self.category if not ensure_text else str(self.category),
            lang='zh' if self.lang and self.lang.startswith('zh') else self.lang,
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
        return '<Post: %s>' % self.title

    @property
    def previous(self) -> "Post":
        return Post.query.order_by(Post.id.desc()).filter(Post.id < self.id).first()

    @property
    def next(self) -> "Post":
        return Post.query.order_by(Post.id.asc()).filter(Post.id > self.id).first()

    def related_post(self) -> Union["Post", None]:
        posts = Post.query.join(Post.tags).filter(
            Tag.id.in_([tag.id for tag in self.tags]),
            Post.id != self.id,
            ~Post.is_draft,
        )
        if posts.count() > 0:
            return choice(posts.all())
        return None


@sa.event.listens_for(Post, 'before_insert')
def init_url(mapper, connection: sa.engine.Connection, target: sa.orm.Mapper) -> None:
    if target.slug:
        return
    target.slug = slugify(target.title)


@sa.event.listens_for(Post, 'before_update')
def update_post(
    mapper, connection: sa.engine.Connection, target: sa.orm.Mapper
) -> None:
    target.last_modified = datetime.utcnow()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    settings = db.Column(db.Text())

    def __init__(self, **kwargs) -> None:
        password = kwargs.pop('password')
        password = generate_password_hash(password)
        kwargs['password'] = password
        super(User, self).__init__(**kwargs)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def get_one(cls) -> "User":
        """Get the admin user. The only one will be returned."""
        rv: Union[None, User] = cls.query.one_or_none()
        if not rv:
            rv = cls(
                username='admin', password=current_app.config['DEFAULT_ADMIN_PASSWORD']
            )
            db.session.add(rv)
            db.session.commit()
        return rv

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return None
        user = cls.query.get(data['id'])
        return user

    def generate_token(self, expiration=24 * 60 * 60):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def read_settings(self) -> dict:
        return json.loads(self.settings or json.dumps(DEFAULT_SETTINGS))

    def write_settings(self, data: dict) -> None:
        self.settings = json.dumps(data)
        db.session.commit()


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
            kwargs['url'] = url_for('tag', text=slugify(kwargs['text']))
        super(Tag, self).__init__(**kwargs)

    def __repr__(self) -> str:
        return '<Tag: {}>'.format(self.text)

    @property
    def heat(self) -> int:
        return self.posts.count()

    def __str__(self) -> str:
        return self.text


class Category(db.Model, GetOrNewMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), unique=True)
    posts = db.relationship('Post', backref='category')

    def __repr__(self) -> str:
        return '<Category: {}>'.format(self.text)

    def __str__(self) -> str:
        return self.text


class Integration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    settings = db.Column(db.Text())
    enabled = db.Column(db.Boolean())


def init_app(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)
    whooshee.init_app(app)
    auto_delete_orphans(Tag, 'posts')
    auto_delete_orphans(Category, 'posts')
