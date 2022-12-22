#!/usr/bin/env python3
from __future__ import annotations

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize

from ..config import baseurl

__version__ = "0.2.4"

_terms_of_use = """By downloading data from this dataset, you agree to the terms and conditions defined at

    https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE

If you do not agree with such terms, do not download the data. """


class StaticField(Dataset):
    terms_of_use = _terms_of_use

    _BASEURL = baseurl

    _static_parameters = ["landu", "mterh", "z"]

    @normalize("parameter", _static_parameters)
    def __init__(self, parameter):

        if parameter == "landu":
            url = self._BASEURL + 'data/static/land_cover.nc'
        elif parameter == "mterh":
            url = self._BASEURL + 'data/static/model_altitude.nc'
        elif parameter == "z":
            url = self._BASEURL + 'data/static/000z.nc'

        self.source = cml.load_source("url", url)
