""" Setup script. """

from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    README = readme_file.read()

setup(
    name="edo_exp",
    version="0.0.10",
    description="Generic functions for running experiments with `edo`.",
    long_description=README,
    url="https://github.com/daffidwilde/edo_exp",
    author="Henry Wilde",
    author_email="henrydavidwilde@gmail.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
)
