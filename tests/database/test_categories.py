import peewee as pw
from pytest import mark

from database.db import Database
from database.models import (
    Asset,
    Category,
    Project,
)


class TestCategories:
    def setup(self):
        self.test_db = Database()
        self.category_data_1 = {
            "name": "FX",
            "description": "Effects",
        }
        self.category_data_2 = {
            "name": "BG",
            "description": "Background",
        }

    def test_create_category(self):
        Category.create(**self.category_data_1)
        c1 = Category.get(**self.category_data_1)
        assert c1.name == self.category_data_1['name']
        assert c1.description == self.category_data_1['description']

        Category.create(**self.category_data_2)
        c2 = Category.get(**self.category_data_2)
        assert c2.name == self.category_data_2['name']
        assert c2.description == self.category_data_2['description']
