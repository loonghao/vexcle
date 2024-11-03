# Import built-in modules
from pathlib import Path

# Import third-party modules
import pytest


@pytest.fixture()
def data_root():
    return Path(__file__).parent / "data"


@pytest.fixture()
def get_test_data(data_root):
    def _get_test_data(file_name):
        return data_root / file_name

    return _get_test_data
