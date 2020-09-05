import os


def ensure_paths(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def get_file_ext(path):
    if os.path.splitext(path)[1]:
        ext = os.path.splitext(path)[1]
        ext = ext.replace(".", "")
        return ext
    else:
        return ""


def sanitize(path):
    """Sanitize the given path.

    Args:
        path (str): The path to sanitize.

    Returns:
        str: The path being sanitized.

    """
    try:
        return path.replace("\\", "/")
    except AttributeError:
        # The path is of None type we we can't process a replace on.
        return ""
