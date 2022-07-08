import imp
from turtle import title
from flask import url_for
from bluelog.models import Post,Category,Link,Comment
from bluelog.extensions import db

from tests.base import BaseTestCase

class AdminTestCase(BaseTestCase):

    def setUp(self):
        super(AdminTestCase,self).setUp()
        self.login()

        category = Category(name='Default')
        post = Post(title='Hello',category=category,body='Blah....')