# -*- coding: utf-8 -*-
from . import db, app
from datetime import datetime
from slugify import slugify
from flask import url_for
from sqlalchemy import event


tags = db.Table(
    'tags',
    db.Column('tag_text', db.String(50), db.ForeignKey('tag.text')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)
    image = db.Column(db.String(400))
    layout = db.Column(db.String(20))
    content = db.Column(db.Text)
    comment = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(400))
    author = db.Column(db.String(50))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('posts', lazy=True))
    url = db.Column(db.String(100))
    category = db.Column(db.String(50), db.ForeignKey('category.text'))

    def __init__(self, **kwargs):
        tags = kwargs.pop('tags', [])
        category = kwargs.pop('category', None)
        super(Post, self).__init__(**kwargs)
        tags_column = []
        for tag in tags:
            tag_object = Tag.query.get(tag)
            if not tag_object:
                tag_object = Tag(text=tag)
                db.session.add(tag_object)
            tags_column.append(tag_object)
        self.tags = tags_column
        if category:
            category_object = Category.query.get(category)
            if not category_object:
                category_object = Category(text=category)
                db.session.add(category_object)
            self.category = category
        db.session.commit()

    def to_dict(self):
        return dict(
            title=self.title,
            date=self.date,
            image=self.image,
            category=self.category,
            layout=self.layout,
            comment=self.comment,
            description=self.description,
            author=self.author,
            tags=self.tags,
            url=self.url,
            content=self.content,
            last_modified=self.last_modified
        )

    def __repr__(self):
        return self.title

    @property
    def previous(self):
        return Post.query.order_by(Post.id.desc())\
            .filter(Post.id < self.id).first()

    @property
    def next(self):
        return Post.query.order_by(Post.id.asc())\
            .filter(Post.id > self.id).first()


@event.listens_for(Post, 'before_insert')
def init_url(mapper, connection, target):
    if not target.date:
        target.date = datetime.utcnow()

    year = str(target.date.year)
    date = target.date.strftime('%m-%d')
    with app.test_request_context():
        target.url = url_for('post', year=year, date=date,
                             title=slugify(target.title))


@event.listens_for(Post, 'before_update')
def update_post(mapper, connection, target):
    target.last_modified = datetime.utcnow()

    year = str(target.date.year)
    date = target.date.strftime('%m-%d')
    with app.test_request_context():
        target.url = url_for('post', year=year, date=date,
                             title=slugify(target.title))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(100))
    password = db.Column(db.String(20))


class Tag(db.Model):
    text = db.Column(db.String(50), primary_key=True)
    url = db.Column(db.String(100))

    def __init__(self, **kwargs):
        with app.test_request_context():
            kwargs['url'] = url_for('tags') + '#' + slugify(kwargs['text'])
        super(Tag, self).__init__(**kwargs)

    def __repr__(self):
        return self.text


class Category(db.Model):
    text = db.Column(db.String(50), primary_key=True)
    posts = db.relationship('Post')

    def __repr__(self):
        return self.text
