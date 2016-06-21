#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from datetime import datetime
from flask import current_app, render_template, request, redirect, \
    url_for, flash
from flask.ext.login import current_user, login_required
from .. import db
from . import user
from .forms import ProfileForm
from ..main.views import get_github_address
from ..models import Admin, WorkExperience, EducationExperience, Skill, \
    Tag


@user.route('/', methods=['GET', 'POST'])
def index():
    """
    user route for show profile
    :return:
    """
    admin = Admin.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']).first()
    work_experience = admin.work_experience.order_by(WorkExperience.start_time.desc())
    edu_experience = admin.edu_experience.order_by(EducationExperience.start_time.asc())
    skills = admin.skills.order_by(Skill.master_degree.asc())
    tag_list = Tag.query.order_by(Tag.count.desc()).all()
    github_address=get_github_address()
    return render_template('user/show_profile.html',
                           admin=admin,
                           work_experience=work_experience,
                           edu_experience=edu_experience,
                           skills=skills, tag_list=tag_list,
                           github_address=github_address)


# auxiliary for edit profile
def check_in_table(table_name, **kwargs):
    """
    check is element in table
    :param table_name: table name in database
    :param kwargs: attribute use in filter_by
    :return: elem if exist else None
    """
    tmp = table_name.query.filter_by(**kwargs).first()
    return tmp if tmp else None


def set_profile_before_post(admin):
    """
    set the data already in table to form before post
    :param admin: admin object from Admin table
    :return: a ProfileForm with pre-set data
    """
    profile_form = ProfileForm()
    # Admin msg
    profile_form.username.data = admin.username
    profile_form.real_name.data = admin.real_name
    profile_form.short_desc.data = admin.short_desc
    profile_form.phone_number.data = admin.phone_number
    profile_form.cur_address.data = admin.cur_address
    profile_form.long_desc.data = admin.long_desc
    # Work experience
    work_exps = admin.work_experience.order_by(WorkExperience.start_time.desc()).all()
    work_exps_len = len(work_exps)
    for i in range(1, work_exps_len + 1):
        if i > 3:
            break
        getattr(profile_form, "work_%d_title" % i).data = work_exps[i - 1].work_title
        getattr(profile_form, "work_%d_type" % i).data = work_exps[i - 1].work_type
        getattr(profile_form, "work_%d_pos" % i).data = work_exps[i - 1].pos_in_work
        getattr(profile_form, "work_%d_desc" % i).data = work_exps[i - 1].work_desc
        getattr(profile_form, "work_%d_st" % i).data = work_exps[i - 1].start_time.strftime("%Y-%m-%d")
        getattr(profile_form, "work_%d_et" % i).data = work_exps[i - 1].end_time.strftime("%Y-%m-%d")
    # Education experience
    edu_exps = admin.edu_experience.order_by(EducationExperience.start_time.desc()).all()
    edu_exps_len = len(edu_exps)
    for i in range(1, edu_exps_len + 1):
        if i > 3:
            break
        getattr(profile_form, "edu_%d_ins" % i).data = edu_exps[i - 1].institution
        getattr(profile_form, "edu_%d_lw" % i).data = edu_exps[i - 1].learn_what
        getattr(profile_form, "edu_%d_gpa" % i).data = edu_exps[i - 1].gpa
        getattr(profile_form, "edu_%d_st" % i).data = edu_exps[i - 1].start_time.strftime("%Y-%m-%d")
        getattr(profile_form, "edu_%d_et" % i).data = edu_exps[i - 1].end_time.strftime("%Y-%m-%d")
    # Skills
    skills = admin.skills.order_by(Skill.add_time.desc()).all()
    skills_len = len(skills)
    for i in range(1, skills_len + 1):
        if i > 2:
            break
        getattr(profile_form, "skill_%d_name" % i).data = skills[i - 1].skill_name
        getattr(profile_form, "skill_%d_md" % i).data = str(skills[i - 1].master_degree)
    return profile_form


def change_or_add_with_form_data(email, form):
    """
    change data already in table or add new to table
    :param email: current user's email
    :param form: post form
    :return: None
    """
    admin = check_in_table(Admin, email=email)
    if admin:
        admin.username     = form.username.data
        admin.real_name    = form.real_name.data
        admin.short_desc   = form.short_desc.data
        admin.phone_number = form.phone_number.data
        admin.github_addr  = form.github_addr.data
        admin.cur_address  = form.cur_address.data
        admin.long_desc    = form.long_desc.data
    # new item list
    new_items = []
    # Work experience
    for i in range(1, 4):
        work_exp = WorkExperience.query.filter_by(
            work_title=getattr(form, "work_%d_title" % i).data
        ).first()
        if work_exp:
            work_exp.work_type   = getattr(form, "work_%d_type" % i).data
            work_exp.pos_in_work = getattr(form, "work_%d_pos" % i).data
            work_exp.work_desc   = getattr(form, "work_%d_desc" % i).data
            work_exp.start_time  = datetime.strptime(getattr(form, "work_%d_st" % i).data or "1999-01-01", "%Y-%m-%d")
            work_exp.end_time    = datetime.strptime(getattr(form, "work_%d_et" % i).data or "1999-01-01", "%Y-%m-%d")
        else:
            new_items.append(WorkExperience(
                work_title=getattr(form, "work_%d_title" % i).data,
                work_type=getattr(form, "work_%d_type" % i).data,
                pos_in_work=getattr(form, "work_%d_pos" % i).data,
                work_desc=getattr(form, "work_%d_desc" % i).data,
                start_time=datetime.strptime(getattr(form, "work_%d_st" % i).data or "1999-01-01", "%Y-%m-%d"),
                end_time=datetime.strptime(getattr(form, "work_%d_et" % i).data or "1999-01-01", "%Y-%m-%d"),
                owner=admin))
    # Education experience
    for i in range(1, 4):
        edu_exp = EducationExperience.query.filter_by(
            institution=getattr(form, "edu_%d_ins" % i).data
        ).first()
        if edu_exp:
            edu_exp.learn_what = getattr(form, "edu_%d_lw" % i).data
            edu_exp.gpa        = getattr(form, "edu_%d_gpa" % i).data or 1.0
            edu_exp.start_time = datetime.strptime(getattr(form, "edu_%d_st" % i).data or "1999-01-01", "%Y-%m-%d")
            edu_exp.end_time   = datetime.strptime(getattr(form, "edu_%d_et" % i).data or "1999-01-01", "%Y-%m-%d")
        else:
            new_items.append(EducationExperience(
                institution=getattr(form, "edu_%d_ins" % i).data,
                learn_what=getattr(form, "edu_%d_lw" % i).data,
                gpa=getattr(form, "edu_%d_gpa" % i).data or 1.0,
                start_time=datetime.strptime(getattr(form, "edu_%d_st" % i).data or "1999-01-01",
                                             "%Y-%m-%d"),
                end_time=datetime.strptime(getattr(form, "edu_%d_et" % i).data or "1999-01-01",
                                           "%Y-%m-%d"),
                owner=admin
            ))
    # Skills
    for i in range(1, 3):
        skill = Skill.query.filter_by(
            skill_name=getattr(form, "skill_%d_name" % i).data
        ).first()
        if skill:
            skill.master_degree = getattr(form, "skill_%d_md" % i).data or 1
        else:
            new_items.append(Skill(
                skill_name=getattr(form, "skill_%d_name" % i).data,
                master_degree=getattr(form, "skill_%d_md" % i).data or 1,
                owner=admin))
    db.session.add_all([admin] + new_items)
    db.session.commit()


@user.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'GET':
        profile_form = set_profile_before_post(current_user)
    else:
        profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        change_or_add_with_form_data(current_user.email, profile_form)
        flash("Profile Modified")
        return redirect(url_for('user.index'))
    tag_list = Tag.query.order_by(Tag.count.desc()).all()
    github_address=get_github_address()
    return render_template('user/edit_profile.html', profile_form=profile_form,
                           tag_list=tag_list,
                           github_address=github_address)
