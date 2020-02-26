import logging
import os

from config.configurations import create_config

logger = logging.getLogger(__name__)


def check_config_file(path: str):
    if os.path.exists(path):
        return
    logger.info("TOML config file not found. Creating new TOML config file at %s", path)
    create_config(path)
