from jinja2 import Markup
from .md import md
from flask import request
from datetime import datetime
from slugify import slugify
from . import app


@app.template_filter()
def date(s, format='%Y-%m-%d'):
    return s.strftime(format)


@app.context_processor
def get_current_time():
    return {'current_time': datetime.now()}


@app.context_processor
def blog_objects():
    url = request.url
    title = request.url_rule.endpoint
    rv = {'url': url, 'title': title}
    return {'page': rv}


@app.template_filter('slugify')
def make_slugify(s):
    return slugify(s)


@app.template_filter('render')
def render_markdown(s):
    return Markup(md(s))


@app.template_filter('toc')
def render_toc(s):
    md.renderer.reset_toc()
    md(s)
    return Markup(md.renderer.render_toc(level=3))
