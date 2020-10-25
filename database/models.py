"""Database Models"""
import peewee as pw

from database.mixins import DateTimeMixin, EmailPhoneMixin, NameDescriptionMixin
from database.validators import ModelValidator

SQLITE_DB = pw.SqliteDatabase(None)


class BaseModel(pw.Model, ModelValidator):
    class Meta:
        database = SQLITE_DB

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


class Category(
    BaseModel,
    NameDescriptionMixin,
):
    def __str__(self):
        return str(self.name)


class Asset(
    BaseModel,
    DateTimeMixin,
    NameDescriptionMixin,
):
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
