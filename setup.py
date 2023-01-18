# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="channelrest",
    version="0.0.1",
    author="Josh P. Sawyer",
    author_email="josh@joshpsawyer.com",
    license="MIT",
    description="Python wrapper for Channel Advisor REST Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wildland-creative/channelrest",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.0',
)