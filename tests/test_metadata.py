# Import third-party modules
import pytest

# Import local modules
from vexcle.metadata import VideoMetadata


@pytest.mark.parametrize("video_name", [
        "9953267-hd_1080_1920_24fps.mp4",
    "12584369_1080_1920_60fps.mp4"
])
def test_get_metadata(get_test_data, video_name):
    video_path = get_test_data(video_name)
    api = VideoMetadata()
    metadata = api.get_metadata(video_path)
    assert metadata.width == 1080
