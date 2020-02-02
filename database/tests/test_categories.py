from pytest import mark
import peewee as pw

from database.models import (
    Asset,
    Category,
    User,
    Project,
)
from database.models import DB_PROXY
from database.utils import insert_entry, get_entry


class TestCategories:
    def setup(self):
        self.test_db = pw.SqliteDatabase(':memory:')
        DB_PROXY.initialize(self.test_db)
        self.test_db.connect()
        self.test_db.create_tables([
            Category,
        ])
        self.category_data_1 = {
            "name": "FX",
            "description": "Effects",
        }
        self.category_data_2 = {
            "name": "BG",
            "description": "Background",
        }

    def test_create_category(self):
        insert_entry(self.test_db, Category, **self.category_data_1)
        c1 = get_entry(self.test_db, Category, id=1)
        assert c1.name == self.category_data_1['name']
        assert c1.description == self.category_data_1['description']

        insert_entry(self.test_db, Category, **self.category_data_2)
        c2 = get_entry(self.test_db, Category, id=2)
        assert c2.name == self.category_data_2['name']
        assert c2.description == self.category_data_2['description']
