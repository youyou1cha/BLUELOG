from ast import Try
import imp
from turtle import title
from urllib import response
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
        comment = Comment(body='A comment',post=post,from_admin=True)
        link = Link(name='Github',url='https://github.com/wwa')
        db.session.add([category,post,comment,link])
        db.session.commit()

    def test_new_post(self):
        response = self.client.get(url_for('admin.new_post'))
        # 感觉是response.get_data 数据
        data = response.get_data(as_text=True)
        self.assertIn('New Post',data)

        response = self.client.post(url_for('admin.new_post'),data=dict(
            title='Something',
            category=1,
            body='Hello,world.'
        ),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post created',data)
        self.assertIn('Something',data)
        self.assertIn('Hello, world',data)
    
    def test_edit_post(self):
        response = self.client.get(url_for('admin.edit_post',post_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Edit Post',data)
        self.assertIn('Hello',data)
        self.assertIn('Blah..',data)

        response = self.client.get(url_for('admin.edit_post',post_id=1),data=dict(
            title='Something Edited',
            category=1,
            body='New post body.'
        ),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post updated.',data)
        self.assertIn('New post body.',data)
        self.assertIn('Blah...',data)
    
    def test_delete_post(self):
        response = self.client.get(url_for('admin.delete_post',post_id=1),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post deleted',data)
        self.assertIn('405 Method Not Allowed',data)

        response = self.client.post(url_for('admin.delete_post',post_id=1),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Post deleted',data)

    def test_delete_comment(self):
        response = self.client.get(url_for('admin.delete_comment',comment_id=1),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Comment deleted.',data)
        self.assertIn('405 Method Not Allowed.',data)
        
        response = self.client.post(url_for('admin.delete_comment',comment_id=1),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Comment deleted.',data)
    
    def test_enable_comment(self):
        post = Post.query.get(1)
        post.can_comment = False
        db.session.commit()
# follow_redirects 追踪重定向
        response = self.client.post(url_for('admin.set_comment',post_id=1),follow_redirects=True)
        data =response.get_data(as_text=True)
        self.assertIn('Comment enabled.',data)

        response = self.client.post(url_for('blog.show_post',post_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('<div id="comment-form">',data)

    def test_disable_comment(self):
        response = self.client.post(url_for('admin.set_coment',post_id=1),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Comment disabled.',data)

        response = self.client.post(url_for('blog.show_post',post_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('<div id="comment-form">',data)

    def test_approve_comment(self):
        self.logout()
        response = self.client.post(url_for('blog.show_post',post_id=1),data=dict(
            author='Guest',
            email='a@b.com',
            site='http://wwa.com',
            body='I am a guest comment',
            post=Post.query.get(1),
        ),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Thanks,your comment will be published after reviewed.',data)
        self.assertNotIn('I am a guest comment.',data)

        self.login()
        response = self.client.post(url_for('admin.approve_comment',comment_id=2),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Comment published.',data)

    def test_new_category(self):
        response = self.client.get(url_for('admin.new_category'))
        data = response.get_data(as_text=True)
        self.assertIn('New Category',data)

        response = self.client.post(url_for('admin.new_category',data=dict(name='Tech'),follow_redirects=True))
        data = response.get_data(as_text=True)
        self.assertIn('Category created.',data)
        self.assertIn('Tech',data)

        response = self.client.post(url_for('admin.new_category'),data=dict(name='Tech'),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Name already in use.',data)

        category = Category.query.get(1)
        post = Post(title='Post Title',category=category)
        db.session.add(post)
        db.session.commit()
        response = self.client.get(url_for('blog.show_category',category_id=1))
        data = response.get_data(as_text=True)
        self.assertIn('Post Title',data)
    
    def test_edit_category(self):
        response = self.client.post(url_for('admin.edit_category',category_id=1),data=dict(
            name='Default edited'
        ),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Category updated.',data)
        self.assertIn('Default',data)
        self.assertNotIn('Default edited',data)
        self.assertIn('You can not edit the default category',data)

        response = self.client.post(url_for('admin.new_category'),data=dict(name='Tech'),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Category created.',data)
        self.assertIn('Tech',data)

        response = self.client.get(url_for('admin.edit_category',category_id=2))
        data = response.get_data(as_text=True)
        self.assertIn('Edit Category',data)
        self.assertIn('Tech',data)

        