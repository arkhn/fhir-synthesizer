import json
import os
from typing import Optional

import numpy as np
from glom import assign, delete

from .getter import get_all_values
from .metadata import DATA_PATH, PATHS_TO_DELETE, PATHS_TO_SAMPLE


def create_fake_data(initial_data: dict, resources: Optional[list[str]] = None):
    """Create and save synthetic data created from `initial_data`, with some arguments removed and
    others sampled from `initial_data`.

    Args:
        initial_data: Real data, from which we want to sample fake information.
        resources: Resources for which to create fake data; if None, create data for all resources
            contained in `initial_data`.
    """
    os.makedirs(DATA_PATH, exist_ok=True)

    if resources is None:
        resources = list(initial_data.keys())

    for resource_name in resources:
        if resource_name not in initial_data:
            raise ValueError(f"Resource '{resource_name}' not found in the initial data.")
        if resource_name not in PATHS_TO_DELETE:
            raise ValueError(f"Resource '{resource_name}' not found in PATH_TO_DELETE.")
        if resource_name not in PATHS_TO_SAMPLE:
            raise ValueError(f"Resource '{resource_name}' not found in PATH_TO_SAMPLE.")

        resource = initial_data[resource_name]

        for path in PATHS_TO_DELETE[resource_name]:  # type: ignore
            for i in range(len(resource["entry"])):
                delete(resource, path.format(i), ignore_missing=True)

        for path, spec, n_flatten in PATHS_TO_SAMPLE[resource_name]:
            all_values = get_all_values(data=resource, spec=spec, n_flatten=n_flatten)
            for i in range(len(resource["entry"])):
                assign(resource, path.format(i), np.random.choice(all_values))

        with open(os.path.join(DATA_PATH, f"fake_{resource_name}.json"), "w") as f:
            json.dump(resource, f, ensure_ascii=False)
