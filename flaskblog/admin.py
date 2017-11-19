from flask import redirect, request, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import (QuerySelectField,
                                             QuerySelectMultipleField)
from flask_admin.contrib.sqla.form import AdminModelConverter
from flask_admin.model.fields import AjaxSelectField, AjaxSelectMultipleField
from flask_admin.helpers import validate_form_on_submit
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from wtforms import Form, PasswordField, SelectField, StringField, validators

from . import db
from .models import Category, Post, Tag, User


class AutoAddSelectField(QuerySelectField):
    def __init__(self, model_factory, *args, **kwargs):
        super(AutoAddSelectField, self).__init__(*args, **kwargs)
        self.model_factory = model_factory

    def _get_data(self):
        if self._formdata is not None:
            for pk, obj in self._get_object_list():
                if pk == self._formdata:
                    self._set_data(obj)
                    break
            else:
                obj = self.model_factory(self._formdata)
                self._set_data(obj)
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def pre_validate(self, form):
        pass


class AutoAddMultiSelectField(QuerySelectMultipleField):
    def __init__(self, model_factory, *args, **kwargs):
        super(AutoAddMultiSelectField, self).__init__(*args, **kwargs)
        self.model_factory = model_factory

    def _get_data(self):
        formdata = self._formdata
        if formdata is not None:
            data = []
            for pk, obj in self._get_object_list():
                if not formdata:
                    break
                elif pk in formdata:
                    formdata.remove(pk)
                    data.append(obj)
            while formdata:
                obj = self.model_factory(formdata.pop())
                data.append(obj)
            self._set_data(data)
            print(self._data)
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def pre_validate(self, form):
        pass


class AutoAddModelConverter(AdminModelConverter):
    def _model_select_field(self, prop, multiple, remote_model, **kwargs):
        loader = getattr(self.view, '_form_ajax_refs', {}).get(prop.key)

        if loader:
            if multiple:
                return AjaxSelectMultipleField(loader, **kwargs)
            else:
                return AjaxSelectField(loader, **kwargs)

        if 'query_factory' not in kwargs:
            kwargs['query_factory'] = lambda: self.session.query(remote_model)

        if multiple:
            return AutoAddMultiSelectField(**kwargs)
        else:
            return AutoAddSelectField(**kwargs)


class PostModelView(ModelView):
    can_view_details = True
    column_exclude_list = ['content']
    form_columns = ['content', 'title', 'slug', 'description', 'category',
                    'author', 'tags', 'image', 'lang', 'comment']
    create_template = 'admin/createmodel.html'
    edit_template = 'admin/editmodel.html'
    list_template = 'admin/mylist.html'
    model_form_converter = AutoAddModelConverter
    form_overrides = {'lang': SelectField}
    form_widget_args = {
        'content': {'data-role': 'mdeditor'},
        'tags': {'data-role': 'select2-free'},
        'category': {'data-role': 'select2-free'},
    }
    form_args = {
        'tags': dict(model_factory=lambda pk: Tag(text=pk),
                     get_label='text'),
        'category': dict(model_factory=lambda pk: Category(text=pk),
                         get_label='text'),
        'lang': dict(choices=[('en', 'English'), ('zh', 'Chinese')])
    }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login', next=request.url))


class LoginForm(Form):
    username = StringField('User Name',
                           validators=[validators.InputRequired()])
    password = PasswordField('Password',
                             validators=[validators.InputRequired()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()


class FlogAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user and current_user.is_authenticated):
            return redirect(url_for('.login'))
        else:
            return super(FlogAdminView, self).index()

    @expose('/login', methods=('POST', 'GET'))
    def login(self):
        form = LoginForm(request.form)
        if validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)
            return redirect(url_for('.index'))
        return self.render('admin/login.html', form=form)

    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('.index'))


admin = Admin(name='FlogAdmin', template_mode='bootstrap3',
              base_template='admin/bootstrap4.html',
              index_view=FlogAdminView())
admin.add_view(PostModelView(Post, db.session))
