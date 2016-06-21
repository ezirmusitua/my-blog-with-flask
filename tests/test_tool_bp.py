#!/usr/bin/env/ python
# coding=utf-8

import unittest
from flask import current_app, url_for
from my_blog import create_app, db
from my_blog.models import Admin


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

    def test_add_tool(self):
        pass
        """
        TODO: Test add_tool view
        self.client.post(url_for('auth.login'), data={
            'email': current_app.config['BLOG_ADMIN_EMAIL'],
            'password': "123456"
        })
        response = self.client.post(url_for('tool.add_tool') ,data={
            'name': u"test-python-tool",
            'desc': u"# Title"
        }, follow_redirects=True)
        print response
        t = PersonalTool.query.filter_by(name=u"test-python-tool").first()
        self.assertTrue(t is not None)
        """


