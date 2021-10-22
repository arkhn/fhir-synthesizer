# Okapy

Anonymization tool for the Oqapi project with the Croix-Rouge. To anonymize data from a Fhir API,
for each resource we want to process, we first fetch it from an API, then preprocess it, and
finally we do the anonymization of the fetched data, before saving it.

To fetch the data from a Fhir API, an environment variable `HAPI_FHIR_URL` must be set, for
instance using a `.env` files, similar to the file `.env.example`.
