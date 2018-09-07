from flask_login import login_user, login_required, logout_user
from flask import redirect, url_for, render_template, flash, request, current_app
from flask_babel import lazy_gettext

from .forms import LoginForm, PostForm
from ..models import User, db, Post, Category


def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = login_form.get_user()
        if not user:
            user = User(
                username=login_form.username.data,
                password=login_form.password.data
            )
            db.session.add(user)
            db.session.commit()
        login_user(user, remember=login_form.remember.data)
        flash(lazy_gettext('You are logged in successfully!'), 'success')
        return redirect(url_for('.posts'))
    return render_template('admin/login.html', form=login_form)


@login_required
def logout():
    logout_user()
    return redirect(url_for('.posts'))


@login_required
def posts():
    paginate = Post.query.join(Post.category)\
                         .filter(Category.text != 'About')\
                         .union(Post.query.filter(Post.category_id.is_(None)))\
                         .order_by(Post.date.desc())\
                         .paginate(per_page=50)
    return render_template('admin/posts.html', paginate=paginate)


@login_required
def settings():
    return render_template('admin/settings.html')


@login_required
def edit_post():
    post = Post.query.get_or_404(request.args.get('id'))
    if request.method == 'GET':
        form = PostForm(data=post.to_dict())
    else:
        form = PostForm()
    if form.validate_on_submit():
        data = form.data.copy()
        data.pop('csrf_token')
        for k, v in data.items():
            setattr(post, k, v)
        db.session.commit()
        return redirect(url_for('.posts'))
    return render_template('admin/writing.html', form=form)


@login_required
def delete_post():
    post = Post.query.get_or_404(request.args.get('id'))
    current_app.logger.info(request.url)
    db.session.delete(post)
    db.session.commit()
    flash(lazy_gettext('Delete post successfully.'), 'success')
    return redirect(url_for('.posts'))


@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        data = form.data.copy()
        data.pop('csrf_token')
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.posts'))
    return render_template('admin/writing.html', form=form)


def init_blueprint(bp):
    bp.add_url_rule('/login', 'login', login, methods=('POST', 'GET'))
    bp.add_url_rule('/logout', 'logout', logout)
    bp.add_url_rule('/', 'posts', posts)
    bp.add_url_rule('/settings', 'settings', settings)
    bp.add_url_rule('/edit', 'edit', edit_post, methods=('GET', 'POST'))
    bp.add_url_rule('/delete', 'delete', delete_post, methods=('POST', 'DELETE'))
    bp.add_url_rule('/new', 'new', new_post, methods=('GET', 'POST'))
