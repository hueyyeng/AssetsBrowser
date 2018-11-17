"""Test Create Config"""
from config.configurations import create_config

ini_content = open('tests/samples/sample.ini', 'r')


def test_create_config_successful(tmpdir):
    ini_file = tmpdir.join('test.ini')
    create_config(ini_file)
    created_ini = ini_file.read()
    existing_ini = ini_content.read()
    assert created_ini == existing_ini
