"""Database Field Validators"""
import re
from voluptuous import Schema, Url, Email


# pylint: disable=no-value-for-parameter
def validate_url(value):
    schema = Schema(Url())
    schema(value)


def validate_email(value):
    schema = Schema(Email())
    schema(value)


def validate_username(value):
    if value is None:
        return
    if re.match(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$', value):
        return value.lower()
    raise Exception("Username may only contain alphanumeric, underscore(_), hyphen(-) and period(.)")


def validate_phone_number(value):
    if value is None:
        return
    if re.match("^[0-9-+ ]+$", value):
        return
    raise Exception("Phone number may only contain plus(+), hyphen(-) and digits only")
