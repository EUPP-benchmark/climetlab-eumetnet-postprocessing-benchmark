#!/usr/bin/env python3
from __future__ import annotations

import numpy as np
import xarray as xr

import climetlab as cml
from climetlab.indexing import PerUrlIndex

from .training_data_forecasts import TrainingDataForecast, TrainingDataForecastSurface, TrainingDataForecastPressure
from ..utils import convert_to_datetime

__version__ = "0.1.1-beta"

# TODO: Add a check for valid reforecast date and then warn the user if not valid


class TrainingDataReforecast(TrainingDataForecast):

    def __init__(self, *args, **kwargs):
        """Do almost nothing. To be overridden by the inherithing class."""
        TrainingDataForecast.__init__(self, *args, **kwargs)

    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):
        if fcs_kwargs is None:
            fcs_kwargs = dict()
        fcs = self.source.to_xarray(**fcs_kwargs)
        valid_time = fcs.valid_time.to_pandas()
        fcs_time_list = list()
        for i in range(valid_time.shape[0]):
            fcs_time_list.append(list(map(convert_to_datetime, valid_time.iloc[i, :])))
        year_months = list()
        for fcs_time in fcs_time_list:
            for t in fcs_time:
                year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
                if year_month not in year_months:
                    year_months.append(year_month)
        days = dict()
        for year_month in year_months:
            days[year_month] = list()
        for fcs_time in fcs_time_list:
            for t in fcs_time:
                year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
                days[year_month].append(str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0') + str(t.day).rjust(2, '0'))

        sources_list = list()
        for year_month in year_months:
            request = {"param": self.parameter,
                       "date": days[year_month],
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "leveltype": self.leveltype,
                       "isodate": "-".join([year_month[:4], year_month[4:]])
                       }
            if self.level is not None:
                request.update({'levelist': self.level})
            source = cml.load_source("indexed-urls", PerUrlIndex(self._ANALYSIS_PATTERN), request)
            sources_list.append(source)
        self.obs_source = cml.load_source("multi", *sources_list)
        obs = self.obs_source.to_xarray(**obs_kwargs)
        valid_time = obs.valid_time.to_pandas()
        obs_time_list = list(map(convert_to_datetime, valid_time.iloc[:, 0]))
        idx = list()
        for i, t in enumerate(obs_time_list):
            for fcs_time in fcs_time_list:
                if t in fcs_time:
                    idx.append(i)
        obs_fcs = obs.isel(time=idx)

        # reshape obs to fit fcs TODO: still messy, should be reworked
        for var in fcs:
            shape = list(fcs[var].shape)
            break
        shape[0] = 1
        obs_dict = obs_fcs.to_dict()
        _, obs_fcs = xr.align(fcs, obs_fcs, join='left', exclude=['number'])
        new_obs_dict = obs_fcs.to_dict()
        new_obs_dict['coords']['valid_time']['data'] = fcs_time_list
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).reshape(shape))
        obs_fcs = obs_fcs.from_dict(new_obs_dict)

        return obs_fcs


class TrainingDataReforecastSurface(TrainingDataReforecast, TrainingDataForecastSurface):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = (
        "{url}data/rfcs/{leveltype}/"
        "EU_reforecast_{kind}_{leveltype}_params_{isodate}_0.grb"
    )

    def __init__(self, date, parameter):

        TrainingDataForecastSurface.__init__(self, date, parameter, "ensemble")


class TrainingDataReforecastPressure(TrainingDataReforecast, TrainingDataForecastPressure):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = (
        "{url}data/rfcs/{leveltype}/"
        "EU_reforecast_{kind}_{leveltype}_params_{isodate}_0.grb"
    )

    def __init__(self, date, parameter, level):

        TrainingDataForecastPressure.__init__(self, date, parameter, level, "ensemble")
