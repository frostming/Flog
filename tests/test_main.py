from flask import current_app, url_for

from .base import BaseTestCase, Post


class MainViewTestCase(BaseTestCase):

    def test_app_exist(self):
        self.assertIsNotNone(current_app)

    def test_index(self):
        response = self.client.get('/')
        data = response.get_data(True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="cover', data)
        self.assertIn('Test Post', data)
        self.assertIn('href="/tag/testing"', data)
        self.assertIn('testing</a>', data)

    def test_post(self):
        post = Post.query.first()
        self.assertTrue(post.url.endswith('test-post'))
        response = self.client.get(post.url)
        data = response.get_data(True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('title">Test Post</h1>', data)
        self.assertIn('<p>Hello World.</p>', data)
        self.assertIn('/tag/testing">testing', data)
        self.assertIn('title">Title</a>', data)

    def test_tag(self):
        response = self.client.get('/tag/testing')
        data = response.get_data(True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('class="cover', data)
        self.assertIn('Test Post', data)

    def test_category(self):
        response = self.client.get('/cat/1')
        data = response.get_data(True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('class="cover', data)
        self.assertIn('Test Post', data)

    def test_not_found(self):
        response = self.client.get('/notfound')
        data = response.get_data(True)
        self.assertEqual(response.status_code, 404)
        self.assertIn('<svg class="me404"', data)

    def test_no_auth(self):
        response = self.client.get(url_for('admin.posts'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('admin.login'), response.location)

    def test_about_page(self):
        data = self.client.get(url_for('about')).get_data(True)
        self.assertIn('About page is not created yet, please click', data)
