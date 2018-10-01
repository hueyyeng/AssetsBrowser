from config.configurations import get_setting, INI_PATH

INI_PATH = INI_PATH
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
