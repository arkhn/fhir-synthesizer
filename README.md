# Okapy

Synthetic data generator for the Oqapi project with the Croix-Rouge. To generate data from a Fhir API,
for each resource we want to process, we first fetch it from an API, then preprocess it, and
finally we generate new data from the fetched data, before saving it.

To fetch the data from a Fhir API, an environment variable `HAPI_FHIR_URL` must be set, for
instance using a `.env` files, similar to the file `.env.example`.

All the algorithms are detailed in `okapy/okapy`.

## Install the requirements

```
pip install -e .
```

## Launch okapy

```
python okapy/main.py
```
