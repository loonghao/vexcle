# Import built-in modules
import importlib
import logging
import os

# Import local modules
from vexcle.filesystem import get_file_ext
from vexcle.filesystem import sanitize
from vexcle.metadata import VideoMetadata


class Model(object):

    def __init__(self, context):
        self._context = context
        self.headers_register = context.headers
        self._headers = []
        self.data = {}
        self.register()

    def register(self):
        for header_name in self.headers_register:
            self.register_plugin(header_name)

    def register_plugin(self, name):
        """Register custom header.

        Args:
            name (str): The name of the custom header script.

        """
        header = importlib.import_module(f"vexcle.headers.{name}")
        custom_header = header.Header()
        logger = logging.getLogger(__name__)
        logger.debug("Register header: %s", custom_header.NAME)
        self.data[name] = {}
        try:
            self._headers.insert(custom_header.INSERT_INDEX, custom_header)
        except AttributeError:
            self._headers.append(custom_header)

    @property
    def headers(self):
        """List of vexcle.header.AbstractHeader: The custom headers."""
        return self._headers

    def get_excel_file_path(self, drag_path):
        return os.path.join(drag_path, self._context.excel_file_name)

    @staticmethod
    def get_video_info(file_path):
        metadata = VideoMetadata.get_metadata(file_path)
        thumbnail = VideoMetadata.export_thumbnail(file_path)
        return {"thumbnail": thumbnail,
                "resolution": f"{metadata.height}x{metadata.width}",
                "frame_range": metadata.frame_count,
                "duration": metadata.duration,
                "fps": metadata.fps,
                "file_name": os.path.basename(file_path)}

    def get_videos(self, drag_path):
        files = []
        for file_name in os.listdir(drag_path):
            ext = get_file_ext(file_name)
            if ext in self._context.support_formats:
                files.append(
                    sanitize(os.path.join(drag_path, file_name))
                )
        return files
