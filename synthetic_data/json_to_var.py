import json
import os
from typing import Optional

from .metadata import ANON_REQUESTS, DATA_PATH, NOT_ANON_REQUESTS


def json_to_var(file_name: Optional[str] = None, only_anon: bool = True, all_pages: bool = False):
    if file_name is None:
        if only_anon:
            file_names = list(ANON_REQUESTS.keys())
        else:
            file_names = list((ANON_REQUESTS | NOT_ANON_REQUESTS).keys())
    else:
        file_names = [file_name]

    d = dict()
    for file_name in file_names:
        if not all_pages:
            file_path = os.path.join(DATA_PATH, f"{file_name}.json")
        else:
            file_path = os.path.join(DATA_PATH, f"{file_name}_all.json")
        with open(file_path, "r", encoding="utf-8") as f:
            d[file_name] = json.load(f)

    return d
