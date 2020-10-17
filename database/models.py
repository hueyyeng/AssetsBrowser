"""Database Models"""
import getpass
import peewee as pw

from database.mixins import NameDescriptionMixin, DateTimeMixin, EmailPhoneMixin
from database.validators import ModelValidator

DB_PROXY = pw.Proxy()


class BaseModel(pw.Model, ModelValidator):
    class Meta:
        database = DB_PROXY

    def validate(self):
        return None


class Project(
    BaseModel,
    DateTimeMixin,
    NameDescriptionMixin,
):
    short_name = pw.FixedCharField(
        max_length=4,
        verbose_name='Short Name',
    )

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class User(
    BaseModel,
    DateTimeMixin,
    EmailPhoneMixin,
):
    username = pw.CharField(
        null=True,
        max_length=255,
        verbose_name='Username',
        unique=True,
    ),
    name = pw.CharField(
        # Retrieve name from environment variables in Windows and workaround
        # for OSError: [Errno 25] Inappropriate ioctl for device
        default=getpass.getuser(),
        max_length=255,
        verbose_name='Name (Full or Preferred Name)',
    )

    def __str__(self):
        return self.username

    def validate(self):
        self.validate_username(self.username)
        self.validate_email(self.email)
        self.validate_phone_number(self.phone_number)


class Client(
    BaseModel,
    DateTimeMixin,
    EmailPhoneMixin,
    NameDescriptionMixin,
):
    users = pw.ManyToManyField(
        User,
        backref='clients',
    )
    website = pw.CharField(
        null=True,
        verbose_name='Website',
    )

    def validate(self):
        self.validate_url(self.website)
        self.validate_email(self.email)
        self.validate_phone_number(self.phone_number)


class Category(
    BaseModel,
    NameDescriptionMixin,
):
    def __str__(self):
        return self.name


class Asset(
    BaseModel,
    DateTimeMixin,
    NameDescriptionMixin,
):
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
        max_length=12,
        verbose_name='Short Name',
    )
    version = pw.SmallIntegerField(
        default=1,
        verbose_name='Version',
    )

    def __str__(self):
        return f"{self.short_name}_v{self.version:03}"
