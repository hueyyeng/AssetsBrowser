import peewee as pw
from pytest import mark

from database.db import Database
from database.models import (
    Asset,
    Category,
    Project,
    User,
)


class TestUsers:
    def setup(self):
        self.test_db = Database()
        self.test_db.create_db_tables([
            User,
        ])

    def test_create_user(self):
        user_name = "John Doe"
        user_username = "john.doe"
        user_phone_number = "555-7890"
        user_email = "john.doe@email.com"
        user_data = {
            "name": user_name,
            "email": user_email,
            "phone_number": user_phone_number,
            "username": user_username,
        }
        u = self.test_db.insert_entry(User, **user_data)
        # TODO: Look into `(<CharField: (unbound)>,)` when GET query from DB for username value
        # v = get_entry(self.test_db, User, name=user_name)
        assert u.name == user_name
        assert u.username == user_username
        assert u.email == user_email
        assert u.phone_number == user_phone_number
