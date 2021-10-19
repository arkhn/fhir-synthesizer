from .metadata import PATHS_TO_SAMPLE
from .sampling_data import SamplingData, to_sampling_data
from .tools.utils import glom_getter


def preprocess_sampling_data(
    resource_name: str,
    resource_bundle: dict,
    id_suffix: str,
    verbose: bool = False,
) -> dict[str, SamplingData]:
    """Compute the relevant sampling data for the input resource bundle.

    Args:
        resource_name: Name of the resource bundle to preprocess.
        resource_bundle: Resource bundle to preprocess.
        id_suffix: Suffix to append to the identifiers, if needed.
        verbose: If True, display information about the current step.

    Returns:
        All the sampling data needed for `resource_bundle`.
    """
    if verbose:
        print(f"Preprocessing resources '{resource_name}'...")

    resource = {"entry": resource_bundle["entry"]}
    resource_sampling_data: dict[str, SamplingData] = {}

    # General case
    if resource_name in PATHS_TO_SAMPLE:
        for path, spec, n_flatten in PATHS_TO_SAMPLE[resource_name]:
            if path not in resource_sampling_data:
                values = glom_getter(
                    data=resource,
                    spec=spec,
                    n_flatten=n_flatten,
                )
                resource_sampling_data[path] = to_sampling_data(values=values)
            else:
                raise ValueError("Path has already been processed.")

    # Deal with the particular case of "activites_planifiees"
    if resource_name == "activites_planifiees":
        for name in ["practitioners", "n_practitioners", "patients", "n_patients", "starts_ends"]:
            if name in resource_sampling_data:
                raise ValueError("Name is already taken")

        # First, gather manually participants and start/end for appointments
        practitioners = []  # all the practitioners that participate
        n_practitioners = []  # number of practitioners per activity
        patients = []  # all the patients that participate
        n_patients = []  # number of patients per activity
        starts_ends = []  # starts and ends of appointments

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
            starts_ends.append((entry["resource"]["start"], entry["resource"]["end"]))

        resource_sampling_data["practitioners"] = to_sampling_data(practitioners)
        resource_sampling_data["n_practitioners"] = to_sampling_data(n_practitioners)
        resource_sampling_data["patients"] = to_sampling_data(patients)
        resource_sampling_data["n_patients"] = to_sampling_data(n_patients)
        resource_sampling_data["starts_ends"] = to_sampling_data(starts_ends)

    if verbose:
        for title, sampling_data in resource_sampling_data.items():
            sampling_data.display_info(title=f"{resource_name} - {title}")

    return resource_sampling_data
