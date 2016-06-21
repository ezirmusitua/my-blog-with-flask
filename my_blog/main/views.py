#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for,\
    flash, request, current_app, session
from . import main
from .. import db
from ..models import Guest, Admin, Post, Comment, Tag
from forms import CommentForm


def get_github_address():
    """
    :return: admin's github address
    """
    git_addr = "//" + Admin.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']). \
        first().github_address or "//github.com"
    return git_addr


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    github_address = get_github_address()
    tag_list       = Tag.query.order_by(Tag.count.desc()).all()
    return render_template('index.html', posts=posts,
                           pagination=pagination, github_address=github_address,
                           tag_list=tag_list)


@main.route('/posts_with_tag/<string:tag_name>', methods=['GET'])
def show_posts_under_tag(tag_name):
    """
    display posts which have tha tag in list-way
    :param tag_name: the tag we may add/delete
    :return: display posts filtered by tag in session
    """
    tag = Tag.query.filter_by(name=tag_name).first()
    github_address = get_github_address()
    tag_list     = Tag.query.order_by(Tag.count.desc()).all()
    # TODO: change blcok show to list show or add pagination
    return render_template('filter_by_tag.html', posts=tag.posts,
                           github_address=github_address,
                           tag_list=tag_list)


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        guest = Guest.query.filter_by(email=comment_form.email.data).first()
        if guest is None:
            guest = Guest(email=comment_form.email.data)
            db.session.add(guest)
        comment = Comment(body=comment_form.body.data, post=post,
                          author=guest)
        db.session.add(comment)
        db.session.commit()
        flash("Comment Published")
        return redirect(url_for('.post', id=post.id))
    comments = post.comments.order_by(Comment.timestamp.asc())
    github_address = get_github_address()
    tag_list     = Tag.query.order_by(Tag.count.desc()).all()
    return render_template('post.html', post=post, form=comment_form,
                           comments=comments, github_address=github_address,
                           tag_list=tag_list)
