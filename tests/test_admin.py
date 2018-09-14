from flask import url_for, g

from flaskblog.models import User, DEFAULT_SETTINGS, Tag, Category, Post
from .base import BaseTestCase


class AdminTestCase(BaseTestCase):

    def login(self, username=None, password=None):
        if username is None and password is None:
            username = password = 'admin'
        return self.client.post(
            url_for('admin.login'),
            data={'username': username, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self.client.get(url_for('admin.logout'), follow_redirects=True)

    def setUp(self):
        super().setUp()
        self.login()

    def test_default_user(self):
        user = User.get_one()
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.check_password('admin'))

    def test_default_settings(self):
        self.assertEqual(g.site, DEFAULT_SETTINGS)

    def test_posts_page(self):
        response = self.client.get(url_for('admin.posts'))
        self.assertIn('Test Post</a>', response.get_data(True))

    def test_new_post_page(self):
        response = self.client.get(url_for('admin.new'))
        data = response.get_data(True)
        self.assertIn('Save Draft</button>', data)
        self.assertIn('Post</button>', data)

    def test_new_post(self):
        response = self.client.post(
            url_for('admin.new'),
            data={
                'title': 'New Post', 'content': 'Test new post', 'author': 'admin',
                'slug': 'new-post', 'category': 'new', 'tags': ['new']
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.query.filter_by(title='New Post').count() > 0)
        self.assertTrue(Tag.query.filter_by(text='new').count() > 0)
        self.assertTrue(Category.query.filter_by(text='new').count() > 0)

    def test_save_draft(self):
        self.client.post(
            url_for('admin.new'),
            data={
                'title': 'New Post', 'content': 'Test new post', 'author': 'admin',
                'slug': 'new-post', 'category': 'new', 'tags': ['new'], 'is_draft': True
            },
            follow_redirects=True
        )
        response = self.client.get(url_for('admin.posts'))
        data = response.get_data(True)
        self.assertIn('<span class="badge badge-light">1</span>', data)

    def test_edit_post_page(self):
        post = Post.query.first()
        response = self.client.get(url_for('admin.edit', id=post.id))
        data = response.get_data(True)
        self.assertIn('value="Test Post"', data)
        self.assertIn('Save</button>', data)
        self.assertNotIn('Save Draft</button>', data)

    def test_edit_post(self):
        post = Post.query.first()
        payload = post.to_dict()
        payload.update(title='Changed Title')
        self.client.post(
            url_for('admin.edit', id=post.id),
            data=payload,
            follow_redirects=True
        )
        post = Post.query.first()
        self.assertEqual(post.title, 'Changed Title')

    def test_change_password(self):
        self.client.post(
            url_for('admin.password'),
            data={
                'old': 'admin',
                'new': 'newpassword',
                'confirm': 'newpassword'
            },
            follow_redirects=True
        )
        self.assertTrue(User.get_one().check_password('newpassword'))

    def test_about_redirect(self):
        response = self.client.get(
            url_for('admin.edit', cat='About')
        )
        self.assertIn(url_for('admin.new'), response.location)

    def test_change_settings(self):
        payload = DEFAULT_SETTINGS.copy()
        payload.update(
            name='Test Site Name',
        )
        self.client.post(
            url_for('admin.settings'),
            data=payload,
            follow_redirects=True
        )
        self.assertEqual(User.get_one().read_settings()['name'], 'Test Site Name')
        data = self.client.get('/').get_data(True)
        self.assertIn('heading">Test Site Name</h1>', data)
