# coding=utf-8

import bleach
from datetime import datetime
from flask import render_template, redirect, url_for, \
    flash, request
from flask.ext.login import current_user, login_required
from ..main.views import get_github_address
from . import post
from .. import db
from ..models import Post, Tag
from forms import PostForm


def split_tags(tags):
    """
    split tags by comma to get tag
    :param tags: input tags-string
    :return: tag list
    """
    tags = bleach.clean(tags)
    if u'，' in tags:
        tags.replace(u'，', ',')
    return tags.split(',')

def add_tag_to_article(article, tags):
    """
    add tags to post
    :param article: article that will be add tags
    :param tags: a string that contain tags
    :return: None
    """
    for tag_name in split_tags(tags):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag and article not in tag.posts:
            tag.count += 1
        elif tag is None:
            tag = Tag(name=tag_name, count=1)
        tag.posts.append(article)
        article.tags.append(tag)


@post.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post_title = post_form.title.data
        post = Post.query.filter_by(title=post_title).first()
        if post:
            flash("Have the same title post,please try another title")
            return render_template('post/add_post', post_form=post_form)
        post_body = post_form.body.data
        post      = Post(
            title=post_title,
            body=post_body,
            author=current_user
        )
        add_tag_to_article(post, post_form.tags.data)
        db.session.add(post)
        db.session.commit()
        flash("Add post successful!")
        return redirect(url_for('main.post', id=post.id))
    tag_list = Tag.query.order_by(Tag.count.desc()).all()
    github_address = get_github_address()
    return render_template("post/add_post", post_form=post_form,
                           tag_list=tag_list,
                           github_address=github_address)


def set_article_before_post(article):
    """
    set article content in form
    :param article: article that need to edit
    :return: post_form with pre-set data
    """
    post_form = PostForm()
    post_form.title.data = article.title
    post_form.body.data  = article.body
    tmp = []
    [tmp.append(tag.name) for tag in article.tags]
    post_form.tags.data = ','.join(tmp)
    return post_form


@post.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    article = Post.query.get_or_404(post_id)
    if request.method == 'GET':
        post_form = set_article_before_post(article)
    else:
        post_form = PostForm()
    if post_form.validate_on_submit():
        article.title = post_form.title.data
        article.body  = post_form.body.data
        article.timestamp = datetime.utcnow()
        add_tag_to_article(article, post_form.tags.data)
        db.session.add(article)
        db.session.commit()
        flash("Post Modified Done")
        return redirect(url_for('main.post' ,id=article.id))
    tag_list = Tag.query.order_by(Tag.count.desc()).all()
    github_address = get_github_address()
    return render_template('post/add_post', post_form=post_form,
                           tag_list=tag_list,
                           github_address=github_address)
