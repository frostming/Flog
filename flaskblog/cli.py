import click
from flask.cli import with_appcontext
import faker
from .models import Post, db
import random
from flask import render_template, current_app

fake = faker.Faker()


def generate_on_fake_post():
    return {
        "title": fake.sentence(nb_words=6, variable_nb_words=True),
        "description": fake.sentence(nb_words=6, variable_nb_words=True),
        "image": fake.image_url(width=800, height=400),
        "slug": fake.slug(),
        "content": "## Hello World\n我是测试数据我是测试数据\n\n![](https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943)\n",
        "author": fake.name(),
        "date": fake.date_time(),
        "is_draft": random.choice([False, True]),
        "lang": random.choice(["en", "zh_Hans_CN"]),
        "category": random.choice(["programming", "essay"]),
        "tags": random.sample(
            ["test", "python", "algorithm", "reading"], random.randint(1, 3)
        ),
    }


@click.command()
@with_appcontext
def reindex():
    """Reindex the searchable models."""
    from .models import whooshee

    whooshee.reindex()
    click.echo("Index created for models.")


@click.command()
@with_appcontext
def fake_db():
    """Insert fake data into database."""
    for _ in range(100):
        post = Post(**generate_on_fake_post())
        db.session.add(post)
    db.session.commit()
    click.echo("Add 100 posts")


@click.command()
@with_appcontext
def export_wxr():
    """Export comments into WXR file"""
    posts = []
    with current_app.test_request_context("/"):
        for post in Post.query.all():
            if not post.comments:
                continue
            posts.append(post)
        with open("wxr.xml", "w", encoding="utf-8") as f:
            f.write(render_template("wxr.xml", posts=posts))


def init_app(app):
    app.cli.add_command(reindex)
    app.cli.add_command(fake_db)
    app.cli.add_command(export_wxr)
