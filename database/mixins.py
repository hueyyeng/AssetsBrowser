"""Database Mixins"""
from datetime import datetime
import peewee as pw

from config.constants import UTC


class NameDescriptionMixin(pw.Model):
    name = pw.CharField(
        max_length=50,
        verbose_name='Name',
    )
    description = pw.CharField(
        null=True,
        max_length=255,
        verbose_name='Description',
    )


class DateTimeMixin(pw.Model):
    created_dt = pw.DateTimeField(
        default=datetime.now(UTC),
        verbose_name='Date Created',
    )
    modified_dt = pw.DateTimeField(
        default=datetime.now(UTC),
        verbose_name='Date Modified',
    )
