import json
import os

import pytest

from okapy.tools.paths import EXAMPLES_PATH, TESTS_DATA_PATH


@pytest.fixture(scope="session")
def test_data_path() -> str:
    """Create the directory to output results in & output its path."""
    os.makedirs(TESTS_DATA_PATH, exist_ok=True)
    return TESTS_DATA_PATH


@pytest.fixture(scope="session")
def patients_actifs_example() -> dict:
    """Read a "patient_actifs" example and output it."""
    with open(os.path.join(EXAMPLES_PATH, "patients_actifs.json"), "r") as file:
        return json.load(file)
