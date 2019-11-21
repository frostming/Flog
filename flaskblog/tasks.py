from functools import update_wrapper

import gevent
from flask import copy_current_request_context, render_template, current_app, g
from flask_mail import Mail, Message
from flask_babel import lazy_gettext

mail = Mail()


def background_task(f):
    def wrapper(*args, **kwargs):
        future = gevent.spawn(copy_current_request_context(f), *args, **kwargs)

        def callback(result):
            exc = result.exception
            current_app.log_exception((type(exc), exc, exc.__traceback__))

        future.link_exception(copy_current_request_context(callback))
        return future

    return update_wrapper(wrapper, f)


@background_task
def notify_reply(reply_to, comment):
    if not reply_to['author'].get('email'):
        return
    recipients = [reply_to['author']['email']]
    subject = (
        "{}|".format(g.site['name'])
        + lazy_gettext("New reply on '%s'") % comment['post']['title']
    )
    html_content = render_template(
        'mail/new_reply.html', reply_to=reply_to, comment=comment
    )
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html_content,
        sender=('Flog Admin', current_app.config['MAIL_DEFAULT_SENDER']),
    )
    mail.send(msg)
    current_app.logger.info('An email is successfully sent to %s', recipients)


@background_task
def notify_comment(author, comment):
    if not author.get('email'):
        return
    recipients = [author['email']]
    subject = "{}|".format(g.site['name']) + lazy_gettext(
        "New comment on '%(title)s'", title=comment['post']['title']
    )
    html_content = render_template(
        'mail/new_comment.html', comment=comment
    )
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html_content,
        sender=('Flog Admin', current_app.config['MAIL_DEFAULT_SENDER']),
    )
    mail.send(msg)
    current_app.logger.info('An email is successfully sent to %s', recipients)
