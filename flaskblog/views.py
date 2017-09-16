from . import app
from datetime import datetime
from werkzeug.contrib.atom import AtomFeed
from flask import render_template, request, abort, send_file
import os
import io
from .md import md
from .models import Post, Tag, Category
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
from .utils import get_tag_cloud


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/blog')
@app.route('/blog/page/<int:page>')
def blog(page=None):
    paginate = Post.query.join(Post.category)\
                         .filter(Category.text != 'About')\
                         .order_by(Post.date.desc())\
                         .paginate(page, app.config['BLOG_PER_PAGE'])
    tag_cloud = get_tag_cloud()
    return render_template('blog.html', posts=paginate.items,
                           tag_cloud=tag_cloud, paginate=paginate)


@app.route('/<int:year>/<date>/<title>')
def post(year, date, title):
    post = Post.query.filter_by(url=request.path).first_or_404()
    md.renderer.reset_toc()
    content = md(post.content)
    toc = md.renderer.render_toc(level=3)
    return render_template('post.html', post=post,
                           content=content, toc=toc)


@app.route('/about')
def about():
    post = Post.query.join(Post.category).filter(Category.text == 'About')\
                                         .first_or_404()
    return render_template('post.html', post=post, content=md(post.content))


@app.route('/tag/<text>')
def tag(text):
    tag = Tag.query.filter_by(url=request.path).first_or_404()
    posts = Post.query.join(Post.tags).filter(Tag.text == tag.text)\
                                      .order_by(Post.date.desc())
    tag_cloud = get_tag_cloud()
    return render_template('blog.html', posts=posts, tag_cloud=tag_cloud,
                           tag=tag)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/feed.xml')
def feed():
    feed = AtomFeed('Recent Article', feed_url=request.url,
                    url=request.url_root)
    posts = Post.query.order_by(Post.date.desc()).limit(15)
    for post in posts:
        feed.add(post.title, str(md(post.content)),
                 content_type='html',
                 author=post.author or 'Unnamed',
                 url=urljoin(request.url_root, post.url),
                 updated=post.last_modified,
                 published=post.date)
    return feed.get_response()


@app.route('/sitemap.xml')
def sitemap():
    posts = Post.query.order_by(Post.date.desc())
    fp = io.BytesIO(render_template('sitemap.xml', posts=posts)
                    .encode('utf-8'))
    return send_file(fp, attachment_filename='sitemap.xml')
