from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="synthetizer",
    version="0.1.0",
    author="Arkhn's Data Team",
    author_email="data@arkhn.com",
    description="Anonymization tool for the Oqapi project with the Croix-Rouge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arkhn/fhir-synthetizer",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache :: 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
