"""Database Mixins"""
from datetime import datetime

import peewee as pw
import pytz

UTC = pytz.utc


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


class EmailPhoneMixin(pw.Model):
    email = pw.CharField(
        null=True,
        max_length=254,  # http://www.rfc-editor.org/errata_search.php?rfc=3696&eid=1690
        verbose_name='Email',
    )
    phone_number = pw.CharField(
        null=True,
        verbose_name='Phone Number',
    )
