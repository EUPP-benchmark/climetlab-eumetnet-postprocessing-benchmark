#!/usr/bin/env python3
from __future__ import annotations

from .training_data_forecasts import TrainingDataForecastSurface, TrainingDataForecastPressure,\
    TrainingDataForecastSurfaceProcessed

__version__ = "0.2.4"


class TrainingDataReforecastSurface(TrainingDataForecastSurface):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    dataset = None

    _PATTERN = "data/stations_data/stations_{kind}_reforecasts_surface_{country}.zarr"

    def __init__(self, country):

        TrainingDataForecastSurface.__init__(self, "ensemble", country)


class TrainingDataReforecastPressure(TrainingDataForecastPressure):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    _PATTERN = "data/stations_data/stations_{kind}_reforecasts_pressure_{level}_{country}.zarr"

    dataset = None

    def __init__(self, level, country):

        TrainingDataForecastPressure.__init__(self, level, "ensemble", country)


class TrainingDataReforecastSurfaceProcessed(TrainingDataForecastSurfaceProcessed):
    name = None  # TODO
    home_page = "-"  # TODO
    licence = "-"  # TODO
    documentation = "-"  # TODO
    citation = "-"  # TODO

    _PATTERN = "data/stations_data/stations_{kind}_reforecasts_surface_postprocessed_{country}.zarr"

    dataset = None

    def __init__(self, country):

        TrainingDataForecastSurfaceProcessed.__init__(self, "ensemble", country)

