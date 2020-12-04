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
        backref='assets',
        verbose_name='Category',
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

    def __str__(self):
        return f"{self.category.name[0].lower()}{self.short_name}"


class Application(
    BaseModel,
    NameDescriptionMixin,
):
    # Max path length for older Windows API is 260 chars
    path = pw.CharField(
        null=True,
        max_length=260,
        verbose_name='Path',
    )

    def __str__(self):
        return self.name


class AssetItemFormat(
    BaseModel,
):
    name = pw.CharField(
        max_length=50,
        verbose_name='Name',
    )
    format = pw.CharField(
        max_length=100,
        verbose_name='Format',
    )
    application = pw.ForeignKeyField(
        Application,
        null=True,
        backref='asset_formats',
        verbose_name='Application',
    )

    def __str__(self):
        return self.short_name


class AssetItem(
    BaseModel,
    DateTimeMixin,
    NameDescriptionMixin,
):
    asset = pw.ForeignKeyField(
        Asset,
        backref='asset_items',
        verbose_name='Asset',
    )
    category = pw.ForeignKeyField(
        Category,
        backref='asset_items',
        verbose_name='Category',
    )
    project = pw.ForeignKeyField(
        Project,
        backref='asset_items',
        verbose_name='Project',
    )
    format = pw.ForeignKeyField(
        AssetItemFormat,
        null=True,
        backref='asset_items',
        verbose_name='Format',
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
        return f"{self.category.name[0].lower()}{self.short_name}_v{self.version:03}"
