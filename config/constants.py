"""Configurations Constants"""
import os

CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))
TOML_FILE = 'settings.toml'
TOML_PATH = os.path.join(CONFIG_DIR, TOML_FILE)
ICON_FILE = 'file.png'

IMAGE_FORMAT = (
    '.jpg',
    '.jpeg',
    '.bmp',
    '.png',
    '.gif',
    '.bmp',
    '.ico',
    '.tga',
    '.tif',
    '.tiff',
)

DEFAULT_CATEGORY = (
    'BG',
    'CH',
    'FX',
    'Props',
    'Vehicles',
)

DEFAULT_SUBFOLDER = (
    'References',
    'Scenes',
    'Textures',
    'WIP',
)

DEFAULT_METADATA = (
    'Author',
    'Category',
    'Date Created',
    'Date Modified',
    'Description',
    'Format',
    'Name',
    'Project',
    'Version',
)
