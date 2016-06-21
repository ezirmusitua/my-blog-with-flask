#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import unittest
from flask import url_for, current_app, session
from my_blog import create_app, db
from my_blog.models import Guest, Admin, Post, Comment, Tag

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app         = create_app('testing')
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
        self.client      = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue("Jferroal" in response.data)

    def test_show_posts_list(self):
        p = Post(title=u"test post", body=u"#Head1", author=self.admin)
        db.session.add(p)
        db.session.commit()
        response = self.client.get('/')
        self.assertTrue("test post" in response.data)
    
    def test_pagination(self):
        Post.generate_fake_posts(12)
        response = self.client.get('/')
        self.assertTrue('pagination' in response.data)
    
    def test_show_post_content(self):
        p = Post(title=u"test post", body=u"# Test Post", author=self.admin)
        db.session.add(p)
        db.session.commit()
        response = self.client.get('/posts/%d' % p.id)
        self.assertTrue('test post' in response.data)

    def test_show_comment_in_post(self):
        g = Guest(email='guest@test.com')
        p = Post(title=u"test post", body=u"# Test Post", author=self.admin)
        c = Comment(body=u"## hello", author=g, post=p)
        db.session.add_all([p, c])
        db.session.commit()
        response = self.client.get('/posts/%d' % self.admin.id)
        self.assertTrue('hello' in response.data)

    def comment(self, post_id, email, body):
        return self.client.post(url_for('main.post', id=post_id), data={
            'email': email, 
            'body': body
        }, follow_redirects=True)

    def test_can_add_comment(self):
        p = Post(title=u"test post", body=u"# Test Post", author=self.admin)
        db.session.add(p)
        db.session.commit()
        response = self.comment(p.id, email=current_app.config['BLOG_ADMIN_EMAIL'], body=u'my name is jferroal')
        self.assertTrue('my name is jferroal' in response.data)
    
    def test_show_tags(self):
        tag_list = [Tag(name=u"tag-"+unicode(i), count=i) for i in range(5)]
        db.session.add_all(tag_list)
        db.session.commit()
        response = self.client.get(url_for('main.index'))
        for i in range(5):
            self.assertTrue("tag-%d" % i in response.data)

    def test_show_post_under_tag(self):
        tag = Tag(name=u"tag")
        posts = [Post(title=u"test%d" % i, body=u"Test", author=self.admin) for i in range(3)]
        [post.tags.append(tag) for post in posts]
        [tag.posts.append(post) for post in posts]
        db.session.add_all([tag] + posts)
        db.session.commit()
        response = self.client.get(url_for('main.show_posts_under_tag',
                                           tag_name=tag.name))
        for i in range(3):
            self.assertTrue("test%d" % i in response.data)

    def test_show_tools(self):
        # TODO: Test show_tools
        pass
        """
        tool_list = [PersonalTool(
            name=u"TestTool%d" % i,
            desc=u"This is the Test Tool %d" % i,
            address=u"https://github.com"
        ) for i in range(4)]
        db.session.add_all(tool_list)
        db.session.commit()
        response = self.client.get(url_for('main.index'))
        for i in range(4):
            self.assertTrue("TestTool%d" % i in response.data)
    """


