from flask import url_for, current_app
from flask_mail import Message
from threading import Thread
from bluelog.extensions import mail


def _send_async_mail(app, message):
    # 想使用app必须有上下文才可以
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    # _get_current_object获取真实的进程，如果新增thread进程需要获取真实的进程
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + "#comments"

    send_mail(subject='New comment', to=current_app.config['BLUELOG_EMAIL'],
              html='<p>New comment in post <i>%s</i>,click the link below to check:</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style='
                   'color:  # 868e96>Do not reply the email.</small></p>'
                   % (post.title, post_url, post_url)
              )

def send_new_reply_email(comment):
	post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
	send_mail(subject='New reply', to=comment.email,
			  html='<p>New reply for the comment you left in post <i>%s<i>,click the link below to check:</p>'
				   '<p><a href= %s'
				   '>%s</a></p>'
				   '<p><small style='
				   'color:  # 868e96>Do not reply the email.</small></p>'
				   % (comment.post_title, post_url, post_url)
			  )
