import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(ROOT_PATH, "data")
TESTS_DATA_PATH = os.path.join(DATA_PATH, "tests")

TESTS_PATH = os.path.join(ROOT_PATH, "tests")
EXAMPLES_PATH = os.path.join(TESTS_PATH, "examples")
