"""Test Config"""
import pytest
from config.configurations import (
    create_config,
    get_config,
    get_setting,
    update_setting,
    bulk_update_settings,
)
from config.exceptions import ConfigNotFoundException


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
        ('Assets', 'MaxChars'),
        ('Assets', 'SubfolderList'),
    ]

    # 3. Check if the value is valid.
    config = get_config(toml_file)
    for section, option in expected_sections_options:
        assert option in config[section]


def test_load_list(tmpdir):
    test_toml = tmpdir.mkdir("load_list").join('test.toml')
    create_config(test_toml)

    existing_assets = get_setting('Assets', 'CategoryList', test_toml)
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


def test_update_config(tmpdir):
    test_toml = tmpdir.mkdir("update_config").join('test.toml')
    create_config(test_toml)

    default_font = get_setting('UI', 'Font', test_toml)
    assert default_font == 'sans-serif'
    update_setting('UI', 'Font', 'Comic Sans MS', test_toml)
    new_font = get_setting('UI', 'Font', test_toml)
    assert new_font == 'Comic Sans MS'


def test_bulk_update_settings(tmpdir):
    test_toml = tmpdir.mkdir('bulk_update_settings').join('test.toml')
    create_config(test_toml)

    new_config = {
        'Font': 'Times New Roman',
        'MaxChars': 666,
    }
    bulk_update_settings(new_config, test_toml)
    font = get_setting('UI', 'Font', test_toml)
    assert font == 'Times New Roman'
    max_chars = get_setting('Assets', 'MaxChars', test_toml)
    assert max_chars == 666
