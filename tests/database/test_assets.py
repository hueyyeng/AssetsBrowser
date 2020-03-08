from pytest import mark
import peewee as pw

from database.models import (
    Asset,
    Category,
    User,
    Project,
)
from database.models import DB_PROXY
from database.utils import create_db_schema, insert_entry, get_entry


class TestAssets:
    def setup(self):
        self.test_db = pw.SqliteDatabase(':memory:')
        DB_PROXY.initialize(self.test_db)
        self.test_db.connect()
        self.test_db.create_tables([
            Asset,
            Category,
            User,
            Project,
        ])
        self.user_data = {
            "name": "John Doe",
            "username": "john.doe",
            "email": "john.doe@email.com",
        }
        self.category_data = {
            "name": "FX",
            "description": "Effects",
        }
        self.project_data = {
            "name": "Super Good",
            "short_name": "SG",
            "description": "Sequel to Good",
        }

    def test_create_asset(self):
        insert_entry(self.test_db, Category, **self.category_data)
        insert_entry(self.test_db, User, **self.user_data)
        insert_entry(self.test_db, Project, **self.project_data)
        asset_name = "Explosion"
        asset_desc = "Fire Magic"
        asset_short_name = "EXP"
        asset_data = {
            "author": 1,
            "category": 1,
            "description": asset_desc,
            "format": "Maya",
            "name": asset_name,
            "short_name": asset_short_name,
            "project": 1,
        }

        insert_entry(self.test_db, Asset, **asset_data)
        a = get_entry(self.test_db, Asset, id=1)
        assert a.name == asset_name
        assert a.description == asset_desc
        assert a.short_name == asset_short_name
        assert str(a) == "EXP_v001"
        assert a.category.name == "FX"
        assert a.project.name == "Super Good"
        assert a.author.name == "John Doe"
