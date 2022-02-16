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
        "A plugin for climetlab to retrieve the Eumetnet postprocessing benchmark dataset."
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Jonathan Demaeyer",
    author_email="jodemaey@meteo.be",
    url="https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark",
    license="BSD-3-Clause License",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["climetlab>=0.9.9"],
    extras_require=extras_require,
    zip_safe=True,
    entry_points={
        "climetlab.datasets": [
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-efi= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastEfi",
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastSurface",
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface-postprocessed= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastSurfacePostProcessed",
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastPressure",
            "eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-surface= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_reforecasts:TrainingDataReforecastSurface",
            "eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_reforecasts:TrainingDataReforecastPressure",
            "eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-surface-postprocessed= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_reforecasts:TrainingDataReforecastSurfacePostProcessed",

            # other datasets can be included here
        ]
        # source plugins would be here
        # "climetlab.sources": []
    },
    keywords=["meteorology", "meteorological-data", "postprocessing"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
