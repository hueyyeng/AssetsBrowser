"""Test Config"""
import pytest
from config.configurations import (
    create_config,
    get_config,
    get_setting,
)
from config.exceptions import ConfigNotFoundException

from config.tests.conftest import (
    DEFAULT_CATEGORY,
    DEFAULT_SUBFOLDER,
    DOUBLE_QUOTES,
    SINGLE_QUOTES,
)


def test_create_config_successful(tmpdir):
    # 1. Create INI in temp directory
    toml_file = tmpdir.mkdir("create_config").join('test.toml')
    create_config(toml_file)

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
    config = get_config(toml_file)
    for section, option in expected_sections_options:
        assert option in config[section]


def test_load_list(tmpdir):
    test_toml = tmpdir.mkdir("load_list").join('test.toml')
    create_config(test_toml)

    existing_assets = get_setting(test_toml, 'Assets', 'CategoryList')
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
    invalid_path = "foo/bar/spam.toml"
    with pytest.raises(ConfigNotFoundException):
        get_config(invalid_path)
