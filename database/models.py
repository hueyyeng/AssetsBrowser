"""Database Models"""
import peewee as pw

from database.mixins import (
    DateTimeMixin,
    NameDescriptionMixin,
)
from database.validators import ModelValidator

SQLITE_DB = pw.SqliteDatabase(None)


class BaseModel(pw.Model, ModelValidator):
    class Meta:
        database = SQLITE_DB


class Project(
    BaseModel,
    DateTimeMixin,
    NameDescriptionMixin,
):
    short_name = pw.FixedCharField(
        max_length=4,
        verbose_name='Short Name',
        unique=True,
    )

    def __str__(self):
        if self.name:
            return f"{self.short_name} - {self.name}"
        return self.short_name


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
    project = pw.ForeignKeyField(
        Project,
        backref='assets',
        verbose_name='Project',
    )
    format = pw.CharField(
        null=True,
        max_length=50,
        verbose_name='Format',
    )
    short_name = pw.FixedCharField(
        max_length=12,
        verbose_name='Short Name',
    )

    def __str__(self):
        return f"{self.category.name[0].lower()}{self.short_name}"
