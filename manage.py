#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import os
import datetime
from my_blog import create_app, db
from my_blog.models import Guest, WorkExperience,\
    EducationExperience, Skill, Admin, Post, Comment, Tag
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print 'Importing environment from .env ... '
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db,
                WorkExperience=WorkExperience,
                EducationExperience=EducationExperience,
                Skill=Skill, Guest=Guest, Admin=Admin, Post=Post,
                Comment=Comment, Tag=Tag)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable]+sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def create_pre_db():
    """Following data for preview"""
    db.drop_all()
    db.create_all()
    admin = Admin(
        email=app.config['BLOG_ADMIN_EMAIL'],
        password="123456",
    )
    work_exp = [WorkExperience(
        work_title=u"Flask Blog-%d" % i,
        work_type=u"Personal Project",
        pos_in_work=u"Total",
        work_desc=u"Use Flask implement a blog application",
        start_time=datetime.date(2016, 2, 5),
        owner=admin
    ) for i in range(3)]
    edu_exp = [EducationExperience(
        institution=u"TongJi University-%d" % i,
        learn_what=u"Information Security",
        gpa=3.89,
        start_time=datetime.date(2016, 2, 5),
        owner=admin
    ) for i in range(3)]
    skills = [Skill(
        skill_name=u"Python-%d" % i,
        master_degree=4,
        owner=admin
    ) for i in range(3)]
    tags = [Tag(name=u"tag-%d" % i) for i in range(10)]
    db.session.add_all([admin]+work_exp+edu_exp+skills+tags)
    db.session.commit()
    Post.generate_fake_posts(12)
    Comment.generate_fake_comments(5)


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def first_run():
    """Initialize for first time running"""
    from my_blog.models import Admin
    is_identify = raw_input("run this script will drop all your data? Sure to run?(y/n)")
    if is_identify is 'y':
        db.drop_all()
        admin_password = raw_input("Enter the admin's password: ")
        github_address = raw_input("Enter the github address of you: ")
        db.create_all()
        admin = Admin(email=app.config['BLOG_ADMIN_EMAIL'],
                      password=admin_password,
                      github_address=github_address)
        db.session.add(admin)
        db.session.commit()
        print "Admin created !\nUse your email and password to login\n" \
              "URL: */auth/login"

@manager.command
def deploy():
    """Run deployment tasks"""
    from flask.ext.migrate import upgrade
    # migrate database to latest revision
    upgrade()

if __name__ == '__main__':
    manager.run()
