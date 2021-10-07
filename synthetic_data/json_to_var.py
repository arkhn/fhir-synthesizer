import json
import os

from .metadata import ANON_REQUESTS, DATA_PATH, NOT_ANON_REQUESTS


def json_to_var(only_anon: bool = True):
    """
    Args:
        only_anon: If True, only get resources to anonymize; else, get resources from all requests.
    """
    if only_anon:
        file_names = ANON_REQUESTS.keys()
    else:
        file_names = (ANON_REQUESTS | NOT_ANON_REQUESTS).keys()

    d = dict()
    for file_name in file_names:
        file_path = os.path.join(DATA_PATH, f"{file_name}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            d[file_name] = json.load(f)

    return d
