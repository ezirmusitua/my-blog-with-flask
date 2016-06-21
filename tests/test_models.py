#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import unittest
from random import seed, randint
from flask import current_app
import forgery_py
from my_blog import create_app, db
from my_blog.models import Guest, Admin, Tag, Post, Comment

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_can_create(self):
        seed()
        u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="tester", password="123456")
        p = Post(title=forgery_py.lorem_ipsum.title(), 
                 body=forgery_py.lorem_ipsum.sentences(randint(1, 5)), 
                 timestamp=forgery_py.date.date(True), 
                 author=u)

        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        assert u in Admin.query.all()
        assert p in Post.query.all()

    def test_password_setter(self):
        u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="tester", password="123456")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="tester", password="123456")
        with self.assertRaises(AttributeError):
            u.password()

    def test_password_verification(self):
        u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="tester", password="123456")
        self.assertTrue(u.verify_password('123456'))
        self.assertFalse(u.verify_password('1234567'))

    def test_password_salt_are_random(self):
        u1 = Admin(email="test1@test.com", username="tester1", password="123456")
        u2 = Admin(email="test2@test.com", username="tester2", password="123456")
        self.assertTrue(u1.password_hash is not u2.password_hash)

    def test_change_email(self):
        u1 = Admin(email="test1@test.com", username="tester1", password="123456")
        u1.change_email(new_email=current_app.config['BLOG_ADMIN_EMAIL'])
        self.assertTrue(Admin.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']).first())

    def test_change_password(self):
        u1 = Admin(email="test1@test.com", username="tester1", password="123456")
        u1.change_password(new_password="234567")
        self.assertTrue(Admin.query.filter_by(email='test1@test.com').first().verify_password('234567'))

    def test_change_username(self):
        u1 = Admin(email="test1@test.com", username="tester1", password="123456")
        u1.change_username(new_username="tester")
        self.assertTrue(Admin.query.filter_by(username="tester").first())

    def test_fake_post_generation(self):
        Post.generate_fake_posts(50)
        fake_posts_count = len(Post.query.all())
        self.assertTrue(fake_posts_count is 50)

    def test_post_body_changed(self):
        u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="jferroal", password="123456")
        test_body = u"# Heading1  \n1. L1  \n2. L2  \n3. L3  \n"
        p = Post(title=u"test post",
                 body=test_body, 
                 author=u)
        db.session.add_all([u, p])
        db.session.commit()
        tmp = Post.query.filter_by(title=u"test post").first()
        self.assertTrue('<h1>Heading1</h1>' in tmp.body_html)
        p.body = u"## Heading2"
        db.session.add(p)
        db.session.commit()
        tmp = Post.query.filter_by(title=u"test post").first()
        self.assertTrue('<h2>Heading2</h2>' in tmp.body_html)

    def test_fake_comment_generation(self):
        Comment.generate_fake_comments()
        fake_comments_count = len(Comment.query.all())
        self.assertTrue(fake_comments_count is 10)

    def test_comment_body_changed(self):
        u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="jferroal", password="123456")
        g = Guest(email="Guest@test.com")
        p = Post(body=u"# Post ... ",
                 title=u"Test Post",
                 author=u)
        c = Comment(body=u"# Comment 1",
                    author=g, 
                    post=p)
        db.session.add_all([u, p, c])
        db.session.commit()
        tmp = Comment.query.filter_by(author=u).first()
        self.assertTrue('<h1>Comment 1</h1>' in tmp.body_html)
        c.body = u"## Comment 2"
        db.session.add(c)
        db.session.commit()
        tmp = Comment.query.filter_by(author=u).first()
        self.assertTrue('<h2>Comment 2</h2>' in tmp.body_html)

    def test_long_desc_body_changed(self):
        u = Admin(
            email=current_app.config['BLOG_ADMIN_EMAIL'],
            username="jferroal",
            password="123456",
            long_desc=u"# Title"
        )
        db.session.add(u)
        db.session.commit()
        self.assertTrue("<h1>Title</h1>" in u.long_desc_html)
        u.long_desc = u"# Hello"
        self.assertTrue("<h1>Hello</h1>" in u.long_desc_html)

    def test_posts_with_tags(self):
        u = Admin(
            email=current_app.config['BLOG_ADMIN_EMAIL'],
            username="jferroal",
            password="123456"
        )
        p1 = Post(
            title=u"test 1",
            body=u"# Test 1" ,
            author=u
        )
        p2 = Post(
            title=u"test 2",
            body=u"# Test 2",
            author=u
        )
        for i in range(5):
            tag = Tag(
                name=u"tag%d" % i
            )
            p1.tags.append(tag)
            p2.tags.append(tag)
        db.session.add_all([u, p1, p2])
        db.session.commit()
        self.assertTrue(len(p1.tags) == len(p2.tags) == 5)


