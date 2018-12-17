"""Custom exceptions"""
import logging

logger = logging.getLogger(__name__)


class InvalidProjectPath(Exception):
    def __init__(self, path):
        self.message = "Project Path doesn't exists: %s", str(path)
        logger.error(self.message)

    def __str__(self):
        return self.message


class ApplicationAlreadyExists(Exception):
    def __init__(self, app):
        self.message = "QApplication instance already exists: %s", str(app)
        logger.error(self.message)

    def __str__(self):
        return self.message
