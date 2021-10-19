import os

import requests
from dotenv import load_dotenv

from .metadata import REQUESTS

load_dotenv()  # Take environment variables from .env
hapi_fhir_url = os.getenv("HAPI_FHIR_URL")
if hapi_fhir_url is None:
    raise ValueError("Missing environment variable for 'HAPI_FHIR_URL'.")


def fetch(resource_names: list[str], all_pages: bool = False) -> dict[str, dict]:
    """Fetch the input data from Hapi Fhir and output it as a dictionary
    {<resource name>: <resource bundle>}.

    Args:
        resource_names: Names of the resources to fetch.
        all_pages: If True, get all pages of resources and store them in a list; else, get
            only the first page (which is far quicker).

    Returns:
        Dictionary {<resource name>: <resource bundle>}.
    """
    resource_bundles = dict()

    for resource_name in resource_names:
        request = REQUESTS[resource_name]

        # A connection to the server is needed to access the data
        r = requests.get(f"{hapi_fhir_url}/{request}_format=json")
        resource_bundle = r.json()

        if not all_pages:
            resource_bundles[resource_name] = resource_bundle
            continue

        relations = {
            k: v for k, v in [(link["relation"], link["url"]) for link in resource_bundle["link"]]
        }
        while "next" in relations.keys():
            next_url = relations["next"]
            r = requests.get(next_url)
            new_result = r.json()
            resource_bundle["entry"] += new_result["entry"]
            relations = {
                k: v for k, v in [(link["relation"], link["url"]) for link in new_result["link"]]
            }

        resource_bundles[resource_name] = resource_bundle

    return resource_bundles
