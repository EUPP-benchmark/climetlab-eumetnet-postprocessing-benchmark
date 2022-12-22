#!/usr/bin/env python3
from __future__ import annotations

import warnings

import climetlab as cml
from climetlab import Dataset
from climetlab.utils.patterns import Pattern

from ...config import EUPP_baseurl

__version__ = "0.2.4"

_terms_of_use = """By downloading data from this dataset, you agree to the terms and conditions defined at

    https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE

If you do not agree with such terms, do not download the data. """


class TrainingDataForecast(Dataset):

    terms_of_use = _terms_of_use

    _BASEURL = EUPP_baseurl

    _PATTERN = ""

    _ensemble_alias = ["ensemble", "ens", "proba", "probabilistic"]

    def __init__(self, *args, **kwargs):
        """Do almost nothing. To be overridden by the inheriting class."""
        self.obs_source = None
        self.request = None

    def to_xarray(self, **kwargs):
        return self.source.to_xarray()

    def get_observations_as_xarray(self):
        if self.request is None:
            warnings.warn("Request first the forecasts before calling this function!")
            return None
        urls = Pattern(self._BASEURL + self._PATTERN).substitute(self.request)
        if 'reforecasts' in urls:
            look_for = 'reforecasts'
        else:
            look_for = 'forecasts'
        lst = urls.split('_')
        i = lst.index(look_for)
        new_lst = lst.copy()
        new_lst[i-1] = new_lst[i]
        new_lst[i] = 'observations'
        new_pattern = '_'.join(new_lst)
        urls = Pattern(new_pattern).substitute({})
        self.obs_source = cml.load_source("zarr", urls)
        return self.obs_source.to_xarray()


class TrainingDataForecastEfi(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = "data/stations_data/stations_forecasts_efi_{country}.zarr"

    def __init__(self, country):

        TrainingDataForecast.__init__(self)

        self.request = {
            "country": country
        }
        urls = Pattern(self._BASEURL + self._PATTERN).substitute(self.request)
        source = cml.load_source("zarr", urls)
        self.source = source

    def get_observations_as_xarray(self):
        warnings.warn("Observations are not available for the EFI forecasts.")
        return None


class TrainingDataForecastSurface(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = "data/stations_data/stations_{kind}_forecasts_surface_{country}.zarr"

    def __init__(self, kind, country):

        TrainingDataForecast.__init__(self)

        self.kind = kind
        if kind in self._ensemble_alias:
            request = {
                       "kind": "ensemble",
                       }
        else:  # default to highres forecasts
            request = {
                "kind": "highres",
            }

        request.update({"country": country})
        urls = Pattern(self._BASEURL + self._PATTERN).substitute(request)
        self.request = request
        self.source = cml.load_source("zarr", urls)


class TrainingDataForecastPressure(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    _PATTERN = "data/stations_data/stations_{kind}_forecasts_pressure_{level}_{country}.zarr"

    dataset = None

    def __init__(self, level, kind, country):

        TrainingDataForecast.__init__(self)
        self.kind = kind
        self.level = str(level)

        if kind in self._ensemble_alias:
            request = {
                "kind": "ensemble",
            }
        else:  # default to highres forecasts
            request = {
                "kind": "highres",
            }
        request.update({
                        "country": country,
                        "level": self.level,
        })
        urls = Pattern(self._BASEURL + self._PATTERN).substitute(request)
        self.request = request
        self.source = cml.load_source("zarr", urls)

    def get_observations_as_xarray(self):
        warnings.warn("Stations observations are not available for the pressure levels forecasts.")
        return None


class TrainingDataForecastSurfaceProcessed(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = "data/stations_data/stations_{kind}_forecasts_surface_postprocessed_{country}.zarr"

    def __init__(self, kind, country):

        TrainingDataForecast.__init__(self)

        self.kind = kind
        if kind in self._ensemble_alias:
            request = {
                "kind": "ensemble",
            }
        else:  # default to highres forecasts
            request = {
                "kind": "highres",
            }

        request.update({"country": country})
        urls = Pattern(self._BASEURL + self._PATTERN).substitute(request)
        self.request = request
        self.source = cml.load_source("zarr", urls)
