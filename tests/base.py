import unittest
from flaskblog.app import create_app
from flaskblog.models import db, Post, Tag, Category


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        self.init_db()

    def init_db(self):
        post = Post(
            title='Test Post',
            author='John Doe',
            description='Test Subtitle',
            content='## Title\nHello World.',
            slug='test-post'
        )
        post.tags.append(Tag(text='testing'))
        post.category = Category(text='testing')
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()
