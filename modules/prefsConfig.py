# -*- coding: utf-8 -*-
import os
import sys
if sys.version_info[0] < 3:  # Check if Python version is less than 3
    import ConfigParser
    config = ConfigParser.ConfigParser()
else:
    import configparser
    config = configparser.ConfigParser()

ROOT_DIR = ''
INI_FILE = 'settings.ini'
INI_PATH = (ROOT_DIR + INI_FILE)

home = os.path.expanduser('~')  # Defaults to home directory


def create_config(INI_PATH):
    # Create a config file with default value
    config.optionxform = str

    config.add_section('Settings')
    config.set('Settings', 'ProjectPath', home.replace('\\', '/'))
    config.set('Settings', 'ShowDescriptionPanel', 'True')
    config.set('Settings', 'CurrentProject', '')

    config.add_section('UI')
    config.set('UI', 'Font', 'Arial')
    config.set('UI', 'Theme', 'Fusion')

    # with open(INI_PATH, 'wb') as config_file:
    with open(INI_PATH, 'w') as config_file:
        config.write(config_file)


def get_config(INI_PATH):
    # Returns the config object
    if not os.path.exists(INI_PATH):
        create_config(INI_PATH)
        print('ERROR INI FILE NOT FOUND')
        print('Creating INI file at ' + INI_PATH)

    config.optionxform = str
    config.read(INI_PATH)
    return config


def get_setting(INI_PATH, section, setting):
    # Print out a setting
    config = get_config(INI_PATH)
    value = config.get(section, setting)
    print('{section} {setting} is {value}'.format(
        section=section, setting=setting, value=value))
    return value


def update_setting(INI_PATH, section, setting, value):
    # Update a setting
    config = get_config(INI_PATH)
    config.set(section, setting, value)
    with open(INI_PATH, 'w') as config_file:
        config.write(config_file)


def delete_setting(INI_PATH, section, setting):
    # Delete a setting
    config = get_config(INI_PATH)
    config.set(section ,setting)
    with open(INI_PATH, 'w') as config_file:
        config.write(config_file)


def current_project():
    project = get_setting(INI_PATH, 'Settings', 'CurrentProject')
    return project


# -------------------------------------------------------------------

DEFAULTPATH = get_setting(INI_PATH, 'Settings', 'ProjectPath')
PROJECTPATH = DEFAULTPATH
CURRENTPROJECT = get_setting(INI_PATH, 'Settings', 'CurrentProject')
THEME = get_setting(INI_PATH, 'UI', 'Theme')

# -------------------------------------------------------------------
