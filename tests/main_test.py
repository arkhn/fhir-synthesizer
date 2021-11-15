from okapy import anonymization_pipeline


def test_anonymization_pipeline(mocker, patients_actifs_example: dict, test_data_path):
    # Mock the function `fetch` in okapy.main (i.e. don't enter the function, just output the
    # `return_value`
    mocker.patch("okapy.main.fetch", return_value=patients_actifs_example)

    # Test the anonymization pipeline with the mocked values
    anonymization_pipeline(
        resource_names=["patients_actifs"],
        output_dir=test_data_path,
    )
