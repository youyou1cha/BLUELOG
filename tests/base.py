import imp
from tkinter.messagebox import NO
import unittest

from flask import url_for
from bluelog import create_app
from bluelog.extensions import db
from bluelog.models import Admin

class BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = Admin(name='Li',username='ww',about='I an test',blog_title='Testlog',blog_sub_title='a test')
        user.set_password('1234')
        db.session.add(user)
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.pop()

    def login(self,username=None,password=None):
        if username is None and password is None:
            username = 'gg'
            password = '123'
        return self.client.post(url_for('auth.login',data=dict(username=username,password=password),follow_redirects=True))
# follow_redirects是重定向
    def logout(self):
        return self.client.get(url_for('auth.logout',follow_redirects=True))