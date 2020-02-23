"""Configurations"""
import logging
import os
from typing import Any

import toml

from config.exceptions import ConfigNotFoundException

logger = logging.getLogger(__name__)

ROOT_DIR = 'config/'
TOML_FILE = 'settings.toml'
TOML_PATH = (ROOT_DIR + TOML_FILE)


def create_config(path: str):
    """Create TOML config file

    Parameters
    ----------
    path : str
        Path to TOML config file

    """
    home = os.path.expanduser('~')  # Defaults to home directory
    config = {}

    # 1.1 Settings
    settings = config['Settings'] = {}
    settings['ProjectPath'] = home.replace('\\', '/')
    settings['ShowDescriptionPanel'] = False
    settings['ShowDebugLog'] = False
    settings['CurrentProject'] = '.nodefaultvalue'

    ui = config['UI'] = {}
    ui['Font'] = 'Arial'
    ui['Theme'] = 'Default'

    assets = config['Assets'] = {}
    assets['UsePrefix'] = True
    assets['PrefixType'] = 0
    assets['UseSuffix'] = False
    assets['SuffixType'] = 0
    assets['SuffixCustomName'] = ''
    assets['CategoryList'] = [
        "BG",
        "CH",
        "FX",
        "Props",
        "Vehicles",
    ]
    assets['SubfolderList'] = [
        "Scenes",
        "Textures",
        "References",
        "WIP",
    ]

    # 2. Write to TOML file
    try:
        with open(path, 'w') as config_file:
            toml.dump(config, config_file)
    except PermissionError as e:
        logger.error(e)


def get_config(path: str) -> dict:
    """Returns dict from parsed TOML config file.

    Parameters
    ----------
    path : str
        Directory path for TOML file.

    Returns
    -------
    dict
        Dict from TOML config file.

    """
    if not os.path.exists(path):
        logger.error('ERROR: INI FILE NOT FOUND AT %s', path)
        raise ConfigNotFoundException

    config = toml.load(path)
    return config


def get_setting(path: str, section: str, setting: str) -> Any:
    """Returns a setting from the TOML file.

    Parameters
    ----------
    path : str
        Directory path for TOML file.
    section : str
        Section name.
    setting : str
        Setting name.

    Returns
    -------
    Any
        The value of the setting.

    """
    config = get_config(path)
    value = config[section][setting]
    message = (
        '{section} {setting} is {value}'.format(
            section=section,
            setting=setting,
            value=value,
        )
    )
    logger.debug(message)
    return value


def update_setting(path: str, section: str, setting: str, value: Any):
    """Update a setting in the TOML file.

    Parameters
    ----------
    path : str
        Directory path for TOML file.
    section : str
        Section name.
    setting : str
        Setting name.
    value : Any
        Value of the setting.

    """
    config = get_config(path)
    config[section][setting] = value
    with open(path, 'w') as config_file:
        toml.dump(config, config_file)


def current_project():
    """Get current project from TOML file.

    Returns
    -------
    str
        The project name.

    """
    project = get_setting(TOML_PATH, 'Settings', 'CurrentProject')
    return project
