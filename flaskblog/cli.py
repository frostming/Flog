import click
from . import db
from . import app
from .models import User
import re
import io
import yaml
import os
from .models import Post, Tag

MARKDOWN_RE = re.compile(
    r'(?:-{3}\n(?P<meta>.+?\n)-{3}\n+)?(?P<content>.*)',
    re.DOTALL)


@app.cli.command()
def init():
    """Application initialization"""
    db.drop_all()
    db.create_all()


@app.cli.command()
@click.option('--username', prompt='Please input a username:')
@click.option('--email', prompt='Please input your email address:')
@click.password_option()
def createadmin(username, email, password):
    """Create an admin user"""
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    click.echo('Admin user {} is created successfully'.format(username))


@app.cli.command()
@click.argument('folder', type=click.Path(exists=True))
def importfile(folder):
    """Input a folder of markdown files to import to Floag"""
    def _import_file(filepath):
        if not filepath.endswith('.md') and not filepath.endswith('.markdown'):
            return
        content = io.open(filepath, encoding='utf-8').read()
        meta, body = MARKDOWN_RE.match(content).groups()
        meta = yaml.load(io.StringIO(meta))
        meta['content'] = body
        if 'photos' in meta:
            meta['image'] = meta.pop('photos')
        if 'categories' in meta:
            meta['category'] = meta.pop('categories')
        db.session.add(Post(**meta))
        db.session.commit()
        click.echo('Imported file: %s' % filepath)

    if os.path.isfile(folder):
        _import_file(folder)
    else:
        for filename in os.listdir(folder):
            full_fp = os.path.join(folder, filename)
            _import_file(full_fp)
