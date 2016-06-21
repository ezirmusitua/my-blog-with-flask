#!usr/bin/env python
# coding=utf-8

import datetime
from flask.ext.wtf import Form
# Should i use this
# from flask.ext.pagedown.fields import PageDownField
from wtforms import TextAreaField, StringField, SelectField, SubmitField


class EmptyWorkExperience(object):
    """If there are no data in WorkExperience table, use this as default"""
    work_title = "Add your work title here"
    work_type  = "Add your work type here"
    pos_in_work = "Add your position in work"
    work_desc   = "Add your work's description"
    start_time  = unicode(datetime.date(2000, 1, 1))
    end_time    = unicode(datetime.date(2099, 1, 1))


class EmptyEducationExperience(object):
    """If there are no data in EducationExperience table, use this as default"""
    institution = "Where you got education"
    learn_what  = "What you learn"
    work_type   = "Add your work type here"
    gpa         = "your grade point average"
    start_time  = unicode(datetime.date(2000, 1, 1))
    end_time    = unicode(datetime.date(2099, 1, 1))


class EmptySkill(object):
    """If there are no data in Skill table, use this as default"""
    skill_name = "The Name of Skill"
    master_degree = "master degree"


class EmptyAdmin():
    """If there are no data in Admin table, use this as default"""
    username        = "Your username"
    real_name       = "Your real name"
    short_desc      = "A short description for you"
    phone_number    = "Phone number of you"
    github_address  = "Github address of you"
    cur_address     = "Current address of you"
    long_desc       = "A long description of you"
    work_experience = [EmptyWorkExperience() for i in range(3)]
    edu_experience  = [EmptyEducationExperience() for i in range(3)]
    skills          = [EmptySkill() for i in range(5)]


class ProfileForm(Form):

    admin        = EmptyAdmin()
    username     = StringField('Username', id="profile-username",
                               render_kw={'placeholder':admin.username})
    real_name    = StringField('Real name of you', id="profile-realname",
                               render_kw={'placeholder':admin.real_name})
    short_desc   = StringField('Short description about you', id="profile-short-desc",
                               render_kw={'placeholder':admin.short_desc})
    phone_number = StringField('Phone number of you', id="phone-number",
                               render_kw={'placeholder':admin.phone_number})
    github_addr  = StringField('Github address of you' ,id="github-address",
                               render_kw={'placeholder':admin.github_address})
    cur_address  = StringField('Current address of you', id="cur_address",
                               render_kw={'placeholder':admin.cur_address})
    long_desc    = TextAreaField('long description about you', id="long-desc",
                                 render_kw={'placeholder':admin.long_desc})

    # Work experience
    work_1_title = StringField('Title', render_kw={'placeholder':admin.work_experience[0].work_title})
    work_1_type  = StringField('Type', render_kw={'placeholder':admin.work_experience[0].work_type})
    work_1_pos   = StringField('Position', render_kw={'placeholder':admin.work_experience[0].pos_in_work})
    work_1_desc  = TextAreaField('Description', render_kw={'placeholder':admin.work_experience[0].work_desc})
    work_1_st    = StringField('Start time', render_kw={'placeholder':admin.work_experience[0].start_time})
    work_1_et    = StringField('End time', render_kw={'placeholder':admin.work_experience[0].end_time})

    work_2_title = StringField('Title', render_kw={'placeholder':admin.work_experience[1].work_title})
    work_2_type  = StringField('Type', render_kw={'placeholder':admin.work_experience[1].work_type})
    work_2_pos   = StringField('Position', render_kw={'placeholder':admin.work_experience[1].pos_in_work})
    work_2_desc  = TextAreaField('Description', render_kw={'placeholder':admin.work_experience[1].work_desc})
    work_2_st    = StringField('Start time', render_kw={'placeholder':admin.work_experience[1].start_time})
    work_2_et    = StringField('End time', render_kw={'placeholder':admin.work_experience[1].end_time})

    work_3_title = StringField('Title', render_kw={'placeholder':admin.work_experience[2].work_title})
    work_3_type  = StringField('Type', render_kw={'placeholder':admin.work_experience[2].work_type})
    work_3_pos   = StringField('Position', render_kw={'placeholder':admin.work_experience[2].pos_in_work})
    work_3_desc  = TextAreaField('Description', render_kw={'placeholder':admin.work_experience[2].work_desc})
    work_3_st    = StringField('Start time', render_kw={'placeholder':admin.work_experience[2].start_time})
    work_3_et    = StringField('End time', render_kw={'placeholder':admin.work_experience[2].end_time})

    # Education experience
    edu_1_ins = StringField('Institution', render_kw={'placeholder':admin.edu_experience[0].institution})
    edu_1_lw  = StringField('Learn what', render_kw={'placeholder':admin.edu_experience[0].learn_what})
    edu_1_gpa = StringField('Grade Point Average', render_kw={'placeholder':admin.edu_experience[0].gpa})
    edu_1_st  = StringField('Start Time', render_kw={'placeholder':admin.edu_experience[0].start_time})
    edu_1_et  = StringField('End Time', render_kw={'placeholder':admin.edu_experience[0].end_time})

    edu_2_ins = StringField('Institution', render_kw={'placeholder':admin.edu_experience[1].institution})
    edu_2_lw  = StringField('Learn what', render_kw={'placeholder':admin.edu_experience[1].learn_what})
    edu_2_gpa = StringField('Grade Point Average', render_kw={'placeholder':admin.edu_experience[1].gpa})
    edu_2_st  = StringField('Start Time', render_kw={'placeholder':admin.edu_experience[1].start_time})
    edu_2_et  = StringField('End Time', render_kw={'placeholder':admin.edu_experience[1].end_time})

    edu_3_ins = StringField('Institution', render_kw={'placeholder':admin.edu_experience[2].institution})
    edu_3_lw  = StringField('Learn what', render_kw={'placeholder':admin.edu_experience[2].learn_what})
    edu_3_gpa = StringField('Grade Point Average', render_kw={'placeholder':admin.edu_experience[2].gpa})
    edu_3_st  = StringField('Start Time', render_kw={'placeholder':admin.edu_experience[2].start_time})
    edu_3_et  = StringField('End Time', render_kw={'placeholder':admin.edu_experience[2].end_time})

    # Skills
    skill_1_name = StringField('Skill Name', render_kw={'placeholder':admin.skills[0].skill_name})
    skill_1_md   = SelectField('Master degree', choices=[(unicode(num), str(num)) for num in range(1, 6)])

    skill_2_name = StringField('Skill Name', render_kw={'placeholder':admin.skills[2].skill_name})
    skill_2_md   = SelectField('Master degree', choices=[(unicode(num), str(num)) for num in range(1, 6)])

    submit = SubmitField('Done', id="profile-submit")


