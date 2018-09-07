# -*- coding: utf-8 -*-
from datetime import datetime
from random import choice

import sqlalchemy as sa
from flask import url_for, current_app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


def auto_delete_orphans(cls, attr):

    @sa.event.listens_for(sa.orm.Session, 'after_flush')
    def delete_orphan_listener(session, ctx):
        session.query(cls).filter(~getattr(cls, attr).any())\
                                   .delete(synchronize_session=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image = db.Column(db.String(400))
    lang = db.Column(db.String(20))
    content = db.Column(db.Text)
    comment = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(400))
    author = db.Column(db.String(50))
    tags = db.relationship('Tag', secondary=tags,
                           backref='posts')
    slug = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    @property
    def url(self):
        return '/%d/%02d-%02d/%s' % (self.date.year, self.date.month,
                                     self.date.day, self.slug)

    def to_dict(self):
        return dict(
            title=self.title,
            date=self.date,
            image=self.image,
            category=self.category,
            lang=self.lang,
            comment=self.comment,
            description=self.description,
            author=self.author,
            tags=self.tags,
            slug=self.slug,
            content=self.content,
            last_modified=self.last_modified,
        )

    def __repr__(self):
        return '<Post: %s>' % self.title

    @property
    def previous(self):
        return Post.query.order_by(Post.id.desc())\
            .filter(Post.id < self.id).first()

    @property
    def next(self):
        return Post.query.order_by(Post.id.asc())\
            .filter(Post.id > self.id).first()

    def related_post(self):
        posts = Post.query.join(Post.tags).filter(
            Tag.id.in_([tag.id for tag in self.tags]),
            Post.id != self.id)
        if posts.count() > 0:
            return choice(posts.all())


@sa.event.listens_for(Post, 'before_insert')
def init_url(mapper, connection, target):
    if target.slug:
        return
    target.slug = slugify(target.title)


@sa.event.listens_for(Post, 'before_update')
def update_post(mapper, connection, target):
    target.last_modified = datetime.utcnow()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        password = generate_password_hash(password)
        kwargs['password'] = password
        super(User, self).__init__(**kwargs)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_one(cls):
        """Get the admin user. The only one will be returned."""
        return cls.query.one()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    url = db.Column(db.String(100))

    def __init__(self, **kwargs):
        with current_app.test_request_context():
            kwargs['url'] = url_for('tag', text=slugify(kwargs['text']))
        super(Tag, self).__init__(**kwargs)

    def __repr__(self):
        return '<Tag: {}>'.format(self.text)

    @property
    def heat(self):
        return self.posts.count()

    def __str__(self):
        return self.text


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    posts = db.relationship('Post',
                            backref='category')

    def __repr__(self):
        return '<Category: {}>'.format(self.text)

    def __str__(self):
        return self.text


def init_app(app):
    db.init_app(app)
    Migrate(app, db)
    auto_delete_orphans(Tag, 'posts')
    auto_delete_orphans(Category, 'posts')
