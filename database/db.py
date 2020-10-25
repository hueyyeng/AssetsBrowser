"""Database"""
import logging
import os

import peewee as pw

from database.constants import DEFAULT_MODELS
from database.models import SQLITE_DB

logger = logging.getLogger(__name__)


DEFAULT_DB = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
SQLITE_MEMORY = ':memory:'


class Database:
    """"Asset's Browser Database.

    Currently configure using sqlite for standalone execution without
    relying on another DB driver like MySQL or Postgres

    """
    def __init__(self, db=None, sqlite_on_delete=True, use_default_db=False):
        self.db = SQLITE_DB
        if not db and use_default_db:
            db = DEFAULT_DB
        self.connect_db(db, sqlite_on_delete)

    def connect_db(self, db=None, sqlite_on_delete: bool = True):
        """Connect to database

        Parameters
        ----------
        db : str or None
            Path to DB. By default, None which will use in memory DB
        sqlite_on_delete : bool
            Set SQLite on Delete. By default, True.

        Returns
        -------
        object : peewee.SqliteDatabase

        """
        if not db:
            db = SQLITE_MEMORY
        self.validate_db(db)
        pragmas = {'foreign_keys': 1} if sqlite_on_delete else {}
        self.db.init(db, pragmas=pragmas)

    def validate_db(self, db: str):
        """Validate DB

        Verify if DB path is valid. If IOError,
        create a new DB file at the specify path.

        Parameters
        ----------
        db : str
            Path to DB

        """
        if not db == SQLITE_MEMORY:
            try:
                open(db, 'r').close()
                logger.info('DB file found: %s', db)
            except IOError:
                open(db, 'w').close()
                logger.error('DB file not found! Creating new empty DB at: %s', db)

    def delete_db(self, db: str = DEFAULT_DB):
        """Delete DB

        Parameters
        ----------
        db : str
            Path to DB

        """
        username = os.getlogin()
        try:
            os.remove(db)
            logger.info("Database deleted by user: %s", username)
        except OSError as e:
            logger.error("Error deleting database: %s - %s.", e.filename, e.strerror)

    def create_db_tables(self, tables: list):
        """Create DB tables

        Parameters
        ----------
        tables : list or str
            List of str. If str, it will convert to to list of str.

        """
        if not isinstance(tables, list):
            tables = list(tables)
        self.db.create_tables(tables)

    def insert_entry(self, model, **kwargs):
        try:
            with self.db.atomic():
                entry = model.create(**kwargs)
                entry.validate()
                return entry
        except pw.IntegrityError as e:
            raise e

    def get_entry(self, model, **kwargs):
        try:
            with self.db.atomic():
                entry = model.get(**kwargs)
                return entry
        except pw.IntegrityError as e:
            raise e

    def create_db_schema(self):
        """Create DB schema."""
        tables = DEFAULT_MODELS
        self.create_db_tables(tables)
