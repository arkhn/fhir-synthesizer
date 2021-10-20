from typing import Any

from glom import PathAccessError, assign, delete, glom
from tqdm.notebook import tqdm

from okapy.metadata import PATHS_DEFAULT_VALUE, PATHS_ID_REF, PATHS_TO_DELETE, PATHS_TO_SAMPLE


def anonymize(
    resource_name: str,
    resource_bundle: dict,
    resource_sampling_data: dict,
    id_suffix: str,
    verbose: bool = False,
) -> dict[str, Any]:
    """Generate synthetic data starting from `resource_bundle`, by deleting the relevant
    attributes and modifying in-place other attributes.

    Args:
        resource_name: Name of the input resource.
        resource_bundle: Bundle of the input resource.
        resource_sampling_data: Sampling data corresponding to the resource.
        id_suffix: Suffix to append to the identifiers, to make sure they are unique.
        verbose: If True, display information about the current step.

    Returns:
        Input resource, modified in-place to make it anonymous.
    """
    if verbose:
        print("Anonymizing...")

    if resource_name == "activites_planifiees":
        practitioners = resource_sampling_data.pop("practitioners")
        n_practitioners = resource_sampling_data.pop("n_practitioners")
        patients = resource_sampling_data.pop("patients")
        n_patients = resource_sampling_data.pop("n_patients")
        starts_ends = resource_sampling_data.pop("starts_ends")
    else:
        practitioners = None
        n_practitioners = None
        patients = None
        n_patients = None
        starts_ends = None

    resource = {"entry": resource_bundle["entry"]}
    n_entries = len(resource["entry"])
    for i, entry in tqdm(enumerate(resource["entry"]), total=n_entries):

        # Update the ids and refs to add a suffix
        if resource_name in PATHS_ID_REF:
            for path in PATHS_ID_REF[resource_name]:
                try:
                    assign(resource, path.format(i), f"{glom(resource, path.format(i))}{id_suffix}")
                except PathAccessError:
                    pass

        # Delete attributes that must be deleted
        if resource_name in PATHS_TO_DELETE:
            for path in PATHS_TO_DELETE[resource_name]:  # type: ignore
                delete(resource, path.format(i), ignore_missing=True)

        # Sample attributes that must be sampled
        if resource_name in PATHS_TO_SAMPLE:
            for path, sampling_data in resource_sampling_data.items():
                new_value = sampling_data.sample()
                assign(resource, path.format(i), new_value)

        # Set default values
        if resource_name in PATHS_DEFAULT_VALUE:
            for path, default_value in PATHS_DEFAULT_VALUE[resource_name]:  # type: ignore
                assign(resource, path.format(i), default_value)

        # In the case of an appointment, handle participants and periods manually
        if resource_name == "activites_planifiees":
            n_patient = n_patients.sample()
            fake_patients = patients.sample(size=n_patient)
            n_practitioner = n_practitioners.sample()
            fake_practitioners = practitioners.sample(size=n_practitioner)
            fake_participants = list(fake_patients) + list(fake_practitioners)
            assign(resource, f"entry.{i}.resource.participant", fake_participants)

            fake_start, fake_end = starts_ends.sample()
            assign(resource, f"entry.{i}.resource.start", fake_start)
            assign(resource, f"entry.{i}.resource.end", fake_end)

    return resource
