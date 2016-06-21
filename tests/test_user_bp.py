#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import unittest
from flask import url_for, current_app
from my_blog import create_app, db
from my_blog.models import Admin, WorkExperience, EducationExperience, Skill
from my_blog.user.views import check_in_table


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_show_profile(self):
        admin = Admin(
            email=current_app.config['BLOG_ADMIN_EMAIL'],
            username="profile_tester",
            real_name=u"测试者",
            short_desc=u"这是测试",
            phone_number="+86 1881781111",
            cur_address=u"测试区",
            long_desc=u"long测试"
        )
        work_exp_0 = WorkExperience(
            work_title=u"测试1",
            work_type=u"测试1",
            pos_in_work=u"测试1",
            work_desc=u"测试1",
            owner=admin
        )
        work_exp_1 = WorkExperience(
            work_title=u"测试2",
            work_type=u"测试2",
            pos_in_work=u"测试2",
            work_desc=u"测试2",
            owner=admin
        )
        edu_exp_0 = EducationExperience(
            institution=u"测试3",
            learn_what=u"测试3",
            gpa=4.0,
            owner=admin
        )
        edu_exp_1 = EducationExperience(
            institution=u"测试4",
            learn_what=u"测试4",
            gpa=4.0,
            owner=admin
        )
        skill_0 = Skill(
            skill_name=u"测试5",
            master_degree=5,
            owner=admin
        )
        skill_1 = Skill(
            skill_name=u"测试6",
            master_degree=5,
            owner=admin
        )
        db.session.add_all([admin, work_exp_0, work_exp_1, edu_exp_0, edu_exp_1,
                            skill_0, skill_1])
        db.session.commit()
        response = self.client.get(url_for('user.index'))
        self.assertTrue("测试1" in response.data)
        self.assertTrue("测试2" in response.data)
        self.assertTrue("测试3" in response.data)
        self.assertTrue("测试4" in response.data)
        self.assertTrue("测试5" in response.data)
        self.assertTrue("测试6" in response.data)
        self.assertTrue("5" in response.data)
        self.assertTrue(current_app.config['BLOG_ADMIN_EMAIL'] in response.data)
        self.assertTrue("测试者" in response.data)
        self.assertTrue("这是测试" in response.data)
        self.assertTrue("+86 1881781111" in response.data)
        self.assertTrue("测试区" in response.data)
        self.assertTrue("long测试" in response.data)

    def test_check_in_table(self):
        admin_1 = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username=u"jferroal", password="123456")
        admin_2 = Admin(email="test@test.com", username="tester", password="123456")
        db.session.add_all([admin_1, admin_2])
        db.session.commit()
        result = check_in_table(Admin, email=current_app.config['BLOG_ADMIN_EMAIL'])
        self.assertTrue(result is not None)
        self.assertTrue(result.username == u"jferroal")

    def test_set_profile_before_post(self):
        admin = Admin(
            email=current_app.config['BLOG_ADMIN_EMAIL'],
            username="profile_tester",
            password="123456",
            real_name=u"测试者",
            short_desc=u"这是测试",
            phone_number="+86 1881781111",
            cur_address=u"测试区",
            long_desc=u"long测试"
        )
        work_exp_0 = WorkExperience(
            work_title=u"测试1",
            work_type=u"测试1",
            pos_in_work=u"测试1",
            work_desc=u"测试1",
            owner=admin
        )
        work_exp_1 = WorkExperience(
            work_title=u"测试2",
            work_type=u"测试2",
            pos_in_work=u"测试2",
            work_desc=u"测试2",
            owner=admin
        )
        edu_exp_0 = EducationExperience(
            institution=u"测试3",
            learn_what=u"测试3",
            gpa=4.0,
            owner=admin
        )
        edu_exp_1 = EducationExperience(
            institution=u"测试4",
            learn_what=u"测试4",
            gpa=4.0,
            owner=admin
        )
        skill_0 = Skill(
            skill_name=u"测试5",
            master_degree=5,
            owner=admin
        )
        skill_1 = Skill(
            skill_name=u"测试6",
            master_degree=5,
            owner=admin
        )
        db.session.add_all([admin, work_exp_0, work_exp_1, edu_exp_0, edu_exp_1,
                            skill_0, skill_1])
        db.session.commit()
        self.client.post(url_for('auth.login'), data={
            'email': current_app.config['BLOG_ADMIN_EMAIL'],
            'password': "123456"
        })
        response = self.client.get(url_for('user.edit_profile'))
        self.assertTrue("测试1" in response.data)
        self.assertTrue("测试2" in response.data)
        self.assertTrue("测试3" in response.data)
        self.assertTrue("测试4" in response.data)
        self.assertTrue("测试5" in response.data)
        self.assertTrue("测试6" in response.data)
        self.assertTrue("5" in response.data)
        self.assertTrue("测试者" in response.data)
        self.assertTrue("这是测试" in response.data)
        self.assertTrue("+86 1881781111" in response.data)
        self.assertTrue("测试区" in response.data)
        self.assertTrue("long测试" in response.data)

    def test_check_in_table(self):
        admin_1 = Admin(email=current_app.config['BLOG_ADMIN_EMAIL'], username=u"jferroal", password="123456")
        admin_2 = Admin(email="test@test.com", username="tester", password="123456")
        db.session.add_all([admin_1, admin_2])
        db.session.commit()
        result = check_in_table(Admin, email=current_app.config['BLOG_ADMIN_EMAIL'])
        self.assertTrue(result is not None)
        self.assertTrue(result.username == u"jferroal")

    def edit_profile(self):
        return self.client.post(url_for('user.edit_profile'), data={
            'real_name': "Lin Jeff",
            'short_desc': "I am Jferroal",
            'phone_number': "+86 110",
            'cur_address': "Shanghai",
            'long_desc': "LLLLong",
            'work_1_title': "work1",
            'work_1_type': "t1",
            'work_1_pos': "p1",
            'work_1_st': "2016-02-02",
            'work_1_et': "2017-01-01",
            'work_2_title': "work1",
            'work_2_type': "t2",
            'work_2_pos': "p2",
            'work_2_st': "2016-02-05",
            'work_2_et': "2017-01-01",
            'work_3_title': "work3",
            'work_3_type': "t3",
            'work_3_pos': "p3",
            'work_3_st': "2016-02-07",
            'work_3_et': "2017-01-01",
            'edu_1_ins': "Tongji",
            'edu_1_lw': "IS",
            'edu_1_gpa': "4.0",
            'edu_2_ins': "Tongji",
            'edu_2_lw': "IS",
            'edu_2_gpa': "4.4",
            'edu_1_st':"2015-06-01",
            'edu_1_et':"2015-06-02",
            'edu_2_st':"2015-06-03",
            'edu_2_et':"2015-06-04",
            'skill_1_name': "Python",
            'skill_1_md': '3',
            'skill_2_name': "Python",
            'skill_2_md': '4'
        }, follow_redirects=True)

    def test_edit_profile(self):
        admin = Admin(
            email=current_app.config['BLOG_ADMIN_EMAIL'],
            username="profile_tester",
            password="123456",
            real_name=u"测试者",
            short_desc=u"这是测试",
            phone_number="+86 1881781111",
            cur_address=u"测试区",
            long_desc=u"long测试"
        )
        work_exp_0 = WorkExperience(
            work_title=u"测试1",
            work_type=u"测试1",
            pos_in_work=u"测试1",
            work_desc=u"测试1",
            owner=admin
        )
        work_exp_1 = WorkExperience(
            work_title=u"测试2",
            work_type=u"测试2",
            pos_in_work=u"测试2",
            work_desc=u"测试2",
            owner=admin
        )
        edu_exp_0 = EducationExperience(
            institution=u"测试3",
            learn_what=u"测试3",
            gpa=4.0,
            owner=admin
        )
        edu_exp_1 = EducationExperience(
            institution=u"测试4",
            learn_what=u"测试4",
            gpa=4.0,
            owner=admin
        )
        skill_0 = Skill(
            skill_name=u"测试5",
            master_degree=5,
            owner=admin
        )
        skill_1 = Skill(
            skill_name=u"测试6",
            master_degree=5,
            owner=admin
        )
        db.session.add_all([admin, work_exp_0, work_exp_1, edu_exp_0, edu_exp_1,
                            skill_0, skill_1])
        db.session.commit()
        self.client.post(url_for('auth.login'), data={
            'email': current_app.config['BLOG_ADMIN_EMAIL'],
            'password': "123456"
        })
        response = self.edit_profile()
        self.assertTrue("Lin Jeff" in response.data)
        self.assertTrue("I am Jferroal" in response.data)
        self.assertTrue("+86 110" in response.data)
        self.assertTrue("Shanghai" in response.data)
        self.assertTrue("LLLLong" in response.data)

