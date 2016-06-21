#!usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
from flask import current_app, request
from flask.ext.login import UserMixin
from . import db, login_manager


class WorkExperience(db.Model):
    __tablename   = 'work_experience'
    id            = db.Column(db.Integer, primary_key=True)
    work_title    = db.Column(db.Unicode(32), default=None)
    work_type     = db.Column(db.Unicode(8), default=None)
    pos_in_work   = db.Column(db.Unicode(8), default=None)
    work_desc     = db.Column(db.UnicodeText, default=None)
    start_time    = db.Column(db.DateTime, default=datetime.utcnow)
    end_time      = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id      = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return u"<Work %r>" % self.work_title


class EducationExperience(db.Model):
    __tablename__ = 'education_experience'
    id            = db.Column(db.Integer, primary_key=True)
    institution   = db.Column(db.Unicode(64), default=None)
    learn_what    = db.Column(db.Unicode(64), default=None)
    gpa           = db.Column(db.Float, default=None)
    start_time    = db.Column(db.DateTime, default=datetime.utcnow)
    end_time      = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id      = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return u"<Education Experience : %r>" % self.institution


class Skill(db.Model):
    __tablename__ = 'skills'
    id            = db.Column(db.Integer, primary_key=True)
    skill_name    = db.Column(db.Unicode(32), default=True)
    master_degree = db.Column(db.Integer, default=0)
    add_time      = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id      = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return u"<Skill : %r>" % self.skill_name


"""
# TODO: while update the tool view rewrite it
class PersonalTool(db.Model):
    __tablename__ = 'personal_tools'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.UnicodeText, default=None ,unique=True)
    desc          = db.Column(db.UnicodeText, default=u"A personal tool")
    desc_html     = db.Column(db.UnicodeText)
    address       = db.Column(db.String(128), default=None)

    @staticmethod
    def on_changed_desc(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr' ,'acronym', 'b', 'blockquote', 'code' ,
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br']
        target.desc_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True)
        )
db.event.listen(PersonalTool.desc, 'set', PersonalTool.on_changed_desc)
"""

class Guest(db.Model):
    __tablename__  = 'guests'
    id             = db.Column(db.Integer, primary_key=True)
    email          = db.Column(db.String(64), unique=True, index=True)
    avatar_hash    = db.Column(db.String(32))
    comments       = db.relationship('Comment', backref='author', lazy='dynamic')

    def gravatar(self, size=100, default='identcon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')
        ).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __init__(self, **kwargs):
        super(Guest, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None :
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<Guest %r>' % self.email


class Admin(UserMixin, db.Model):

    __tablename__   = 'admin'
    id              = db.Column(db.Integer, primary_key=True)
    email           = db.Column(db.String(64), unique=True, index=True)
    username        = db.Column(db.String(64), unique=True, index=True)
    real_name       = db.Column(db.Unicode(8), unique=True, default=None)
    short_desc      = db.Column(db.Unicode(128), default=None)
    phone_number    = db.Column(db.String(32), default=None)
    cur_address     = db.Column(db.Unicode(64), default=None)
    github_address  = db.Column(db.String(128), default="https://github.com/")
    long_desc       = db.Column(db.Unicode(256), default=None)
    long_desc_html  = db.Column(db.Unicode(1024))
    work_experience = db.relationship('WorkExperience', backref='owner', lazy='dynamic')
    edu_experience  = db.relationship('EducationExperience', backref='owner', lazy='dynamic')
    skills          = db.relationship('Skill', backref='owner', lazy='dynamic')
    password_hash   = db.Column(db.String(128))
    avatar_hash     = db.Column(db.String(32))
    posts           = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None :
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identcon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')
        ).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # following three methods used in shell
    def change_email(self ,new_email):
        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def change_password(self, new_password):
        self.password = new_password
        db.session.add(self)
        return True

    def change_username(self, new_username):
        self.username = new_username
        db.session.add(self)
        return True

    @staticmethod
    def on_changed_long_desc(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr' ,'acronym', 'b', 'blockquote', 'code' ,
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br']
        target.long_desc_html = bleach.linkify(bleach.clean(
            markdown(value, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ], output_format='html'),
            tags=allowed_tags, strip=True)
        )

    def __repr__(self):
        return '<Admin %r>' % self.username

db.event.listen(Admin.long_desc, 'set', Admin.on_changed_long_desc)

# how to make this more efficient
posts_tags_table = db.Table('posts_tags', db.Model.metadata,
                            db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                            db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Tag(db.Model):

    __tablename__ = 'tags'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.Unicode(128), default=None, unique=True)
    count         = db.Column(db.Integer, default=0)
    posts         = db.relationship('Post', secondary=posts_tags_table,
                                    backref=db.backref('tag', lazy='dynamic'))

    def __repr__(self):
        return u"<Tag: %r>" % self.name


class Post(db.Model):

    __tablename__ = 'posts'
    id        = db.Column(db.Integer, primary_key=True)
    title     = db.Column(db.Unicode(128))
    body      = db.Column(db.UnicodeText)
    body_html = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    comments  = db.relationship('Comment', backref='post', lazy='dynamic')
    tags      = db.relationship('Tag', secondary=posts_tags_table,
                                backref=db.backref('post', lazy='dynamic'))

    @staticmethod
    def generate_fake_posts(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        # create a tester admin
        u = Admin.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']).first()
        if u is None:
            u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="jferroal", password="123456")
            db.session.add(u)
        db.session.commit()
        for i in range(count):
            p = Post(title=forgery_py.lorem_ipsum.title(),
                     body=forgery_py.lorem_ipsum.sentences(randint(5, 20)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr' ,'acronym', 'b', 'blockquote', 'code' ,
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ], output_format='html'),
            tags=allowed_tags, strip=True)
        )

db.event.listen(Post.body, 'set', Post.on_changed_body)

class Comment(db.Model):

    __tablename__ = 'comments'
    id        = db.Column(db.Integer, primary_key=True)
    body      = db.Column(db.UnicodeText)
    body_html = db.Column(db.UnicodeText)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    post_id   = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def generate_fake_comments(count=10):
        from random import seed, randint
        import forgery_py
        seed()
        # create a tester user
        u = Admin.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']).first()
        if u is None:
            u = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username="jferroal", password="123456")
            db.session.add(u)
        p = Post.query.filter_by(title=u"Test Post").first()
        if p is None:
            p = Post(title=u"Test Post",
                     body=u"# 测试项目 <br> 这是一片用于测试的文章",
                     author=u)
            db.session.add(p)
        g = Guest.query.filter_by(email="guest@test.com").first()
        if g is None:
            g = Guest(email="commenter@test.com")
            db.session.add(g)
        db.session.commit()
        for i in range(count):
            c = Comment(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                        timestamp=forgery_py.date.date(True),
                        author=g,
                        post=p)
            db.session.add(c)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr' ,'acronym', 'b', 'blockquote', 'code' ,
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ], output_format='html'),
            tags=allowed_tags, strip=True)
        )

db.event.listen(Comment.body, 'set', Comment.on_changed_body)
