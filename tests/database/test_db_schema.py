from pytest import mark
import peewee as pw

from database.models import (
    Asset,
    Category,
    User,
    Client,
    Project,
)
from database.constants import DEFAULT_MODELS
from database.db import Database


def test_create_db_schema():
    test_db = Database()
    test_db.create_db_schema()
    for model in DEFAULT_MODELS:
        result = test_db.db.table_exists(model._meta.table_name)
        assert result is True


@mark.parametrize("model,fields", [
    (Asset, [
        'author',
        'category',
        'format',
        'project',
        'short_name',
        'version',
        'created_dt',
        'modified_dt',
        'name',
        'description',
    ]),
    (Category, [
        'name',
        'description',
    ]),
    (User, [
        'username',
        'name',
        'created_dt',
        'modified_dt',
        'email',
        'phone_number',
    ]),
    (Client, [
        'name',
        'description',
        'email',
        'phone_number',
        'users',
        'website',
    ]),
    (Project, [
        'name',
        'short_name',
        'description',
        'created_dt',
        'modified_dt',
    ]),
])
def test_db_model_fields(
        model,
        fields,
):
    for field in fields:
        result = hasattr(model, field)
        assert result
