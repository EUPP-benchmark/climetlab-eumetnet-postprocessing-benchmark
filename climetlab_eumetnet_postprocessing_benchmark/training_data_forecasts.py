#!/usr/bin/env python3
from __future__ import annotations

import datetime
import numpy as np
import xarray as xr

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize
from climetlab.indexing import PerUrlIndex

__version__ = "0.1.0"


class TrainingDataForecastEfi(Dataset):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    terms_of_use = (
        "By downloading data from this dataset, "
        "you agree to the terms and conditions defined at "
        "https://github.com/Climdyn/"
        "climetlab_eumetnet_postprocessing_benchmark/"
        "LICENSE"
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    _BASEURL = "https://storage.ecmwf.europeanweather.cloud/benchmark-dataset/"

    _PATTERN = (
        "{url}data/fcs/efi/"
        "EU_forecast_efi_params_{year}-{month}_0.grb"
    )
    _efi_params = ["capesi", "10fgi", "capei", "sfi", "10wsi", "2ti", "mx2ti", "mn2ti", "tpi"]

    @normalize("parameter", _efi_params)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter):
        self.parameter = parameter
        self.date = date
        self.year = date[:4]
        self.month = date[4:6]
        self.step = ["0-24", "24-48", "48-72", "72-96", "96-120", "120-144",  "144-168"]  # TODO : deal with the 240-360 steprange for 10wsi, 2ti, tpi
        request = {"param": self.parameter,
                   "date": self.date,
                   "step": self.step,
                   # Parameters passed to the filename mangling
                   "url": self._BASEURL,
                   "month": self.month,
                   "year": self.year}
        self.source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)


class TrainingDataForecastSurface(Dataset):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    terms_of_use = (
        "By downloading data from this dataset, "
        "you agree to the terms and conditions defined at "
        "https://github.com/Climdyn/"
        "climetlab_eumetnet_postprocessing_benchmark/"
        "LICENSE"
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    _BASEURL = "https://storage.ecmwf.europeanweather.cloud/benchmark-dataset/"

    _PATTERN = (
        "{url}data/fcs/{ltype}/"
        "EU_forecast_{kind}_{ltype}_params_{isodate}_0.grb"
    )

    _ANALYSIS_PATTERN = (
        "{url}data/ana/{ltype}/"
        "EU_analysis_{ltype}_params_{isodate}.grb"
    )

    _surf_parameters = ["2t", "10u", "10v", "tcc", "tp", "100u", "100v", "cape", "stl1", "sshf", "slhf",
                        "tcw", "tcwv", "swvl1", "ssr", "str", "sd", "cp", "cin", "ssrd", "strd", "3020", "all"]
    # _surf_pp_parameters = ["10fg6", "mn2t6", "mx2t6"]  TODO: obs not yet ready
    _surf_pp_parameters = []

    _ensemble_alias = ["ensemble", "ens", "proba", "probabilistic"]

    @normalize("parameter", _surf_parameters + _surf_pp_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter, kind):
        if parameter == "all":
            self.parameter = self._surf_parameters
        else:
            self.parameter = parameter
        self.date = date
        self.ltype = "surf"
        self.kind = kind
        self.obs_source = None
        self.isodate = "-".join([date[:4], date[4:6], date[6:]])
        if kind in self._ensemble_alias:
            request = {"param": self.parameter,
                       # "date": self.date,  ## Not needed
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "ens",
                       "ltype": self.ltype,
                       "isodate": self.isodate
                       }
            self.ens_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            request.update({"date": self.date,
                            # Parameters passed to the filename mangling
                            "kind": "ctr",
                            "isodate": self.isodate[:7]
                            })
            self.ctr_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            self.source = cml.load_source("multi", self.ens_source, self.ctr_source)
        else:  # default to highres forecasts
            request = {"param": self.parameter,
                       "date": self.date,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "hr",
                       "ltype": self.ltype,
                       "isodate": self.isodate[:7]
                       }
            self.source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)

    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):
        if fcs_kwargs is None:
            fcs_kwargs = dict()
        fcs = self.source.to_xarray(**fcs_kwargs)
        valid_time = fcs.valid_time.to_pandas()
        fcs_time_list = list(map(_convert, valid_time.iloc[0, :]))
        year_months = list()
        for t in fcs_time_list:
            year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
            if year_month not in year_months:
                year_months.append(year_month)
        days = dict()
        for year_month in year_months:
            days[year_month] = list()
        for t in fcs_time_list:
            year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
            days[year_month].append(str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0') + str(t.day).rjust(2, '0'))

        sources_list = list()
        for year_month in year_months:
            request = {"param": self.parameter,
                       "date": days[year_month],
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "ltype": self.ltype,
                       "isodate": "-".join([year_month[:4], year_month[4:]])
                       }
            source = cml.load_source("indexed-urls", PerUrlIndex(self._ANALYSIS_PATTERN), request)
            sources_list.append(source)
        self.obs_source = cml.load_source("multi", *sources_list)
        obs = self.obs_source.to_xarray(**obs_kwargs)
        valid_time = obs.valid_time.to_pandas()
        obs_time_list = list(map(_convert, valid_time.iloc[:, 0]))
        idx = list()
        for i, t in enumerate(obs_time_list):
            if t in fcs_time_list:
                idx.append(i)
        obs_fcs = obs.isel(time=idx)

        # reshape obs to fit fcs TODO: still messy, should be reworked
        obs_dict = obs_fcs.to_dict()
        _, obs_fcs = xr.align(fcs, obs_fcs, join='left', exclude=['number'])
        new_obs_dict = obs_fcs.to_dict()
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).swapaxes(1, 2))
        obs_fcs = obs_fcs.from_dict(new_obs_dict)

        return obs_fcs


class TrainingDataForecastPressure(Dataset):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    terms_of_use = (
        "By downloading data from this dataset, "
        "you agree to the terms and conditions defined at "
        "https://github.com/Climdyn/"
        "climetlab_eumetnet_postprocessing_benchmark/"
        "LICENSE"
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    _BASEURL = "https://storage.ecmwf.europeanweather.cloud/benchmark-dataset/"

    _PATTERN = (
        "{url}data/fcs/{ltype}/"
        "EU_forecast_{kind}_{ltype}_params_{isodate}_0.grb"
    )

    _ANALYSIS_PATTERN = (
        "{url}data/ana/{ltype}/"
        "EU_analysis_{ltype}_params_{isodate}.grb"
    )

    _pressure_parameters = ['z', 'u', 'v', 'q', 't', 'r']

    _ensemble_alias = ["ensemble", "ens", "proba", "probabilistic"]

    @normalize("parameter", _pressure_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter, level, kind):
        self.parameter = parameter
        self.date = date
        self.ltype = "pressure"
        self.kind = kind
        self.level = str(level)
        self.obs_source = None
        self.isodate = "-".join([date[:4], date[4:6], date[6:]])
        if kind in self._ensemble_alias:
            request = {"param": self.parameter,
                       # "date": self.date,  ## Not needed
                       "levelist": self.level,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "ens",
                       "ltype": self.ltype,
                       "isodate": self.isodate
                       }
            self.ens_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            request.update({"date": self.date,
                            # Parameters passed to the filename mangling
                            "kind": "ctr",
                            "isodate": self.isodate[:7]
                            })
            self.ctr_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            self.source = cml.load_source("multi", self.ens_source, self.ctr_source)
        else:  # default to highres forecasts
            request = {"param": self.parameter,
                       "date": self.date,
                       "levelist": self.level,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "hr",
                       "ltype": self.ltype,
                       "isodate": self.isodate[:7]
                       }
            self.source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)

    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):
        if fcs_kwargs is None:
            fcs_kwargs = dict()
        fcs = self.source.to_xarray(**fcs_kwargs)
        valid_time = fcs.valid_time.to_pandas()
        fcs_time_list = list(map(_convert, valid_time.iloc[0, :]))
        year_months = list()
        for t in fcs_time_list:
            year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
            if year_month not in year_months:
                year_months.append(year_month)
        days = dict()
        for year_month in year_months:
            days[year_month] = list()
        for t in fcs_time_list:
            year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
            days[year_month].append(str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0') + str(t.day).rjust(2, '0'))

        sources_list = list()
        for year_month in year_months:
            request = {"param": self.parameter,
                       "date": days[year_month],
                       "levelist": self.level,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "ltype": self.ltype,
                       "isodate": "-".join([year_month[:4], year_month[4:]])
                       }
            source = cml.load_source("indexed-urls", PerUrlIndex(self._ANALYSIS_PATTERN), request)
            sources_list.append(source)
        self.obs_source = cml.load_source("multi", *sources_list)
        obs = self.obs_source.to_xarray(**obs_kwargs)
        valid_time = obs.valid_time.to_pandas()
        obs_time_list = list(map(_convert, valid_time.iloc[:, 0]))
        idx = list()
        for i, t in enumerate(obs_time_list):
            if t in fcs_time_list:
                idx.append(i)
        obs_fcs = obs.isel(time=idx)

        # reshape obs to fit fcs TODO: still messy, should be reworked
        obs_dict = obs_fcs.to_dict()
        _, obs_fcs = xr.align(fcs, obs_fcs, join='left', exclude=['number'])
        new_obs_dict = obs_fcs.to_dict()
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).swapaxes(1, 2))
        obs_fcs = obs_fcs.from_dict(new_obs_dict)

        return obs_fcs


def _convert(t):
    return datetime.datetime(t.year, t.month, t.day, t.hour)
