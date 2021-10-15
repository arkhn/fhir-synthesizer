import os

import requests
from dotenv import load_dotenv

from .metadata import REQUESTS
from .tools.paths import DATA_PATH

load_dotenv()  # Take environment variables from .env
hapi_fhir_url = os.getenv("HAPI_FHIR_URL")
if hapi_fhir_url is None:
    raise ValueError("Missing environment variable for 'HAPI_FHIR_URL'.")


def fetch(all_pages: bool = False) -> dict:
    """Fetch the input data from Hapi Fhir and output it as a dictionary.

    Args:
        all_pages: If True, get all pages of resources and store them in a list; else, get
            only the first page.

    Returns:
        A dictionary {resource_name: request_result}
    """
    os.makedirs(DATA_PATH, exist_ok=True)

    data = dict()
    for resource_name, request in REQUESTS.items():
        # A connection to the server is needed to access the data
        r = requests.get(f"{hapi_fhir_url}/{request}_format=json")
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
