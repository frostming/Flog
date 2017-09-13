from datetime import datetime
from wtforms import SelectField
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import AdminModelConverter
from flask_admin.contrib.sqla.fields import QuerySelectField, QuerySelectMultipleField
from . import db, app
from .models import Post, Tag, Category
from flask import url_for
from slugify import slugify


admin = Admin(name='FlogAdmin', template_mode='bootstrap3',
              base_template='admin/bootstrap4.html')


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
    form_columns = ['content', 'title', 'description', 'category',
                    'author', 'tags', 'image', 'lang']
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


admin.add_view(PostModelView(Post, db.session))
