"""Configurations"""
import logging
import os
from typing import Any

import toml
from config.constants import TOML_PATH, DEFAULT_CATEGORY, DEFAULT_SUBFOLDER
from config.exceptions import ConfigNotFoundException

logger = logging.getLogger(__name__)


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
    assets['CategoryList'] = DEFAULT_CATEGORY
    assets['SubfolderList'] = DEFAULT_SUBFOLDER

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
        logger.error('ERROR: TOML FILE NOT FOUND AT %s', path)
        raise ConfigNotFoundException

    config = toml.load(path)
    return config


def get_setting(section: str, setting: str, path=None) -> Any:
    """Returns a setting from the TOML file.

    Parameters
    ----------
    section : str
        Section name.
    setting : str
        Setting name.
    path : str or None
        Directory path for TOML file. If None, default to TOML_PATH

    Returns
    -------
    Any
        The value of the setting.

    """
    if not path:
        path = TOML_PATH
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


def update_setting(section: str, setting: str, value: Any, path=None):
    """Update a setting in the TOML file.

    Parameters
    ----------
    section : str
        Section name.
    setting : str
        Setting name.
    value : Any
        Value of the setting.
    path : str or None
        Directory path for TOML file. If None, default to TOML_PATH

    """
    if not path:
        path = TOML_PATH
    config = get_config(path)
    config[section][setting] = value
    with open(path, 'w') as config_file:
        toml.dump(config, config_file)
