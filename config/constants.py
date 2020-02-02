from config.configurations import get_setting, INI_PATH

INI_PATH = INI_PATH
ASSETS_CATEGORY_LIST = get_setting(INI_PATH, 'Assets', 'CategoryList')
ASSETS_SUBFOLDER_LIST = get_setting(INI_PATH, 'Assets', 'SubfolderList')
CURRENT_PROJECT = get_setting(INI_PATH, 'Settings', 'CurrentProject')
DEFAULT_PATH = get_setting(INI_PATH, 'Settings', 'ProjectPath')
PROJECT_PATH = DEFAULT_PATH
THEME = get_setting(INI_PATH, 'UI', 'Theme')


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
