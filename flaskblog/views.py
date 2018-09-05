import io

from flask import abort, render_template, request, send_file
from werkzeug.contrib.atom import AtomFeed

from . import app
from .md import markdown
from .models import Category, Post, Tag
from .utils import get_tag_cloud, calc_token

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


@app.route('/')
@app.route('/page/<int:page>')
def home(page=None):
    paginate = Post.query.join(Post.category)\
                         .filter(Category.text != 'About')\
                         .order_by(Post.date.desc())\
                         .paginate(page, app.config['BLOG_PER_PAGE'])
    tag_cloud = get_tag_cloud()
    return render_template(
        'index.html',
        posts=paginate.items,
        tag_cloud=tag_cloud,
        paginate=paginate)


@app.route('/<int:year>/<date>/<title>')
def post(year, date, title):
    post = None
    for item in Post.query.all():
        if item.url == request.path:
            post = item
            break
    if not post:
        abort(404)
    content = markdown(post.content)
    toc = markdown.renderer.render_toc()
    return render_template('post.html', post=post, content=content, toc=toc)


@app.route('/about')
def about():
    lang = request.args.get('lang', 'zh')
    post = Post.query.filter_by(lang=lang)\
               .join(Post.category).filter(Category.text == 'About')\
               .first_or_404()
    return render_template('post.html', post=post, content=markdown(post.content))


@app.route('/tag/<text>')
def tag(text):
    tag = Tag.query.filter_by(url=request.path).first_or_404()
    posts = Post.query.join(Post.tags).filter(Tag.text == tag.text)\
                                      .order_by(Post.date.desc())
    tag_cloud = get_tag_cloud()
    return render_template(
        'index.html', posts=posts, tag_cloud=tag_cloud, tag=tag)


@app.route('/cat/<int:cat_id>')
def category(cat_id):
    cat = Category.query.get(cat_id)
    posts = cat.posts
    tag_cloud = get_tag_cloud()
    return render_template(
        'index.html', posts=posts, tag_cloud=tag_cloud, cat=cat)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/feed.xml')
def feed():
    feed = AtomFeed(
        'Recent Article', feed_url=request.url, url=request.url_root)
    posts = Post.query.order_by(Post.date.desc()).limit(15)
    for post in posts:
        feed.add(
            post.title,
            str(markdown(post.content)),
            content_type='html',
            author=post.author or 'Unnamed',
            url=urljoin(request.url_root, post.url),
            updated=post.last_modified,
            published=post.date)
    return feed.get_response()


@app.route('/sitemap.xml')
def sitemap():
    posts = Post.query.order_by(Post.date.desc())
    fp = io.BytesIO(
        render_template('sitemap.xml', posts=posts).encode('utf-8'))
    return send_file(fp, attachment_filename='sitemap.xml')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


if app.config.get('ENABLE_COS_UPLOAD', False):
    app.add_url_rule('/upload-token', 'upload_token', calc_token)
