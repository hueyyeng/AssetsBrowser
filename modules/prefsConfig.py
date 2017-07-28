# -*- coding: utf-8 -*-
import os
import ConfigParser


# ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = ''
INI_FILE = 'settings.ini'
INI_PATH = (ROOT_DIR + INI_FILE)


def create_config(INI_PATH):
    """
    Create a config file
    """

    config = ConfigParser.ConfigParser()
    config.optionxform = str

    config.add_section('Settings')

    config.set('Settings', 'ProjectPath', 'P:/')
    config.set('Settings', 'ShowDescriptionPanel', 'True')
    config.set('Settings', 'ShowDebugLog', 'False')

    config.add_section('UI')

    config.set('UI', 'Font', 'Arial')
    config.set('UI', 'Theme', 'windowsvista')

    with open(INI_PATH, 'wb') as config_file:
        config.write(config_file)


def get_config(INI_PATH):
    """
    Returns the config object
    """

    if not os.path.exists(INI_PATH):
        # create_config(INI_PATH)
        print 'ERROR INI FILE NOT FOUND'

    config = ConfigParser.ConfigParser()
    config.optionxform=str
    config.read(INI_PATH)
    return config


def get_setting(INI_PATH, section, setting):
    """
    Print out a setting
    """

    config = get_config(INI_PATH)
    value = config.get(section, setting)
    # print '{section} {setting} is {value}'.format(
    #     section=section, setting=setting, value=value)
    return value


def update_setting(INI_PATH, section, setting, value):
    """
    Update a setting
    """

    config = get_config(INI_PATH)
    config.set(section, setting, value)
    with open(INI_PATH, 'wb') as config_file:
        config.write(config_file)


def delete_setting(INI_PATH, section, setting):
    """
    Delete a setting
    """
    config = get_config(INI_PATH)
    config.set(section ,setting)
    with open(INI_PATH, 'wb') as config_file:
        config.write(config_file)


# if __name__ == '__main__':
#     get_setting(INI_PATH, 'Settings', 'ProjectPath')
#     get_setting(INI_PATH, 'UI', 'Theme')
#     create_config(INI_PATH)
#     update_setting(INI_PATH, 'UI', 'Theme', 'windowsvista')
