#!/usr/bin/env python3
from __future__ import annotations

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize

from ...config import hacky_baseurl

__version__ = "0.1.9"

_terms_of_use = """By downloading data from this dataset, you agree to the terms and conditions defined at

    https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE

If you do not agree with such terms, do not download the data. """


class StaticField(Dataset):
    terms_of_use = _terms_of_use

    _BASEURL = hacky_baseurl

    _static_parameters = ["landu", "mterh"]

    @normalize("parameter", _static_parameters)
    def __init__(self, parameter):

        if parameter == "landu":
            url = self._BASEURL + 'data/gridded_data/gridded_land_usage.zarr'
        elif parameter == "mterh":
            url = self._BASEURL + 'data/gridded_data/gridded_model_terrain_height.zarr'

        self.source = cml.load_source("zarr", url)
