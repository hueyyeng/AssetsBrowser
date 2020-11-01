import logging
import os

import pytest
from peewee import SqliteDatabase

from database.db import Database
from database.models import BaseModel


class DummyModel(BaseModel):
    pass


def test_use_default_db():
    test_db = Database(use_default_db=True)
    assert isinstance(test_db.db, SqliteDatabase)


def test_insert_single_table():
    test_db = Database()
    test_db.create_db_tables(DummyModel)


def test_validate_db_with_valid_db_path(
    tmp_path,
    caplog,
):
    caplog.set_level(logging.INFO)
    db = tmp_path / "dummy.db"
    db.write_text("")
    test_db = Database()
    test_db.validate_db(db)
    assert f"DB file found" in caplog.text


def test_validate_db_with_non_exist_db_path(
    tmp_path,
    caplog,
):
    caplog.set_level(logging.ERROR)
    db = tmp_path / "aloha.db"
    test_db = Database()
    test_db.validate_db(db)
    assert f"DB file not found! Creating new empty DB at" in caplog.text


@pytest.mark.parametrize("db_name,success", [
    ("success.db", True),
    ("failure.db", False),
])
def test_delete_db(
    success,
    db_name,
    tmp_path,
    caplog,
):
    db = tmp_path / db_name
    test_db = Database()
    if success:
        caplog.set_level(logging.INFO)
        username = os.getlogin()
        db.write_text("Test")
        test_db.delete_db(db)
        assert os.path.exists(db) is False
        assert "Database deleted by user" in caplog.text
        assert username in caplog.text
    else:
        caplog.set_level(logging.ERROR)
        test_db.delete_db(db)
        assert "Error deleting database" in caplog.text
        assert db_name in caplog.text
