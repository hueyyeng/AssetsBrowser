"""Test Create Config"""
import configparser
from config.configurations import create_config

config = configparser.ConfigParser()


def test_create_config_successful(tmpdir):
    ini_file = tmpdir.join('test.ini')
    create_config(ini_file)
    config.read(ini_file)

    expected_sections_options = [
        ('Settings', 'ProjectPath'),
        ('Settings', 'ShowDescriptionPanel'),
        ('Settings', 'CurrentProject'),
        ('UI', 'Font'),
        ('UI', 'Theme'),
        ('Assets', 'CategoryList'),
        ('Assets', 'SubfolderList'),
    ]

    for section, option in expected_sections_options:
        print(section, option)
        assert config.has_option(section, option) is True
