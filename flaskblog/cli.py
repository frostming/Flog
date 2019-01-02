import io
import os
import re

import click
import yaml
from flask.cli import with_appcontext

from .models import Post, db

MARKDOWN_RE = re.compile(
    r'(?:-{3}\n(?P<meta>.+?\n)-{3}\n+)?(?P<content>.*)',
    re.DOTALL)


@click.command()
@click.argument('folder', type=click.Path(exists=True))
def imp(folder):
    """Input a folder of markdown files to import as posts"""
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


@click.command()
@click.option('-o', '--output', type=click.Path(file_okay=False))
def exp(output):
    """Export all the posts to markdown files, including post meta"""
    if not output:
        output = '.'
    if not os.path.exists(output):
        os.mkdir(output)
    cwd = os.getcwd()
    os.chdir(output)
    for post in Post.query:
        meta = post.to_dict()
        filename = meta.pop('url').rsplit('/', 1)[-1] + '.md'
        content = meta.pop('content')
        container = io.StringIO()
        yaml.dump(meta, container, allow_unicode=True)
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write('---\n' + container.getvalue().rstrip() +
                     '\n---\n\n' + content)
        click.echo('Writing to file %s' % os.path.join(output, filename))
    os.chdir(cwd)


@click.command()
@with_appcontext
def reindex():
    """Reindex the searchable models."""
    from .models import whooshee
    whooshee.reindex()
    click.echo("Index created for models.")


def init_app(app):
    app.cli.add_command(imp)
    app.cli.add_command(exp)
    app.cli.add_command(reindex)
