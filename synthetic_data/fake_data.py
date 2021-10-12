import json
import os

import numpy as np
from glom import PathAccessError, assign, delete, glom

from .getter import get_all_values
from .metadata import DATA_PATH, PATHS_DEFAULT_VALUE, PATHS_ID_REF, PATHS_TO_DELETE, PATHS_TO_SAMPLE


def create_fake_data(initial_data: dict, id_suffix: str):
    """Create and save synthetic data created from `initial_data`, with some arguments removed and
    others sampled from `initial_data`.

    Args:
        initial_data: Real data, from which we want to sample fake information.
        id_suffix: Suffix to add to ids and refs.
    """
    os.makedirs(DATA_PATH, exist_ok=True)

    resources = list(initial_data.keys())

    for resource_name in resources:

        resource = {"entry": initial_data[resource_name]["entry"]}

        values_to_sample = {}
        if resource_name in PATHS_TO_SAMPLE:
            for path, spec, n_flatten in PATHS_TO_SAMPLE[resource_name]:
                values_to_sample[path] = get_all_values(
                    data=resource, spec=spec, n_flatten=n_flatten
                )

        # First, gather manually participants and start/end for appointments
        practitioners = []  # all the practitioners that participate
        n_practitioners = []  # number of practitioners per activity
        patients = []  # all the patients that participate
        n_patients = []  # number of patients per activity
        periods = []  # starts and ends of appointments
        if resource_name == "activites_planifiees":
            for entry in resource["entry"]:
                n_pat, n_pract = 0, 0
                participants = entry["resource"]["participant"]
                for participant in participants:
                    participant["actor"].pop("identifier", None)
                    if "reference" in participant["actor"]:
                        participant["actor"]["reference"] += id_suffix
                    if participant["actor"]["type"] == "Patient":
                        patients.append(participant)
                        n_pat += 1
                    elif participant["actor"]["type"] == "Practitioner":
                        practitioners.append(participant)
                        n_pract += 1
                n_practitioners.append(n_pract)
                n_patients.append(n_pat)

                # Start / end
                periods.append((entry["resource"]["start"], entry["resource"]["end"]))

        for i, entry in enumerate(resource["entry"]):

            # Update the ids and refs to add a suffix
            if resource_name in PATHS_ID_REF:
                for path in PATHS_ID_REF[resource_name]:
                    try:
                        assign(
                            resource, path.format(i), f"{glom(resource, path.format(i))}{id_suffix}"
                        )
                    except PathAccessError:
                        pass

            # Delete attributes that must be deleted
            if resource_name in PATHS_TO_DELETE:
                for path in PATHS_TO_DELETE[resource_name]:  # type: ignore
                    delete(resource, path.format(i), ignore_missing=True)

            # Sample attributes that must be sampled
            if resource_name in PATHS_TO_SAMPLE:
                for path, all_values in values_to_sample.items():
                    assign(resource, path.format(i), np.random.choice(all_values))

            # Set default values
            if resource_name in PATHS_DEFAULT_VALUE:
                for path, default_value in PATHS_DEFAULT_VALUE[resource_name]:  # type: ignore
                    assign(resource, path.format(i), default_value)

            # In the case of an appointment, handle participants and periods manually
            if resource_name == "activites_planifiees":
                fake_participants = list(
                    np.random.choice(patients, size=np.random.choice(n_patients), replace=False)
                ) + list(
                    np.random.choice(
                        practitioners, size=np.random.choice(n_practitioners), replace=False
                    )
                )
                assign(resource, f"entry.{i}.resource.participant", fake_participants)
                fake_start, fake_end = periods[np.random.choice(len(periods))]
                assign(resource, f"entry.{i}.resource.start", fake_start)
                assign(resource, f"entry.{i}.resource.end", fake_end)

        with open(os.path.join(DATA_PATH, f"fake_{resource_name}.json"), "w") as f:
            json.dump(resource, f, ensure_ascii=False)
