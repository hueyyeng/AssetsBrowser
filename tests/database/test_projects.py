from pytest import mark
import peewee as pw

from database.models import (
    Asset,
    Category,
    User,
    Project,
)
from database.db import Database


class TestProjects:
    def setup(self):
        self.test_db = Database()
        self.test_db.create_db_tables([
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
        self.test_db.insert_entry(Project, **project_data)
        p = self.test_db.get_entry(Project, id=1)
        assert p.name == project_name
        assert p.description == project_desc
        assert p.short_name == project_short_name
        assert str(p) == "Super Good (SG)"
