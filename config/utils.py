import logging
import os

from config.configurations import create_config
from config.constants import DEFAULT_CATEGORY, DEFAULT_SUBFOLDER

logger = logging.getLogger(__name__)


def check_config_file(path: str):
    """Check for TOML config file

    If doesn't exists, create one with default value.

    Parameters
    ----------
    path : str
        Path to TOML config file

    """
    if os.path.exists(path):
        return
    logger.info("TOML config file not found. Creating new TOML config file at %s", path)
    create_config(path)


def create_project_structure_dirs(project=None):
    """Create sample project structure directories

    Project structure tree
    ----------------------
    Project
        Category 1
            Subfolder 1
            Subfolder 2
        Category 2
            Subfolder 1
            Subfolder 2

    Parameters
    ----------
    project : str or None
        Project name. If None, default to Project

    """
    home = os.path.expanduser('~')  # Defaults to home directory
    if not project:
        project = "Project"
    for category in DEFAULT_CATEGORY:
        for subfolder in DEFAULT_SUBFOLDER:
            path = os.path.join(home, project, category, subfolder)
            logger.info("Create %s directory", path)
            os.makedirs(path)
