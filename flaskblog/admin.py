from datetime import datetime
from flask_admin import Admin
from flask_admin.form.fields import Select2TagsField
from flask_admin.contrib.sqla import ModelView
from . import db, app
from .models import Post, Tag
from flask import url_for
from slugify import slugify


admin = Admin(name='FlogAdmin', template_mode='bootstrap3')


class TagsField(Select2TagsField):
    def __init__(self, *args, **kwargs):
        kwargs.pop('allow_blank')
        super(TagsField, self).__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        data = []
        to_add = []
        if valuelist:
            for v in valuelist[0].split(','):
                v = v.strip()
                if not v:
                    continue
                obj = Tag.query.get(self.coerce(v))
                if not obj:
                    obj = Tag(text=self.coerce(v))
                    to_add.append(obj)
                data.append(obj)
            db.session.add_all(to_add)
        self.data = data


class PostModelView(ModelView):
    form_overrides = {'tags': TagsField}
    can_view_details = True
    column_exclude_list = ['content']
    form_columns = ['content', 'title', 'description',
                    'author', 'tags', 'image']
    create_template = 'admin/createmodel.html'
    edit_template = 'admin/editmodel.html'
    form_widget_args = {
        'content': {'data-role': 'mdeditor'},
    }


admin.add_view(PostModelView(Post, db.session))
