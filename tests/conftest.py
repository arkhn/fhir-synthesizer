import os

import pytest

from okapy.tools.paths import TESTS_DATA_PATH


@pytest.fixture(scope="session")
def test_data_path() -> str:
    """Create the directory to output results in & output its path."""
    os.makedirs(TESTS_DATA_PATH, exist_ok=True)
    return TESTS_DATA_PATH
