# Fhir-Synthetizer

Synthetic data generator for the Oqapi project with the Croix-Rouge. To generate data from a Fhir API,
for each resource we want to process, we first fetch it from an API, then preprocess it, and
finally we generate new data from the fetched data, before saving it.

To fetch the data from a Fhir API, an environment variable `HAPI_FHIR_URL` must be set, along
with authentication credentials, for instance using a `.env` file, similar to the file `.env. example`.

## Install the requirements

To install the requirements, along with Fhir-Synthetizer's package, simply install it with `pip`,
for instance with:

```
pip install -e .
```

from the root of the repository.

## Launch Fhir-Synthetizer

To launch Fhir-Synthetizer within the CLI, you can run:

```
python synthetizer/main.py
```

You can access the main documentation with:

```
python synthetizer/main.py --help
```

There, you can have a detailed explanation of all the parameters.
