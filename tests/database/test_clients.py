import peewee as pw
import pytest
from pytest import mark

from database.db import Database
from database.models import (
    Asset,
    Category,
    Client,
    Project,
    User,
)


class TestClients:
    def setup(self):
        self.test_db = Database()
        self.test_db.create_db_tables([
            Client,
        ])
        self.client_data = {
            "name": "Little Red Dot Studio",
            "description": "Production House",
            "email": "enquiry@littlereddot.com",
            "phone_number": "+6037552525",
            "website": "http://littlered.test",
        }

    def test_create_client_successful(self):
        self.test_db.insert_entry(Client, **self.client_data)
        client = self.test_db.get_entry(Client, id=1)
        assert client.name == self.client_data['name']
        assert client.description == self.client_data['description']
        assert client.email == self.client_data['email']
        assert client.phone_number == self.client_data['phone_number']
        assert client.website == self.client_data['website']

    def test_create_client_invalid_email(self):
        self.client_data['email'] = "aloha@com"
        with pytest.raises(Exception):
            self.test_db.insert_entry(Client, **self.client_data)

    def test_create_client_invalid_website(self):
        self.client_data['website'] = "http:/slashy.co"
        with pytest.raises(Exception):
            self.test_db.insert_entry(Client, **self.client_data)

    def test_create_client_invalid_phone(self):
        self.client_data['phone_number'] = "+I23456789"
        with pytest.raises(Exception):
            self.test_db.insert_entry(Client, **self.client_data)
