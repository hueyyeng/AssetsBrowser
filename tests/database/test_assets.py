import peewee as pw
from pytest import mark

from database.db import Database
from database.models import (
    Asset,
    Category,
    Project,
    User,
)


class TestAssets:
    def setup(self):
        self.test_db = Database()
        self.test_db.create_db_tables([
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
        self.test_db.insert_entry(Category, **self.category_data)
        self.test_db.insert_entry(User, **self.user_data)
        self.test_db.insert_entry(Project, **self.project_data)
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

        self.test_db.insert_entry(Asset, **asset_data)
        a = self.test_db.get_entry(Asset, id=1)
        assert a.name == asset_name
        assert a.description == asset_desc
        assert a.short_name == asset_short_name
        assert str(a) == "EXP_v001"
        assert a.category.name == "FX"
        assert a.project.name == "Super Good"
        assert a.author.name == "John Doe"
