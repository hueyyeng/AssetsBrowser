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
    """"Assets' Browser Database.

    Currently configure using sqlite for standalone execution without
    relying on another DB driver like MySQL or Postgres

    """
    def __init__(self, db=None, sqlite_on_delete=True, use_default_db=False):
        self.db = SQLITE_DB
        if not db and use_default_db:
            db = DEFAULT_DB
        self.connect_db(db, sqlite_on_delete)
        self.check_db_schema()

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

        Verify if DB path exists. If IOError,
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

    def check_db_schema(self):
        """Check DB Schema

        Always create DB schema on creation startup if using SQLITE_MEMORY.
        If a DB path are given, verify if the DB has existing tables
        and create tables if none (for new DB file)

        """
        if not self.db.get_tables():
            self.create_db_schema()

    def create_db_schema(self):
        """Create DB schema"""
        self.create_db_tables(DEFAULT_MODELS)

    def create_db_tables(self, tables: list or pw.Model):
        """Create DB tables

        Parameters
        ----------
        tables : list or peewee.Model
            List of str. If Model, convert to list of Model.

        """
        if not isinstance(tables, list):
            tables = [tables]
        self.db.create_tables(tables)
