#!/usr/bin/env python3
from __future__ import annotations

import warnings

import datetime

import numpy as np
import xarray as xr

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize
from climetlab.indexing import PerUrlIndex

from ..config import baseurl
from ..utils import convert_to_datetime

__version__ = "0.2.4"

_terms_of_use = """By downloading data from this dataset, you agree to the terms and conditions defined at

    https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE

If you do not agree with such terms, do not download the data. """


class TrainingDataForecast(Dataset):

    terms_of_use = _terms_of_use

    _BASEURL = baseurl

    _PATTERN = ""

    _ANALYSIS_PATTERN = (
        "{url}data/ana/{leveltype}/"
        "EU_analysis_{leveltype}_params_{isodate}.grb"
    )

    _ensemble_alias = ["ensemble", "ens", "proba", "probabilistic"]

    def __init__(self, *args, **kwargs):
        """Do almost nothing. To be overridden by the inheriting class."""
        self.parameter = list()
        self.date = ""
        self.leveltype = ""
        self.kind = ""
        self.obs_source = None
        self.isodate = ""
        self.level = None
        self.year = ""
        self.month = ""
        self.step = []
        
    def to_xarray(self, **kwargs):
        return self.source.to_xarray(xarray_open_dataset_kwargs={"backend_kwargs": {"ignore_keys": ["dataType"]}}, **kwargs)

    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):
        if fcs_kwargs is None:
            fcs_kwargs = dict()
        fcs = self.source.to_xarray(xarray_open_dataset_kwargs={"backend_kwargs": {"ignore_keys": ["dataType"]}}, **fcs_kwargs)
        fcs_valid_time = fcs.valid_time.to_pandas()
        fcs_time_list = list(map(convert_to_datetime, fcs_valid_time.iloc[0, :]))
        days = dict()
        for t in fcs_time_list:
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
        obs_valid_time = obs.valid_time.to_pandas()
        obs_time_list = list(map(convert_to_datetime, obs_valid_time.iloc[:, 0]))
        idx = list()
        for i, t in enumerate(obs_time_list):
            if t in fcs_time_list:
                idx.append(i)
        obs_fcs = obs.isel(time=idx)

        # reshape obs to fit fcs TODO: still messy, should be reworked
        obs_dict = obs_fcs.to_dict()
        _, obs_fcs = xr.align(fcs, obs_fcs, join='left', exclude=['number'])
        new_obs_dict = obs_fcs.to_dict()
        new_obs_dict['coords']['valid_time']['data'] = [fcs_time_list]
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).swapaxes(1, 2))
        obs_fcs = obs_fcs.from_dict(new_obs_dict)

        return obs_fcs


class TrainingDataForecastEfi(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = (
        "{url}data/fcs/efi/"
        "EU_forecast_efi_params_{year}-{month}_0.grb"
    )
    _efi_parameters = ["capesi", "10fgi", "capei", "sfi", "10wsi", "2ti", "mx2ti", "mn2ti", "tpi", "all"]

    @normalize("parameter", _efi_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter):

        TrainingDataForecast.__init__(self)

        if isinstance(date, (list, tuple)):
            warnings.warn('Please note that you can only download one forecast date per `climmetlab.load_dataset` call.\n' +
                          'Providing a list of dates might lead to a failure.')

        if parameter == "all":
            self.parameter = self._efi_parameters
        else:
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

    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):
        warnings.warn("Observations are not available for the EFI forecasts.")
        return None


class TrainingDataForecastSurface(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = (
        "{url}data/fcs/{leveltype}/"
        "EU_forecast_{kind}_{leveltype}_params_{isodate}_0.grb"
    )

    _surf_parameters = ["2t", "10u", "10v", "tcc", "100u", "100v", "cape", "stl1", "sd",
                        "tcw", "tcwv", "swvl1", "vis", "all"]
    _surf_parameters += ["cin"]

    @normalize("parameter", _surf_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter, kind):

        TrainingDataForecast.__init__(self)

        if isinstance(date, (list, tuple)):
            warnings.warn('Please note that you can only download one forecast date per `climmetlab.load_dataset` call.\n' +
                          'Providing a list of dates might lead to a failure.')

        if parameter == "all":
            self.parameter = self._surf_parameters
        else:
            self.parameter = parameter
        self.date = date
        self.leveltype = "surf"
        self.kind = kind
        self.obs_source = None
        self.isodate = "-".join([date[:4], date[4:6], date[6:]])
        if kind in self._ensemble_alias:
            request = {"param": self.parameter,
                       # "date": self.date,  ## Not needed
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "ens",
                       "leveltype": self.leveltype,
                       "isodate": self.isodate
                       }
            ens_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            request.update({"date": self.date,
                            # Parameters passed to the filename mangling
                            "kind": "ctr",
                            "isodate": self.isodate[:7]
                            })
            ctr_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            self.source = cml.load_source("multi", ens_source, ctr_source)
        else:  # default to highres forecasts
            request = {"param": self.parameter,
                       "date": self.date,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "hr",
                       "leveltype": self.leveltype,
                       "isodate": self.isodate[:7]
                       }
            self.source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)


class TrainingDataForecastPressure(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = (
        "{url}data/fcs/{leveltype}/"
        "EU_forecast_{kind}_{leveltype}_params_{isodate}_0.grb"
    )

    _pressure_parameters = ['z', 'u', 'v', 'q', 't', 'r', 'all']

    _pressure_parameters_by_level = {500: ['z'],
                                     700: ['u', 'v', 'q'],
                                     850: ['t', 'r']}

    @normalize("parameter", _pressure_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter, level, kind):

        TrainingDataForecast.__init__(self)

        if isinstance(date, (list, tuple)):
            warnings.warn('Please note that you can only download one forecast date per `climmetlab.load_dataset` call.\n' +
                          'Providing a list of dates might lead to a failure.')

        if parameter == "all":
            self.parameter = self._pressure_parameters_by_level[int(level)]
        else:
            self.parameter = parameter
        self.date = date
        self.leveltype = "pressure"
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
                       "leveltype": self.leveltype,
                       "isodate": self.isodate
                       }
            ens_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            request.update({"date": self.date,
                            # Parameters passed to the filename mangling
                            "kind": "ctr",
                            "isodate": self.isodate[:7]
                            })
            ctr_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            self.source = cml.load_source("multi", ens_source, ctr_source)
        else:  # default to highres forecasts
            request = {"param": self.parameter,
                       "date": self.date,
                       "levelist": self.level,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "hr",
                       "leveltype": self.leveltype,
                       "isodate": self.isodate[:7]
                       }
            self.source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)


class TrainingDataForecastSurfaceProcessed(TrainingDataForecast):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = (
        "{url}data/fcs/{leveltype}/"
        "EU_forecast_{kind}_{leveltype}_params_{isodate}_0.grb"
    )

    _surf_pp_parameters = ["tp", "sshf", "slhf", "ssr", "str", "cp", "ssrd", "strd", "10fg6", "mn2t6", "mx2t6"]
    # _surf_pp_parameters += ["cin"]

    _not_6 = []

    for par in _surf_pp_parameters:
        if '6' not in par:
            _not_6.append(par)

    _to_diff = ["tp", "sshf", "slhf", "ssr", "str", "cp", "ssrd", "strd"]  # accumulated parameters to differentiate

    _parameters_ufunc = {"10fg6": "max",
                         "mn2t6": "min",
                         "mx2t6": "max"}

    for par in _not_6:
        _parameters_ufunc[par] = 'sum'

    _parameters_base = {"10fg6": 0,
                        "mn2t6": 0,
                        "mx2t6": 0}

    for par in _not_6:
        _parameters_base[par] = 0

    _parameters_loffset = {"10fg6": 0,
                           "mn2t6": 0,
                           "mx2t6": 0}

    for par in _not_6:
        _parameters_loffset[par] = '5H'

    @normalize("parameter", _surf_pp_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter, kind):

        TrainingDataForecast.__init__(self)

        if isinstance(date, (list, tuple)):
            warnings.warn('Please note that you can only download one forecast date per `climmetlab.load_dataset` call.\n' +
                          'Providing a list of dates might lead to a failure.')

        if isinstance(parameter, (tuple, list)):
            if 'tp' in parameter and len(parameter) > 1:
                    warnings.warn("For technical reason, the parameter 'tp' can only be downloaded alone. \nRemoving this parameter from the list.\n"
                                  "Please make a new separate request with only 'tp' as parameter.")
                    npar = parameter
                    parameter = list()
                    for par in npar:
                        if par != 'tp':
                            parameter.append(par)
        else:
            parameter = [parameter]

        self.parameter = parameter
        self.date = date
        self.leveltype = "surf"
        self.kind = kind
        self.obs_source = None
        self.isodate = "-".join([date[:4], date[4:6], date[6:]])
        if kind in self._ensemble_alias:
            request = {"param": self.parameter,
                       # "date": self.date,  ## Not needed
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "ens",
                       "leveltype": self.leveltype,
                       "isodate": self.isodate
                       }
            ens_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            request.update({"date": self.date,
                            # Parameters passed to the filename mangling
                            "kind": "ctr",
                            "isodate": self.isodate[:7]
                            })
            ctr_source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)
            self.source = cml.load_source("multi", ens_source, ctr_source)
        else:  # default to highres forecasts
            request = {"param": self.parameter,
                       "date": self.date,
                       # Parameters passed to the filename mangling
                       "url": self._BASEURL,
                       "kind": "hr",
                       "leveltype": self.leveltype,
                       "isodate": self.isodate[:7]
                       }
            self.source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)

    def to_xarray(self, **kwargs):
        fcs = self.source.to_xarray(xarray_open_dataset_kwargs={"backend_kwargs": {"ignore_keys": ["dataType"]}}, **kwargs)
        variables = list(fcs.keys())
        ds_list = list()
        for var in variables:
            if var in self._to_diff:  # need to do a finite difference to get the accumulation per step
                da = fcs[var].diff('step')
            # elif var == 'cin':
            #     da = fcs[var].isel(step=slice(1, None))
            else:
                da = fcs[var]
            if var == 'p10fg6':  # remove first step for wind gusts
                var = var[1:]

            if self._parameters_ufunc[var] == "sum":
                ds_resampled = da.resample({'step': '6H'}, label='right', closed='right',
                                           base=self._parameters_base[var],
                                           loffset=self._parameters_loffset[var]).sum()
            elif self._parameters_ufunc[var] == "min":
                ds_resampled = da.resample({'step': '6H'}, label='right', closed='right',
                                           base=self._parameters_base[var],
                                           loffset=self._parameters_loffset[var]).min()
            elif self._parameters_ufunc[var] == "max":
                ds_resampled = da.resample({'step': '6H'}, label='right', closed='right',
                                           base=self._parameters_base[var],
                                           loffset=self._parameters_loffset[var]).max()
            else:  # for debug, do nothing
                ds_resampled = da
            ds_list.append(ds_resampled.to_dataset())

        ds = xr.merge(ds_list).assign_attrs(fcs.attrs)
        for var in variables:
            if var in self._not_6:
                try:
                    new_ds = ds.rename_vars({var: var + '6'})
                    ds = new_ds
                except:
                    pass

        return ds.assign_coords(valid_time=ds.time + ds.step)

    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):

        if fcs_kwargs is None:
            fcs_kwargs = dict()
        fcs = self.to_xarray(**fcs_kwargs)
        fcs_valid_time = fcs.valid_time.to_pandas()
        fcs_time_list = list(map(convert_to_datetime, fcs_valid_time.iloc[0, :]))
        initial_time = fcs_time_list[0]
        final_time = fcs_time_list[-1]
        previous_time = initial_time - datetime.timedelta(days=1)
        tlist = [previous_time] + fcs_time_list
        days = dict()
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
        obs_time = new_obs.time.to_pandas()
        obs_valid_time = (final_time >= obs_time) & (obs_time >= initial_time - datetime.timedelta(hours=5))
        obs_fcs = new_obs.isel(time=obs_valid_time)

        # filter obs to fit fcs
        variables = list(obs_fcs.keys())
        ds_list = list()
        for var in variables:
            da = obs_fcs[var].set_index(time="time")
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

        obs_fcs = xr.merge(ds_list).assign_attrs(obs.attrs)

        # reshape obs to fit fcs TODO: still messy, should be reworked
        shape = list(fcs[list(fcs.keys())[0]].shape)
        shape[0] = 1
        obs_dict = obs_fcs.to_dict()
        _, obs_fcs = xr.align(fcs, obs, join='left', exclude=['number'])
        new_obs_dict = obs_fcs.to_dict()
        new_obs_dict['coords']['valid_time']['data'] = [fcs_time_list]
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).swapaxes(-1, -2).swapaxes(-2, -3) .reshape(shape))
        obs_fcs = obs_fcs.from_dict(new_obs_dict)
        var_name = dict()
        for var in obs_fcs.keys():
            if var == 'fg10':
                var_name[var] = "p10fg6"
            elif var in ['mn2t', 'mx2t'] or var in self._not_6:
                var_name[var] = var + '6'
        obs_fcs = obs_fcs.rename_vars(var_name)

        return obs_fcs
