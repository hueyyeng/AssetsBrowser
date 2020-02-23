"""Configurations Constants"""
from config.configurations import TOML_PATH, get_setting

ASSETS_CATEGORY_LIST = get_setting(TOML_PATH, 'Assets', 'CategoryList')
ASSETS_SUBFOLDER_LIST = get_setting(TOML_PATH, 'Assets', 'SubfolderList')
CURRENT_PROJECT = get_setting(TOML_PATH, 'Settings', 'CurrentProject')
PROJECT_PATH = get_setting(TOML_PATH, 'Settings', 'ProjectPath')
THEME = get_setting(TOML_PATH, 'UI', 'Theme')


IMAGE_FORMAT = [
    'jpg',
    'jpeg',
    'bmp',
    'png',
    'gif',
    'bmp',
    'ico',
    'tga',
    'tif',
    'tiff',
]

DEFAULT_CATEGORY = [
    "BG",
    "CH",
    "FX",
    "Props",
    "Vehicles",
]

DEFAULT_SUBFOLDER = [
    "References",
    "Scenes",
    "Textures",
    "WIP",
]

DEFAULT_METADATA = [
    "Author",
    "Category",
    "Date Created",
    "Date Modified",
    "Description",
    "Format",
    "Name",
    "Project",
    "Version",
]
