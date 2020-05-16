from functools import update_wrapper

from flask import render_template, current_app, g
from flask.globals import _app_ctx_stack, _request_ctx_stack
from flask_mail import Mail, Message
from flask_babel import lazy_gettext

mail = Mail()

try:
    import gevent
except ModuleNotFoundError:
    # On windows gevent can't be installed, fall back to concurrent.futures instead.
    from concurrent.futures import ThreadPoolExecutor

    pool = ThreadPoolExecutor()

    def background_task(f):
        def callback(result):
            exc = result.exception
            if exc:
                current_app.log_exception((type(exc), exc, exc.__traceback__))

        def wrapper(*args, **kwargs):
            future = pool.submit(with_app_context(f), *args, **kwargs)
            future.add_done_callback(with_app_context(callback))
            return future

        return update_wrapper(wrapper, f)
else:
    def background_task(f):
        def callback(result):
            exc = result.exception
            current_app.log_exception((type(exc), exc, exc.__traceback__))

        def wrapper(*args, **kwargs):
            future = gevent.spawn(with_app_context(f), *args, **kwargs)

            future.link_exception(with_app_context(callback))
            return future

        return update_wrapper(wrapper, f)


def with_app_context(f):
    ctx = _app_ctx_stack.top
    req_ctx = _request_ctx_stack.top.copy()

    def wrapper(*args, **kwargs):
        with ctx:
            with req_ctx:
                return f(*args, **kwargs)
    return update_wrapper(wrapper, f)


@background_task
def notify_reply(reply_to, comment):
    if not reply_to['author'].get('email'):
        return
    recipients = [reply_to['author']['email']]
    subject = (
        "{}|".format(g.site['name'])
        + lazy_gettext("New reply on '%(title)s'", title=comment['post']['title'])
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
