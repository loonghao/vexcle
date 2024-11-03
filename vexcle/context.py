# Import built-in modules
import logging

# Import local modules
from vexcle.filesystem import get_resource_path
from vexcle.filesystem import read_config


class Context:

    def __init__(self, app):
        self._logger = logging.getLogger(__name__)
        self.data = read_config()
        self.app = app

    @property
    def app_name(self):
        return self.data["app_name"]

    @property
    def app_version(self):
        return self.data["app_version"]
    @property
    def excel_file_name(self):
        return self.data["excel_file_name"]

    @property
    def headers(self):
        return self.data["headers"]

    @property
    def support_formats(self):
        return self.data["support_formats"]

    @property
    def style_file(self):
        return get_resource_path("styles.qss")

    def get_icon(self, *paths):
        icon_file = get_resource_path("icons", *paths)
        self._logger.debug("Get icon: %s", icon_file)
        return icon_file
