import os
import configparser
import logging

logger = logging.getLogger(__name__)

ROOT_DIR = 'config/'
INI_FILE = 'settings.ini'
INI_PATH = (ROOT_DIR + INI_FILE)

config = configparser.ConfigParser(strict=False)


def create_config(path):
    # TODO: Break create_config into smaller chunk (DRY)
    # TODO: Handle PermissionError when trying to open directory as file
    """Create an INI config file with default value.

    Parameters
    ----------
    path : str
        Directory path for INI file.

    Returns
    -------
    None

    """
    config.optionxform = str
    home = os.path.expanduser('~')  # Defaults to home directory

    # 1. Settings (General settings for Assets Browser)
    config.add_section('Settings')
    config.set(
        'Settings',
        'ProjectPath',
        home.replace('\\', '/'),
    )
    config.set(
        'Settings',
        'ShowDescriptionPanel',
        'True',
    )
    config.set(
        'Settings',
        'CurrentProject',
        '.nodefaultvalue'
    )

    # 2. UI (UI settings for Assets Browser)
    config.add_section('UI')
    config.set(
        'UI',
        'Font',
        'Arial',
    )
    config.set(
        'UI',
        'Theme',
        'Fusion',
    )

    # 3. Assets (Assets' settings for Assets Browser)
    config.add_section('Assets')
    config.set(
        'Assets',
        'CategoryList',
        '["BG","CH","FX","Props","Vehicles"]',
    )
    config.set(
        'Assets',
        'SubfolderList',
        '["Scenes","Textures","References","WIP"]',
    )

    # 4.1 Write to INI file
    try:
        with open(path, 'w') as config_file:
            config.write(config_file)
    except PermissionError as e:
        logger.error(e)


def get_config(path):
    """Returns the INI config object.

    Parameters
    ----------
    path : str
        Directory path for INI file.

    Returns
    -------
    object
        INI Config object.

    """
    if not os.path.exists(path):
        create_config(path)
        logger.error('ERROR INI FILE NOT FOUND')
        logger.debug('Creating INI file at %s', path)

    config.optionxform = str
    config.read(path)
    return config


def get_setting(path, section, setting):
    """Returns a setting from the INI file.

    Parameters
    ----------
    path : str
        Directory path for INI file.
    section : str
        Section name.
    setting : str
        Setting name.

    Returns
    -------
    str
        The value of the setting.

    """
    ini = get_config(path)
    value = ini.get(section, setting)
    message = (
        '{section} {setting} is {value}'.format(
            section=section,
            setting=setting,
            value=value,
        )
    )
    logger.debug(message)
    return value


def update_setting(path, section, setting, value):
    """Update a setting in the INI file.

    Parameters
    ----------
    path : str
        Directory path for INI file.
    section : str
        Section name.
    setting : str
        Setting name.
    value : str or int
        Value of the setting.

    Returns
    -------
    None

    """
    ini = get_config(path)
    ini.set(section, setting, value)
    with open(path, 'w') as config_file:
        ini.write(config_file)


def delete_setting(path, section, setting):
    """Delete a setting from the INI file.

    Parameters
    ----------
    path : str
        Directory path for INI file.
    section : str
        Section name.
    setting : str
        Setting name.

    Returns
    -------
    None

    """
    ini = get_config(path)
    ini.set(section, setting)
    with open(path, 'w') as config_file:
        ini.write(config_file)


def current_project():
    """Get current project from INI file.

    Returns
    -------
    str
        The project name.

    """
    project = get_setting(INI_PATH, 'Settings', 'CurrentProject')
    return project
