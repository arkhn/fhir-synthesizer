from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="synthetic-data",
    version="0.1.0",
    author="Arkhn's Data Team",
    author_email="data@arkhn.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arkhn/synthetic-data",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache :: 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
