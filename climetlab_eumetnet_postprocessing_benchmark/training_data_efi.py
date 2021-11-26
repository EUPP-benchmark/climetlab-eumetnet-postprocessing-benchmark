#!/usr/bin/env python3
from __future__ import annotations

import climetlab as cml
from climetlab import Dataset
from climetlab.normalize import normalize
from climetlab.indexing import PerUrlIndex

__version__ = "0.1.0"



class TrainingDataEfi(Dataset):
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
                   "step" :self.step,
                   # Parameters passed to the filename mangling
                   "url": self._BASEURL,
                   "month": self.month,
                   "year": self.year}
        self.source = cml.load_source("indexed-urls", PerUrlIndex(self._PATTERN), request)


