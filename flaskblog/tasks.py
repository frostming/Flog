from functools import update_wrapper

import gevent
from flask import copy_current_request_context, render_template, current_app
from flask_mail import Mail, Message
from flask_babel import lazy_gettext

mail = Mail()


def background_task(f):

    def wrapper(*args, **kwargs):
        future = gevent.spawn(copy_current_request_context(f), *args, **kwargs)
        return future
    return update_wrapper(wrapper, f)


@background_task
def notify_reply(reply_to, comment):
    if not reply_to['author'].get('email'):
        return
    recipients = [reply_to['author']['email']]
    subject = lazy_gettext("You got a new reply for your comment on '%s'") % comment['post']['title']
    html_content = render_template('mail/new_reply.html', reply_to=reply_to, comment=comment)
    msg = Message(subject=subject, recipients=recipients, html=html_content)
    mail.send(msg)
    current_app.logger.info('An email is successfully sent to %s', recipients)


# @background_task
def notify_comment(author, comment):
    current_app.logger.info('%s %s', author, comment)
    if not author.get('email'):
        return
    recipients = [author['email']]
    subject = lazy_gettext("Your post '%(title)s' has got a new comment", title=comment['post']['title'])
    html_content = render_template('mail/new_comment.html', author=author, comment=comment)
    msg = Message(subject=subject, recipients=recipients, html=html_content)
    mail.send(msg)
    current_app.logger.info('An email is successfully sent to %s', recipients)
