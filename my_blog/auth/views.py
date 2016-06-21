#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm
from ..models import Admin

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Admin.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            flash("Login successful.")
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid username or password")
    return render_template('auth/login.html', form=login_form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logout.')
    return redirect(url_for('main.index'))
