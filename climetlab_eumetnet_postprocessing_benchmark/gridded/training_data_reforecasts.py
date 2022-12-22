#!/usr/bin/env python3
from __future__ import annotations

import datetime

import numpy as np
import xarray as xr

import climetlab as cml
from climetlab.indexing import PerUrlIndex

from .training_data_forecasts import TrainingDataForecast, TrainingDataForecastSurface, TrainingDataForecastPressure,\
    TrainingDataForecastSurfaceProcessed
from ..utils import convert_to_datetime

__version__ = "0.2.4"

# TODO: Add a check for valid reforecast date and then warn the user if not valid


class TrainingDataReforecast(TrainingDataForecast):

    def __init__(self, *args, **kwargs):
        """Do almost nothing. To be overridden by the inherithing class."""
        TrainingDataForecast.__init__(self, *args, **kwargs)

    def get_observations_as_xarray(self, rfcs_kwargs=None, **obs_kwargs):
        if rfcs_kwargs is None:
            rfcs_kwargs = dict()
        rfcs = self.source.to_xarray(xarray_open_dataset_kwargs={"backend_kwargs": {"ignore_keys": ["dataType"]}}, **rfcs_kwargs)
        rfcs_valid_time = rfcs.valid_time.to_pandas()
        rfcs_time_list = list()
        for i in range(rfcs_valid_time.shape[0]):
            rfcs_time_list.append(list(map(convert_to_datetime, rfcs_valid_time.iloc[i, :])))
        days = dict()
        for rfcs_time in rfcs_time_list:
            for t in rfcs_time:
                year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
                if year_month not in days:
                    days[year_month] = list()
                day = year_month + str(t.day).rjust(2, '0')
                if day not in days[year_month]:
                    days[year_month].append(day)

        if isinstance(self.parameter, (tuple, list)):  # fix for cin observations bug in the dataset, should be solved later at the analysis dataset level
            parameters = [param for param in self.parameter if param != "cin"]
        elif self.parameter == "cin":
            parameters = ""
        else:
            parameters = self.parameter
        sources_list = list()
        for year_month in days:
            request = {"param": parameters,
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
        obs_time = obs.valid_time.to_pandas()
        obs_time_list = list(map(convert_to_datetime, obs_time.iloc[:, 0]))
        idx = list()
        for i, t in enumerate(obs_time_list):
            for rfcs_time in rfcs_time_list:
                if t in rfcs_time:
                    idx.append(i)
        obs_rfcs = obs.isel(time=idx)

        # reshape obs to fit rfcs TODO: still messy, should be reworked
        shape = list(rfcs[list(rfcs.keys())[0]].shape)
        shape[0] = 1
        obs_dict = obs_rfcs.to_dict()
        _, obs_rfcs = xr.align(rfcs, obs_rfcs, join='left', exclude=['number'])
        new_obs_dict = obs_rfcs.to_dict()
        new_obs_dict['coords']['valid_time']['data'] = rfcs_time_list
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).reshape(shape))
        obs_rfcs = obs_rfcs.from_dict(new_obs_dict)

        return obs_rfcs


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


class TrainingDataReforecastSurfaceProcessed(TrainingDataReforecast, TrainingDataForecastSurfaceProcessed):
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

        TrainingDataForecastSurfaceProcessed.__init__(self, date, parameter, "ensemble")
        for par in self._not_6:
            self._parameters_loffset.update({par: 0})

    # Warning : function not yet ready !!!!
    def get_observations_as_xarray(self, rfcs_kwargs=None, **obs_kwargs):

        if rfcs_kwargs is None:
            rfcs_kwargs = dict()
        rfcs = self.to_xarray(**rfcs_kwargs)
        rfcs_valid_time = rfcs.valid_time.to_pandas()
        rfcs_time_list = list()
        initial_time_list = list()
        previous_time_list = list()
        final_time_list = list()
        for i in range(rfcs_valid_time.shape[0]):
            rfcs_time_list.append(list(map(convert_to_datetime, rfcs_valid_time.iloc[i, :])))
            initial_time_list.append(rfcs_time_list[-1][0])
            final_time_list.append(rfcs_time_list[-1][-1])
            previous_time_list.append(initial_time_list[-1] - datetime.timedelta(days=1))
        days = dict()
        extra_date_list = list()
        for i, rfcs_time in enumerate(rfcs_time_list):
            tlist = [previous_time_list[i]] + rfcs_time
            extra_date = None
            for t in tlist:
                year_month = str(t.year).rjust(4, '0') + str(t.month).rjust(2, '0')
                if year_month not in days:
                    days[year_month] = list()
                day = year_month + str(t.day).rjust(2, '0')
                if day not in days[year_month]:
                    days[year_month].append(day)
                    if t.day == 1:  # Edge case when crossing months
                        pt = t - datetime.timedelta(days=1)
                        iso_pt = str(pt.year).rjust(4, '0') + str(pt.month).rjust(2, '0') + str(pt.day).rjust(2, '0')
                        extra_date = {year_month: iso_pt}
            extra_date_list.append(extra_date)

        parameters = list()
        for param in self.parameter:
            if param not in self._not_6:
                parameters.append(param[:-1])
            else:
                parameters.append(param)
        sources_list = list()
        for year_month in days:
            request = {"param": parameters,
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

        extra_sources_list = list()
        for extra_date in extra_date_list:
            if extra_date is not None:  # Edge case when crossing months
                for year_month in extra_date:
                    request = {"param": parameters,
                               "date": extra_date[year_month],
                               # Parameters passed to the filename mangling
                               "url": self._BASEURL,
                               "leveltype": self.leveltype,
                               "isodate": "-".join([year_month[:4], year_month[4:]])
                               }
                    if self.level is not None:
                        request.update({'levelist': self.level})
                    extra_source = cml.load_source("indexed-urls", PerUrlIndex(self._ANALYSIS_PATTERN), request)
                    extra_sources_list.append(extra_source)

        if extra_sources_list:
            extra_source = cml.load_source("multi", *extra_sources_list)
        else:
            extra_source = None

        self.obs_source = cml.load_source("multi", *sources_list)
        obs = self.obs_source.to_xarray(**obs_kwargs)
        if extra_source is not None:
            extra_obs = extra_source.to_xarray(**obs_kwargs)
            new_obs = obs.merge(extra_obs)
        else:
            new_obs = obs
        new_obs = new_obs.stack(datetime=("time", "step")).drop_vars("datetime").swap_dims({"datetime": "time"}).rename({"valid_time": "time"})
        new_obs = new_obs.where(new_obs['time.year'] >= 1997, drop=True)  # Treats edge cases near the start of 2017
        obs_time = new_obs.time.to_pandas()
        obs_time_list = list(map(convert_to_datetime, obs_time))
        idx = list()
        for i, t in enumerate(obs_time_list):
            for final_time, initial_time in zip(final_time_list, initial_time_list):
                if final_time >= t >= initial_time - datetime.timedelta(hours=5):
                    idx.append(i)
        obs_rfcs = new_obs.isel(time=idx)

        # filter obs to fit fcs
        variables = list(obs_rfcs.keys())
        ds_list = list()
        for var in variables:
            da = obs_rfcs[var].set_index(time="time")
            if var == 'fg10':
                var = '10fg6'
            elif var in ['mn2t', 'mx2t']:
                var += '6'

            if self._parameters_ufunc[var] == "sum":
                ds_resampled = da.resample({'time': '6H'}, label='right', closed='right').sum()
            elif self._parameters_ufunc[var] == "min":
                ds_resampled = da.resample({'time': '6H'}, label='right', closed='right').min()
            elif self._parameters_ufunc[var] == "max":
                ds_resampled = da.resample({'time': '6H'}, label='right', closed='right').max()
            else:  # for debug, do nothing
                ds_resampled = da
            ds_list.append(ds_resampled.to_dataset())

        obs_rfcs = xr.merge(ds_list).assign_attrs(obs.attrs)
        new_obs_time = obs_rfcs.time.to_pandas()
        new_obs_time_list = list(map(convert_to_datetime, new_obs_time))
        idx = list()
        for i, t in enumerate(new_obs_time_list):
            for rfcs_time in rfcs_time_list:
                if t in rfcs_time:
                    idx.append(i)
        obs_rfcs = obs_rfcs.isel(time=idx)

        # reshape obs to fit fcs TODO: still messy, should be reworked
        shape = list(rfcs[list(rfcs.keys())[0]].shape)
        shape[0] = 1
        obs_dict = obs_rfcs.to_dict()
        _, obs_rfcs = xr.align(rfcs, obs, join='left', exclude=['number'])
        new_obs_dict = obs_rfcs.to_dict()
        new_obs_dict['coords']['valid_time']['data'] = rfcs_time_list
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).swapaxes(1, -1).reshape(shape))
        obs_rfcs = obs_rfcs.from_dict(new_obs_dict)
        var_name = dict()
        for var in obs_rfcs.keys():
            if var == 'fg10':
                var_name[var] = "p10fg6"
            elif var in ['mn2t', 'mx2t'] or var in self._not_6:
                var_name[var] = var + '6'
        obs_rfcs = obs_rfcs.rename_vars(var_name)

        return obs_rfcs
