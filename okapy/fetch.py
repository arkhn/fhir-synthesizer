import os
from typing import Any

import requests
from dotenv import load_dotenv

from .metadata import REQUESTS

load_dotenv()  # Take environment variables from .env
hapi_fhir_url = os.getenv("HAPI_FHIR_URL")
if hapi_fhir_url is None:
    raise ValueError("Missing environment variable for 'HAPI_FHIR_URL'.")


def fetch(
    resource_name: str,
    all_pages: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """Fetch the input data from Hapi Fhir corresponding to `resource_name` and output it in a
    bundle format.

    Args:
        resource_name: Name of the resource bundle to fetch.
        all_pages: If True, get all pages of resources and store them in a list; else, get
            only the first page (which is far quicker).
        verbose: If True, display information about the current step.

    Returns:
        Requested resource bundle.
    """
    if verbose:
        print(f"Fetching resources `{resource_name}`...")

    request = REQUESTS[resource_name]

    # A connection to the server is needed to access the data
    r = requests.get(f"{hapi_fhir_url}/{request}_format=json")
    resource_bundle = r.json()

    if not all_pages:
        return resource_bundle

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

    return resource_bundle
