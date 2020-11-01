"""Database Field Validators"""
import re

from voluptuous import Email, Schema, Url


# pylint: disable=no-value-for-parameter
class ModelValidator:
    def validate_url(self, value):
        schema = Schema(Url())
        schema(value)

    def validate_email(self, value):
        schema = Schema(Email())
        schema(value)

    def validate_username(self, value):
        if value is None:
            return
        if re.match(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$', value):
            return value.lower()
        raise Exception("Username may only contain alphanumeric, underscore(_), hyphen(-) and period(.)")

    def validate_phone_number(self, value):
        if value is None:
            return
        if re.match("^[0-9-+ ]+$", value):
            return
        raise Exception("Phone number may only contain plus(+), hyphen(-) and digits only")
