import os

import requests

from .metadata import ANON_REQUESTS, DATA_PATH, NOT_ANON_REQUESTS


def fetch_hapi(only_anon: bool = True, all_pages: bool = False):
    """
    Args:
        only_anon: If True, only get resources to anonymize; else, get resources from all requests.
        all_pages: If True, get all pages of resources and store them in a list; else, get
            only the first page.

    Returns:
        A dictionary {resource_name: request_result}
    """
    os.makedirs(DATA_PATH, exist_ok=True)

    if only_anon:
        file2request = ANON_REQUESTS
    else:
        file2request = ANON_REQUESTS | NOT_ANON_REQUESTS

    data = dict()
    for resource_name, request in file2request.items():
        # A connection to the server is needed to access the data
        r = requests.get(f"http://10.203.0.30/hapi/fhir{request}_format=json")
        result = r.json()

        if not all_pages:
            data[resource_name] = result
            continue

        relations = {k: v for k, v in [(link["relation"], link["url"]) for link in result["link"]]}
        while "next" in relations.keys():
            next_url = relations["next"]
            r = requests.get(next_url)
            new_result = r.json()
            result["entry"] += new_result["entry"]
            relations = {
                k: v for k, v in [(link["relation"], link["url"]) for link in new_result["link"]]
            }

        data[resource_name] = result

    return data
