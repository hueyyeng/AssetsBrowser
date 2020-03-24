"""Helpers Enums"""
from enum import Enum


class FileManager(Enum):
    WINDOWS = 'Explorer'
    DARWIN = 'Finder'
    LINUX = 'File Manager'
