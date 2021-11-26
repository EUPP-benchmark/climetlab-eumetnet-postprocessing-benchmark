#!/usr/bin/env python3
from __future__ import annotations

import datetime

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize
from climetlab.indexing import PerUrlIndex

__version__ = "0.1.0"


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

    _ANA_PATTERN = (
        "{url}data/ana/{ltype}/"
        "EU_analysis_{ltype}_params_{isodate}.grb"
    )

    _surf_parameters = ["2t", "10u", "10v", "tcc", "tp", "100u", "100v", "cape", "stl1", "sshf", "slhf",
                       "tcw", "tcwv", "swvl1", "ssr", "str", "sd", "cp", "cin", "ssrd", "strd", "3020"]
    # _surf_pp_parameters = ["10fg6", "mn2t6", "mx2t6"]  TODO: obs not yet ready
    _surf_pp_parameters = []

    @normalize("parameter", _surf_parameters + _surf_pp_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter, kind):
        self.parameter = parameter
        self.date = date
        self.ltype = "surf"
        self.kind = kind
        if kind == "ensemble":
            self.isodate = "-".join([date[:4], date[4:6], date[6:]])
            request = {"param": self.parameter,
                       "date": self.date,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "ens",
                       "ltype": self.ltype,
                       "isodate": self.isodate
                       }
            self.ens_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            request.update({# Parameters passed to the filename mangling
                           "kind": "ctr",
                           "isodate": self.isodate[:7]
                           })
            self.ctr_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            self.source = cml.load_source("multi", self.ens_source, self.ctr_source)
        else:  # default to highres forecasts
            self.isodate = "-".join([date[:4], date[4:6]])
            request = {"param": self.parameter,
                       "date": self.date,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "hr",
                       "ltype": self.ltype,
                       "isodate": self.isodate
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
                       "isodate": year_month[:4] + '-' + year_month[4:]
                       }
            source = cml.load_source("indexed-urls", PerUrlIndex(self._ANA_PATTERN), request)
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
        return obs_fcs



_convert = lambda t: datetime.datetime(t.year, t.month, t.day, t.hour)