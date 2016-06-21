#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import unittest
from flask import url_for, current_app
from my_blog import create_app, db
from my_blog.models import Admin, Post


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app         = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page(self):
        response = self.client.get(url_for('auth.login'))
        self.assertTrue('Welcome to Jferroal\'s Blog' in response.data)

    def login(self, email, password):
        return self.client.post(url_for('auth.login'), data={
            'email':email, 
            'password':password, 
        }, follow_redirects=True)

    def test_login(self):
        # add a tester
        test_u   = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username='tester', password='123456')
        db.session.add(test_u)
        db.session.commit()
        # use tester to login
        response = self.login(email=current_app.config['BLOG_ADMIN_EMAIL'], password='123456')
        self.assertTrue('Jferroal' in response.data)

    def test_logout(self):
        test_u   = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username='tester', password='123456')
        db.session.add(test_u)
        db.session.commit()
        response = self.login(email=current_app.config['BLOG_ADMIN_EMAIL'], password='123456')
        self.assertTrue("Login successful." in response.data)
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue("You have been logout." in response.data)


    def test_login_require(self):
        test_u   = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username='tester', password='123456')
        test_p = Post(title=u"Test", body=u"Hello World", author=test_u)
        db.session.add_all([test_p, test_u])
        db.session.commit()
        response = self.client.get(url_for('post.edit_post', post_id=test_p.id), follow_redirects=True)
        self.assertTrue('Welcome' in response.data)
        self.login(email=current_app.config['BLOG_ADMIN_EMAIL'], password='123456')
        response = self.client.get(url_for('post.edit_post', post_id=test_p.id), follow_redirects=True)
        self.assertTrue("Test" in response.data)






