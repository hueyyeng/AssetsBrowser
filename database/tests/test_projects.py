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


class TestProjects:
    def setup(self):
        self.test_db = pw.SqliteDatabase(':memory:')
        DB_PROXY.initialize(self.test_db)
        self.test_db.connect()
        self.test_db.create_tables([
            Project,
        ])


    def test_create_project(self):
        project_name = "Super Good"
        project_short_name = "SG"
        project_desc = "Sequel to Good"
        project_data = {
            "name": project_name,
            "short_name": project_short_name,
            "description": project_desc,
        }
        insert_entry(self.test_db, Project, **project_data)
        p = get_entry(self.test_db, Project, id=1)
        assert p.name == project_name
        assert p.description == project_desc
        assert p.short_name == project_short_name
        assert str(p) == "Super Good (SG)"
