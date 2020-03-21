"""Helpers Constants"""
from enum import Enum

FILE_MANAGER = {
    'Windows': 'Explorer',
    'Darwin': 'Finder',
    'Linux': 'File Manager',
}


class FileManager(Enum):
    WINDOWS = 'Explorer'
    DARWIN = 'Finder'
    LINUX = 'File Manager'
