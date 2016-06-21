# coding=utf-8

from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
# Should i use this
# from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import DataRequired

class PostForm(Form):
    title = StringField('Post Title', validators=[DataRequired()])
    body = TextAreaField('Post Body(MarkDown)', id="post-body",
                         validators=[DataRequired()],
                         render_kw={'placeholder': "Write article using markdown"})
    tags = StringField('Tags For Post', validators=[DataRequired()], render_kw={
        'placeholder': "Tags for post, split by comma"
    })
    submit = SubmitField('Submit', id="post-submit")