# coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
# from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import DataRequired

class ToolForm(Form):
    # TODO: label and placeholder use chinese maybe a good idea
    name = StringField("Tool's name", validators=[
        DataRequired()], render_kw={'placeholder':"Tool's name"})
    desc = TextAreaField("Tool's description", validators=[
        DataRequired()], render_kw={'placeholder':"Tool's description"})
    address = StringField("Tool's url", render_kw={
        'placeholder': "Maybe the project address in github"
    })
    submit = SubmitField("Add Tool")