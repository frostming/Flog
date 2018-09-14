from flask import g
from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import (BooleanField, Form, PasswordField, StringField,
                     SubmitField, fields, widgets)
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from ..models import Category, Tag, User


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
        in_query = False
        for pk, obj in self._get_objects():
            if obj == self.data:
                in_query = True
            yield self.get_label(obj), self.get_label(obj), obj == self.data
        if not in_query and self.data:
            yield self.get_label(self.data), self.get_label(self.data), True


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

    def iter_choices(self):
        for pk, obj in self._get_objects():
            yield self.get_label(obj), self.get_label(obj), obj in self.data

    data = property(_get_data, _set_data)

    def process_formdata(self, valuelist):
        self._formdata = set(valuelist)


class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('User Name'),
                           validators=[InputRequired()])
    password = PasswordField(lazy_gettext('Password'),
                             validators=[InputRequired()])
    remember = BooleanField(lazy_gettext('Remember Me'))
    submit = SubmitField(lazy_gettext('Login'))

    def validate_username(self, field):
        user = User.get_one()

        if field.data != user.username:
            raise ValidationError(lazy_gettext('Invalid user'))

    def validate_password(self, field):
        user = User.get_one()
        if not user.check_password(field.data):
            raise ValidationError(lazy_gettext('Incorrect password'))


class PostForm(FlaskForm):
    title = StringField(
        lazy_gettext('Title'),
        validators=[InputRequired()],
        render_kw={'placeholder': lazy_gettext('Title goes here')}
    )
    description = StringField(
        lazy_gettext('Subtitle'),
        render_kw={'placeholder': lazy_gettext('A simple description of the post')}
    )
    image = StringField(lazy_gettext('Header Image URL'))
    author = StringField(
        lazy_gettext('Author'),
        validators=[InputRequired()]
    )
    slug = StringField(
        lazy_gettext('URL Name'),
        validators=[InputRequired()]
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
    is_draft = BooleanField(
        'Is Draft',
        default=False
    )


class SocialLink(Form):
    name = StringField(
        lazy_gettext('Name'),
        validators=[InputRequired()]
    )
    icon = StringField(
        lazy_gettext('Icon'),
        validators=[InputRequired()],
        render_kw={
            'placeholder': lazy_gettext('FontAwesome short name')
        }
    )
    link = StringField(
        lazy_gettext('Link'),
        validators=[InputRequired()]
    )


class SettingsForm(FlaskForm):
    name = StringField(lazy_gettext('Site Name'))
    description = StringField(lazy_gettext('Site Description'))
    avatar = StringField(lazy_gettext('Avatar URL'))
    cover_url = StringField(lazy_gettext('Cover Image URL'))
    locale = fields.SelectField(
        lazy_gettext('Language'),
        choices=[
            ('en', lazy_gettext('English')),
            ('zh_Hans_CN', lazy_gettext('Chinese'))
        ],
        default='en'
    )
    google_site_verification = StringField(
        lazy_gettext('Google Site Verification Code')
    )
    disqus_shortname = StringField(
        lazy_gettext('Disqus Shortname')
    )
    sociallinks = fields.FieldList(
        fields.FormField(SocialLink),
        lazy_gettext('Social Links'),
        min_entries=1
    )
    icp = StringField(lazy_gettext('ICP No.'))

    @classmethod
    def from_local(cls):
        return cls(data=g.site)


class ChangePasswordForm(FlaskForm):
    old = PasswordField(lazy_gettext('Old Password'))
    new = PasswordField(lazy_gettext('New Password'), [InputRequired(), Length(8, 16)])
    confirm = PasswordField(
        lazy_gettext('Confirm Password'),
        [EqualTo('new')]
    )

    def validate_old(self, field):
        admin = User.get_one()
        if not admin.check_password(field.data):
            raise ValidationError(lazy_gettext('Incorrect password'))
