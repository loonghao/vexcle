# Import built-in modules
import os
from pathlib import Path

# Import third-party modules
import yaml


def ensure_paths(path: str):
    if not os.path.isdir(path):
        os.makedirs(path)


def get_file_ext(path: str):
    filename, ext = os.path.splitext(path)
    if ext:
        return ext.lstrip(".").lower()
    else:
        return ""


def sanitize(path) -> str:
    """Sanitize the given path.

    Args:
        path (str): The path to sanitize.

    Returns:
        str: The path being sanitized.

    """
    try:
        return path.replace("\\", "/")
    except AttributeError:
        # The path is of None type we  can't process a replace on.
        return ""


def this_root() -> Path:
    return Path(__file__).resolve().parent


def read_config():
    config_file = get_resource_path("config.yaml")
    with open(config_file) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_resource_path(*paths):
    return os.path.join(this_root(), "resources", *paths)
