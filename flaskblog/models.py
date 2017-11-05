# -*- coding: utf-8 -*-
from . import db, app
from datetime import datetime
from slugify import slugify
from flask import url_for
import sqlalchemy as sa
from random import sample
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


def auto_delete_orphans(attr):
    target_class = attr.parent.class_

    @sa.event.listens_for(sa.orm.Session, 'after_flush')
    def delete_orphan_listener(session, ctx):
        session.query(target_class).filter(~attr.any())\
                                   .delete(synchronize_session=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
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

    def __init__(self, **kwargs):
        tags = kwargs.pop('tags', [])
        category = kwargs.pop('category', None)
        super(Post, self).__init__(**kwargs)
        tags_column = []
        for tag in tags:
            tag_object = Tag.query.filter_by(text=tag).first()
            if not tag_object:
                tag_object = Tag(text=tag)
            tags_column.append(tag_object)
        self.tags = tags_column
        if category:
            category_object = Category.query.filter_by(text=category).first()
            if not category_object:
                category_object = Category(text=category)
            self.category = category_object

    @property
    def url(self):
        return '/%d/%0d-%0d/%s' % (self.date.year, self.date.month,
                                   self.date.day, self.slug)

    def to_dict(self):
        return dict(
            title=self.title,
            date=self.date,
            image=self.image,
            category=self.category.text,
            lang=self.lang,
            comment=self.comment,
            description=self.description,
            author=self.author,
            tags=[tag.text for tag in self.tags],
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

    def related_post(self, maxnum=1):
        posts = Post.query.join(Post.tags)\
                          .filter(Tag.text.in_([tag.text for tag in self.tags]))
        num = min(posts.count(), maxnum)
        return sample(posts.all(), num)


@sa.event.listens_for(Post, 'before_insert')
def init_url(mapper, connection, target):
    if taraget.slug:
        return

    if not target.date:
        target.date = datetime.utcnow()

    year = str(target.date.year)
    date = target.date.strftime('%m-%d')
    target.last_modified = datetime.utcnow()
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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    url = db.Column(db.String(100))

    def __init__(self, **kwargs):
        with app.test_request_context():
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
