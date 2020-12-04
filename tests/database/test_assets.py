import peewee as pw
from pytest import mark

from database.db import Database
from database.models import (
    Asset,
    Category,
    Project,
)


class TestAssets:
    def setup(self):
        self.test_db = Database()
        self.category_data = {
            "name": "FX",
            "description": "Effects",
        }
        self.project_data = {
            "name": "Super Good",
            "short_name": "SG",
            "description": "Sequel to Good",
        }
        self.category = Category.create(**self.category_data)
        self.project = Project.create(**self.project_data)

    def test_create_asset(self):
        asset_name = "Explosion"
        asset_desc = "Fire Magic"
        asset_short_name = "EXP"
        asset_data = {
            "category": self.category.id,
            "description": asset_desc,
            "name": asset_name,
            "short_name": asset_short_name,
            "project": self.project.id,
        }

        Asset.create(**asset_data)
        a = Asset.get(**asset_data)
        assert a.name == asset_name
        assert a.description == asset_desc
        assert a.short_name == asset_short_name
        assert a.category.name == "FX"
        assert a.project.name == "Super Good"
        assert str(a) == "fEXP"
