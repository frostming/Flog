from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import fields, validators, widgets
from flask_babel import lazy_gettext

from ..models import User, Category, Tag


class AutoAddSelectWidget(widgets.Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')
        return super(AutoAddSelectWidget, self).__call__(field, **kwargs)


class AutoAddSelectField(fields.SelectFieldBase):

    widget = AutoAddSelectWidget()

    def __init__(self, model, label_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.label_key = label_key

    def _get_data(self):
        if self._formdata is not None:
            obj = self.model.query.filter_by(**{self.label_key: self._formdata}).first()
            if not obj:
                obj = self.model(**{self.label_key: self._formdata})
            self._set_data(obj)
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def process_formdata(self, valuelist):
        if valuelist:
            self._data = None
            self._formdata = valuelist[0]

    def _get_objects(self):
        for obj in self.model.query.all():
            yield obj.id, obj

    def get_label(self, obj):
        return getattr(obj, self.label_key)

    def iter_choices(self):
        for pk, obj in self._get_objects():
            yield pk, self.get_label(obj), obj == self.data


class AutoAddMultiSelectField(AutoAddSelectField):

    widget = AutoAddSelectWidget(multiple=True)

    def __init__(self, model, label_key, *args, **kwargs):
        kwargs.setdefault('default', [])
        super().__init__(model, label_key, *args, **kwargs)

    def _get_data(self):
        if self._formdata is not None:
            data = []
            for label in self._formdata:
                obj = self.model.query.filter_by(**{self.label_key: label}).first()
                if not obj:
                    obj = self.model(**{self.label_key: label})
                data.append(obj)
                self._set_data(data)
        return self._data

    def _set_data(self, data):
        self._data = data
        self._formdata = None

    data = property(_get_data, _set_data)

    def process_formdata(self, valuelist):
        self._formdata = set(valuelist)


class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('User Name'),
                           validators=[validators.InputRequired()])
    password = PasswordField(lazy_gettext('Password'),
                             validators=[validators.InputRequired()])
    remember = BooleanField(lazy_gettext('Remember Me'))
    submit = SubmitField(lazy_gettext('Login'))

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            if (
                field.data == 'admin' and
                self.password.data == current_app.config['DEFAULT_ADMIN_PASSWORD']
            ):
                return True
            raise validators.ValidationError(lazy_gettext('Invalid user'))

        # we're comparing the plaintext pw with the the hash from the db
        if not user.check_password(self.password.data):
            raise validators.ValidationError(lazy_gettext('Incorrect password'))

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()


class PostForm(FlaskForm):
    title = StringField(
        lazy_gettext('Title'),
        validators=[validators.InputRequired()],
        render_kw={'placeholder': lazy_gettext('Title goes here')}
    )
    description = StringField(
        lazy_gettext('Subtitle'),
        render_kw={'placeholder': lazy_gettext('A simple description of the post')}
    )
    image = StringField(lazy_gettext('Cover Image URL'))
    author = StringField(
        lazy_gettext('Author'),
        validators=[validators.InputRequired()]
    )
    slug = StringField(
        lazy_gettext('URL Name'),
        validators=[validators.InputRequired()]
    )
    category = AutoAddSelectField(Category, 'text', lazy_gettext('Category'))
    tags = AutoAddMultiSelectField(Tag, 'text', lazy_gettext('Tags'))
    content = fields.TextAreaField('Content', render_kw={'data-role': 'mdeditor'})
    lang = fields.SelectField(
        lazy_gettext('Language'),
        choices=[
            ('en', lazy_gettext('English')),
            ('zh', lazy_gettext('Chinese'))
        ],
        default='en'
    )
    comment = BooleanField(
        lazy_gettext('Enable Comment'),
        default=True
    )
