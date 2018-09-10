from flask_login import login_user, login_required, logout_user
from flask import redirect, url_for, render_template, flash, request, current_app, g
from flask_babel import lazy_gettext

from .forms import LoginForm, PostForm, SettingsForm, ChangePasswordForm
from ..models import User, db, Post, Category, generate_password_hash


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
    is_draft = request.endpoint.endswith('drafts')
    paginate = Post.query.join(Post.category)\
                         .filter(Category.text != 'About')\
                         .union(Post.query.filter(Post.category_id.is_(None)))\
                         .filter(Post.is_draft == is_draft)\
                         .order_by(Post.date.desc())\
                         .paginate(per_page=50)
    draft_count = Post.query.filter_by(is_draft=True).count()
    return render_template(
        'admin/posts.html', paginate=paginate, draft_count=draft_count)


@login_required
def settings():
    if request.method == 'GET':
        form = SettingsForm.from_local()
    else:
        form = SettingsForm()
    if form.validate_on_submit():
        data = form.data.copy()
        data.pop('csrf_token', None)
        g.site.update(data)
        User.get_one().write_settings(data)
        flash(lazy_gettext('Update settings successfully.'), 'success')
        return redirect(url_for('.settings'))
    pform = ChangePasswordForm()
    return render_template('admin/settings.html', form=form, pform=pform)


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
        flash(lazy_gettext('Update post successfully.'), 'success')
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
        if post.is_draft:
            flash(lazy_gettext(
                "The draft '%(title)s' is saved!", title=post.title
            ), 'success')
        else:
            flash(lazy_gettext(
                "The article '%(title)s' is posted successfully!", title=post.title
            ), 'success')
        return redirect(url_for('.posts'))
    return render_template('admin/writing.html', form=form)


@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        admin = User.get_one()
        admin.password = generate_password_hash(form.new.data)
        db.session.commit()
        flash(lazy_gettext('The password is updated!'), 'success')
        return redirect(url_for('.settings'))


def init_blueprint(bp):
    bp.add_url_rule('/login', 'login', login, methods=('POST', 'GET'))
    bp.add_url_rule('/logout', 'logout', logout)
    bp.add_url_rule('/', 'posts', posts)
    bp.add_url_rule('/drafts', 'drafts', posts)
    bp.add_url_rule('/settings', 'settings', settings, methods=('GET', 'POST'))
    bp.add_url_rule('/edit', 'edit', edit_post, methods=('GET', 'POST'))
    bp.add_url_rule('/delete', 'delete', delete_post, methods=('POST', 'DELETE'))
    bp.add_url_rule('/new', 'new', new_post, methods=('GET', 'POST'))
    bp.add_url_rule('/password', 'password', change_password, methods=('POST',))
