#!/usr/bin/env python3
from __future__ import annotations

import warnings

import numpy as np
import xarray as xr

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize
from climetlab.indexing import PerUrlIndex

from ..utils import convert_to_datetime

__version__ = "0.1.1-beta"

_terms_of_use = """By downloading data from this dataset, you agree to the terms and conditions defined at

    https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/LICENSE
    
and

    https://github.com/Climdyn/climetlab_eumetnet_postprocessing_benchmark/blob/main/DATA_LICENSE

If you do not agree with such terms, do not download the data. """


class TrainingDataForecast(Dataset):

    terms_of_use = _terms_of_use

    _BASEURL = "https://storage.ecmwf.europeanweather.cloud/benchmark-dataset/"

    _PATTERN = ""

    _ANALYSIS_PATTERN = (
        "{url}data/ana/{leveltype}/"
        "EU_analysis_{leveltype}_params_{isodate}.grb"
    )

    _ensemble_alias = ["ensemble", "ens", "proba", "probabilistic"]

    def __init__(self, *args, **kwargs):
        """Do almost nothing. To be overridden by the inherithing class."""
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

    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):
        if fcs_kwargs is None:
            fcs_kwargs = dict()
        fcs = self.source.to_xarray(**fcs_kwargs)
        valid_time = fcs.valid_time.to_pandas()
        fcs_time_list = list(map(convert_to_datetime, valid_time.iloc[0, :]))
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
            day = year_month + str(t.day).rjust(2, '0')
            if day not in days[year_month]:
                days[year_month].append(day)

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

    _surf_parameters = ["2t", "10u", "10v", "tcc", "100u", "100v", "cape", "stl1", "sshf", "slhf",
                        "tcw", "tcwv", "swvl1", "ssr", "str", "sd", "cp", "cin", "ssrd", "strd", "vis", "all"]

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


class TrainingDataForecastSurfacePostProcessed(TrainingDataForecast):
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

    _surf_pp_parameters = ["tp", "10fg6", "mn2t6", "mx2t6"]

    _parameters_ufunc = {"tp": 'sum',
                         "10fg6": "max",
                         "mn2t6": "min",
                         "mx2t6": "max"}

    _parameters_base = {"tp": 6,
                        "10fg6": 0,
                        "mn2t6": 0,
                        "mx2t6": 0}

    _parameters_loffset = {"tp": '-1H',
                           "10fg6": 0,
                           "mn2t6": 0,
                           "mx2t6": 0}

    @normalize("parameter", _surf_pp_parameters)
    @normalize("date", "date(%Y%m%d)")
    def __init__(self, date, parameter, kind):

        TrainingDataForecast.__init__(self)

        if isinstance(date, (list, tuple)):
            warnings.warn('Please note that you can only download one forecast date per `climmetlab.load_dataset` call.\n' +
                          'Providing a list of dates might lead to a failure.')

        if parameter == "all":
            self.parameter = self._surf_pp_parameters
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

    def to_xarray(self, **kwargs):
        fcs = self.source.to_xarray(**kwargs)
        variables = list(fcs.keys())
        ds_list = list()
        for var in variables:
            if var == 'tp':  # need to skip the first time at 00:00:00 for total precip
                da = fcs[var][:, :, 1:]
            else:
                da = fcs[var]
            if var == 'p10fg6':
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
        try:
            new_ds = ds.rename_vars({'tp': 'tp6'})
            ds = new_ds
        except:
            pass

        return ds

    # WARNING: Function not yet working as it should !!!!!!
    def get_observations_as_xarray(self, fcs_kwargs=None, **obs_kwargs):
        if fcs_kwargs is None:
            fcs_kwargs = dict()
        fcs = self.source.to_xarray(**fcs_kwargs)
        valid_time = fcs.valid_time.to_pandas()
        fcs_time_list = list(map(convert_to_datetime, valid_time.iloc[0, :]))
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
            day = year_month + str(t.day).rjust(2, '0')
            if day not in days[year_month]:
                days[year_month].append(day)

        parameters = list()
        for param in self.parameter:
            if param == 'tp':
                parameters.append(param)
            else:
                parameters.append(param[:-1])
        sources_list = list()
        for year_month in year_months:
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

        # TODO: transforms obs to a file compatible with the forecasts first: 1 time and then steps (and take one day before to get the first 6 h)

        # reshape obs to fit fcs
        variables = list(obs.keys())
        ds_list = list()
        for var in variables:
            da = obs[var][:, :, 1:]
            if var == 'p10fg6':
                var = var[1:]
            elif var in ['mn2t', 'mx2t', '10fg']:
                var += '6'

            if self._parameters_ufunc[var] == "sum":
                ds_resampled = da.resample({'step': '6H'}, label='right', closed='right',
                                           base=6,
                                           loffset="-1H").sum()
            elif self._parameters_ufunc[var] == "min":
                ds_resampled = da.resample({'step': '6H'}, label='right', closed='right',
                                           base=6,
                                           loffset="-1H").min()
            elif self._parameters_ufunc[var] == "max":
                ds_resampled = da.resample({'step': '6H'}, label='right', closed='right',
                                           base=6,
                                           loffset="-1H").max()
            else:  # for debug, do nothing
                ds_resampled = da
            ds_list.append(ds_resampled.to_dataset())

        obs_fcs = xr.merge(ds_list).assign_attrs(obs.attrs)

        # reshape obs to fit fcs TODO: still messy, should be reworked
        obs_dict = obs_fcs.to_dict()
        _, obs_fcs = xr.align(fcs, obs_fcs, join='left', exclude=['number'])
        new_obs_dict = obs_fcs.to_dict()
        for var in new_obs_dict['data_vars']:
            new_obs_dict['data_vars'][var]['data'] = list(np.array(obs_dict['data_vars'][var]["data"]).swapaxes(1, 2))
        obs_fcs = obs_fcs.from_dict(new_obs_dict)

        return obs_fcs
