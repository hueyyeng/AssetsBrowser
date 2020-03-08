from pytest import mark
import pytest
import peewee as pw

from database.models import (
    Asset,
    Category,
    Client,
    User,
    Project,
)
from database.models import DB_PROXY
from database.utils import create_db_schema, insert_entry, get_entry


class TestClients:
    def setup(self):
        self.test_db = pw.SqliteDatabase(':memory:')
        DB_PROXY.initialize(self.test_db)
        self.test_db.connect()
        self.test_db.create_tables([
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
        insert_entry(self.test_db, Client, **self.client_data)
        client = get_entry(self.test_db, Client, id=1)
        assert client.name == self.client_data['name']
        assert client.description == self.client_data['description']
        assert client.email == self.client_data['email']
        assert client.phone_number == self.client_data['phone_number']
        assert client.website == self.client_data['website']

    def test_create_client_invalid_email(self):
        self.client_data['email'] = "aloha@com"
        with pytest.raises(Exception):
            insert_entry(self.test_db, Client, **self.client_data)

    def test_create_client_invalid_website(self):
        self.client_data['website'] = "http:/slashy.co"
        with pytest.raises(Exception):
            insert_entry(self.test_db, Client, **self.client_data)

    def test_create_client_invalid_phone(self):
        self.client_data['phone_number'] = "+I23456789"
        with pytest.raises(Exception):
            insert_entry(self.test_db, Client, **self.client_data)
