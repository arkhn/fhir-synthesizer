import json
import os
import time
from typing import List, Optional

import typer

from synthetizer.anonymize import anonymize
from synthetizer.fetch import fetch
from synthetizer.metadata import RESOURCE_NAMES
from synthetizer.preprocess import preprocess_sampling_data
from synthetizer.tools.paths import DATA_PATH


def anonymization_pipeline(
    resource_names: List[str] = RESOURCE_NAMES,
    id_suffix: str = "",
    all_pages: bool = True,
    verbose: bool = False,
    output_dir: Optional[str] = DATA_PATH,
):
    """Full anonymization pipeline, which fetches the resources one by one, preprocess then &
    anonymize them, before saving them in json files.

    Args:
        resource_names: Names of the resources to anonymize.
        id_suffix: Suffix to append to all identifiers to make sure they remain unique.
        all_pages: If False, fetch only the first page of each resource.
        verbose: If True, display information about the current step.
        output_dir: Path of the directory to save the outputs in; if None, don't save them.
    """
    n_resource_names = len(resource_names)
    for i, resource_name in enumerate(resource_names):

        t0 = time.time()
        if verbose:
            print(f"Resources {i + 1}/{n_resource_names}: '{resource_name}'...")

        resource_bundle = fetch(
            resource_name=resource_name,
            all_pages=all_pages,
            verbose=verbose,
        )

        resource_sampling_data = preprocess_sampling_data(
            resource_name=resource_name,
            resource_bundle=resource_bundle,
            id_suffix=id_suffix,
            verbose=verbose,
        )

        resource_bundle = anonymize(
            resource_name=resource_name,
            resource_bundle=resource_bundle,
            resource_sampling_data=resource_sampling_data,
            id_suffix=id_suffix,
            verbose=verbose,
        )

        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, f"{resource_name}.json"), "w") as f:
                json.dump(resource_bundle, f, ensure_ascii=False)

        t1 = time.time()
        if verbose:
            print(f"Resources '{resource_name}' done in {round(t1-t0, 3)}s.\n")


if __name__ == "__main__":
    typer.run(anonymization_pipeline)
