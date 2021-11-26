#!/usr/bin/env python


import io
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


package_name = "climetlab_eumetnet_postprocessing_benchmark"  # noqa: E501

version = None
lines = read(f"{package_name}/version").split("\n")
if lines:
    version = lines[0]

assert version


extras_require = {}

setuptools.setup(
    name=package_name,
    version=version,
    description=(
        "A dataset plugin for climetlab for the dataset "
        "eumetnet-postprocessing-benchmark/"  # noqa: E501
        "training-data."  # noqa: E501
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Jonathan Demaeyer",
    author_email="jodemaey@meteo.be",
    url="https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark",
    license="BSD-3-Clause License",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["climetlab>=0.5.6"],
    extras_require=extras_require,
    zip_safe=True,
    entry_points={
        "climetlab.datasets": [
            "eumetnet-postprocessing-benchmark-training-data= climetlab_eumetnet_postprocessing_benchmark.training_data:TrainingData",  # noqa: E501
            "eumetnet-postprocessing-benchmark-training-data-forecasts-efi= climetlab_eumetnet_postprocessing_benchmark.training_data_forecasts:TrainingDataForecastEfi",
            "eumetnet-postprocessing-benchmark-training-data-forecasts-surface= climetlab_eumetnet_postprocessing_benchmark.training_data_forecasts:TrainingDataForecastSurface",

            # other datasets can be included here
        ]
        # source plugins would be here
        # "climetlab.sources": []
    },
    keywords="meteorology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
