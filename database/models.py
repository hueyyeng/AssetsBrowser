"""Database Models"""
import os
import peewee as pw

from .mixins import NameDescriptionMixin, DateTimeMixin
from .validators import (
    validate_username,
    validate_email,
    validate_phone_number,
    validate_url,
)
from . import DATABASE


class BaseModel(pw.Model):
    class Meta:
        database = DATABASE

    def validate(self):
        pass


class Project(BaseModel, DateTimeMixin, NameDescriptionMixin):
    def __str__(self):
        return self.name


class Client(BaseModel, DateTimeMixin, NameDescriptionMixin):
    website = pw.CharField(
        null=True,
        verbose_name='Website',
    )

    def validate(self):
        validate_url(self.website)


class User(BaseModel, DateTimeMixin):
    username = pw.CharField(
        null=True,
        max_length=255,
        verbose_name='Username',
    ),
    name = pw.CharField(
        default=os.getlogin(),
        max_length=255,
        verbose_name='Name (Full or Preferred Name)',
    )
    email = pw.CharField(
        null=True,
        verbose_name='Email',
    )
    phone_number = pw.CharField(
        null=True,
        verbose_name='Phone Number',
    )
    client = pw.ForeignKeyField(
        Client,
        null=True,
        backref='users',
        verbose_name='Client',
    )

    def validate(self):
        validate_username(self.username)
        validate_email(self.email)
        validate_phone_number(self.phone_number)


class Category(BaseModel, NameDescriptionMixin):
    def __str__(self):
        return self.name


class Asset(BaseModel, DateTimeMixin, NameDescriptionMixin):
    author = pw.ForeignKeyField(
        User,
        verbose_name='Author',
    )
    category = pw.ForeignKeyField(
        Category,
        verbose_name='Category',
    )
    format = pw.CharField(
        verbose_name='Format',
        max_length=50,
    )
    project = pw.ForeignKeyField(
        Project,
        backref='assets',
        verbose_name='Project',
    )
    short_name = pw.FixedCharField(
        max_length=4,
        verbose_name='Short Name',
    )
    version = pw.SmallIntegerField(
        default=1,
        verbose_name='Version',
    )

    def __str__(self):
        return f"{self.short_name}_v{self.version:03}"
