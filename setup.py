# -*- coding: utf-8 -*-
import setuptools
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('shelly2sgready/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="shelly2sgready",
    version=version,
    author="Christian Vihar",
    author_email="chrisv1180-github@yahoo.com",
    description="Wrapper for SG-Ready heatpumps controlled by Shelly relays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisv1180/shelly2sgready",
    packages=["shelly2sgready"],
    license="MIT",
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)