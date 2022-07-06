#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import  SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_wtf  import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manage = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()

@login_manage.user_loader
def load_user(user_id):
	from bluelog.models import Admin
	user = Admin.query.get(int(user_id))
	return user

login_manage.login_view  = 'auth.login'
login_manage.login_manage = 'You custom message'
login_manage.login_manage_category = 'warning'