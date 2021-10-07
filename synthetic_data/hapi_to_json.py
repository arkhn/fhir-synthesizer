import json
import os

import requests

from .metadata import ANON_REQUESTS, DATA_PATH, NOT_ANON_REQUESTS


def hapi_to_json(only_anon: bool = True, all_pages: bool = False):
    """
    Args:
        only_anon: If True, only get resources to anonymize; else, get resources from all requests.
        all_pages: If True, get all pages of resources and store them in a list; else, get
            only the first page.
    """
    os.makedirs(DATA_PATH, exist_ok=True)

    if only_anon:
        file2request = ANON_REQUESTS
    else:
        file2request = ANON_REQUESTS | NOT_ANON_REQUESTS

    for file_name, request in file2request.items():
        # A connection to the server is needed to access the data
        r = requests.get(f"http://10.203.0.30/hapi/fhir{request}_format=json")
        result = r.json()

        if not all_pages:
            with open(os.path.join(DATA_PATH, f"{file_name}.json"), "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False)
            continue

        pages = [result]
        relations = {k: v for k, v in [(link["relation"], link["url"]) for link in result["link"]]}
        while "next" in relations.keys():
            next_url = relations["next"]
            r = requests.get(next_url)
            result = r.json()
            pages.append(result)
            relations = {
                k: v for k, v in [(link["relation"], link["url"]) for link in result["link"]]
            }

        with open(os.path.join(DATA_PATH, f"{file_name}.json"), "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False)