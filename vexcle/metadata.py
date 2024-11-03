# Import built-in modules
import os
from pprint import pformat

# Import third-party modules
import ffmpeg

# Import local modules
from vexcle import filesystem
from vexcle.error import FfmpegError


class VideoMetadata:
    data = None

    @classmethod
    def get_metadata(cls, video_file):
        cls.data = ffmpeg.probe(video_file, cmd=filesystem.get_resource_path("bin", "ffprobe.exe"))
        return cls()

    @property
    def fps(self):
        return int(self.video["r_frame_rate"].split("/")[0])

    @property
    def frame_count(self):
        return self.video["duration_ts"]

    def __str__(self):
        return pformat(self.data)

    @property
    def streams(self):
        return self.data["streams"]

    @staticmethod
    def get_temp_thumb_dir(drag_path):
        return os.path.join(drag_path, "thumbs")

    @classmethod
    def export_thumbnail(cls, video_file):
        video_metadata = cls()
        drag_path, mov_name = os.path.split(video_file)
        path, _ = os.path.splitext(video_file)
        thumb_dir = video_metadata.get_temp_thumb_dir(drag_path)
        filesystem.ensure_paths(thumb_dir)
        name = mov_name.split(".")[0]
        thumb_file = filesystem.sanitize(os.path.join(thumb_dir, f"{name}.jpg"))
        process = (
            ffmpeg
                .input(video_file)
                .filter("scale", 300, -1)
                .output(thumb_file, vframes=1, format="image2", vcodec="mjpeg")
                .overwrite_output()
        )
        ffmpeg_cmd = process.compile()
        process = process.run_async(cmd=filesystem.get_resource_path("bin", "ffmpeg.exe"),
                                    pipe_stdout=True, pipe_stderr=True)

        out, err = process.communicate()

        if process.returncode:
            raise FfmpegError("", cmd=ffmpeg_cmd, stdout=out, stderr=err)
        return thumb_file

    def __getattribute__(self, item):
        if item == "video" or item == "audio":
            for info in self.streams:
                if info["codec_type"].lower() == item:
                    return info
        return super().__getattribute__(item)

    @property
    def width(self) -> int:
        return self.video["width"]

    @property
    def height(self) -> int:
        return self.video["height"]

    @property
    def duration(self) -> float:
        return self.video["duration"]
