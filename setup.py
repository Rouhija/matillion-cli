from setuptools import setup, find_packages

import os
import sys

py_version = sys.version_info[:2]
if not (3, 5) < py_version < (3, 9):
    raise RuntimeError('snowflake-cli needs Python version 3.6 - 3.8 to run')

with open("README.md", "r") as f:
    long_description = f.read()

dist = setup(
    name='matillioncli',
    version='1.0.2',
	url='https://github.com/Rouhija/matillion-cli',
	description="A cli tool for running Matillion jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sami Rouhe",
    author_email="rouhesami@gmail.com",
	packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
			'matillioncli = client.console:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
)