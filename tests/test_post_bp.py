#!/usr/bin/env/ python
# coding=utf-8

import unittest
from flask import current_app, url_for
from my_blog import create_app, db
from my_blog.models import Admin, Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.admin = Admin(
            email=current_app.config['BLOG_ADMIN_EMAIL'],
            username="tester",
            password="123456"
        )
        db.session.add(self.admin)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_post(self):
        self.client.post(url_for('auth.login'), data={
            'email': current_app.config['BLOG_ADMIN_EMAIL'],
            'password': "123456"
        })
        response = self.client.get(url_for('post.add_post'))
        self.assertTrue("Post Title" in response.data)
        response = self.client.post(url_for('post.add_post'), data={
            'title': '测试文章',
            'body': "## 测试内容",
            'tags': u"标签1,标签2,标签3"
        }, follow_redirects=True)
        self.assertTrue("测试文章" in response.data)
        self.assertTrue("测试内容" in response.data)

    def test_edit_post(self):
        post = Post(
            title=u"test",
            body=u"test body",
            author=self.admin
        )
        db.session.add(post)
        db.session.commit()
        self.client.post(url_for('auth.login'), data={
            'email': current_app.config['BLOG_ADMIN_EMAIL'],
            'password': "123456"
        })
        response = self.client.get(url_for('post.edit_post', post_id=post.id))
        self.assertTrue("test" in response.data)
        response = self.client.post((url_for('post.edit_post', post_id=post.id)),
                                    data={'title':"hello world"}, follow_redirects=True)
        self.assertTrue("hello world" in response.data)
