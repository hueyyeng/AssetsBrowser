from pytest import mark
import peewee as pw

from database.models import (
    Asset,
    Category,
    Project,
)
from database.db import Database


class TestProjects:
    def setup(self):
        self.test_db = Database()

    def test_create_project(self):
        project_name = "Super Good"
        project_short_name = "SG"
        project_desc = "Sequel to Good"
        project_data = {
            "name": project_name,
            "short_name": project_short_name,
            "description": project_desc,
        }
        Project.create(**project_data)
        p = Project.get(**project_data)
        assert p.name == project_name
        assert p.description == project_desc
        assert p.short_name == project_short_name
        assert str(p) == "SG - Super Good"

    def test_create_project_with_short_name_only(self):
        project_short_name = "SG"
        project_data = {
            "short_name": project_short_name,
        }
        Project.create(**project_data)
        p = Project.get(**project_data)
        assert not p.name
        assert not p.description
        assert p.short_name == project_short_name
        assert str(p) == "SG"
