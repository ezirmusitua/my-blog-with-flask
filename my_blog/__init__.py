#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
# from flask.ext.pagedown import PageDown
from flask.ext.moment import Moment
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
# pagedown  = PageDown()
moment    = Moment()


def create_app(config_name):
    """
    :param config_name: specific config name
    :return: an app object with specific config
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    # pagedown.init_app(app)
    moment.init_app(app)

    from .main import main as main_blugprint
    app.register_blueprint(main_blugprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")
    from .post import post as post_blueprint
    app.register_blueprint(post_blueprint, url_prefix="/post")
    from .tool import tool as tool_blueprint
    app.register_blueprint(tool_blueprint, url_prefix="/tool")

    return app
