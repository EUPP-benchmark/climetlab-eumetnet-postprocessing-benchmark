#!/usr/bin/env python3
from __future__ import annotations

import warnings

import climetlab as cml
from climetlab import Dataset
from climetlab.utils.patterns import Pattern
from climetlab.normalize import normalize

from ..config import EUPreciP_baseurl

__version__ = "0.3.1"

_terms_of_use = """By downloading data from this dataset, you agree to the terms and conditions defined at

    https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE

If you do not agree with such terms, do not download the data. """


class CosmoDataForecast(Dataset):

    terms_of_use = _terms_of_use

    _BASEURL = EUPreciP_baseurl

    _PATTERN = "data/gridded_data/EUPreciPBench{kind}.zarr"

    def __init__(self, kind, *args, **kwargs):
        """Prepare the source with the provided `kind` argument."""
        self.obs_source = None

        request = {
            "kind": kind
        }

        urls = Pattern(self._BASEURL + self._PATTERN).substitute(request)
        self.request = request
        self.source = cml.load_source("zarr", urls)

    def to_xarray(self, **kwargs):
        return self.source.to_xarray()


class PrecipitationForecast(CosmoDataForecast):

    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    def __init__(self):
        CosmoDataForecast.__init__(self, "_tp")


class PredictorsForecast(CosmoDataForecast):

    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    def __init__(self):
        CosmoDataForecast.__init__(self, "_predictors")


class PrecipitationObservation(CosmoDataForecast):

    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    def __init__(self):
        CosmoDataForecast.__init__(self, "_EURADCLIM_tp")


class StaticField(CosmoDataForecast):

    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _static_parameters = ["landu", "mterh", "z"]

    @normalize("parameter", _static_parameters)
    def __init__(self, parameter):

        if parameter == "landu":
            CosmoDataForecast.__init__(self, "_land_usage")
        elif parameter == "mterh":
            CosmoDataForecast.__init__(self, "_model_terrain_height")
        elif parameter == "z":
            CosmoDataForecast.__init__(self, "_z")
