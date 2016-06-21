#!/usr/bin/env python
# -*- coding:utf-8 -*- 
from flask.ext.wtf import Form
# Should i use this?
# from flask.ext.pagedown.fields import PageDownField
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Length,\
    Email

class CommentForm(Form):
    body   = TextAreaField('Your comment', id="comment-body",
                           validators=[DataRequired()])
    email  = StringField('Email', id="comment-email",
                         validators=[DataRequired(), Length(1, 64),Email()])
    submit = SubmitField('Submit', id="comment-submit")
