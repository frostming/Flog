import os.path as op
from datetime import datetime

import yaml
from flask import request
from jinja2 import Markup
from slugify import slugify

from .md import markdown
from .models import Category

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


def date(s, format='%Y-%m-%d'):
    return s.strftime(format)


def get_current_time():
    return {'current_time': datetime.now()}


def blog_objects():
    url = request.url
    title = request.url_rule.endpoint if request.url_rule else ''
    categories = Category.query.filter(Category.text != 'About').all()
    rv = {'url': url, 'title': title}
    return {'page': rv, 'urljoin': urljoin, 'categories': categories}


def site_config():
    config_yml = op.join(op.dirname(__file__), 'site.yml')
    with open(config_yml, encoding='utf-8') as fp:
        return {'site': yaml.load(fp)}


def make_slugify(s):
    return slugify(s)


def render_markdown(s):
    return Markup(markdown(s))


def init_app(app):
    app.add_template_filter(date)
    app.add_template_filter(make_slugify, 'slugify')
    app.add_template_filter(render_markdown, 'render')
    app.context_processor(get_current_time)
    app.context_processor(blog_objects)
    app.context_processor(site_config)
