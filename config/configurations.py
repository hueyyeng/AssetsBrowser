# -*- coding: utf-8 -*-
import os
import sys
if sys.version_info[0] < 3:  # Check if Python version is less than 3
    import ConfigParser
    config = ConfigParser.ConfigParser()
else:
    import configparser
    config = configparser.ConfigParser()

ROOT_DIR = 'config/'
INI_FILE = 'settings.ini'
INI_PATH = (ROOT_DIR + INI_FILE)

home = os.path.expanduser('~')  # Defaults to home directory


def create_config(INI_PATH):
    """Create an INI config file with default value.

    Parameters
    ----------
    INI_PATH : str
        Directory path for INI file.

    Returns
    -------
    None

    """
    config.optionxform = str

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
        ''
    )

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

    # with open(INI_PATH, 'wb') as config_file:
    with open(INI_PATH, 'w') as config_file:
        config.write(config_file)


def get_config(INI_PATH):
    """Returns the INI config object.

    Parameters
    ----------
    INI_PATH : str
        Directory path for INI file.

    Returns
    -------
    object
        INI Config object.

    """
    if not os.path.exists(INI_PATH):
        create_config(INI_PATH)
        print('ERROR INI FILE NOT FOUND')
        print('Creating INI file at ' + INI_PATH)

    config.optionxform = str
    config.read(INI_PATH)
    return config


def get_setting(INI_PATH, section, setting):
    """Returns a setting from the INI file.

    Parameters
    ----------
    INI_PATH : str
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
    ini = get_config(INI_PATH)
    value = ini.get(section, setting)
    print('{section} {setting} is {value}'.format(
        section=section,
        setting=setting,
        value=value,
        )
    )
    return value


def update_setting(INI_PATH, section, setting, value):
    """Update a setting in the INI file.

    Parameters
    ----------
    INI_PATH : str
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
    ini = get_config(INI_PATH)
    ini.set(section, setting, value)
    with open(INI_PATH, 'w') as config_file:
        ini.write(config_file)


def delete_setting(INI_PATH, section, setting):
    """Delete a setting from the INI file.

    Parameters
    ----------
    INI_PATH : str
        Directory path for INI file.
    section : str
        Section name.
    setting : str
        Setting name.

    Returns
    -------
    None

    """
    ini = get_config(INI_PATH)
    ini.set(section ,setting)
    with open(INI_PATH, 'w') as config_file:
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


DEFAULTPATH = get_setting(INI_PATH, 'Settings', 'ProjectPath')
PROJECTPATH = DEFAULTPATH
CURRENTPROJECT = get_setting(INI_PATH, 'Settings', 'CurrentProject')
THEME = get_setting(INI_PATH, 'UI', 'Theme')
