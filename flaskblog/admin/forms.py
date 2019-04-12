import sqlalchemy as sa
from flask import g
from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    Form,
    PasswordField,
    StringField,
    SubmitField,
    fields,
    widgets,
)
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError

from ..models import Category, Tag, User
from typing import Iterator, Tuple, Iterable, Optional, List


class AutoAddSelectWidget(widgets.Select):
    def __call__(self, field: fields.Field, **kwargs) -> str:
        kwargs.setdefault('data-role', u'select2')
        return super(AutoAddSelectWidget, self).__call__(field, **kwargs)


class AutoAddSelectField(fields.SelectFieldBase):

    widget: AutoAddSelectWidget = AutoAddSelectWidget()

    def __init__(self, model, label_key: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model = model
        self.label_key = label_key

    def _get_data(self) -> sa.orm.Mapper:
        if self._formdata is not None:
            obj = self.model.query.filter_by(**{self.label_key: self._formdata}).first()
            if not obj:
                obj = self.model(**{self.label_key: self._formdata})
            self._set_data(obj)
        return self._data

    def _set_data(self, data: sa.orm.Mapper) -> None:
        self._data = data
        self._formdata: Optional[str] = None

    data = property(_get_data, _set_data)

    def process_formdata(self, valuelist: List[str]) -> None:
        if valuelist:
            self._data = None
            self._formdata = valuelist[0]

    def _get_objects(self) -> Iterator[Tuple[int, sa.orm.Mapper]]:
        for obj in self.model.query.all():
            yield obj.id, obj

    def get_label(self, obj: sa.orm.Mapper) -> str:
        return getattr(obj, self.label_key)

    def iter_choices(self) -> Iterator[Tuple[str, str, bool]]:
        in_query = False
        for pk, obj in self._get_objects():
            if obj == self.data:
                in_query = True
            yield self.get_label(obj), self.get_label(obj), obj == self.data
        if not in_query and self.data:
            yield self.get_label(self.data), self.get_label(self.data), True


class AutoAddMultiSelectField(AutoAddSelectField):

    widget: AutoAddSelectWidget = AutoAddSelectWidget(multiple=True)

    def __init__(self, model, label_key: str, *args, **kwargs):
        kwargs.setdefault('default', [])
        super().__init__(model, label_key, *args, **kwargs)

    def _get_data(self) -> Iterable[sa.orm.Mapper]:
        if self._formdata is not None:
            data = []
            for label in self._formdata:
                obj = self.model.query.filter_by(**{self.label_key: label}).first()
                if not obj:
                    obj = self.model(**{self.label_key: label})
                data.append(obj)
            self._set_data(data)
        return self._data

    def _set_data(self, data: Iterable[sa.orm.Mapper]) -> None:
        self._data = data
        self._formdata = None       # type: ignore

    def iter_choices(self) -> Iterator[Tuple[str, str, bool]]:
        for pk, obj in self._get_objects():
            yield self.get_label(obj), self.get_label(obj), obj in self.data

    data = property(_get_data, _set_data)

    def process_formdata(self, valuelist: List[str]) -> None:
        self._formdata = set(valuelist)     # type: ignore


class LoginForm(FlaskForm):
    username: fields.Field = StringField(
        lazy_gettext('User Name'), validators=[InputRequired()]
    )
    password: fields.Field = PasswordField(
        lazy_gettext('Password'), validators=[InputRequired()]
    )
    remember: fields.Field = BooleanField(lazy_gettext('Remember Me'))
    submit: fields.Field = SubmitField(lazy_gettext('Login'))

    def validate_username(self, field: fields.Field) -> None:
        user: User = User.get_one()

        if field.data != user.username:
            raise ValidationError(lazy_gettext('Invalid user'))

    def validate_password(self, field: fields.Field) -> None:
        user: User = User.get_one()
        if not user.check_password(field.data):
            raise ValidationError(lazy_gettext('Incorrect password'))


class PostForm(FlaskForm):
    title: fields.Field = StringField(
        lazy_gettext('Title'),
        validators=[InputRequired()],
        render_kw={'placeholder': lazy_gettext('Title goes here')},
    )
    description: fields.Field = StringField(
        lazy_gettext('Subtitle'),
        render_kw={'placeholder': lazy_gettext('A simple description of the post')},
    )
    image: fields.Field = StringField(lazy_gettext('Header Image URL'))
    author: fields.Field = StringField(
        lazy_gettext('Author'), validators=[InputRequired()]
    )
    slug: fields.Field = StringField(
        lazy_gettext('URL Name'), validators=[InputRequired()]
    )
    category: fields.Field = AutoAddSelectField(
        Category, 'text', lazy_gettext('Category')
    )
    tags: fields.Field = AutoAddMultiSelectField(Tag, 'text', lazy_gettext('Tags'))
    content: fields.Field = fields.TextAreaField(
        'Content', render_kw={'data-role': 'mdeditor'}
    )
    lang: fields.Field = fields.SelectField(
        lazy_gettext('Language'),
        choices=[('en', lazy_gettext('English')), ('zh', lazy_gettext('Chinese'))],
        default='en',
    )
    comment: fields.Field = BooleanField(lazy_gettext('Enable Comment'), default=True)
    is_draft: fields.Field = BooleanField('Is Draft', default=False)


class SocialLink(Form):
    name: fields.Field = StringField(lazy_gettext('Name'))
    icon: fields.Field = StringField(
        lazy_gettext('Icon'),
        render_kw={'placeholder': lazy_gettext('FontAwesome short name')},
    )
    link: fields.Field = StringField(lazy_gettext('Link'))


class FriendLink(Form):
    url: fields.Field = StringField(lazy_gettext('Link URL'))
    text: fields.Field = StringField(lazy_gettext('Link Text'))


class SettingsForm(FlaskForm):
    name: fields.Field = StringField(lazy_gettext('Site Name'))
    description: fields.Field = StringField(lazy_gettext('Site Description'))
    avatar: fields.Field = StringField(lazy_gettext('Avatar URL'))
    cover_url: fields.Field = StringField(lazy_gettext('Cover Image URL'))
    locale: fields.Field = fields.SelectField(
        lazy_gettext('Language'),
        choices=[
            ('en', lazy_gettext('English')),
            ('zh_Hans_CN', lazy_gettext('Chinese')),
        ],
        default='en',
    )
    google_site_verification: fields.Field = StringField(
        lazy_gettext('Google Site Verification Code')
    )
    google_analytics_id = StringField(
        lazy_gettext('Google Analytics ID')
    )
    disqus_shortname: fields.Field = StringField(lazy_gettext('Disqus Shortname'))
    sociallinks: fields.Field = fields.FieldList(
        fields.FormField(SocialLink), lazy_gettext('Social Links'), min_entries=1
    )
    icp: fields.Field = StringField(lazy_gettext('ICP No.'))
    links: fields.Field = fields.FieldList(
        fields.FormField(FriendLink), lazy_gettext('Friend Links'), min_entries=1
    )
    primary_color = fields.StringField(lazy_gettext('Primary Color'))

    @classmethod
    def from_local(cls) -> "SettingsForm":
        return cls(data=g.site)


class ChangePasswordForm(FlaskForm):
    old: fields.Field = PasswordField(lazy_gettext('Old Password'))
    new: fields.Field = PasswordField(
        lazy_gettext('New Password'), [InputRequired(), Length(8, 16)]
    )
    confirm: fields.Field = PasswordField(
        lazy_gettext('Confirm Password'), [EqualTo('new')]
    )

    def validate_old(self, field: fields.Field) -> None:
        admin = User.get_one()
        if not admin.check_password(field.data):
            raise ValidationError(lazy_gettext('Incorrect password'))
