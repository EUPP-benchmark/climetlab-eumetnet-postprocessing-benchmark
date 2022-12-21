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
    install_requires=["climetlab>=0.9.9", "zarr>=2.13.3", "s3fs"],
    extras_require=extras_require,
    zip_safe=True,
    entry_points={
        "climetlab.datasets": [

            # original gridded datasets
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-efi= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastEfi",
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastSurface",
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-surface-processed= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastSurfaceProcessed",
            "eumetnet-postprocessing-benchmark-training-data-gridded-forecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_forecasts:TrainingDataForecastPressure",
            "eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-surface= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_reforecasts:TrainingDataReforecastSurface",
            "eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_reforecasts:TrainingDataReforecastPressure",
            "eumetnet-postprocessing-benchmark-training-data-gridded-reforecasts-surface-processed= climetlab_eumetnet_postprocessing_benchmark.gridded.training_data_reforecasts:TrainingDataReforecastSurfaceProcessed",
            "eumetnet-postprocessing-benchmark-training-data-gridded-static-fields= climetlab_eumetnet_postprocessing_benchmark.gridded.static_fields_data:StaticField",

            # EUPP phase datasets
            # gridded datasets
            "EUPPBench-training-data-gridded-forecasts-efi= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.training_data_forecasts:TrainingDataForecastEfi",
            "EUPPBench-training-data-gridded-forecasts-surface= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.training_data_forecasts:TrainingDataForecastSurface",
            "EUPPBench-training-data-gridded-forecasts-surface-processed= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.training_data_forecasts:TrainingDataForecastSurfaceProcessed",
            "EUPPBench-training-data-gridded-forecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.training_data_forecasts:TrainingDataForecastPressure",
            "EUPPBench-training-data-gridded-reforecasts-surface= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.training_data_reforecasts:TrainingDataReforecastSurface",
            "EUPPBench-training-data-gridded-reforecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.training_data_reforecasts:TrainingDataReforecastPressure",
            "EUPPBench-training-data-gridded-reforecasts-surface-processed= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.training_data_reforecasts:TrainingDataReforecastSurfaceProcessed",
            "EUPPBench-training-data-gridded-static-fields= climetlab_eumetnet_postprocessing_benchmark.EUPP.gridded.static_fields_data:StaticField",

            # stations datasets
            "EUPPBench-training-data-stations-forecasts-efi= climetlab_eumetnet_postprocessing_benchmark.EUPP.stations.training_data_forecasts:TrainingDataForecastEfi",
            "EUPPBench-training-data-stations-forecasts-surface= climetlab_eumetnet_postprocessing_benchmark.EUPP.stations.training_data_forecasts:TrainingDataForecastSurface",
            "EUPPBench-training-data-stations-forecasts-surface-processed= climetlab_eumetnet_postprocessing_benchmark.EUPP.stations.training_data_forecasts:TrainingDataForecastSurfaceProcessed",
            "EUPPBench-training-data-stations-forecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.EUPP.stations.training_data_forecasts:TrainingDataForecastPressure",
            "EUPPBench-training-data-stations-reforecasts-surface= climetlab_eumetnet_postprocessing_benchmark.EUPP.stations.training_data_reforecasts:TrainingDataReforecastSurface",
            "EUPPBench-training-data-stations-reforecasts-pressure= climetlab_eumetnet_postprocessing_benchmark.EUPP.stations.training_data_reforecasts:TrainingDataReforecastPressure",
            "EUPPBench-training-data-stations-reforecasts-surface-processed= climetlab_eumetnet_postprocessing_benchmark.EUPP.stations.training_data_reforecasts:TrainingDataReforecastSurfaceProcessed",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
