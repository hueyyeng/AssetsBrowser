"""Test Create Config"""
import json
import pytest
from config.configurations import (
    create_config,
    get_config,
    get_setting,
)
from config.exceptions import ConfigNotFoundException

from .conftest import (
    default_category,
    default_subfolder,
    list_double_quotes,
    list_single_quotes,
)


def test_create_config_successful(tmpdir):
    # 1. Create INI in temp directory
    ini_file = tmpdir.mkdir("create_config").join('test.ini')
    create_config(ini_file)

    # 2. List of expected tuples
    expected_sections_options = [
        ('Settings', 'ProjectPath'),
        ('Settings', 'ShowDescriptionPanel'),
        ('Settings', 'CurrentProject'),
        ('UI', 'Font'),
        ('UI', 'Theme'),
        ('Assets', 'CategoryList'),
        ('Assets', 'SubfolderList'),
    ]

    # 3. Check if the value is valid.
    config = get_config(ini_file)
    for section, option in expected_sections_options:
        print(section, option)
        assert config.has_option(section, option) is True


def test_load_list(tmpdir):
    ini_file = tmpdir.mkdir("load_list").join('test.ini')
    create_config(ini_file)

    existing_assets = json.loads(get_setting(ini_file, 'Assets', 'CategoryList'))
    existing_qty = len(existing_assets)

    expected_assets = [
        "BG",
        "CH",
        "FX",
        "Props",
        "Vehicles",
    ]
    expected_qty = len(expected_assets)

    assert existing_qty == expected_qty
    for asset in expected_assets:
        assert asset in existing_assets


def test_config_not_found():
    invalid_path = "foo/bar/spam.ini"
    with pytest.raises(ConfigNotFoundException):
        get_config(invalid_path)


def test_double_quotes_value():
    value = list_double_quotes
    assert json.loads(value)


def test_single_quotes_value():
    value = list_single_quotes
    with pytest.raises(json.JSONDecodeError):
        assert json.loads(value)
