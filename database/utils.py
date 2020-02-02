"""Database Utils"""
import os
import logging
import peewee as pw

from database.models import DB_PROXY, Client
from database.constants import DEFAULT_MODELS

logger = logging.getLogger(__name__)

# Default path for DB file (located in the same directory as this file)
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
SQLITE_MEMORY = ':memory:'


def connect_db(db=None, sqlite_on_delete: bool = True):
    if not db:
        db = SQLITE_MEMORY
    validate_db(db)
    pragmas = {'foreign_keys': 1} if sqlite_on_delete else {}
    return pw.SqliteDatabase(db, pragmas=pragmas)


def validate_db(db: str):
    if not db == SQLITE_MEMORY:
        try:
            open(db, 'r').close()
            logger.info('DB file found: %s', db)
        except IOError:
            open(db, 'w').close()
            logger.error('DB file not found! Creating new empty DB at: %s', db)


def delete_db(db: str = DEFAULT_DB_PATH):
    username = os.getlogin()
    try:
        os.remove(db)
        logger.info("Database deleted by user: %s", username)
    except OSError as e:
        logger.error("Error deleting database: %s - %s.", e.filename, e.strerror)


def create_db_tables(db: DB_PROXY, tables):
    if not isinstance(tables, list):
        tables = list(tables)
    db.create_tables(tables)


def insert_entry(db, model, **kwargs):
    try:
        with db.atomic():
            entry = model.create(**kwargs)
            entry.validate()
            return entry
    except pw.IntegrityError as e:
        raise e


def get_entry(db, model, **kwargs):
    try:
        with db.atomic():
            entry = model.get(**kwargs)
            return entry
    except pw.IntegrityError as e:
        raise e


def create_db_schema(db: DB_PROXY):
    """Create DB schema.

    Parameters
    ----------
    db : DB_PROXY
        peewee.Proxy

    """
    tables = DEFAULT_MODELS
    # Peewee requires explicit handling for through model unlike Django
    user_client_through = Client.users.get_through_model()
    tables.append(user_client_through)
    create_db_tables(db, tables)
