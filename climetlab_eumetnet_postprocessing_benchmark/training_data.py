#!/usr/bin/env python3
from __future__ import annotations

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize_args

__version__ = "0.1.0"

URL = "https://storage.ecmwf.europeanweather.cloud"

PATTERN = (
    "{url}/climetlab/test-data/0.5/fixtures/"
    "climetlab-cookiecutter-dataset/{year}-{parameter}.grib"
)


class TrainingData(Dataset):
    name = None
    home_page = "-"
    licence = "-"
    documentation = "-"
    citation = "-"

    terms_of_use = (
        "By downloading data from this dataset, "
        "you agree to the terms and conditions defined at "
        "https://github.com/Climdyn/"
        "climetlab_eumetnet_postprocessing_benchmark/"
        "LICENSE"
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    @normalize_args(parameter=["tp", "t2m"])
    def __init__(self, year, parameter):
        self.year = year
        self.parameter = parameter
        request = dict(parameter=self.parameter, url=URL, year=self.year)
        self.source = cml.load_source("url-pattern", PATTERN, request)
