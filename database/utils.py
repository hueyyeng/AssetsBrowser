"""Database Utils"""
import os
import logging
import peewee as pw

logger = logging.getLogger(__name__)

# Default path for DB file (located in the same directory as this file)
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
SQLITE_MEMORY = ':memory:'


def connect_db(db=None, sqlite_on_delete=True):
    if not db:
        db = SQLITE_MEMORY
    validate_db(db)
    pragmas = {'foreign_keys': 1} if sqlite_on_delete else {}
    return pw.SqliteDatabase(db, pragmas=pragmas)


def validate_db(db_path):
    if not db_path == SQLITE_MEMORY:
        try:
            open(db_path, 'r').close()
            logger.info('DB file found: %s' % db_path)
        except IOError:
            open(db_path, 'w').close()
            logger.error('DB file not found! Creating new empty DB at: %s' % db_path)


def delete_db(db_path=DEFAULT_DB_PATH):
    username = os.getlogin()
    try:
        os.remove(db_path)
        logger.info("Database deleted by user: %s" % username)
    except OSError as e:
        logger.error("Error deleting database: %s - %s." % (e.filename, e.strerror))


def create_tables(db, table):
    if not isinstance(table, list):
        table = list(table)
    with db:
        db.create_tables(table)


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
